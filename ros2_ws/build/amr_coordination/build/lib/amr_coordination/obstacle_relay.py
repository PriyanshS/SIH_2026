"""Obstacle Relay — detects unexpected lidar obstacles, broadcasts to peers,
and injects peer-reported obstacles into own local costmap via virtual scan."""

import math
import json

import rclpy
from rclpy.node import Node
from rclpy.callback_groups import ReentrantCallbackGroup
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped, TransformStamped
from std_msgs.msg import String, Header
from amr_msgs.msg import DetectedObstacle
from builtin_interfaces.msg import Time

import tf2_ros


class ObstacleRelay(Node):
    def __init__(self):
        super().__init__('obstacle_relay')

        self.declare_parameter('robot_id', 'robot1')
        self.declare_parameter('obstacle_min_range', 0.3)
        self.declare_parameter('obstacle_max_range', 3.0)
        self.declare_parameter('cluster_threshold', 0.3)
        self.declare_parameter('min_cluster_size', 3)
        self.declare_parameter('broadcast_cooldown', 2.0)

        self.robot_id = self.get_parameter('robot_id').value
        self.obstacle_min_range = self.get_parameter('obstacle_min_range').value
        self.obstacle_max_range = self.get_parameter('obstacle_max_range').value
        self.cluster_threshold = self.get_parameter('cluster_threshold').value
        self.min_cluster_size = self.get_parameter('min_cluster_size').value
        self.broadcast_cooldown = self.get_parameter('broadcast_cooldown').value

        self.current_pose = None
        self.current_yaw = 0.0
        self.static_map = None
        self.map_info = None
        self.recent_broadcasts = []  # list of (x, y, time)

        self.cb_group = ReentrantCallbackGroup()

        # Subscribe to ground-truth pose from Gazebo pose publisher
        self.pose_sub = self.create_subscription(
            PoseStamped,
            f'/{self.robot_id}/ground_truth_pose',
            self._pose_cb,
            10,
        )

        # Subscribe to own scan
        self.scan_sub = self.create_subscription(
            LaserScan,
            f'/{self.robot_id}/scan',
            self._scan_cb,
            5,
        )

        # Subscribe to static map for wall filtering
        self.map_sub = self.create_subscription(
            OccupancyGrid,
            f'/{self.robot_id}/map',
            self._map_cb,
            rclpy.qos.QoSProfile(
                reliability=rclpy.qos.ReliabilityPolicy.RELIABLE,
                durability=rclpy.qos.DurabilityPolicy.TRANSIENT_LOCAL,
                depth=1,
            ),
        )

        # Obstacle broadcast pub/sub
        self.obstacle_pub = self.create_publisher(
            DetectedObstacle, '/detected_obstacles', 10
        )
        self.obstacle_sub = self.create_subscription(
            DetectedObstacle,
            '/detected_obstacles',
            self._obstacle_cb,
            10,
        )

        # Virtual scan publisher for injecting obstacles into own costmap
        self.virtual_scan_pub = self.create_publisher(
            LaserScan,
            f'/{self.robot_id}/virtual_scan',
            10,
        )

        # Metrics publisher
        self.metrics_pub = self.create_publisher(String, '/metrics', 10)

        self.get_logger().info(f'[{self.robot_id}] Obstacle relay started')

    def _pose_cb(self, msg):
        pose = msg.pose.pose if hasattr(msg.pose, 'pose') else msg.pose
        self.current_pose = (
            pose.position.x,
            pose.position.y,
        )
        # Extract yaw from quaternion
        q = pose.orientation
        siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        self.current_yaw = math.atan2(siny_cosp, cosy_cosp)

    def _map_cb(self, msg: OccupancyGrid):
        self.static_map = msg.data
        self.map_info = msg.info
        self.get_logger().info(
            f'[{self.robot_id}] Static map received: '
            f'{msg.info.width}x{msg.info.height}'
        )

    def _is_on_known_wall(self, x, y):
        """Check if a point in map frame corresponds to a known wall."""
        if self.static_map is None or self.map_info is None:
            return False
        # Convert map coords to grid indices
        mi = self.map_info
        gx = int((x - mi.origin.position.x) / mi.resolution)
        gy = int((y - mi.origin.position.y) / mi.resolution)
        for dx in (-2, -1, 0, 1, 2):
            for dy in (-2, -1, 0, 1, 2):
                cx = gx + dx
                cy = gy + dy
                if 0 <= cx < mi.width and 0 <= cy < mi.height:
                    idx = cy * mi.width + cx
                    if idx < len(self.static_map) and self.static_map[idx] > 50:
                        return True
        return False

    def _scan_cb(self, msg: LaserScan):
        """Process lidar scan to detect unexpected obstacles."""
        if self.current_pose is None or self.static_map is None:
            return

        rx, ry = self.current_pose
        unknown_points = []

        for i, r in enumerate(msg.ranges):
            if r < self.obstacle_min_range or r > self.obstacle_max_range:
                continue
            if math.isinf(r) or math.isnan(r):
                continue

            # Convert to map frame
            angle = msg.angle_min + i * msg.angle_increment + self.current_yaw
            px = rx + r * math.cos(angle)
            py = ry + r * math.sin(angle)

            # Filter: skip if on known wall
            if not self._is_on_known_wall(px, py):
                unknown_points.append((px, py))

        if len(unknown_points) < self.min_cluster_size:
            return

        # Simple clustering: find clusters of nearby points
        clusters = self._simple_cluster(unknown_points)

        now = self.get_clock().now()
        for cluster in clusters:
            if len(cluster) < self.min_cluster_size:
                continue
            cx = sum(p[0] for p in cluster) / len(cluster)
            cy = sum(p[1] for p in cluster) / len(cluster)
            radius = max(
                math.sqrt((p[0] - cx)**2 + (p[1] - cy)**2)
                for p in cluster
            ) + 0.15

            if not self._recently_broadcast(cx, cy, now):
                obstacle = DetectedObstacle()
                obstacle.reporter_id = self.robot_id
                obstacle.position.x = cx
                obstacle.position.y = cy
                obstacle.position.z = 0.0
                obstacle.radius = radius
                obstacle.stamp = now.to_msg()
                obstacle.ttl = 10.0
                self.obstacle_pub.publish(obstacle)
                self.recent_broadcasts.append((cx, cy, now))

                self.get_logger().info(
                    f'[{self.robot_id}] Broadcast obstacle at ({cx:.1f}, {cy:.1f}), '
                    f'r={radius:.2f}m'
                )

    def _simple_cluster(self, points):
        """Simple greedy clustering (lightweight DBSCAN substitute)."""
        if not points:
            return []
        used = [False] * len(points)
        clusters = []
        for i in range(len(points)):
            if used[i]:
                continue
            cluster = [points[i]]
            used[i] = True
            for j in range(i + 1, len(points)):
                if used[j]:
                    continue
                dx = points[j][0] - points[i][0]
                dy = points[j][1] - points[i][1]
                if math.sqrt(dx * dx + dy * dy) < self.cluster_threshold:
                    cluster.append(points[j])
                    used[j] = True
            clusters.append(cluster)
        return clusters

    def _recently_broadcast(self, x, y, now):
        """Check if we recently broadcast an obstacle near this location."""
        # Clean old entries
        self.recent_broadcasts = [
            (bx, by, bt) for bx, by, bt in self.recent_broadcasts
            if (now - bt).nanoseconds / 1e9 < self.broadcast_cooldown
        ]
        for bx, by, bt in self.recent_broadcasts:
            if math.sqrt((x - bx)**2 + (y - by)**2) < 0.5:
                return True
        return False

    def _obstacle_cb(self, msg: DetectedObstacle):
        """Receive obstacle from peer — inject into own costmap via virtual scan."""
        if msg.reporter_id == self.robot_id:
            return  # self-filter

        if self.current_pose is None:
            return

        self.get_logger().info(
            f'[{self.robot_id}] Received obstacle from {msg.reporter_id} at '
            f'({msg.position.x:.1f}, {msg.position.y:.1f})'
        )

        # Create a virtual laser scan that contains "hits" at the obstacle location
        self._inject_virtual_obstacle(
            msg.position.x, msg.position.y, msg.radius, msg.ttl
        )

        # Publish metric
        metric = {
            'robot_id': self.robot_id,
            'event': 'OBSTACLE_RECEIVED',
            'from': msg.reporter_id,
            'position': [msg.position.x, msg.position.y],
            'mode': 'coordinated',
        }
        m = String()
        m.data = json.dumps(metric)
        self.metrics_pub.publish(m)

    def _inject_virtual_obstacle(self, ox, oy, radius, ttl):
        """Publish a virtual LaserScan with hits at the obstacle location."""
        if self.current_pose is None:
            return

        rx, ry = self.current_pose
        dx = ox - rx
        dy = oy - ry
        dist_to_obstacle = math.sqrt(dx * dx + dy * dy)
        angle_to_obstacle = math.atan2(dy, dx) - self.current_yaw

        # Normalize angle
        while angle_to_obstacle > math.pi:
            angle_to_obstacle -= 2.0 * math.pi
        while angle_to_obstacle < -math.pi:
            angle_to_obstacle += 2.0 * math.pi

        # Create a virtual scan
        num_rays = 360
        scan = LaserScan()
        scan.header = Header()
        scan.header.stamp = self.get_clock().now().to_msg()
        scan.header.frame_id = f'{self.robot_id}/lidar_link'
        scan.angle_min = -math.pi
        scan.angle_max = math.pi
        scan.angle_increment = 2.0 * math.pi / num_rays
        scan.time_increment = 0.0
        scan.scan_time = 0.1
        scan.range_min = 0.12
        scan.range_max = 12.0
        scan.ranges = [float('inf')] * num_rays

        # Set a few rays to hit the obstacle
        angular_width = math.atan2(radius, max(dist_to_obstacle, 0.1))
        for i in range(num_rays):
            ray_angle = scan.angle_min + i * scan.angle_increment
            angle_diff = abs(ray_angle - angle_to_obstacle)
            if angle_diff > math.pi:
                angle_diff = 2.0 * math.pi - angle_diff
            if angle_diff < angular_width:
                scan.ranges[i] = dist_to_obstacle

        self.virtual_scan_pub.publish(scan)


def main(args=None):
    rclpy.init(args=args)
    node = ObstacleRelay()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

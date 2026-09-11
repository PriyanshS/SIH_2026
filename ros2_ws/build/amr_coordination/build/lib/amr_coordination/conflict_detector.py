"""Conflict Detector — compares shared paths for spatial/temporal overlap."""

import math

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from rclpy.action import ActionClient
from rclpy.callback_groups import ReentrantCallbackGroup
from nav2_msgs.action import NavigateToPose
from amr_msgs.msg import RobotPlan
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String


class ConflictDetector(Node):
    def __init__(self):
        super().__init__('conflict_detector')

        self.declare_parameter('robot_id', 'robot1')
        self.declare_parameter('conflict_radius', 0.8)
        self.declare_parameter('temporal_window', 3.0)
        self.declare_parameter('check_rate', 2.0)
        self.declare_parameter('max_lookahead', 15.0)

        self.robot_id = self.get_parameter('robot_id').value
        self.conflict_radius = self.get_parameter('conflict_radius').value
        self.temporal_window = self.get_parameter('temporal_window').value
        self.check_rate = self.get_parameter('check_rate').value
        self.max_lookahead = self.get_parameter('max_lookahead').value

        self.own_plan = None
        self.own_velocity = 0.3
        self.peer_plans = {}
        self.is_yielding = False

        self.cb_group = ReentrantCallbackGroup()

        # Subscribe to shared plans
        shared_plan_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            depth=3,
        )
        self.plan_sub = self.create_subscription(
            RobotPlan,
            '/shared_plans',
            self._plan_cb,
            shared_plan_qos,
        )

        # Metrics publisher for conflict events
        self.metrics_pub = self.create_publisher(String, '/metrics', 10)

        # Check for conflicts periodically
        self.create_timer(
            1.0 / self.check_rate,
            self._check_conflicts,
            callback_group=self.cb_group,
        )

        self.get_logger().info(f'[{self.robot_id}] Conflict detector started')

    def _plan_cb(self, msg: RobotPlan):
        """Store plans from all robots."""
        if msg.robot_id == self.robot_id:
            self.own_plan = msg
            self.own_velocity = max(msg.estimated_velocity, 0.05)
        else:
            self.peer_plans[msg.robot_id] = msg

    def _assign_times(self, poses, velocity):
        """Walk along path, assign elapsed time to each pose."""
        result = []
        t = 0.0
        max_poses = min(len(poses), 60)  # downsample to avoid O(n²) blowup
        step = max(1, len(poses) // max_poses)

        for i in range(0, len(poses), step):
            pose = poses[i]
            if i > 0:
                prev = poses[max(0, i - step)]
                dx = pose.pose.position.x - prev.pose.position.x
                dy = pose.pose.position.y - prev.pose.position.y
                seg = math.sqrt(dx * dx + dy * dy)
                t += seg / max(velocity, 0.05)
            result.append((
                pose.pose.position.x,
                pose.pose.position.y,
                t,
            ))
            if t > self.max_lookahead:
                break
        return result

    def _check_conflicts(self):
        """Periodic check for path conflicts with peers."""
        if self.own_plan is None or len(self.own_plan.path.poses) == 0:
            return

        if self.is_yielding:
            return

        own_timed = self._assign_times(
            self.own_plan.path.poses,
            self.own_velocity,
        )

        for peer_id, peer_plan in self.peer_plans.items():
            if len(peer_plan.path.poses) == 0:
                continue

            peer_vel = max(peer_plan.estimated_velocity, 0.05)
            peer_timed = self._assign_times(peer_plan.path.poses, peer_vel)

            for ox, oy, ot in own_timed:
                for px, py, pt in peer_timed:
                    if abs(ot - pt) < self.temporal_window:
                        dist = math.sqrt((ox - px)**2 + (oy - py)**2)
                        if dist < self.conflict_radius:
                            self._handle_conflict(peer_id, ox, oy, ot)
                            return  # handle one at a time

    def _handle_conflict(self, peer_id, cx, cy, ct):
        """Resolve conflict: higher robot_id string yields."""
        if self.robot_id > peer_id:
            self.get_logger().warn(
                f'[{self.robot_id}] CONFLICT with {peer_id} at '
                f'({cx:.1f}, {cy:.1f}), t={ct:.1f}s — YIELDING'
            )
            self.is_yielding = True

            # Publish conflict event
            import json
            metric = {
                'robot_id': self.robot_id,
                'event': 'CONFLICT_YIELD',
                'peer': peer_id,
                'position': [cx, cy],
                'mode': 'coordinated',
            }
            msg = String()
            msg.data = json.dumps(metric)
            self.metrics_pub.publish(msg)

            # Wait and then clear yielding flag (one-shot)
            _t = [None]
            def _resume():
                if _t[0] is not None:
                    self.destroy_timer(_t[0])
                self._clear_yield()
            _t[0] = self.create_timer(3.0, _resume, callback_group=self.cb_group)
        else:
            self.get_logger().info(
                f'[{self.robot_id}] Conflict with {peer_id} — '
                f'peer will yield (I have priority)'
            )

    def _clear_yield(self):
        """Resume after yielding."""
        self.is_yielding = False
        self.get_logger().info(f'[{self.robot_id}] Resuming after yield')


def main(args=None):
    rclpy.init(args=args)
    node = ConflictDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

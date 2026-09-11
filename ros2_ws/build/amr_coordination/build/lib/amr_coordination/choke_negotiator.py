"""Choke Negotiator — request/ack token system for chokepoint passage.

States: IDLE → REQUESTING → GRANTED → IN_CHOKE → (back to IDLE via RELEASE)
"""

import math
import yaml

import rclpy
from rclpy.node import Node
from rclpy.callback_groups import ReentrantCallbackGroup
from geometry_msgs.msg import PoseStamped, Twist
from std_msgs.msg import String
from amr_msgs.msg import ChokeRequest


class ChokeNegotiator(Node):
    # States
    IDLE = 0
    REQUESTING = 1
    GRANTED = 2
    IN_CHOKE = 3

    def __init__(self):
        super().__init__('choke_negotiator')

        self.declare_parameter('robot_id', 'robot1')
        self.declare_parameter('priority', 1)
        self.declare_parameter('chokepoint_file', '')
        self.declare_parameter('heartbeat_interval', 0.5)
        self.declare_parameter('grant_timeout_base', 5.0)

        self.robot_id = self.get_parameter('robot_id').value
        self.priority = self.get_parameter('priority').value
        chokepoint_file = self.get_parameter('chokepoint_file').value
        self.heartbeat_interval = self.get_parameter('heartbeat_interval').value
        grant_timeout_base = self.get_parameter('grant_timeout_base').value

        # Jittered grant timeout: higher priority (lower number) waits shorter
        self.grant_timeout = grant_timeout_base + self.priority * 0.3

        # Load chokepoint polygon
        with open(chokepoint_file, 'r') as f:
            config = yaml.safe_load(f)

        choke = config['chokepoint']
        self.centroid = choke['centroid']
        self.vertices = [tuple(v) for v in choke['vertices']]
        self.approach_distance = choke.get('approach_distance', 2.0)

        # State
        self.state = self.IDLE
        self.current_pose = None
        self.grant_timer = None
        self.heartbeat_timer = None
        self.stop_timer = None
        self.peer_requests = {}       # {robot_id: ChokeRequest}
        self.peer_heartbeats = {}     # {robot_id: last_time}
        self.choke_occupied_by = set()

        self.cb_group = ReentrantCallbackGroup()

        # Subscribe to ground-truth pose from Gazebo pose publisher
        self.pose_sub = self.create_subscription(
            PoseStamped,
            f'/{self.robot_id}/ground_truth_pose',
            self._pose_cb,
            10,
        )

        # Choke negotiation pub/sub
        self.choke_pub = self.create_publisher(
            ChokeRequest, '/choke_negotiation', 30
        )
        self.choke_sub = self.create_subscription(
            ChokeRequest,
            '/choke_negotiation',
            self._choke_msg_cb,
            30,
        )

        # Cmd_vel override publisher (for stopping before choke)
        self.cmd_vel_pub = self.create_publisher(
            Twist, f'/{self.robot_id}/cmd_vel', 10
        )

        # "Why waiting" annotation publisher (Section 4 of addendum)
        # Subscribers: RViz text display, logging nodes, panel demo
        self.reason_pub = self.create_publisher(
            String, f'/{self.robot_id}/choke_reason', 10
        )

        # Main check loop at 5 Hz
        self.create_timer(0.2, self._tick, callback_group=self.cb_group)

        # Peer heartbeat stale check at 1 Hz
        self.create_timer(1.0, self._check_stale_peers, callback_group=self.cb_group)

        self.get_logger().info(
            f'[{self.robot_id}] Choke negotiator started, priority={self.priority}, '
            f'timeout={self.grant_timeout:.1f}s'
        )

    def _pose_cb(self, msg):
        pose = msg.pose.pose if hasattr(msg.pose, 'pose') else msg.pose
        self.current_pose = (
            pose.position.x,
            pose.position.y,
        )

    def _distance_to_centroid(self):
        if self.current_pose is None:
            return float('inf')
        dx = self.current_pose[0] - self.centroid[0]
        dy = self.current_pose[1] - self.centroid[1]
        return math.sqrt(dx * dx + dy * dy)

    def _point_in_polygon(self, px, py):
        """Ray-casting point-in-polygon test."""
        n = len(self.vertices)
        inside = False
        j = n - 1
        for i in range(n):
            xi, yi = self.vertices[i]
            xj, yj = self.vertices[j]
            if ((yi > py) != (yj > py)) and \
               (px < (xj - xi) * (py - yi) / (yj - yi) + xi):
                inside = not inside
            j = i
        return inside

    def _in_chokepoint(self):
        if self.current_pose is None:
            return False
        return self._point_in_polygon(self.current_pose[0], self.current_pose[1])

    def _publish_choke(self, msg_type):
        msg = ChokeRequest()
        msg.robot_id = self.robot_id
        msg.msg_type = msg_type
        msg.priority = self.priority
        msg.distance_to_choke = self._distance_to_centroid()
        msg.stamp = self.get_clock().now().to_msg()
        self.choke_pub.publish(msg)

    def _choke_msg_cb(self, msg: ChokeRequest):
        """Handle incoming choke negotiation messages."""
        if msg.robot_id == self.robot_id:
            return  # self-filter

        now = self.get_clock().now()

        if msg.msg_type == ChokeRequest.REQUEST:
            self.peer_requests[msg.robot_id] = msg

            if self.state == self.REQUESTING:
                # Check if peer has higher priority
                if msg.priority < self.priority:
                    # Peer has higher priority — yield and reset our timeout
                    reason = (
                        f'yielding to {msg.robot_id}, '
                        f'lower priority ({msg.priority} < {self.priority})'
                    )
                    self._publish_reason(reason)
                    self._reset_grant_timer()
                elif msg.priority == self.priority:
                    # Tie-break: lower distance wins; then lower robot_id
                    my_dist = self._distance_to_centroid()
                    if msg.distance_to_choke < my_dist:
                        reason = (
                            f'yielding to {msg.robot_id}, '
                            f'closer to chokepoint ({msg.distance_to_choke:.2f}m < {my_dist:.2f}m)'
                        )
                        self._publish_reason(reason)
                        self._reset_grant_timer()
                    elif msg.distance_to_choke == my_dist and \
                         msg.robot_id < self.robot_id:
                        reason = (
                            f'yielding to {msg.robot_id}, '
                            f'lower robot_id tie-break'
                        )
                        self._publish_reason(reason)
                        self._reset_grant_timer()

        elif msg.msg_type == ChokeRequest.GRANT:
            # A peer self-granted
            self.choke_occupied_by.add(msg.robot_id)

        elif msg.msg_type == ChokeRequest.RELEASE:
            self.choke_occupied_by.discard(msg.robot_id)
            self.peer_requests.pop(msg.robot_id, None)

            # If we're REQUESTING, re-evaluate
            if self.state == self.REQUESTING:
                if self._no_higher_priority_pending():
                    self._self_grant()

        elif msg.msg_type == ChokeRequest.HEARTBEAT:
            self.peer_heartbeats[msg.robot_id] = now
            self.choke_occupied_by.add(msg.robot_id)

    def _no_higher_priority_pending(self):
        """Check if no pending request has higher priority than us."""
        for rid, req in self.peer_requests.items():
            if rid in self.choke_occupied_by:
                continue  # already in choke, not contending
            if req.priority < self.priority:
                return False
            if req.priority == self.priority:
                my_dist = self._distance_to_centroid()
                if req.distance_to_choke < my_dist:
                    return False
                if req.distance_to_choke == my_dist and req.robot_id < self.robot_id:
                    return False
        return True

    def _tick(self):
        """Main 5 Hz state machine tick."""
        if self.current_pose is None:
            return

        if self.state == self.IDLE:
            dist = self._distance_to_centroid()
            if dist < self.approach_distance + 1.0:
                # Approaching chokepoint — start requesting
                self.get_logger().info(
                    f'[{self.robot_id}] Approaching chokepoint (dist={dist:.1f}m) — REQUESTING'
                )
                self.state = self.REQUESTING
                self._publish_choke(ChokeRequest.REQUEST)
                self._start_grant_timer()

        elif self.state == self.REQUESTING:
            # Keep publishing REQUEST at 2 Hz (timer runs at 5 Hz, publish every other tick)
            self._publish_choke(ChokeRequest.REQUEST)

            # If close to choke boundary and not granted, STOP
            dist = self._distance_to_centroid()
            if dist < self.approach_distance:
                self._stop_robot()

        elif self.state == self.GRANTED:
            # We have the token — allow Nav2 to proceed
            if self._in_chokepoint():
                self.get_logger().info(
                    f'[{self.robot_id}] Entered chokepoint — IN_CHOKE'
                )
                self.state = self.IN_CHOKE
                self._start_heartbeat()

        elif self.state == self.IN_CHOKE:
            if not self._in_chokepoint():
                self.get_logger().info(
                    f'[{self.robot_id}] Exited chokepoint — RELEASING'
                )
                self._publish_choke(ChokeRequest.RELEASE)
                self._stop_heartbeat()
                self.state = self.IDLE

    def _stop_robot(self):
        """Send zero velocity to override Nav2."""
        stop = Twist()
        self.cmd_vel_pub.publish(stop)

    def _publish_reason(self, reason: str):
        """Publish a human-readable explanation of why this robot is yielding."""
        self.get_logger().info(f'[{self.robot_id}] {reason}')
        msg = String()
        msg.data = f'[{self.robot_id}] {reason}'
        self.reason_pub.publish(msg)

    def _start_grant_timer(self):
        """Start the jittered grant timeout."""
        self.grant_timer = self.create_timer(
            self.grant_timeout,
            self._grant_timeout_cb,
            callback_group=self.cb_group,
        )

    def _reset_grant_timer(self):
        """Reset the grant timeout (a higher-priority peer was seen)."""
        if self.grant_timer is not None:
            self.destroy_timer(self.grant_timer)
        self._start_grant_timer()

    def _grant_timeout_cb(self):
        """No higher-priority contender seen — self-grant."""
        if self.state == self.REQUESTING:
            if self._no_higher_priority_pending() and \
               len(self.choke_occupied_by) == 0:
                self._self_grant()
            else:
                # Someone is still in the choke or has higher priority — keep waiting
                self._reset_grant_timer()

    def _self_grant(self):
        """Grant ourselves passage through the chokepoint."""
        self.get_logger().info(f'[{self.robot_id}] SELF-GRANTED chokepoint passage')
        if self.grant_timer is not None:
            self.destroy_timer(self.grant_timer)
            self.grant_timer = None
        self._publish_choke(ChokeRequest.GRANT)
        self.state = self.GRANTED

    def _start_heartbeat(self):
        """Publish heartbeats while in chokepoint."""
        self.heartbeat_timer = self.create_timer(
            self.heartbeat_interval,
            lambda: self._publish_choke(ChokeRequest.HEARTBEAT),
            callback_group=self.cb_group,
        )

    def _stop_heartbeat(self):
        if self.heartbeat_timer is not None:
            self.destroy_timer(self.heartbeat_timer)
            self.heartbeat_timer = None

    def _check_stale_peers(self):
        """Remove peers whose heartbeats are stale (>3s)."""
        now = self.get_clock().now()
        stale = []
        for rid, last_time in self.peer_heartbeats.items():
            elapsed = (now - last_time).nanoseconds / 1e9
            if elapsed > 3.0:
                stale.append(rid)

        for rid in stale:
            if rid in self.choke_occupied_by:
                self.get_logger().warn(
                    f'[{self.robot_id}] Peer {rid} heartbeat stale — treating choke as free'
                )
                self.choke_occupied_by.discard(rid)
                del self.peer_heartbeats[rid]

                # Re-evaluate if we're waiting
                if self.state == self.REQUESTING:
                    if self._no_higher_priority_pending() and \
                       len(self.choke_occupied_by) == 0:
                        self._self_grant()


def main(args=None):
    rclpy.init(args=args)
    node = ChokeNegotiator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

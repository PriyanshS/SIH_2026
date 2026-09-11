"""Goal Dispatcher — click-to-goal assignment with idle/busy state tracking.

Behavior (Section 2 of addendum):
  - Subscribe to /clicked_point (RViz "Publish Point" tool)
  - Track each robot's idle/busy status via /<ns>/robot_status topics
  - On click: find nearest IDLE robot by Euclidean distance; send NavigateToPose goal
  - If all robots busy: queue the point; dispatch when any robot goes IDLE
  - Robot reports IDLE only once its NavigateToPose action reports SUCCESS

Topic map:
  SUBSCRIBES:
    /clicked_point            geometry_msgs/PointStamped  (from RViz)
    /robot1/robot_status      amr_msgs/RobotStatus
    /robot2/robot_status      amr_msgs/RobotStatus
    /robot3/robot_status      amr_msgs/RobotStatus

  ACTIONS:
    /robot1/navigate_to_pose  nav2_msgs/NavigateToPose (action client)
    /robot2/navigate_to_pose  nav2_msgs/NavigateToPose (action client)
    /robot3/navigate_to_pose  nav2_msgs/NavigateToPose (action client)

  PUBLISHES:
    /dispatcher/queue_size    std_msgs/Int32    (current backlog depth)
    /dispatcher/log           std_msgs/String   (assignment decisions log)
"""

import math
from collections import deque

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.callback_groups import ReentrantCallbackGroup
from geometry_msgs.msg import PointStamped, PoseStamped
from std_msgs.msg import String, Int32
from nav2_msgs.action import NavigateToPose
from amr_msgs.msg import RobotStatus


class GoalDispatcher(Node):

    def __init__(self):
        super().__init__('goal_dispatcher')

        self.declare_parameter('robot_ids', ['robot1', 'robot2', 'robot3'])
        self.declare_parameter('goal_z_orientation_w', 1.0)  # face forward by default

        self.robot_ids = self.get_parameter('robot_ids').value
        self._default_orientation_w = self.get_parameter('goal_z_orientation_w').value

        self.cb_group = ReentrantCallbackGroup()

        # Default spawn locations in warehouse
        spawns = {'robot1': (3.0, 2.0), 'robot2': (10.0, 1.5), 'robot3': (17.0, 2.0)}
        # Per-robot state: status + last known position
        self._robot_state: dict[str, dict] = {
            rid: {
                'status': RobotStatus.IDLE,
                'pose_x': spawns.get(rid, (0.0, 0.0))[0],
                'pose_y': spawns.get(rid, (0.0, 0.0))[1],
            }
            for rid in self.robot_ids
        }
        # Currently active goal handles keyed by robot_id
        self._active_handles: dict[str, object] = {}

        # Goal queue for points that arrive when all robots are busy
        self._goal_queue: deque[PointStamped] = deque()

        # ── Publishers ─────────────────────────────────────────────────────────
        self._queue_size_pub = self.create_publisher(Int32, '/dispatcher/queue_size', 10)
        self._log_pub = self.create_publisher(String, '/dispatcher/log', 20)

        # ── Subscriptions ──────────────────────────────────────────────────────
        # RViz "Publish Point" tool
        self.create_subscription(
            PointStamped,
            '/clicked_point',
            self._clicked_point_cb,
            10,
            callback_group=self.cb_group,
        )
        # RViz "2D Goal Pose" tool
        self.create_subscription(
            PoseStamped,
            '/goal_pose',
            self._goal_pose_cb,
            10,
            callback_group=self.cb_group,
        )

        # Ground-truth pose from Gazebo PosePublisher for live real-time positions
        for rid in self.robot_ids:
            self.create_subscription(
                PoseStamped,
                f'/{rid}/ground_truth_pose',
                lambda msg, r=rid: self._ground_truth_pose_cb(msg, r),
                10,
                callback_group=self.cb_group,
            )

        # Per-robot status from coordination stack
        for rid in self.robot_ids:
            self.create_subscription(
                RobotStatus,
                f'/{rid}/robot_status',
                lambda msg, r=rid: self._status_cb(msg, r),
                10,
                callback_group=self.cb_group,
            )

        # ── Nav2 action clients ────────────────────────────────────────────────
        self._nav_clients: dict[str, ActionClient] = {}
        for rid in self.robot_ids:
            self._nav_clients[rid] = ActionClient(
                self,
                NavigateToPose,
                f'/{rid}/navigate_to_pose',
                callback_group=self.cb_group,
            )

        self.get_logger().info(
            f'[dispatcher] Ready. Managing robots: {self.robot_ids}'
        )

    # ── Callbacks ──────────────────────────────────────────────────────────────

    def _ground_truth_pose_cb(self, msg: PoseStamped, robot_id: str):
        """Update live robot position from Gazebo ground-truth pose."""
        self._robot_state[robot_id]['pose_x'] = msg.pose.position.x
        self._robot_state[robot_id]['pose_y'] = msg.pose.position.y

    def _status_cb(self, msg: RobotStatus, robot_id: str):
        """Update per-robot state and trigger queue drain if robot went IDLE."""
        prev_status = self._robot_state[robot_id]['status']
        self._robot_state[robot_id]['status'] = msg.status
        if msg.pose_x != 0.0 or msg.pose_y != 0.0:
            self._robot_state[robot_id]['pose_x'] = msg.pose_x
            self._robot_state[robot_id]['pose_y'] = msg.pose_y

        if prev_status == RobotStatus.BUSY and msg.status == RobotStatus.IDLE:
            self._log(f'{robot_id} is now IDLE — checking queue (depth={len(self._goal_queue)})')
            self._drain_queue()

    def _clicked_point_cb(self, msg: PointStamped):
        """Assign click to nearest idle robot, or queue if all busy."""
        pose = PoseStamped()
        pose.header = msg.header
        if pose.header.frame_id == '':
            pose.header.frame_id = 'map'
        pose.pose.position = msg.point
        pose.pose.orientation.w = self._default_orientation_w
        self._log(
            f'Received click at ({msg.point.x:.2f}, {msg.point.y:.2f})'
        )
        self._try_dispatch(pose)

    def _goal_pose_cb(self, msg: PoseStamped):
        """Assign 2D Goal Pose to nearest idle robot, or queue if all busy."""
        if msg.header.frame_id == '':
            msg.header.frame_id = 'map'
        self._log(
            f'Received 2D Goal Pose at ({msg.pose.position.x:.2f}, {msg.pose.position.y:.2f})'
        )
        self._try_dispatch(msg)

    # ── Dispatch logic ─────────────────────────────────────────────────────────

    def _try_dispatch(self, pose: PoseStamped):
        """Try to assign the goal to the nearest idle robot. Queue on failure."""
        best_robot = None
        best_dist = float('inf')

        target_x = pose.pose.position.x
        target_y = pose.pose.position.y

        for rid, state in self._robot_state.items():
            if state['status'] != RobotStatus.IDLE:
                continue
            if rid in self._active_handles:
                continue  # still has pending handle
            dx = target_x - state['pose_x']
            dy = target_y - state['pose_y']
            dist = math.sqrt(dx * dx + dy * dy)
            if dist < best_dist:
                best_dist = dist
                best_robot = rid

        if best_robot is None:
            self._log(
                f'All robots busy — queuing goal at '
                f'({target_x:.2f}, {target_y:.2f}). '
                f'Queue depth: {len(self._goal_queue) + 1}'
            )
            self._goal_queue.append(pose)
            self._publish_queue_size()
            return

        self._assign_goal(best_robot, pose, best_dist)

    def _drain_queue(self):
        """Assign queued goals to idle robots until queue is empty or all busy."""
        while self._goal_queue:
            # Check if any robot is idle
            has_idle = any(
                s['status'] == RobotStatus.IDLE and rid not in self._active_handles
                for rid, s in self._robot_state.items()
            )
            if not has_idle:
                break
            pose = self._goal_queue.popleft()
            self._publish_queue_size()
            self._try_dispatch(pose)

    def _assign_goal(self, robot_id: str, pose: PoseStamped, distance: float):
        """Send NavigateToPose action goal to the chosen robot."""
        # Mark as occupied immediately (before action response arrives)
        self._robot_state[robot_id]['status'] = RobotStatus.BUSY

        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = pose
        if goal_msg.pose.header.frame_id == '':
            goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        if goal_msg.pose.pose.orientation.w == 0.0 and goal_msg.pose.pose.orientation.z == 0.0:
            goal_msg.pose.pose.orientation.w = self._default_orientation_w

        self._log(
            f'Assigning goal ({pose.pose.position.x:.2f}, {pose.pose.position.y:.2f}) '
            f'to {robot_id} (dist={distance:.2f}m)'
        )

        client = self._nav_clients[robot_id]
        if not client.server_is_ready():
            self.get_logger().warn(
                f'[dispatcher] {robot_id} action server not ready — re-queuing'
            )
            self._robot_state[robot_id]['status'] = RobotStatus.IDLE
            self._goal_queue.appendleft(pose)
            self._publish_queue_size()
            return

        send_future = client.send_goal_async(goal_msg)
        send_future.add_done_callback(
            lambda fut, rid=robot_id, pt=pose: self._goal_response_cb(fut, rid, pt)
        )

    def _goal_response_cb(self, future, robot_id: str, pose: PoseStamped):
        """Handle goal acceptance."""
        handle = future.result()
        if not handle.accepted:
            self.get_logger().error(
                f'[dispatcher] {robot_id} rejected goal — re-queuing'
            )
            self._robot_state[robot_id]['status'] = RobotStatus.IDLE
            self._goal_queue.appendleft(pose)
            self._publish_queue_size()
            return

        self._log(f'{robot_id} accepted goal — waiting for result')
        self._active_handles[robot_id] = handle
        result_future = handle.get_result_async()
        result_future.add_done_callback(
            lambda fut, rid=robot_id: self._goal_result_cb(fut, rid)
        )

    def _goal_result_cb(self, future, robot_id: str):
        """Handle goal completion. Robot's own goal_sequencer also publishes IDLE."""
        self._active_handles.pop(robot_id, None)
        result = future.result()

        from action_msgs.msg import GoalStatus
        if result.status == GoalStatus.STATUS_SUCCEEDED:
            self._log(f'{robot_id} reached goal successfully')
        else:
            self.get_logger().warn(
                f'[dispatcher] {robot_id} goal ended with status {result.status}'
            )
        # RobotStatus.IDLE will arrive from goal_sequencer; queue drain happens there.
        # As belt-and-suspenders: mark idle locally too in case status message is delayed.
        self._robot_state[robot_id]['status'] = RobotStatus.IDLE
        self._drain_queue()

    # ── Helpers ────────────────────────────────────────────────────────────────

    def _log(self, text: str):
        """Publish a log message to /dispatcher/log and to the logger."""
        self.get_logger().info(f'[dispatcher] {text}')
        msg = String()
        msg.data = f'[dispatcher] {text}'
        self._log_pub.publish(msg)

    def _publish_queue_size(self):
        msg = Int32()
        msg.data = len(self._goal_queue)
        self._queue_size_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = GoalDispatcher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

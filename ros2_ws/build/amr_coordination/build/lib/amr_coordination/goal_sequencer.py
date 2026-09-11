"""Goal Sequencer — sends navigation goals in sequence and records completion times.

Modes:
  coordinated  — auto-sends waypoints from config; coordinates with peers
  baseline     — auto-sends waypoints with priority-based stagger delay
  dispatcher   — passive mode: waits for goals from goal_dispatcher node;
                  does NOT auto-send waypoints; publishes RobotStatus
"""

import json
import math
import yaml
import os

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.callback_groups import ReentrantCallbackGroup
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
from std_msgs.msg import String
from action_msgs.msg import GoalStatus
from amr_msgs.msg import RobotStatus


class GoalSequencer(Node):
    def __init__(self):
        super().__init__('goal_sequencer')

        self.declare_parameter('robot_id', 'robot1')
        self.declare_parameter('mode', 'coordinated')
        self.declare_parameter('waypoints_file', '')

        self.robot_id = self.get_parameter('robot_id').value
        self.mode = self.get_parameter('mode').value
        waypoints_file = self.get_parameter('waypoints_file').value

        # Load waypoints
        with open(waypoints_file, 'r') as f:
            all_waypoints = yaml.safe_load(f)

        robot_config = all_waypoints.get(self.robot_id, {})
        self.goals = robot_config.get('goals', [])

        self.get_logger().info(
            f'[{self.robot_id}] Goal sequencer started in {self.mode} mode '
            f'with {len(self.goals)} goals'
        )

        # Nav2 action client
        self.cb_group = ReentrantCallbackGroup()
        self.nav_client = ActionClient(
            self,
            NavigateToPose,
            f'/{self.robot_id}/navigate_to_pose',
            callback_group=self.cb_group,
        )

        # Metrics publisher
        self.metrics_pub = self.create_publisher(String, '/metrics', 10)

        self.current_goal_idx = 0
        self.retry_count = 0
        self.max_retries = 3
        self.start_time = None
        self.goal_send_time = None

        # Priority-based delay for baseline mode
        priority_map = {'robot1': 1, 'robot2': 2, 'robot3': 3}
        self.priority = priority_map.get(self.robot_id, 1)

        # ── RobotStatus publisher — read by goal_dispatcher ─────────────────
        self.status_pub = self.create_publisher(
            RobotStatus, f'/{self.robot_id}/robot_status', 10
        )
        # Current pose for position reporting to dispatcher
        self._current_x = 0.0
        self._current_y = 0.0
        self.pose_sub = self.create_subscription(
            PoseStamped,
            f'/{self.robot_id}/ground_truth_pose',
            self._pose_cb,
            10,
            callback_group=self.cb_group,
        )
        # Publish IDLE status immediately
        self._publish_status(RobotStatus.IDLE)

        # Wait for Nav2 to be ready, then start sending goals
        self._wait_timer = self.create_timer(2.0, self._wait_for_nav2, callback_group=self.cb_group)

    def _create_one_shot_timer(self, delay, callback):
        timer = [None]
        def _wrapper():
            if timer[0] is not None:
                self.destroy_timer(timer[0])
            callback()
        timer[0] = self.create_timer(delay, _wrapper, callback_group=self.cb_group)
        return timer[0]

    def _pose_cb(self, msg):
        """Track current position for RobotStatus reporting."""
        pose = msg.pose.pose if hasattr(msg.pose, 'pose') else msg.pose
        self._current_x = pose.position.x
        self._current_y = pose.position.y

    def _publish_status(self, status_val: int):
        """Publish current robot status (IDLE or BUSY) with position."""
        msg = RobotStatus()
        msg.robot_id = self.robot_id
        msg.status = status_val
        msg.pose_x = self._current_x
        msg.pose_y = self._current_y
        msg.stamp = self.get_clock().now().to_msg()
        self.status_pub.publish(msg)

    def _wait_for_nav2(self):
        """Wait for Nav2 action server, then start goals."""
        if not self.nav_client.wait_for_server(timeout_sec=1.0):
            self.get_logger().info(
                f'[{self.robot_id}] Waiting for Nav2 action server...'
            )
            return

        self.get_logger().info(f'[{self.robot_id}] Nav2 is ready!')
        # Destroy the waiting timer
        self.destroy_timer(self._wait_timer)

        if self.mode == 'baseline':
            # In baseline mode, stagger start by priority
            delay = (self.priority - 1) * 10.0
            self.get_logger().info(
                f'[{self.robot_id}] Baseline mode: waiting {delay}s before starting'
            )
            self._create_one_shot_timer(
                delay if delay > 0 else 0.1,
                self._start_goals,
            )
        elif self.mode == 'dispatcher':
            # Dispatcher mode: do NOT auto-send waypoints.
            # goal_dispatcher will send NavigateToPose goals directly.
            # This node remains alive to publish RobotStatus and handle callbacks.
            self.get_logger().info(
                f'[{self.robot_id}] Dispatcher mode: ready, waiting for goals from dispatcher'
            )
        else:
            self._start_goals()

    def _start_goals(self):
        """Begin sending goals."""
        # Destroy the delay timer if it exists
        if hasattr(self, '_delay_timer'):
            self.destroy_timer(self._delay_timer)

        self.start_time = self.get_clock().now()
        self._send_next_goal()

    def _send_next_goal(self):
        """Send the next goal in the sequence."""
        if self.current_goal_idx >= len(self.goals):
            self._all_goals_done()
            return

        goal = self.goals[self.current_goal_idx]
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = PoseStamped()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = float(goal[0])
        goal_msg.pose.pose.position.y = float(goal[1])

        # Convert yaw to quaternion
        yaw = float(goal[2])
        goal_msg.pose.pose.orientation.z = math.sin(yaw / 2.0)
        goal_msg.pose.pose.orientation.w = math.cos(yaw / 2.0)

        self.goal_send_time = self.get_clock().now()
        self.get_logger().info(
            f'[{self.robot_id}] Sending goal {self.current_goal_idx}: '
            f'({goal[0]}, {goal[1]})'
        )

        # Mark BUSY before sending so dispatcher knows immediately
        self._publish_status(RobotStatus.BUSY)

        send_goal_future = self.nav_client.send_goal_async(
            goal_msg,
            feedback_callback=self._feedback_cb,
        )
        send_goal_future.add_done_callback(self._goal_response_cb)

    def _goal_response_cb(self, future):
        """Handle goal acceptance/rejection."""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error(
                f'[{self.robot_id}] Goal {self.current_goal_idx} rejected!'
            )
            # Retry after a short delay
            self._create_one_shot_timer(
                3.0,
                self._send_next_goal,
            )
            return

        self.get_logger().info(
            f'[{self.robot_id}] Goal {self.current_goal_idx} accepted'
        )
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self._goal_result_cb)

    def _goal_result_cb(self, future):
        """Handle goal completion."""
        result = future.result()
        status = result.status
        now = self.get_clock().now()

        duration = (now - self.goal_send_time).nanoseconds / 1e9

        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info(
                f'[{self.robot_id}] Goal {self.current_goal_idx} reached '
                f'in {duration:.1f}s'
            )
            self.retry_count = 0
        else:
            self.get_logger().warn(
                f'[{self.robot_id}] Goal {self.current_goal_idx} finished '
                f'with status {status} in {duration:.1f}s'
            )
            if self.retry_count < self.max_retries:
                self.retry_count += 1
                self.get_logger().info(
                    f'[{self.robot_id}] Retrying goal {self.current_goal_idx} '
                    f'(attempt {self.retry_count}/{self.max_retries}) in 2.0s...'
                )
                self._create_one_shot_timer(
                    2.0,
                    self._send_next_goal,
                )
                return
            else:
                self.get_logger().error(
                    f'[{self.robot_id}] Goal {self.current_goal_idx} failed after '
                    f'{self.max_retries} retries — skipping.'
                )
                self.retry_count = 0
                # Skip failed goal — publish a failed metric then fall through
                metric = {
                    'robot_id': self.robot_id,
                    'waypoint_idx': self.current_goal_idx,
                    'send_time': self.goal_send_time.nanoseconds / 1e9,
                    'reach_time': self.get_clock().now().nanoseconds / 1e9,
                    'duration': (self.get_clock().now() - self.goal_send_time).nanoseconds / 1e9,
                    'mode': self.mode,
                    'status': status,
                    'skipped': True,
                }
                msg2 = String()
                msg2.data = json.dumps(metric)
                self.metrics_pub.publish(msg2)
                self.current_goal_idx += 1
                self._send_next_goal()
                return

        # Publish metric
        metric = {
            'robot_id': self.robot_id,
            'waypoint_idx': self.current_goal_idx,
            'send_time': self.goal_send_time.nanoseconds / 1e9,
            'reach_time': now.nanoseconds / 1e9,
            'duration': duration,
            'mode': self.mode,
            'status': status,
        }
        msg = String()
        msg.data = json.dumps(metric)
        self.metrics_pub.publish(msg)

        # Move to next goal
        self.current_goal_idx += 1
        if self.mode == 'baseline' and self.current_goal_idx < len(self.goals):
            # In baseline mode, add a small inter-goal delay
            self._create_one_shot_timer(
                2.0,
                self._send_next_goal,
            )
        else:
            self._send_next_goal()

    def _all_goals_done(self):
        """All goals completed — publish summary."""
        if hasattr(self, '_completed') and self._completed:
            return
        self._completed = True
        now = self.get_clock().now()
        total_time = (now - self.start_time).nanoseconds / 1e9

        self.get_logger().info(
            f'[{self.robot_id}] ALL GOALS DONE in {total_time:.1f}s ({self.mode} mode)'
        )

        metric = {
            'robot_id': self.robot_id,
            'event': 'ALL_DONE',
            'total_time': total_time,
            'mode': self.mode,
        }
        msg = String()
        msg.data = json.dumps(metric)
        self.metrics_pub.publish(msg)

        # Report IDLE — dispatcher will assign next queued goal if any
        self._publish_status(RobotStatus.IDLE)

    def _feedback_cb(self, feedback_msg):
        """Optional: log navigation feedback."""
        pass


def main(args=None):
    rclpy.init(args=args)
    node = GoalSequencer()
    # _wait_timer is already stored in __init__ — do NOT reassign here.
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

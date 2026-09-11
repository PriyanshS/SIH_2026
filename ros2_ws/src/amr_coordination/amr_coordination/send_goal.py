"""Interactive and CLI tool to send custom navigation goals to any robot.

Usage:
  # CLI mode:
  ros2 run amr_coordination send_goal --robot robot1 --x 14.0 --y 8.0
  ros2 run amr_coordination send_goal --robot robot2 --x 5.0 --y 12.0 --yaw 90

  # Interactive mode (prompts for inputs):
  ros2 run amr_coordination send_goal
"""

import argparse
import math
import sys
import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose
from action_msgs.msg import GoalStatus


class CustomGoalSender(Node):
    def __init__(self, robot_id: str, x: float, y: float, yaw_deg: float):
        super().__init__('custom_goal_sender')
        self.robot_id = robot_id
        self.target_x = x
        self.target_y = y
        self.target_yaw_rad = math.radians(yaw_deg)

        self.action_client = ActionClient(
            self,
            NavigateToPose,
            f'/{self.robot_id}/navigate_to_pose'
        )

        self.get_logger().info(
            f'Connecting to Nav2 action server: /{self.robot_id}/navigate_to_pose...'
        )

    def execute(self, timeout_sec: float = 60.0) -> bool:
        if not self.action_client.wait_for_server(timeout_sec=10.0):
            self.get_logger().error(
                f'Action server /{self.robot_id}/navigate_to_pose not available!'
            )
            return False

        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = PoseStamped()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = float(self.target_x)
        goal_msg.pose.pose.position.y = float(self.target_y)
        goal_msg.pose.pose.position.z = 0.0

        # Orientation from yaw
        goal_msg.pose.pose.orientation.z = math.sin(self.target_yaw_rad / 2.0)
        goal_msg.pose.pose.orientation.w = math.cos(self.target_yaw_rad / 2.0)

        self.get_logger().info(
            f'>>> Sending custom goal to [{self.robot_id}]: '
            f'X={self.target_x:.2f}, Y={self.target_y:.2f}, Yaw={math.degrees(self.target_yaw_rad):.1f}°'
        )

        send_goal_future = self.action_client.send_goal_async(
            goal_msg,
            feedback_callback=self._feedback_cb
        )
        rclpy.spin_until_future_complete(self, send_goal_future)

        goal_handle = send_goal_future.result()
        if not goal_handle.accepted:
            self.get_logger().error(f'Goal rejected by {self.robot_id} Nav2 stack!')
            return False

        self.get_logger().info(f'Goal accepted by {self.robot_id}! Robot is now driving.')
        result_future = goal_handle.get_result_async()
        start_time = time.time()

        while rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0.2)
            if result_future.done():
                status = result_future.result().status
                elapsed = time.time() - start_time
                if status == GoalStatus.STATUS_SUCCEEDED:
                    self.get_logger().info(
                        f'SUCCESS: [{self.robot_id}] reached custom goal ({self.target_x:.2f}, {self.target_y:.2f}) in {elapsed:.1f}s!'
                    )
                    return True
                else:
                    self.get_logger().warn(
                        f'Navigation finished with status {status} in {elapsed:.1f}s'
                    )
                    return False

            if time.time() - start_time > timeout_sec:
                self.get_logger().error('Navigation timed out!')
                goal_handle.cancel_goal_async()
                return False

        return False

    def _feedback_cb(self, feedback_msg):
        feedback = feedback_msg.feedback
        dist = feedback.distance_remaining
        time_elapsed = feedback.navigation_time.sec
        print(f'\r[{self.robot_id}] Remaining distance: {dist:.2f} m | Time: {time_elapsed} s', end='', flush=True)


def main(args=None):
    parser = argparse.ArgumentParser(description='Send custom navigation goals to warehouse AMRs')
    parser.add_argument('--robot', type=str, default=None, choices=['robot1', 'robot2', 'robot3'],
                        help='Target robot name')
    parser.add_argument('--x', type=float, default=None, help='Target map X coordinate (1.0 to 19.0)')
    parser.add_argument('--y', type=float, default=None, help='Target map Y coordinate (1.0 to 14.0)')
    parser.add_argument('--yaw', type=float, default=0.0, help='Target orientation in degrees (default 0.0)')
    parser.add_argument('--timeout', type=float, default=90.0, help='Navigation timeout in seconds (default 90.0)')

    # Parse known args to avoid ROS 2 CLI flags interfering
    parsed, remaining = parser.parse_known_args(args=sys.argv[1:])

    robot_id = parsed.robot
    x = parsed.x
    y = parsed.y
    yaw = parsed.yaw

    # Interactive prompt if parameters are missing
    if robot_id is None or x is None or y is None:
        print('\n======================================================')
        print('      AMR Custom Goal Dispatcher (Interactive)       ')
        print('======================================================')
        print('Warehouse Bounds: X: [1.0m to 19.0m], Y: [1.0m to 14.0m]')
        print('Chokepoint is at: X: [9.0m to 11.0m], Y: [6.0m to 8.5m]\n')

        if robot_id is None:
            choice = input('Select Robot (1: robot1 [Red], 2: robot2 [Green], 3: robot3 [Blue]) [1]: ').strip()
            robot_map = {'1': 'robot1', '2': 'robot2', '3': 'robot3', 'robot1': 'robot1', 'robot2': 'robot2', 'robot3': 'robot3'}
            robot_id = robot_map.get(choice, 'robot1')

        if x is None:
            val = input(f'Enter Target X coordinate for {robot_id} (e.g. 14.0): ').strip()
            x = float(val) if val else 10.0

        if y is None:
            val = input(f'Enter Target Y coordinate for {robot_id} (e.g. 8.0): ').strip()
            y = float(val) if val else 8.0

        yaw_input = input('Enter Target Heading / Yaw in degrees [default 0.0]: ').strip()
        if yaw_input:
            yaw = float(yaw_input)

    rclpy.init(args=args)
    node = CustomGoalSender(robot_id, x, y, yaw)
    try:
        success = node.execute(timeout_sec=parsed.timeout)
        print('')  # newline after feedback
        sys.exit(0 if success else 1)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

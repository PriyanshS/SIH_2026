"""Scenario T5: Rapid multi-goal dispatch.

Exercises the goal_dispatcher queuing logic.
Presenter clicks 5 goals in quick succession:
  - First two go to the two nearest idle robots
  - Third arrives before either finishes → queued
  - Fourth and fifth → also queued
  - As each robot finishes, the next queued goal is dispatched

No waypoints are pre-programmed — the dispatcher provides all goals from
RViz clicks or the automated click simulation below.

For automated testing (no RViz needed):
  ros2 topic pub --once /clicked_point geometry_msgs/PointStamped \
    '{header: {frame_id: map}, point: {x: 3.0, y: 2.0, z: 0.0}}'

Run with:
  ros2 launch amr_bringup scenarios/rapid_dispatch.launch.py

Then in RViz: use the "Publish Point" tool to click 5 points quickly.
Watch /dispatcher/queue_size and /dispatcher/log:
  ros2 topic echo /dispatcher/log
  ros2 topic echo /dispatcher/queue_size
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    pkg_amr_bringup = get_package_share_directory('amr_bringup')

    headless = LaunchConfiguration('headless')
    declare_headless = DeclareLaunchArgument('headless', default_value='false')

    # Full demo in dispatcher mode — robots wait for clicks rather than auto-navigating
    full_demo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_amr_bringup, 'launch', 'full_demo.launch.py')
        ),
        launch_arguments={
            'headless': headless,
            'mode': 'dispatcher',  # goal_sequencers wait for dispatcher goals
        }.items(),
    )

    return LaunchDescription([
        declare_headless,
        full_demo,
    ])

"""Interactive RViz demo launch — Gazebo + Nav2 + Dispatcher mode + RViz.

In this mode, robots sit in IDLE waiting for user/evaluator input.
Click anywhere on the map in RViz using the 'Publish Point' tool (hotkey 'p')
or the '2D Goal Pose' tool to dynamically dispatch the nearest robot to that location in real time!
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    pkg_amr_bringup = get_package_share_directory('amr_bringup')
    headless = LaunchConfiguration('headless')

    declare_headless = DeclareLaunchArgument(
        'headless', default_value='false',
        description='Run Gazebo in server-only headless mode'
    )

    full_demo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_amr_bringup, 'launch', 'full_demo.launch.py')
        ),
        launch_arguments={
            'mode': 'dispatcher',
            'rviz': 'true',
            'headless': headless,
        }.items(),
    )

    return LaunchDescription([
        declare_headless,
        full_demo,
    ])

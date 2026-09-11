"""Scenario T6: Dynamic obstacle appears mid-path.

Spawns a box obstacle in the path of robot2 after it has already started
navigating. Demonstrates the obstacle_relay pipeline:
  1. robot2's lidar detects the box
  2. obstacle_relay clusters it and broadcasts on /detected_obstacles
  3. robot1 and robot3's obstacle_relay nodes receive it and inject a virtual
     LaserScan into their costmaps
  4. All robots' Nav2 planners replan around the new obstacle
  5. robot2 itself replans via its own local costmap

This scenario can also be triggered manually:
  ros2 run gazebo_ros spawn_entity.py -entity obstacle_box \
    -x 0.0 -y -1.0 -z 0.5 \
    -urdf -param /robot_description_box

Expected behavior:
  - robot2 stops, replans, takes alternate route
  - /detected_obstacles shows reporter_id=robot2
  - Virtual scan injection visible in RViz local costmap of robot1

Run with:
  ros2 launch amr_bringup scenarios/dynamic_obstacle.launch.py
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    ExecuteProcess,
    IncludeLaunchDescription,
    TimerAction,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    pkg_amr_bringup = get_package_share_directory('amr_bringup')
    pkg_amr_gazebo = get_package_share_directory('amr_gazebo')

    headless = LaunchConfiguration('headless')
    declare_headless = DeclareLaunchArgument('headless', default_value='false')

    # Full coordinated demo
    full_demo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_amr_bringup, 'launch', 'full_demo.launch.py')
        ),
        launch_arguments={'headless': headless, 'mode': 'coordinated'}.items(),
    )

    # Spawn the obstacle box after 60 s (robots will be mid-path by then)
    # The box is placed at (0, -1, 0.5) — directly in robot2's chokepoint path
    obstacle_sdf = os.path.join(pkg_amr_gazebo, 'models', 'obstacle_box', 'model.sdf')

    spawn_obstacle = TimerAction(
        period=60.0,
        actions=[
            ExecuteProcess(
                cmd=[
                    'ros2', 'service', 'call',
                    '/world/warehouse/create',
                    'ros_gz_interfaces/srv/SpawnEntity',
                    (
                        '{'
                        '"xml": "<?xml version=\\"1.0\\" ?>'
                        '<sdf version=\\"1.9\\">'
                        '<model name=\\"obstacle_box\\">'
                        '<static>true</static>'
                        '<pose>0 -1 0.5 0 0 0</pose>'
                        '<link name=\\"link\\">'
                        '<collision name=\\"collision\\">'
                        '<geometry><box><size>0.5 0.5 1.0</size></box></geometry>'
                        '</collision>'
                        '<visual name=\\"visual\\">'
                        '<geometry><box><size>0.5 0.5 1.0</size></box></geometry>'
                        '<material><ambient>1 0.5 0 1</ambient></material>'
                        '</visual>'
                        '</link>'
                        '</model>'
                        '</sdf>"'
                        '}'
                    ),
                ],
                output='screen',
            )
        ],
    )

    return LaunchDescription([
        declare_headless,
        full_demo,
        spawn_obstacle,
    ])

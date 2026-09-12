"""Full demo launch — Gazebo + Nav2 (×3) + Coordination (all nodes).

Localization & Architecture:
  - Ground-truth localization: Robot position is published by Gazebo's PosePublisher plugin.
  - Map: Static warehouse map provided by nav2_map_server.
  - TF tree: map → <ns>/odom (static transform at spawn) → <ns>/base_link (Gazebo diff-drive odom).

Timing rationale:
  0 s  — Gazebo simulation world starts with all 3 AMR robots
 10 s  — Nav2 stack for robot1
 12.5s — Nav2 stack for robot2
 15 s  — Nav2 stack for robot3
 25 s  — Coordination nodes launch & issue navigation goals; all robots start driving!
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_amr_gazebo = get_package_share_directory('amr_gazebo')
    pkg_amr_nav = get_package_share_directory('amr_nav')
    pkg_amr_coordination = get_package_share_directory('amr_coordination')

    headless = LaunchConfiguration('headless')
    mode = LaunchConfiguration('mode')
    rviz = LaunchConfiguration('rviz')

    declare_headless = DeclareLaunchArgument(
        'headless', default_value='false',
        description='Run Gazebo in server-only headless mode'
    )
    declare_mode = DeclareLaunchArgument(
        'mode', default_value='coordinated',
        description='Coordination mode: coordinated | baseline | dispatcher'
    )
    declare_rviz = DeclareLaunchArgument(
        'rviz', default_value='true',
        description='Launch RViz2 visualization automatically'
    )

    # 1. Launch Gazebo world with 3 robots
    sim_world = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_amr_gazebo, 'launch', 'sim_world.launch.py')
        ),
        launch_arguments={'headless': headless}.items(),
    )

    # 2. Launch Nav2 for each robot
    nav_robot1 = TimerAction(
        period=12.0,
        actions=[IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_amr_nav, 'launch', 'robot_nav.launch.py')
            ),
            launch_arguments={'namespace': 'robot1'}.items(),
        )],
    )

    nav_robot2 = TimerAction(
        period=14.5,
        actions=[IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_amr_nav, 'launch', 'robot_nav.launch.py')
            ),
            launch_arguments={'namespace': 'robot2'}.items(),
        )],
    )

    nav_robot3 = TimerAction(
        period=17.0,
        actions=[IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_amr_nav, 'launch', 'robot_nav.launch.py')
            ),
            launch_arguments={'namespace': 'robot3'}.items(),
        )],
    )

    # 3. Coordination nodes (wait for Nav2 lifecycle managers to activate)
    coordination = TimerAction(
        period=24.0,
        actions=[IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_amr_coordination, 'launch', 'coordination.launch.py')
            ),
            launch_arguments={'mode': mode}.items(),
        )],
    )

    # 4. RViz2 node (opens multi_robot.rviz for live visualization & dispatching)
    rviz_node = TimerAction(
        period=22.0,
        actions=[Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', os.path.join(pkg_amr_gazebo, 'rviz', 'multi_robot.rviz')],
            parameters=[{'use_sim_time': True}],
            condition=IfCondition(rviz),
        )],
    )

    return LaunchDescription([
        declare_headless,
        declare_mode,
        declare_rviz,
        sim_world,
        nav_robot1,
        nav_robot2,
        nav_robot3,
        coordination,
        rviz_node,
    ])

"""Web Demo Launch — Gazebo + Nav2 (x3) + Coordination + Web Fleet Dashboard.

Launches the complete decentralized fleet along with the real-time Web Bridge Node.
Access the web dashboard in your browser at: http://localhost:8090
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
        'mode', default_value='dispatcher',
        description='Coordination mode: dispatcher (interactive UI) | coordinated (automated)'
    )
    declare_rviz = DeclareLaunchArgument(
        'rviz', default_value='false',
        description='Launch RViz2 alongside the Web UI (default: false)'
    )

    # 1. Gazebo simulation world
    sim_world = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_amr_gazebo, 'launch', 'sim_world.launch.py')
        ),
        launch_arguments={'headless': headless}.items(),
    )

    # 2. Nav2 for each robot
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

    # 3. Peer Coordination nodes
    coordination = TimerAction(
        period=24.0,
        actions=[IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_amr_coordination, 'launch', 'coordination.launch.py')
            ),
            launch_arguments={'mode': mode}.items(),
        )],
    )

    # 4. Web Bridge Node (starts at t=20s so UI is ready when fleet comes online)
    web_bridge = TimerAction(
        period=20.0,
        actions=[Node(
            package='amr_coordination',
            executable='web_bridge_node',
            name='web_bridge_node',
            output='screen',
            parameters=[{'use_sim_time': True}],
        )],
    )

    # 5. Optional RViz2
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
        web_bridge,
        rviz_node,
    ])

"""Full baseline launch — Gazebo + Nav2 (×3) + Baseline (no coordination).

Same scenario but with sequential stop-and-wait instead of coordination.
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    pkg_amr_gazebo = get_package_share_directory('amr_gazebo')
    pkg_amr_nav = get_package_share_directory('amr_nav')
    pkg_amr_coordination = get_package_share_directory('amr_coordination')

    headless = LaunchConfiguration('headless')
    declare_headless = DeclareLaunchArgument(
        'headless', default_value='false',
        description='Run Gazebo in server-only headless mode'
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
        period=10.0,
        actions=[IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_amr_nav, 'launch', 'robot_nav.launch.py')
            ),
            launch_arguments={'namespace': 'robot1'}.items(),
        )],
    )

    nav_robot2 = TimerAction(
        period=12.5,
        actions=[IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_amr_nav, 'launch', 'robot_nav.launch.py')
            ),
            launch_arguments={'namespace': 'robot2'}.items(),
        )],
    )

    nav_robot3 = TimerAction(
        period=15.0,
        actions=[IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_amr_nav, 'launch', 'robot_nav.launch.py')
            ),
            launch_arguments={'namespace': 'robot3'}.items(),
        )],
    )

    # 3. Launch baseline nodes (no coordination — just staggered goals)
    baseline = TimerAction(
        period=25.0,
        actions=[IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_amr_coordination, 'launch', 'baseline.launch.py')
            ),
        )],
    )

    return LaunchDescription([
        declare_headless,
        sim_world,
        nav_robot1,
        nav_robot2,
        nav_robot3,
        baseline,
    ])

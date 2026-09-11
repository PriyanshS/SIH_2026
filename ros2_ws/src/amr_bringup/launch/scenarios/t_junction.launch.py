"""Scenario T1: T-junction / 4-way conflict.

Three robots approach one intersection simultaneously.
Waypoints override routes all three to converge at the center T-junction.

Expected behavior:
  - All three robots approach the junction at the same time
  - conflict_detector detects spatial-temporal overlap
  - Robots yield in priority order: robot1 proceeds, robot2 yields, robot3 yields last
  - Terminal shows reason strings from choke_reason topics

Run with:
  ros2 launch amr_bringup scenarios/t_junction.launch.py
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_amr_gazebo = get_package_share_directory('amr_gazebo')
    pkg_amr_nav = get_package_share_directory('amr_nav')
    pkg_amr_coordination = get_package_share_directory('amr_coordination')

    chokepoint_file = os.path.join(pkg_amr_coordination, 'config', 'chokepoint.yaml')

    headless = LaunchConfiguration('headless')
    declare_headless = DeclareLaunchArgument('headless', default_value='false')

    sim_world = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_amr_gazebo, 'launch', 'sim_world.launch.py')
        ),
        launch_arguments={'headless': headless}.items(),
    )

    # Nav2 stacks for all three robots (ground-truth localization)
    nav_robots = [
        TimerAction(period=10.0 + i * 2.5,
            actions=[IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(pkg_amr_nav, 'launch', 'robot_nav.launch.py')
                ),
                launch_arguments={'namespace': f'robot{i+1}'}.items(),
            )])
        for i in range(3)
    ]

    # T-junction waypoints: all robots aim at the junction centre
    # Robot 1: approaches from west  (-6, 0) → (0, 0) → (-6, 0)
    # Robot 2: approaches from east  ( 6, 0) → (0, 0) → ( 6, 0)
    # Robot 3: approaches from north ( 0, 5) → (0, 0) → ( 0, 5)
    robots = [
        {'name': 'robot1', 'priority': 1,
         'goals': [[-6.0, 0.0, 0.0], [0.0, 0.0, 0.0], [-6.0, 0.0, 3.14]]},
        {'name': 'robot2', 'priority': 2,
         'goals': [[6.0, 0.0, 3.14], [0.0, 0.0, 0.0], [6.0, 0.0, 0.0]]},
        {'name': 'robot3', 'priority': 3,
         'goals': [[0.0, 5.0, -1.57], [0.0, 0.0, 0.0], [0.0, 5.0, 1.57]]},
    ]
    peer_ids = [r['name'] for r in robots]

    coordination_nodes = []
    for robot in robots:
        ns = robot['name']
        pri = robot['priority']

        coordination_nodes.append(Node(
            package='amr_coordination', executable='choke_negotiator',
            name=f'{ns}_choke_negotiator', output='screen',
            parameters=[{'robot_id': ns, 'priority': pri,
                         'chokepoint_file': chokepoint_file,
                         'heartbeat_interval': 0.5, 'grant_timeout_base': 5.0,
                         'use_sim_time': True}],
        ))
        coordination_nodes.append(Node(
            package='amr_coordination', executable='conflict_detector',
            name=f'{ns}_conflict_detector', output='screen',
            parameters=[{'robot_id': ns, 'conflict_radius': 0.8,
                         'temporal_window': 3.0, 'check_rate': 2.0,
                         'use_sim_time': True}],
        ))
        coordination_nodes.append(Node(
            package='amr_coordination', executable='path_sharer',
            name=f'{ns}_path_sharer', output='screen',
            parameters=[{'robot_id': ns, 'peer_ids': peer_ids, 'use_sim_time': True}],
        ))
        coordination_nodes.append(Node(
            package='amr_coordination', executable='obstacle_relay',
            name=f'{ns}_obstacle_relay', output='screen',
            parameters=[{'robot_id': ns, 'use_sim_time': True}],
        ))
        # Inline goals via parameter (overrides file-based waypoints)
        coordination_nodes.append(Node(
            package='amr_coordination', executable='goal_sequencer',
            name=f'{ns}_goal_sequencer', output='screen',
            parameters=[{
                'robot_id': ns,
                'mode': 'coordinated',
                'goals_inline': str(robot['goals']),  # parsed in sequencer
                'use_sim_time': True,
            }],
        ))

    coordination = TimerAction(period=25.0, actions=coordination_nodes)

    return LaunchDescription([
        declare_headless,
        sim_world,
        *nav_robots,
        coordination,
    ])

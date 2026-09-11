"""Scenario T2: Dead-end deadlock.

Two robots face each other in a single-lane dead-end corridor.
One must back off to let the other pass.

Setup:
  - robot1 starts at west end, navigates east into the dead-end
  - robot2 starts at east end, navigates west into the dead-end
  - They meet in the middle with no room to pass

Expected behavior:
  - conflict_detector flags head-on overlap
  - robot2 (lower priority) yields, reverses to start
  - robot1 proceeds, robot2 then follows
  - choke_reason messages explain each yield decision

Run with:
  ros2 launch amr_bringup scenarios/dead_end_deadlock.launch.py
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

    # Only 2 robots for this scenario
    sim_world = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_amr_gazebo, 'launch', 'sim_world.launch.py')
        ),
        launch_arguments={'headless': headless, 'robots': 'robot1,robot2'}.items(),
    )

    nav_robots = [
        TimerAction(period=10.0 + i * 2.5,
            actions=[IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(pkg_amr_nav, 'launch', 'robot_nav.launch.py')
                ),
                launch_arguments={'namespace': f'robot{i+1}'}.items(),
            )])
        for i in range(2)
    ]

    # robot1: west→east; robot2: east→west — direct head-on collision path
    robots_cfg = [
        {'name': 'robot1', 'priority': 1, 'goals': [[4.0, 0.0, 0.0], [-4.0, 0.0, 3.14]]},
        {'name': 'robot2', 'priority': 2, 'goals': [[-4.0, 0.0, 3.14], [4.0, 0.0, 0.0]]},
    ]
    peer_ids = [r['name'] for r in robots_cfg]

    coordination_nodes = []
    for robot in robots_cfg:
        ns = robot['name']
        pri = robot['priority']

        for exe, name_suffix, params in [
            ('choke_negotiator', 'choke_negotiator',
             {'robot_id': ns, 'priority': pri, 'chokepoint_file': chokepoint_file,
              'heartbeat_interval': 0.5, 'grant_timeout_base': 5.0, 'use_sim_time': True}),
            ('conflict_detector', 'conflict_detector',
             {'robot_id': ns, 'conflict_radius': 0.8, 'temporal_window': 3.0,
              'check_rate': 2.0, 'use_sim_time': True}),
            ('path_sharer', 'path_sharer',
             {'robot_id': ns, 'peer_ids': peer_ids, 'use_sim_time': True}),
            ('obstacle_relay', 'obstacle_relay',
             {'robot_id': ns, 'use_sim_time': True}),
            ('goal_sequencer', 'goal_sequencer',
             {'robot_id': ns, 'mode': 'coordinated',
              'goals_inline': str(robot['goals']), 'use_sim_time': True}),
        ]:
            coordination_nodes.append(Node(
                package='amr_coordination',
                executable=exe,
                name=f'{ns}_{name_suffix}',
                output='screen',
                parameters=[params],
            ))

    coordination = TimerAction(period=25.0, actions=coordination_nodes)

    return LaunchDescription([
        declare_headless,
        sim_world,
        *nav_robots,
        coordination,
    ])

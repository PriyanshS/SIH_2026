"""Scenario T3: Simultaneous chokepoint requests.

All three robots request the same chokepoint at the same simulated instant
(start delays are set to zero). Verifies that the tie-break rule resolves
cleanly: priority → distance → robot_id, with no deadlock or infinite wait.

Expected behavior:
  - All three choke_negotiator instances enter REQUESTING simultaneously
  - robot1 (priority=1) self-grants first (shortest timeout)
  - robot2 yields to robot1, grants after robot1 releases
  - robot3 yields to both, grants last
  - No robot waits indefinitely — clean GRANT→IN_CHOKE→RELEASE sequence

Monitor:
  ros2 topic echo /choke_negotiation
  ros2 topic echo /robot1/choke_reason
  ros2 topic echo /robot2/choke_reason
  ros2 topic echo /robot3/choke_reason

Run with:
  ros2 launch amr_bringup scenarios/simultaneous_choke.launch.py
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

    # All robots aim directly at the chokepoint centre simultaneously
    # Start positions are equidistant so tie-break falls to priority
    robots_cfg = [
        {'name': 'robot1', 'priority': 1,
         'goals': [[0.0, 0.0, 0.0], [-5.0, 0.0, 3.14]]},
        {'name': 'robot2', 'priority': 2,
         'goals': [[0.0, 0.0, 0.0], [5.0, 2.0, 0.0]]},
        {'name': 'robot3', 'priority': 3,
         'goals': [[0.0, 0.0, 0.0], [5.0, -2.0, 0.0]]},
    ]
    peer_ids = [r['name'] for r in robots_cfg]

    coordination_nodes = []
    for robot in robots_cfg:
        ns = robot['name']
        pri = robot['priority']

        coordination_nodes.extend([
            Node(package='amr_coordination', executable='choke_negotiator',
                 name=f'{ns}_choke_negotiator', output='screen',
                 parameters=[{'robot_id': ns, 'priority': pri,
                              'chokepoint_file': chokepoint_file,
                              'heartbeat_interval': 0.5,
                              'grant_timeout_base': 5.0, 'use_sim_time': True}]),
            Node(package='amr_coordination', executable='conflict_detector',
                 name=f'{ns}_conflict_detector', output='screen',
                 parameters=[{'robot_id': ns, 'conflict_radius': 0.8,
                              'temporal_window': 3.0, 'check_rate': 2.0,
                              'use_sim_time': True}]),
            Node(package='amr_coordination', executable='path_sharer',
                 name=f'{ns}_path_sharer', output='screen',
                 parameters=[{'robot_id': ns, 'peer_ids': peer_ids, 'use_sim_time': True}]),
            Node(package='amr_coordination', executable='obstacle_relay',
                 name=f'{ns}_obstacle_relay', output='screen',
                 parameters=[{'robot_id': ns, 'use_sim_time': True}]),
            Node(package='amr_coordination', executable='goal_sequencer',
                 name=f'{ns}_goal_sequencer', output='screen',
                 parameters=[{'robot_id': ns, 'mode': 'coordinated',
                              'goals_inline': str(robot['goals']), 'use_sim_time': True}]),
        ])

    coordination = TimerAction(period=25.0, actions=coordination_nodes)

    return LaunchDescription([
        declare_headless,
        sim_world,
        *nav_robots,
        coordination,
    ])

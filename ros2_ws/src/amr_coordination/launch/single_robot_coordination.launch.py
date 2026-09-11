"""Launch coordination nodes for a single robot (useful for multi-laptop P2P deployment).

Usage:
  ros2 launch amr_coordination single_robot_coordination.launch.py robot_id:=robot1 priority:=1
  ros2 launch amr_coordination single_robot_coordination.launch.py robot_id:=robot2 priority:=2
  ros2 launch amr_coordination single_robot_coordination.launch.py robot_id:=robot3 priority:=3
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg = get_package_share_directory('amr_coordination')
    waypoints_file = os.path.join(pkg, 'config', 'waypoints.yaml')
    chokepoint_file = os.path.join(pkg, 'config', 'chokepoint.yaml')

    robot_id = LaunchConfiguration('robot_id')
    priority = LaunchConfiguration('priority')
    mode = LaunchConfiguration('mode')
    use_sim_time = LaunchConfiguration('use_sim_time')

    declare_robot_id = DeclareLaunchArgument(
        'robot_id',
        default_value='robot1',
        description='Robot namespace / ID (e.g. robot1, robot2, robot3)',
    )
    declare_priority = DeclareLaunchArgument(
        'priority',
        default_value='1',
        description='Arbitration priority rank (1 = highest)',
    )
    declare_mode = DeclareLaunchArgument(
        'mode',
        default_value='coordinated',
        description='Goal sequencer mode: coordinated | baseline | dispatcher',
    )
    declare_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation clock',
    )

    peer_ids = ['robot1', 'robot2', 'robot3']

    return LaunchDescription([
        declare_robot_id,
        declare_priority,
        declare_mode,
        declare_sim_time,

        # 1. Path Sharer (broadcasts local Nav2 plan over /shared_plans)
        Node(
            package='amr_coordination',
            executable='path_sharer',
            name='path_sharer',
            namespace=robot_id,
            output='screen',
            parameters=[{
                'robot_id': robot_id,
                'peer_ids': peer_ids,
                'use_sim_time': use_sim_time,
            }],
        ),

        # 2. Conflict Detector (spatio-temporal conflict detection & yielding)
        Node(
            package='amr_coordination',
            executable='conflict_detector',
            name='conflict_detector',
            namespace=robot_id,
            output='screen',
            parameters=[{
                'robot_id': robot_id,
                'conflict_radius': 0.8,
                'temporal_window': 3.0,
                'check_rate': 2.0,
                'use_sim_time': use_sim_time,
            }],
        ),

        # 3. Choke Negotiator (mutual exclusion token protocol)
        Node(
            package='amr_coordination',
            executable='choke_negotiator',
            name='choke_negotiator',
            namespace=robot_id,
            output='screen',
            parameters=[{
                'robot_id': robot_id,
                'priority': priority,
                'chokepoint_file': chokepoint_file,
                'heartbeat_interval': 0.5,
                'grant_timeout_base': 5.0,
                'use_sim_time': use_sim_time,
            }],
        ),

        # 4. Obstacle Relay (cooperative perception & virtual scan injection)
        Node(
            package='amr_coordination',
            executable='obstacle_relay',
            name='obstacle_relay',
            namespace=robot_id,
            output='screen',
            parameters=[{
                'robot_id': robot_id,
                'use_sim_time': use_sim_time,
            }],
        ),

        # 5. Goal Sequencer (dispatches waypoint sequences)
        Node(
            package='amr_coordination',
            executable='goal_sequencer',
            name='goal_sequencer',
            namespace=robot_id,
            output='screen',
            parameters=[{
                'robot_id': robot_id,
                'mode': mode,
                'waypoints_file': waypoints_file,
                'use_sim_time': use_sim_time,
            }],
        ),
    ])

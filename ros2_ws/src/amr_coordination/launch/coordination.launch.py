"""Launch all coordination nodes for 3 robots.

Accepts a 'mode' argument:
  coordinated  (default) — each robot auto-sequences its own waypoints
  baseline               — staggered sequential, no coordination
  dispatcher             — robots wait for goal_dispatcher click-to-goal assignments
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

    mode = LaunchConfiguration('mode')
    declare_mode = DeclareLaunchArgument(
        'mode',
        default_value='coordinated',
        description='Goal mode: coordinated | baseline | dispatcher',
    )

    robots = [
        {'name': 'robot1', 'priority': 1},
        {'name': 'robot2', 'priority': 2},
        {'name': 'robot3', 'priority': 3},
    ]
    peer_ids = [r['name'] for r in robots]

    ld = LaunchDescription([declare_mode])

    for robot in robots:
        ns = robot['name']
        pri = robot['priority']

        # Path Sharer
        ld.add_action(Node(
            package='amr_coordination',
            executable='path_sharer',
            name=f'{ns}_path_sharer',
            output='screen',
            parameters=[{
                'robot_id': ns,
                'peer_ids': peer_ids,
                'use_sim_time': True,
            }],
        ))

        # Conflict Detector
        ld.add_action(Node(
            package='amr_coordination',
            executable='conflict_detector',
            name=f'{ns}_conflict_detector',
            output='screen',
            parameters=[{
                'robot_id': ns,
                'conflict_radius': 0.8,
                'temporal_window': 3.0,
                'check_rate': 2.0,
                'use_sim_time': True,
            }],
        ))

        # Choke Negotiator — publishes /<ns>/choke_reason for "why waiting" annotation
        ld.add_action(Node(
            package='amr_coordination',
            executable='choke_negotiator',
            name=f'{ns}_choke_negotiator',
            output='screen',
            parameters=[{
                'robot_id': ns,
                'priority': pri,
                'chokepoint_file': chokepoint_file,
                'heartbeat_interval': 0.5,
                'grant_timeout_base': 5.0,
                'use_sim_time': True,
            }],
        ))

        # Obstacle Relay — uses ground_truth_pose from Gazebo
        ld.add_action(Node(
            package='amr_coordination',
            executable='obstacle_relay',
            name=f'{ns}_obstacle_relay',
            output='screen',
            parameters=[{
                'robot_id': ns,
                'use_sim_time': True,
            }],
        ))

        # Goal Sequencer — mode controls behavior (coordinated / baseline / dispatcher)
        ld.add_action(Node(
            package='amr_coordination',
            executable='goal_sequencer',
            name=f'{ns}_goal_sequencer',
            output='screen',
            parameters=[{
                'robot_id': ns,
                'mode': mode,
                'waypoints_file': waypoints_file,
                'use_sim_time': True,
            }],
        ))

    # Metrics Logger (one instance)
    ld.add_action(Node(
        package='amr_coordination',
        executable='metrics_logger',
        name='metrics_logger',
        output='screen',
        parameters=[{
            'output_dir': os.path.join(
                os.path.expanduser('~'), 'Desktop', 'SIH', 'ros2_ws', 'results'
            ),
            'expected_robots': 3,
            'use_sim_time': True,
        }],
    ))

    # Goal Dispatcher (one global instance — no per-robot namespace)
    # Subscribes to /clicked_point from RViz, assigns NavigateToPose to nearest idle robot
    ld.add_action(Node(
        package='amr_coordination',
        executable='goal_dispatcher',
        name='goal_dispatcher',
        output='screen',
        parameters=[{
            'robot_ids': ['robot1', 'robot2', 'robot3'],
            'use_sim_time': True,
        }],
    ))

    return ld

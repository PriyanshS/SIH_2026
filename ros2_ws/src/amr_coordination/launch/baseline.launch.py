"""Launch baseline mode — sequential stop-and-wait without coordination."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    pkg = get_package_share_directory('amr_coordination')
    waypoints_file = os.path.join(pkg, 'config', 'waypoints.yaml')

    robots = [
        {'name': 'robot1', 'priority': 1},
        {'name': 'robot2', 'priority': 2},
        {'name': 'robot3', 'priority': 3},
    ]

    ld = LaunchDescription()

    for robot in robots:
        ns = robot['name']

        # Goal Sequencer ONLY — baseline mode (no coordination nodes)
        ld.add_action(Node(
            package='amr_coordination',
            executable='goal_sequencer',
            name=f'{ns}_goal_sequencer',
            output='screen',
            parameters=[{
                'robot_id': ns,
                'mode': 'baseline',
                'waypoints_file': waypoints_file,
                'use_sim_time': True,
            }],
        ))

    # Locate results directory dynamically relative to workspace
    results_dir = os.path.abspath(
        os.path.join(pkg, '..', '..', '..', '..', 'results')
    )
    if not os.path.exists(results_dir):
        os.makedirs(results_dir, exist_ok=True)

    # Metrics Logger
    ld.add_action(Node(
        package='amr_coordination',
        executable='metrics_logger',
        name='metrics_logger',
        output='screen',
        parameters=[{
            'output_dir': results_dir,
            'expected_robots': 3,
            'use_sim_time': True,
        }],
    ))

    return ld

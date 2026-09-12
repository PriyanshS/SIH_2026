"""Scenario T4: Robot goes silent mid-task.

Launches the full coordinated demo, then automatically terminates robot3's
coordination nodes after 30 seconds. Verifies that robot1 and robot2:
  - Detect robot3's stale heartbeat (>3s timeout in choke_negotiator)
  - Clear the chokepoint block if robot3 was holding it
  - Continue their tasks unaffected — decentralized operation proven live

This is the single most convincing proof of decentralization for a panel.

Expected behavior:
  1. All three robots start navigating (0–30 s)
  2. kill_robot3.sh fires at 30 s — robot3 processes terminate
  3. robot1/robot2 print "Peer robot3 heartbeat stale" within 3 s
  4. robot1 and robot2 continue to their goals normally
  5. If robot3 had the chokepoint: the other robots get it within 5 s

Monitor the liveliness detection:
  ros2 topic echo /choke_negotiation | grep -i stale

Run with:
  ros2 launch amr_bringup scenarios/robot_goes_silent.launch.py

Kill robot3 manually (alternative to the auto-kill timer):
  bash src/amr_coordination/scripts/kill_robot3.sh
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
    pkg_amr_coordination = get_package_share_directory('amr_coordination')

    headless = LaunchConfiguration('headless')
    declare_headless = DeclareLaunchArgument('headless', default_value='false')

    # Full coordinated demo
    full_demo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_amr_bringup, 'launch', 'full_demo.launch.py')
        ),
        launch_arguments={'headless': headless, 'mode': 'coordinated'}.items(),
    )

    # Auto-kill robot3's coordination nodes after 75 s (45 s startup + 30 s running)
    # This uses the shell script that sends SIGTERM to all robot3 node processes
    ws_root = os.path.abspath(os.path.join(pkg_amr_coordination, '..', '..', '..', '..'))
    kill_script = os.path.join(
        ws_root, 'src', 'amr_coordination', 'scripts', 'kill_robot3.sh'
    )

    kill_robot3 = TimerAction(
        period=75.0,
        actions=[
            ExecuteProcess(
                cmd=['bash', kill_script],
                output='screen',
            )
        ],
    )

    return LaunchDescription([
        declare_headless,
        full_demo,
        kill_robot3,
    ])

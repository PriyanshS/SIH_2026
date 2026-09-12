"""RViz-only launch — opens RViz2 with the multi-robot config.

This launch file opens ONLY RViz2 for 3D visualization and point-dispatch.
It does NOT start Gazebo. Run sim_world.launch.py separately (or via the
launcher) to have a live simulation to visualize.

Usage:
  ros2 launch amr_bringup rviz_demo.launch.py
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    pkg_amr_gazebo = get_package_share_directory('amr_gazebo')

    rviz_config = os.path.join(pkg_amr_gazebo, 'rviz', 'multi_robot.rviz')

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': True}],
        output='screen',
    )

    return LaunchDescription([rviz_node])

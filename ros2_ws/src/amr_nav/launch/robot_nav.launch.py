"""Launch Nav2 stack for a single robot using ground-truth localization.

Localization & Mapping:
  - Map is provided by nav2_map_server loading warehouse_map.yaml.
  - Robot ground-truth pose is provided by Gazebo's PosePublisher plugin on /<ns>/ground_truth_pose.
  - TF chain: map → <ns>/odom (static transform at spawn) → <ns>/base_link (Gazebo diff-drive odom).
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    GroupAction,
)
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node, PushRosNamespace
from launch_ros.descriptions import ParameterFile
from nav2_common.launch import ReplaceString, RewrittenYaml


def generate_launch_description():
    pkg_amr_nav = get_package_share_directory('amr_nav')

    namespace = LaunchConfiguration('namespace')
    params_file = LaunchConfiguration('params_file')
    map_file = LaunchConfiguration('map')
    use_sim_time = LaunchConfiguration('use_sim_time')
    autostart = LaunchConfiguration('autostart')

    declare_ns = DeclareLaunchArgument('namespace', default_value='robot1')
    declare_params = DeclareLaunchArgument(
        'params_file',
        default_value=os.path.join(pkg_amr_nav, 'config', 'nav2_params.yaml'),
    )
    declare_map = DeclareLaunchArgument(
        'map',
        default_value=os.path.join(pkg_amr_nav, 'maps', 'warehouse_map.yaml'),
        description='Full path to map file to load',
    )
    declare_sim_time = DeclareLaunchArgument('use_sim_time', default_value='true')
    declare_autostart = DeclareLaunchArgument('autostart', default_value='true')

    remappings = [('tf', '/tf'), ('tf_static', '/tf_static')]

    # Substitute <robot_namespace> in nav2_params.yaml with actual namespace
    params_file_replaced = ReplaceString(
        source_file=params_file,
        replacements={'<robot_namespace>': namespace},
    )

    configured_params = ParameterFile(
        RewrittenYaml(
            source_file=params_file_replaced,
            root_key=namespace,
            param_rewrites={
                'autostart': autostart,
                'use_sim_time': use_sim_time,
                'yaml_filename': map_file,
            },
            convert_types=True,
        ),
        allow_substs=True,
    )

    # ── Nav2 nodes with map_server (ground-truth map + TF) ───────────────────
    nav2_nodes = GroupAction(
        actions=[
            PushRosNamespace(namespace),

            Node(
                package='nav2_map_server',
                executable='map_server',
                name='map_server',
                output='screen',
                parameters=[configured_params, {'yaml_filename': map_file}],
                remappings=remappings,
            ),
            Node(
                package='nav2_controller',
                executable='controller_server',
                name='controller_server',
                output='screen',
                parameters=[configured_params],
                remappings=remappings + [('cmd_vel', 'cmd_vel')],
            ),
            Node(
                package='nav2_planner',
                executable='planner_server',
                name='planner_server',
                output='screen',
                parameters=[configured_params],
                remappings=remappings,
            ),
            Node(
                package='nav2_behaviors',
                executable='behavior_server',
                name='behavior_server',
                output='screen',
                parameters=[configured_params],
                remappings=remappings + [('cmd_vel', 'cmd_vel')],
            ),
            Node(
                package='nav2_bt_navigator',
                executable='bt_navigator',
                name='bt_navigator',
                output='screen',
                parameters=[configured_params],
                remappings=remappings,
            ),
            Node(
                package='nav2_lifecycle_manager',
                executable='lifecycle_manager',
                name='lifecycle_manager',
                output='screen',
                parameters=[configured_params],
            ),
        ]
    )

    return LaunchDescription([
        declare_ns,
        declare_params,
        declare_map,
        declare_sim_time,
        declare_autostart,
        nav2_nodes,
    ])

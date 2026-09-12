"""Launch Gazebo Harmonic warehouse world with 3 AMR robots and ROS-GZ bridges."""

import os
import tempfile

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    ExecuteProcess,
    IncludeLaunchDescription,
    TimerAction,
)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_amr_gazebo = get_package_share_directory('amr_gazebo')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    world_file = os.path.join(pkg_amr_gazebo, 'worlds', 'warehouse.sdf')
    model_file = os.path.join(pkg_amr_gazebo, 'models', 'amr_robot', 'model.sdf')

    # Robot configurations: name, x, y, yaw, color (r,g,b)
    # Spawned in the lower green staging zones of the 60×40m warehouse
    robots = [
        {'name': 'robot1', 'x': '10.0', 'y': '2.0', 'yaw': '0.0',
         'color': ('0.8', '0.2', '0.2')},   # red   — staging zone 1
        {'name': 'robot2', 'x': '30.0', 'y': '2.0', 'yaw': '0.0',
         'color': ('0.2', '0.8', '0.2')},   # green — staging zone 2
        {'name': 'robot3', 'x': '50.0', 'y': '2.0', 'yaw': '0.0',
         'color': ('0.2', '0.2', '0.8')},   # blue  — staging zone 3
    ]

    from launch.substitutions import PythonExpression

    headless = LaunchConfiguration('headless')
    declare_headless = DeclareLaunchArgument(
        'headless', default_value='false',
        description='Run Gazebo in server-only headless mode'
    )

    use_ground_truth_tf = LaunchConfiguration('use_ground_truth_tf')
    declare_use_ground_truth = DeclareLaunchArgument(
        'use_ground_truth_tf', default_value='true',
        description='Publish static map->odom TF for ground-truth localization'
    )

    gz_args = PythonExpression([
        "'-s -r ' + '", world_file, "' if '", headless, "' == 'true' else '-r ' + '", world_file, "'"
    ])

    # --- Launch Gazebo Harmonic ---
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={
            'gz_args': gz_args,
            'on_exit_shutdown': 'true',
        }.items(),
    )

    # --- Clock bridge (one for the whole sim) ---
    clock_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='clock_bridge',
        arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'],
        output='screen',
    )

    ld = LaunchDescription()
    ld.add_action(declare_headless)
    ld.add_action(declare_use_ground_truth)
    ld.add_action(gz_sim)
    ld.add_action(clock_bridge)

    for i, robot in enumerate(robots):
        ns = robot['name']

        # Read template SDF, substitute namespace and color
        with open(model_file, 'r') as f:
            sdf_content = f.read()

        sdf_content = sdf_content.replace('__NS__', ns)
        # Substitute color for the base link visual
        sdf_content = sdf_content.replace(
            '<ambient>0.2 0.2 0.8 1</ambient>\n          <diffuse>0.2 0.2 0.8 1</diffuse>',
            f'<ambient>{robot["color"][0]} {robot["color"][1]} {robot["color"][2]} 1</ambient>\n'
            f'          <diffuse>{robot["color"][0]} {robot["color"][1]} {robot["color"][2]} 1</diffuse>',
            1  # only replace first occurrence (base link)
        )

        # Write to temp file
        tmp_sdf = os.path.join(tempfile.gettempdir(), f'{ns}_robot.sdf')
        with open(tmp_sdf, 'w') as f:
            f.write(sdf_content)

        # Spawn robot in Gazebo
        spawn = ExecuteProcess(
            cmd=[
                'gz', 'service',
                '-s', '/world/warehouse/create',
                '--reqtype', 'gz.msgs.EntityFactory',
                '--reptype', 'gz.msgs.Boolean',
                '--timeout', '10000',
                '--req',
                f'sdf_filename: "{tmp_sdf}", name: "{ns}", '
                f'pose: {{position: {{x: {robot["x"]}, y: {robot["y"]}, z: 0.08}}, '
                f'orientation: {{x: 0, y: 0, z: 0, w: 1}}}}'
            ],
            output='screen',
        )

        # ROS-GZ bridge for this robot's topics
        bridge = Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name=f'{ns}_bridge',
            arguments=[
                # cmd_vel: ROS → GZ
                f'/{ns}/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
                # odom: GZ → ROS
                f'/{ns}/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
                # scan: GZ → ROS
                f'/{ns}/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
                # imu: GZ → ROS
                f'/{ns}/imu@sensor_msgs/msg/Imu[gz.msgs.IMU',
                # TF: GZ → ROS
                f'/{ns}/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
            ],
            remappings=[
                (f'/{ns}/tf', '/tf'),
            ],
            output='screen',
            parameters=[{'use_sim_time': True}],
        )

        # Ground-truth pose from Gazebo model pose
        # We use gz-ros bridge for the pose topic published by PosePublisher plugin
        # The PosePublisher publishes on /model/{ns}/pose
        pose_bridge = Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name=f'{ns}_pose_bridge',
            arguments=[
                f'/model/{ns}/pose@geometry_msgs/msg/PoseStamped[gz.msgs.Pose',
            ],
            remappings=[
                (f'/model/{ns}/pose', f'/{ns}/ground_truth_pose'),
            ],
            output='screen',
            parameters=[{'use_sim_time': True}],
        )

        # Static TF: map → <ns>/odom (spawn position — ground truth localization)
        static_tf = Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name=f'{ns}_map_to_odom',
            arguments=[
                '--x', str(robot['x']), '--y', str(robot['y']), '--z', '0',
                '--roll', '0', '--pitch', '0', '--yaw', str(robot.get('yaw', '0.0')),
                '--frame-id', 'map',
                '--child-frame-id', f'{ns}/odom',
            ],
            parameters=[{'use_sim_time': True}],
            condition=IfCondition(use_ground_truth_tf),
        )

        # Static TF: <ns>/base_link → <ns>/lidar_link
        static_tf_lidar = Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name=f'{ns}_base_to_lidar',
            arguments=[
                '--x', '0', '--y', '0', '--z', '0.1',
                '--roll', '0', '--pitch', '0', '--yaw', '0',
                '--frame-id', f'{ns}/base_link',
                '--child-frame-id', f'{ns}/lidar_link',
            ],
            parameters=[{'use_sim_time': True}],
        )

        # Static TF: <ns>/base_link → <ns>/imu_link
        static_tf_imu = Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name=f'{ns}_base_to_imu',
            arguments=[
                '--x', '0', '--y', '0', '--z', '0.05',
                '--roll', '0', '--pitch', '0', '--yaw', '0',
                '--frame-id', f'{ns}/base_link',
                '--child-frame-id', f'{ns}/imu_link',
            ],
            parameters=[{'use_sim_time': True}],
        )

        # Delay spawns slightly so Gazebo entity factory service and GUI renderer are fully ready
        delay = 6.0 + float(i) * 2.0
        ld.add_action(TimerAction(period=delay, actions=[spawn]))
        ld.add_action(TimerAction(period=delay + 1.0, actions=[bridge]))
        ld.add_action(TimerAction(period=delay + 1.0, actions=[pose_bridge]))
        ld.add_action(static_tf)
        ld.add_action(static_tf_lidar)
        ld.add_action(static_tf_imu)

    return ld

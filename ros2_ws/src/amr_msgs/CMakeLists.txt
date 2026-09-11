cmake_minimum_required(VERSION 3.8)
project(amr_msgs)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(builtin_interfaces REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(std_msgs REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/RobotPlan.msg"
  "msg/DetectedObstacle.msg"
  "msg/ChokeRequest.msg"
  "msg/RobotStatus.msg"
  DEPENDENCIES builtin_interfaces geometry_msgs nav_msgs std_msgs
)

ament_package()

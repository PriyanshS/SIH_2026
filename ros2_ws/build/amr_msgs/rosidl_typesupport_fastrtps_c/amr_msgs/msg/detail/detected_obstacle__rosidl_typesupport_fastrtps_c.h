// generated from rosidl_typesupport_fastrtps_c/resource/idl__rosidl_typesupport_fastrtps_c.h.em
// with input from amr_msgs:msg/DetectedObstacle.idl
// generated code does not contain a copyright notice
#ifndef AMR_MSGS__MSG__DETAIL__DETECTED_OBSTACLE__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
#define AMR_MSGS__MSG__DETAIL__DETECTED_OBSTACLE__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_


#include <stddef.h>
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "amr_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "amr_msgs/msg/detail/detected_obstacle__struct.h"
#include "fastcdr/Cdr.h"

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_amr_msgs
bool cdr_serialize_amr_msgs__msg__DetectedObstacle(
  const amr_msgs__msg__DetectedObstacle * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_amr_msgs
bool cdr_deserialize_amr_msgs__msg__DetectedObstacle(
  eprosima::fastcdr::Cdr &,
  amr_msgs__msg__DetectedObstacle * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_amr_msgs
size_t get_serialized_size_amr_msgs__msg__DetectedObstacle(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_amr_msgs
size_t max_serialized_size_amr_msgs__msg__DetectedObstacle(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_amr_msgs
bool cdr_serialize_key_amr_msgs__msg__DetectedObstacle(
  const amr_msgs__msg__DetectedObstacle * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_amr_msgs
size_t get_serialized_size_key_amr_msgs__msg__DetectedObstacle(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_amr_msgs
size_t max_serialized_size_key_amr_msgs__msg__DetectedObstacle(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_amr_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, amr_msgs, msg, DetectedObstacle)();

#ifdef __cplusplus
}
#endif

#endif  // AMR_MSGS__MSG__DETAIL__DETECTED_OBSTACLE__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_

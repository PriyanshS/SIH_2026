// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from amr_msgs:msg/RobotStatus.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "amr_msgs/msg/robot_status.h"


#ifndef AMR_MSGS__MSG__DETAIL__ROBOT_STATUS__STRUCT_H_
#define AMR_MSGS__MSG__DETAIL__ROBOT_STATUS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

/// Constant 'IDLE'.
/**
  * status constants
 */
enum
{
  amr_msgs__msg__RobotStatus__IDLE = 0
};

/// Constant 'BUSY'.
enum
{
  amr_msgs__msg__RobotStatus__BUSY = 1
};

// Include directives for member types
// Member 'robot_id'
#include "rosidl_runtime_c/string.h"
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in msg/RobotStatus in the package amr_msgs.
/**
  * Per-robot idle/busy state published for the goal dispatcher
 */
typedef struct amr_msgs__msg__RobotStatus
{
  rosidl_runtime_c__String robot_id;
  uint8_t status;
  double pose_x;
  double pose_y;
  builtin_interfaces__msg__Time stamp;
} amr_msgs__msg__RobotStatus;

// Struct for a sequence of amr_msgs__msg__RobotStatus.
typedef struct amr_msgs__msg__RobotStatus__Sequence
{
  amr_msgs__msg__RobotStatus * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} amr_msgs__msg__RobotStatus__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AMR_MSGS__MSG__DETAIL__ROBOT_STATUS__STRUCT_H_

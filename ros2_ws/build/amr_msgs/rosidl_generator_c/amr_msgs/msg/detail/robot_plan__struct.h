// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from amr_msgs:msg/RobotPlan.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "amr_msgs/msg/robot_plan.h"


#ifndef AMR_MSGS__MSG__DETAIL__ROBOT_PLAN__STRUCT_H_
#define AMR_MSGS__MSG__DETAIL__ROBOT_PLAN__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'robot_id'
#include "rosidl_runtime_c/string.h"
// Member 'path'
#include "nav_msgs/msg/detail/path__struct.h"
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in msg/RobotPlan in the package amr_msgs.
/**
  * Robot's shared navigation plan
 */
typedef struct amr_msgs__msg__RobotPlan
{
  rosidl_runtime_c__String robot_id;
  uint32_t plan_seq;
  nav_msgs__msg__Path path;
  double estimated_velocity;
  builtin_interfaces__msg__Time stamp;
} amr_msgs__msg__RobotPlan;

// Struct for a sequence of amr_msgs__msg__RobotPlan.
typedef struct amr_msgs__msg__RobotPlan__Sequence
{
  amr_msgs__msg__RobotPlan * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} amr_msgs__msg__RobotPlan__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AMR_MSGS__MSG__DETAIL__ROBOT_PLAN__STRUCT_H_

// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from amr_msgs:msg/DetectedObstacle.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "amr_msgs/msg/detected_obstacle.h"


#ifndef AMR_MSGS__MSG__DETAIL__DETECTED_OBSTACLE__STRUCT_H_
#define AMR_MSGS__MSG__DETAIL__DETECTED_OBSTACLE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'reporter_id'
#include "rosidl_runtime_c/string.h"
// Member 'position'
#include "geometry_msgs/msg/detail/point__struct.h"
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in msg/DetectedObstacle in the package amr_msgs.
/**
  * Dynamic obstacle detected by a robot and relayed to peers
 */
typedef struct amr_msgs__msg__DetectedObstacle
{
  rosidl_runtime_c__String reporter_id;
  geometry_msgs__msg__Point position;
  double radius;
  builtin_interfaces__msg__Time stamp;
  double ttl;
} amr_msgs__msg__DetectedObstacle;

// Struct for a sequence of amr_msgs__msg__DetectedObstacle.
typedef struct amr_msgs__msg__DetectedObstacle__Sequence
{
  amr_msgs__msg__DetectedObstacle * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} amr_msgs__msg__DetectedObstacle__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AMR_MSGS__MSG__DETAIL__DETECTED_OBSTACLE__STRUCT_H_

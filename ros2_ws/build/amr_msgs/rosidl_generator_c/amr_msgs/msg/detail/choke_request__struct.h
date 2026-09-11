// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from amr_msgs:msg/ChokeRequest.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "amr_msgs/msg/choke_request.h"


#ifndef AMR_MSGS__MSG__DETAIL__CHOKE_REQUEST__STRUCT_H_
#define AMR_MSGS__MSG__DETAIL__CHOKE_REQUEST__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

/// Constant 'REQUEST'.
/**
  * msg_type constants
 */
enum
{
  amr_msgs__msg__ChokeRequest__REQUEST = 0
};

/// Constant 'GRANT'.
enum
{
  amr_msgs__msg__ChokeRequest__GRANT = 1
};

/// Constant 'RELEASE'.
enum
{
  amr_msgs__msg__ChokeRequest__RELEASE = 2
};

/// Constant 'HEARTBEAT'.
enum
{
  amr_msgs__msg__ChokeRequest__HEARTBEAT = 3
};

// Include directives for member types
// Member 'robot_id'
// Member 'reason'
#include "rosidl_runtime_c/string.h"
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in msg/ChokeRequest in the package amr_msgs.
/**
  * Chokepoint negotiation protocol message
 */
typedef struct amr_msgs__msg__ChokeRequest
{
  rosidl_runtime_c__String robot_id;
  uint8_t msg_type;
  uint32_t priority;
  double distance_to_choke;
  /// human-readable yield reason e.g. "yielding to robot2, lower priority"
  rosidl_runtime_c__String reason;
  builtin_interfaces__msg__Time stamp;
} amr_msgs__msg__ChokeRequest;

// Struct for a sequence of amr_msgs__msg__ChokeRequest.
typedef struct amr_msgs__msg__ChokeRequest__Sequence
{
  amr_msgs__msg__ChokeRequest * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} amr_msgs__msg__ChokeRequest__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AMR_MSGS__MSG__DETAIL__CHOKE_REQUEST__STRUCT_H_

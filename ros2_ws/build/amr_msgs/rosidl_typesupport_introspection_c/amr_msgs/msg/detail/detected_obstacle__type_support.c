// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from amr_msgs:msg/DetectedObstacle.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "amr_msgs/msg/detail/detected_obstacle__rosidl_typesupport_introspection_c.h"
#include "amr_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "amr_msgs/msg/detail/detected_obstacle__functions.h"
#include "amr_msgs/msg/detail/detected_obstacle__struct.h"


// Include directives for member types
// Member `reporter_id`
#include "rosidl_runtime_c/string_functions.h"
// Member `position`
#include "geometry_msgs/msg/point.h"
// Member `position`
#include "geometry_msgs/msg/detail/point__rosidl_typesupport_introspection_c.h"
// Member `stamp`
#include "builtin_interfaces/msg/time.h"
// Member `stamp`
#include "builtin_interfaces/msg/detail/time__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void amr_msgs__msg__DetectedObstacle__rosidl_typesupport_introspection_c__DetectedObstacle_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  amr_msgs__msg__DetectedObstacle__init(message_memory);
}

void amr_msgs__msg__DetectedObstacle__rosidl_typesupport_introspection_c__DetectedObstacle_fini_function(void * message_memory)
{
  amr_msgs__msg__DetectedObstacle__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember amr_msgs__msg__DetectedObstacle__rosidl_typesupport_introspection_c__DetectedObstacle_message_member_array[5] = {
  {
    "reporter_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(amr_msgs__msg__DetectedObstacle, reporter_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "position",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(amr_msgs__msg__DetectedObstacle, position),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "radius",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(amr_msgs__msg__DetectedObstacle, radius),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "stamp",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(amr_msgs__msg__DetectedObstacle, stamp),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "ttl",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(amr_msgs__msg__DetectedObstacle, ttl),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers amr_msgs__msg__DetectedObstacle__rosidl_typesupport_introspection_c__DetectedObstacle_message_members = {
  "amr_msgs__msg",  // message namespace
  "DetectedObstacle",  // message name
  5,  // number of fields
  sizeof(amr_msgs__msg__DetectedObstacle),
  false,  // has_any_key_member_
  amr_msgs__msg__DetectedObstacle__rosidl_typesupport_introspection_c__DetectedObstacle_message_member_array,  // message members
  amr_msgs__msg__DetectedObstacle__rosidl_typesupport_introspection_c__DetectedObstacle_init_function,  // function to initialize message memory (memory has to be allocated)
  amr_msgs__msg__DetectedObstacle__rosidl_typesupport_introspection_c__DetectedObstacle_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t amr_msgs__msg__DetectedObstacle__rosidl_typesupport_introspection_c__DetectedObstacle_message_type_support_handle = {
  0,
  &amr_msgs__msg__DetectedObstacle__rosidl_typesupport_introspection_c__DetectedObstacle_message_members,
  get_message_typesupport_handle_function,
  &amr_msgs__msg__DetectedObstacle__get_type_hash,
  &amr_msgs__msg__DetectedObstacle__get_type_description,
  &amr_msgs__msg__DetectedObstacle__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_amr_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, amr_msgs, msg, DetectedObstacle)() {
  amr_msgs__msg__DetectedObstacle__rosidl_typesupport_introspection_c__DetectedObstacle_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Point)();
  amr_msgs__msg__DetectedObstacle__rosidl_typesupport_introspection_c__DetectedObstacle_message_member_array[3].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, builtin_interfaces, msg, Time)();
  if (!amr_msgs__msg__DetectedObstacle__rosidl_typesupport_introspection_c__DetectedObstacle_message_type_support_handle.typesupport_identifier) {
    amr_msgs__msg__DetectedObstacle__rosidl_typesupport_introspection_c__DetectedObstacle_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &amr_msgs__msg__DetectedObstacle__rosidl_typesupport_introspection_c__DetectedObstacle_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

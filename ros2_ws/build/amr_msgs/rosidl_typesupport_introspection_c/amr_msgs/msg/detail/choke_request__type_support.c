// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from amr_msgs:msg/ChokeRequest.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "amr_msgs/msg/detail/choke_request__rosidl_typesupport_introspection_c.h"
#include "amr_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "amr_msgs/msg/detail/choke_request__functions.h"
#include "amr_msgs/msg/detail/choke_request__struct.h"


// Include directives for member types
// Member `robot_id`
// Member `reason`
#include "rosidl_runtime_c/string_functions.h"
// Member `stamp`
#include "builtin_interfaces/msg/time.h"
// Member `stamp`
#include "builtin_interfaces/msg/detail/time__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void amr_msgs__msg__ChokeRequest__rosidl_typesupport_introspection_c__ChokeRequest_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  amr_msgs__msg__ChokeRequest__init(message_memory);
}

void amr_msgs__msg__ChokeRequest__rosidl_typesupport_introspection_c__ChokeRequest_fini_function(void * message_memory)
{
  amr_msgs__msg__ChokeRequest__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember amr_msgs__msg__ChokeRequest__rosidl_typesupport_introspection_c__ChokeRequest_message_member_array[6] = {
  {
    "robot_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(amr_msgs__msg__ChokeRequest, robot_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "msg_type",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(amr_msgs__msg__ChokeRequest, msg_type),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "priority",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(amr_msgs__msg__ChokeRequest, priority),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "distance_to_choke",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(amr_msgs__msg__ChokeRequest, distance_to_choke),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "reason",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(amr_msgs__msg__ChokeRequest, reason),  // bytes offset in struct
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
    offsetof(amr_msgs__msg__ChokeRequest, stamp),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers amr_msgs__msg__ChokeRequest__rosidl_typesupport_introspection_c__ChokeRequest_message_members = {
  "amr_msgs__msg",  // message namespace
  "ChokeRequest",  // message name
  6,  // number of fields
  sizeof(amr_msgs__msg__ChokeRequest),
  false,  // has_any_key_member_
  amr_msgs__msg__ChokeRequest__rosidl_typesupport_introspection_c__ChokeRequest_message_member_array,  // message members
  amr_msgs__msg__ChokeRequest__rosidl_typesupport_introspection_c__ChokeRequest_init_function,  // function to initialize message memory (memory has to be allocated)
  amr_msgs__msg__ChokeRequest__rosidl_typesupport_introspection_c__ChokeRequest_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t amr_msgs__msg__ChokeRequest__rosidl_typesupport_introspection_c__ChokeRequest_message_type_support_handle = {
  0,
  &amr_msgs__msg__ChokeRequest__rosidl_typesupport_introspection_c__ChokeRequest_message_members,
  get_message_typesupport_handle_function,
  &amr_msgs__msg__ChokeRequest__get_type_hash,
  &amr_msgs__msg__ChokeRequest__get_type_description,
  &amr_msgs__msg__ChokeRequest__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_amr_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, amr_msgs, msg, ChokeRequest)() {
  amr_msgs__msg__ChokeRequest__rosidl_typesupport_introspection_c__ChokeRequest_message_member_array[5].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, builtin_interfaces, msg, Time)();
  if (!amr_msgs__msg__ChokeRequest__rosidl_typesupport_introspection_c__ChokeRequest_message_type_support_handle.typesupport_identifier) {
    amr_msgs__msg__ChokeRequest__rosidl_typesupport_introspection_c__ChokeRequest_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &amr_msgs__msg__ChokeRequest__rosidl_typesupport_introspection_c__ChokeRequest_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

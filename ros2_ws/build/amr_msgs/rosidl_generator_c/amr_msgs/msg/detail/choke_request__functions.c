// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from amr_msgs:msg/ChokeRequest.idl
// generated code does not contain a copyright notice
#include "amr_msgs/msg/detail/choke_request__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `robot_id`
// Member `reason`
#include "rosidl_runtime_c/string_functions.h"
// Member `stamp`
#include "builtin_interfaces/msg/detail/time__functions.h"

bool
amr_msgs__msg__ChokeRequest__init(amr_msgs__msg__ChokeRequest * msg)
{
  if (!msg) {
    return false;
  }
  // robot_id
  if (!rosidl_runtime_c__String__init(&msg->robot_id)) {
    amr_msgs__msg__ChokeRequest__fini(msg);
    return false;
  }
  // msg_type
  // priority
  // distance_to_choke
  // reason
  if (!rosidl_runtime_c__String__init(&msg->reason)) {
    amr_msgs__msg__ChokeRequest__fini(msg);
    return false;
  }
  // stamp
  if (!builtin_interfaces__msg__Time__init(&msg->stamp)) {
    amr_msgs__msg__ChokeRequest__fini(msg);
    return false;
  }
  return true;
}

void
amr_msgs__msg__ChokeRequest__fini(amr_msgs__msg__ChokeRequest * msg)
{
  if (!msg) {
    return;
  }
  // robot_id
  rosidl_runtime_c__String__fini(&msg->robot_id);
  // msg_type
  // priority
  // distance_to_choke
  // reason
  rosidl_runtime_c__String__fini(&msg->reason);
  // stamp
  builtin_interfaces__msg__Time__fini(&msg->stamp);
}

bool
amr_msgs__msg__ChokeRequest__are_equal(const amr_msgs__msg__ChokeRequest * lhs, const amr_msgs__msg__ChokeRequest * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // robot_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->robot_id), &(rhs->robot_id)))
  {
    return false;
  }
  // msg_type
  if (lhs->msg_type != rhs->msg_type) {
    return false;
  }
  // priority
  if (lhs->priority != rhs->priority) {
    return false;
  }
  // distance_to_choke
  if (lhs->distance_to_choke != rhs->distance_to_choke) {
    return false;
  }
  // reason
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->reason), &(rhs->reason)))
  {
    return false;
  }
  // stamp
  if (!builtin_interfaces__msg__Time__are_equal(
      &(lhs->stamp), &(rhs->stamp)))
  {
    return false;
  }
  return true;
}

bool
amr_msgs__msg__ChokeRequest__copy(
  const amr_msgs__msg__ChokeRequest * input,
  amr_msgs__msg__ChokeRequest * output)
{
  if (!input || !output) {
    return false;
  }
  // robot_id
  if (!rosidl_runtime_c__String__copy(
      &(input->robot_id), &(output->robot_id)))
  {
    return false;
  }
  // msg_type
  output->msg_type = input->msg_type;
  // priority
  output->priority = input->priority;
  // distance_to_choke
  output->distance_to_choke = input->distance_to_choke;
  // reason
  if (!rosidl_runtime_c__String__copy(
      &(input->reason), &(output->reason)))
  {
    return false;
  }
  // stamp
  if (!builtin_interfaces__msg__Time__copy(
      &(input->stamp), &(output->stamp)))
  {
    return false;
  }
  return true;
}

amr_msgs__msg__ChokeRequest *
amr_msgs__msg__ChokeRequest__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  amr_msgs__msg__ChokeRequest * msg = (amr_msgs__msg__ChokeRequest *)allocator.allocate(sizeof(amr_msgs__msg__ChokeRequest), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(amr_msgs__msg__ChokeRequest));
  bool success = amr_msgs__msg__ChokeRequest__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
amr_msgs__msg__ChokeRequest__destroy(amr_msgs__msg__ChokeRequest * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    amr_msgs__msg__ChokeRequest__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
amr_msgs__msg__ChokeRequest__Sequence__init(amr_msgs__msg__ChokeRequest__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  amr_msgs__msg__ChokeRequest * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(amr_msgs__msg__ChokeRequest)) {
      return false;
    }
    data = (amr_msgs__msg__ChokeRequest *)allocator.zero_allocate(size, sizeof(amr_msgs__msg__ChokeRequest), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = amr_msgs__msg__ChokeRequest__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        amr_msgs__msg__ChokeRequest__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
amr_msgs__msg__ChokeRequest__Sequence__fini(amr_msgs__msg__ChokeRequest__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      amr_msgs__msg__ChokeRequest__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

amr_msgs__msg__ChokeRequest__Sequence *
amr_msgs__msg__ChokeRequest__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  amr_msgs__msg__ChokeRequest__Sequence * array = (amr_msgs__msg__ChokeRequest__Sequence *)allocator.allocate(sizeof(amr_msgs__msg__ChokeRequest__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = amr_msgs__msg__ChokeRequest__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
amr_msgs__msg__ChokeRequest__Sequence__destroy(amr_msgs__msg__ChokeRequest__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    amr_msgs__msg__ChokeRequest__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
amr_msgs__msg__ChokeRequest__Sequence__are_equal(const amr_msgs__msg__ChokeRequest__Sequence * lhs, const amr_msgs__msg__ChokeRequest__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!amr_msgs__msg__ChokeRequest__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
amr_msgs__msg__ChokeRequest__Sequence__copy(
  const amr_msgs__msg__ChokeRequest__Sequence * input,
  amr_msgs__msg__ChokeRequest__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(amr_msgs__msg__ChokeRequest)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(amr_msgs__msg__ChokeRequest);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    amr_msgs__msg__ChokeRequest * data =
      (amr_msgs__msg__ChokeRequest *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!amr_msgs__msg__ChokeRequest__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          amr_msgs__msg__ChokeRequest__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!amr_msgs__msg__ChokeRequest__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

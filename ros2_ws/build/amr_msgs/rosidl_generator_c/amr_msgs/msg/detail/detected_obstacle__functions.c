// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from amr_msgs:msg/DetectedObstacle.idl
// generated code does not contain a copyright notice
#include "amr_msgs/msg/detail/detected_obstacle__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `reporter_id`
#include "rosidl_runtime_c/string_functions.h"
// Member `position`
#include "geometry_msgs/msg/detail/point__functions.h"
// Member `stamp`
#include "builtin_interfaces/msg/detail/time__functions.h"

bool
amr_msgs__msg__DetectedObstacle__init(amr_msgs__msg__DetectedObstacle * msg)
{
  if (!msg) {
    return false;
  }
  // reporter_id
  if (!rosidl_runtime_c__String__init(&msg->reporter_id)) {
    amr_msgs__msg__DetectedObstacle__fini(msg);
    return false;
  }
  // position
  if (!geometry_msgs__msg__Point__init(&msg->position)) {
    amr_msgs__msg__DetectedObstacle__fini(msg);
    return false;
  }
  // radius
  // stamp
  if (!builtin_interfaces__msg__Time__init(&msg->stamp)) {
    amr_msgs__msg__DetectedObstacle__fini(msg);
    return false;
  }
  // ttl
  return true;
}

void
amr_msgs__msg__DetectedObstacle__fini(amr_msgs__msg__DetectedObstacle * msg)
{
  if (!msg) {
    return;
  }
  // reporter_id
  rosidl_runtime_c__String__fini(&msg->reporter_id);
  // position
  geometry_msgs__msg__Point__fini(&msg->position);
  // radius
  // stamp
  builtin_interfaces__msg__Time__fini(&msg->stamp);
  // ttl
}

bool
amr_msgs__msg__DetectedObstacle__are_equal(const amr_msgs__msg__DetectedObstacle * lhs, const amr_msgs__msg__DetectedObstacle * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // reporter_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->reporter_id), &(rhs->reporter_id)))
  {
    return false;
  }
  // position
  if (!geometry_msgs__msg__Point__are_equal(
      &(lhs->position), &(rhs->position)))
  {
    return false;
  }
  // radius
  if (lhs->radius != rhs->radius) {
    return false;
  }
  // stamp
  if (!builtin_interfaces__msg__Time__are_equal(
      &(lhs->stamp), &(rhs->stamp)))
  {
    return false;
  }
  // ttl
  if (lhs->ttl != rhs->ttl) {
    return false;
  }
  return true;
}

bool
amr_msgs__msg__DetectedObstacle__copy(
  const amr_msgs__msg__DetectedObstacle * input,
  amr_msgs__msg__DetectedObstacle * output)
{
  if (!input || !output) {
    return false;
  }
  // reporter_id
  if (!rosidl_runtime_c__String__copy(
      &(input->reporter_id), &(output->reporter_id)))
  {
    return false;
  }
  // position
  if (!geometry_msgs__msg__Point__copy(
      &(input->position), &(output->position)))
  {
    return false;
  }
  // radius
  output->radius = input->radius;
  // stamp
  if (!builtin_interfaces__msg__Time__copy(
      &(input->stamp), &(output->stamp)))
  {
    return false;
  }
  // ttl
  output->ttl = input->ttl;
  return true;
}

amr_msgs__msg__DetectedObstacle *
amr_msgs__msg__DetectedObstacle__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  amr_msgs__msg__DetectedObstacle * msg = (amr_msgs__msg__DetectedObstacle *)allocator.allocate(sizeof(amr_msgs__msg__DetectedObstacle), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(amr_msgs__msg__DetectedObstacle));
  bool success = amr_msgs__msg__DetectedObstacle__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
amr_msgs__msg__DetectedObstacle__destroy(amr_msgs__msg__DetectedObstacle * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    amr_msgs__msg__DetectedObstacle__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
amr_msgs__msg__DetectedObstacle__Sequence__init(amr_msgs__msg__DetectedObstacle__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  amr_msgs__msg__DetectedObstacle * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(amr_msgs__msg__DetectedObstacle)) {
      return false;
    }
    data = (amr_msgs__msg__DetectedObstacle *)allocator.zero_allocate(size, sizeof(amr_msgs__msg__DetectedObstacle), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = amr_msgs__msg__DetectedObstacle__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        amr_msgs__msg__DetectedObstacle__fini(&data[i - 1]);
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
amr_msgs__msg__DetectedObstacle__Sequence__fini(amr_msgs__msg__DetectedObstacle__Sequence * array)
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
      amr_msgs__msg__DetectedObstacle__fini(&array->data[i]);
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

amr_msgs__msg__DetectedObstacle__Sequence *
amr_msgs__msg__DetectedObstacle__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  amr_msgs__msg__DetectedObstacle__Sequence * array = (amr_msgs__msg__DetectedObstacle__Sequence *)allocator.allocate(sizeof(amr_msgs__msg__DetectedObstacle__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = amr_msgs__msg__DetectedObstacle__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
amr_msgs__msg__DetectedObstacle__Sequence__destroy(amr_msgs__msg__DetectedObstacle__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    amr_msgs__msg__DetectedObstacle__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
amr_msgs__msg__DetectedObstacle__Sequence__are_equal(const amr_msgs__msg__DetectedObstacle__Sequence * lhs, const amr_msgs__msg__DetectedObstacle__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!amr_msgs__msg__DetectedObstacle__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
amr_msgs__msg__DetectedObstacle__Sequence__copy(
  const amr_msgs__msg__DetectedObstacle__Sequence * input,
  amr_msgs__msg__DetectedObstacle__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(amr_msgs__msg__DetectedObstacle)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(amr_msgs__msg__DetectedObstacle);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    amr_msgs__msg__DetectedObstacle * data =
      (amr_msgs__msg__DetectedObstacle *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!amr_msgs__msg__DetectedObstacle__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          amr_msgs__msg__DetectedObstacle__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!amr_msgs__msg__DetectedObstacle__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

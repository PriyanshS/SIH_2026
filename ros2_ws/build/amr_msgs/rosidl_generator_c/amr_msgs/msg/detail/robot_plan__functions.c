// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from amr_msgs:msg/RobotPlan.idl
// generated code does not contain a copyright notice
#include "amr_msgs/msg/detail/robot_plan__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `robot_id`
#include "rosidl_runtime_c/string_functions.h"
// Member `path`
#include "nav_msgs/msg/detail/path__functions.h"
// Member `stamp`
#include "builtin_interfaces/msg/detail/time__functions.h"

bool
amr_msgs__msg__RobotPlan__init(amr_msgs__msg__RobotPlan * msg)
{
  if (!msg) {
    return false;
  }
  // robot_id
  if (!rosidl_runtime_c__String__init(&msg->robot_id)) {
    amr_msgs__msg__RobotPlan__fini(msg);
    return false;
  }
  // plan_seq
  // path
  if (!nav_msgs__msg__Path__init(&msg->path)) {
    amr_msgs__msg__RobotPlan__fini(msg);
    return false;
  }
  // estimated_velocity
  // stamp
  if (!builtin_interfaces__msg__Time__init(&msg->stamp)) {
    amr_msgs__msg__RobotPlan__fini(msg);
    return false;
  }
  return true;
}

void
amr_msgs__msg__RobotPlan__fini(amr_msgs__msg__RobotPlan * msg)
{
  if (!msg) {
    return;
  }
  // robot_id
  rosidl_runtime_c__String__fini(&msg->robot_id);
  // plan_seq
  // path
  nav_msgs__msg__Path__fini(&msg->path);
  // estimated_velocity
  // stamp
  builtin_interfaces__msg__Time__fini(&msg->stamp);
}

bool
amr_msgs__msg__RobotPlan__are_equal(const amr_msgs__msg__RobotPlan * lhs, const amr_msgs__msg__RobotPlan * rhs)
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
  // plan_seq
  if (lhs->plan_seq != rhs->plan_seq) {
    return false;
  }
  // path
  if (!nav_msgs__msg__Path__are_equal(
      &(lhs->path), &(rhs->path)))
  {
    return false;
  }
  // estimated_velocity
  if (lhs->estimated_velocity != rhs->estimated_velocity) {
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
amr_msgs__msg__RobotPlan__copy(
  const amr_msgs__msg__RobotPlan * input,
  amr_msgs__msg__RobotPlan * output)
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
  // plan_seq
  output->plan_seq = input->plan_seq;
  // path
  if (!nav_msgs__msg__Path__copy(
      &(input->path), &(output->path)))
  {
    return false;
  }
  // estimated_velocity
  output->estimated_velocity = input->estimated_velocity;
  // stamp
  if (!builtin_interfaces__msg__Time__copy(
      &(input->stamp), &(output->stamp)))
  {
    return false;
  }
  return true;
}

amr_msgs__msg__RobotPlan *
amr_msgs__msg__RobotPlan__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  amr_msgs__msg__RobotPlan * msg = (amr_msgs__msg__RobotPlan *)allocator.allocate(sizeof(amr_msgs__msg__RobotPlan), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(amr_msgs__msg__RobotPlan));
  bool success = amr_msgs__msg__RobotPlan__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
amr_msgs__msg__RobotPlan__destroy(amr_msgs__msg__RobotPlan * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    amr_msgs__msg__RobotPlan__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
amr_msgs__msg__RobotPlan__Sequence__init(amr_msgs__msg__RobotPlan__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  amr_msgs__msg__RobotPlan * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(amr_msgs__msg__RobotPlan)) {
      return false;
    }
    data = (amr_msgs__msg__RobotPlan *)allocator.zero_allocate(size, sizeof(amr_msgs__msg__RobotPlan), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = amr_msgs__msg__RobotPlan__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        amr_msgs__msg__RobotPlan__fini(&data[i - 1]);
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
amr_msgs__msg__RobotPlan__Sequence__fini(amr_msgs__msg__RobotPlan__Sequence * array)
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
      amr_msgs__msg__RobotPlan__fini(&array->data[i]);
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

amr_msgs__msg__RobotPlan__Sequence *
amr_msgs__msg__RobotPlan__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  amr_msgs__msg__RobotPlan__Sequence * array = (amr_msgs__msg__RobotPlan__Sequence *)allocator.allocate(sizeof(amr_msgs__msg__RobotPlan__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = amr_msgs__msg__RobotPlan__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
amr_msgs__msg__RobotPlan__Sequence__destroy(amr_msgs__msg__RobotPlan__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    amr_msgs__msg__RobotPlan__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
amr_msgs__msg__RobotPlan__Sequence__are_equal(const amr_msgs__msg__RobotPlan__Sequence * lhs, const amr_msgs__msg__RobotPlan__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!amr_msgs__msg__RobotPlan__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
amr_msgs__msg__RobotPlan__Sequence__copy(
  const amr_msgs__msg__RobotPlan__Sequence * input,
  amr_msgs__msg__RobotPlan__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(amr_msgs__msg__RobotPlan)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(amr_msgs__msg__RobotPlan);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    amr_msgs__msg__RobotPlan * data =
      (amr_msgs__msg__RobotPlan *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!amr_msgs__msg__RobotPlan__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          amr_msgs__msg__RobotPlan__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!amr_msgs__msg__RobotPlan__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

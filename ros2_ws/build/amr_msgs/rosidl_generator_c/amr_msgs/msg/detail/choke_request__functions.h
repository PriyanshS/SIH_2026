// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from amr_msgs:msg/ChokeRequest.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "amr_msgs/msg/choke_request.h"


#ifndef AMR_MSGS__MSG__DETAIL__CHOKE_REQUEST__FUNCTIONS_H_
#define AMR_MSGS__MSG__DETAIL__CHOKE_REQUEST__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/action_type_support_struct.h"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_runtime_c/service_type_support_struct.h"
#include "rosidl_runtime_c/type_description/type_description__struct.h"
#include "rosidl_runtime_c/type_description/type_source__struct.h"
#include "rosidl_runtime_c/type_hash.h"
#include "rosidl_runtime_c/visibility_control.h"
#include "amr_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "amr_msgs/msg/detail/choke_request__struct.h"

/// Initialize msg/ChokeRequest message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * amr_msgs__msg__ChokeRequest
 * )) before or use
 * amr_msgs__msg__ChokeRequest__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_amr_msgs
bool
amr_msgs__msg__ChokeRequest__init(amr_msgs__msg__ChokeRequest * msg);

/// Finalize msg/ChokeRequest message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_amr_msgs
void
amr_msgs__msg__ChokeRequest__fini(amr_msgs__msg__ChokeRequest * msg);

/// Create msg/ChokeRequest message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * amr_msgs__msg__ChokeRequest__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_amr_msgs
amr_msgs__msg__ChokeRequest *
amr_msgs__msg__ChokeRequest__create(void);

/// Destroy msg/ChokeRequest message.
/**
 * It calls
 * amr_msgs__msg__ChokeRequest__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_amr_msgs
void
amr_msgs__msg__ChokeRequest__destroy(amr_msgs__msg__ChokeRequest * msg);

/// Check for msg/ChokeRequest message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_amr_msgs
bool
amr_msgs__msg__ChokeRequest__are_equal(const amr_msgs__msg__ChokeRequest * lhs, const amr_msgs__msg__ChokeRequest * rhs);

/// Copy a msg/ChokeRequest message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_amr_msgs
bool
amr_msgs__msg__ChokeRequest__copy(
  const amr_msgs__msg__ChokeRequest * input,
  amr_msgs__msg__ChokeRequest * output);

/// Retrieve pointer to the hash of the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_amr_msgs
const rosidl_type_hash_t *
amr_msgs__msg__ChokeRequest__get_type_hash(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_amr_msgs
const rosidl_runtime_c__type_description__TypeDescription *
amr_msgs__msg__ChokeRequest__get_type_description(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the single raw source text that defined this type.
ROSIDL_GENERATOR_C_PUBLIC_amr_msgs
const rosidl_runtime_c__type_description__TypeSource *
amr_msgs__msg__ChokeRequest__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the recursive raw sources that defined the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_amr_msgs
const rosidl_runtime_c__type_description__TypeSource__Sequence *
amr_msgs__msg__ChokeRequest__get_type_description_sources(
  const rosidl_message_type_support_t * type_support);

/// Initialize array of msg/ChokeRequest messages.
/**
 * It allocates the memory for the number of elements and calls
 * amr_msgs__msg__ChokeRequest__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_amr_msgs
bool
amr_msgs__msg__ChokeRequest__Sequence__init(amr_msgs__msg__ChokeRequest__Sequence * array, size_t size);

/// Finalize array of msg/ChokeRequest messages.
/**
 * It calls
 * amr_msgs__msg__ChokeRequest__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_amr_msgs
void
amr_msgs__msg__ChokeRequest__Sequence__fini(amr_msgs__msg__ChokeRequest__Sequence * array);

/// Create array of msg/ChokeRequest messages.
/**
 * It allocates the memory for the array and calls
 * amr_msgs__msg__ChokeRequest__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_amr_msgs
amr_msgs__msg__ChokeRequest__Sequence *
amr_msgs__msg__ChokeRequest__Sequence__create(size_t size);

/// Destroy array of msg/ChokeRequest messages.
/**
 * It calls
 * amr_msgs__msg__ChokeRequest__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_amr_msgs
void
amr_msgs__msg__ChokeRequest__Sequence__destroy(amr_msgs__msg__ChokeRequest__Sequence * array);

/// Check for msg/ChokeRequest message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_amr_msgs
bool
amr_msgs__msg__ChokeRequest__Sequence__are_equal(const amr_msgs__msg__ChokeRequest__Sequence * lhs, const amr_msgs__msg__ChokeRequest__Sequence * rhs);

/// Copy an array of msg/ChokeRequest messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_amr_msgs
bool
amr_msgs__msg__ChokeRequest__Sequence__copy(
  const amr_msgs__msg__ChokeRequest__Sequence * input,
  amr_msgs__msg__ChokeRequest__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // AMR_MSGS__MSG__DETAIL__CHOKE_REQUEST__FUNCTIONS_H_

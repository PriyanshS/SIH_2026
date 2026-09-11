// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from amr_msgs:msg/ChokeRequest.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "amr_msgs/msg/choke_request.hpp"


#ifndef AMR_MSGS__MSG__DETAIL__CHOKE_REQUEST__STRUCT_HPP_
#define AMR_MSGS__MSG__DETAIL__CHOKE_REQUEST__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__amr_msgs__msg__ChokeRequest __attribute__((deprecated))
#else
# define DEPRECATED__amr_msgs__msg__ChokeRequest __declspec(deprecated)
#endif

namespace amr_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ChokeRequest_
{
  using Type = ChokeRequest_<ContainerAllocator>;

  explicit ChokeRequest_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->robot_id = "";
      this->msg_type = 0;
      this->priority = 0ul;
      this->distance_to_choke = 0.0;
      this->reason = "";
    }
  }

  explicit ChokeRequest_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : robot_id(_alloc),
    reason(_alloc),
    stamp(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->robot_id = "";
      this->msg_type = 0;
      this->priority = 0ul;
      this->distance_to_choke = 0.0;
      this->reason = "";
    }
  }

  // field types and members
  using _robot_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _robot_id_type robot_id;
  using _msg_type_type =
    uint8_t;
  _msg_type_type msg_type;
  using _priority_type =
    uint32_t;
  _priority_type priority;
  using _distance_to_choke_type =
    double;
  _distance_to_choke_type distance_to_choke;
  using _reason_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _reason_type reason;
  using _stamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _stamp_type stamp;

  // setters for named parameter idiom
  Type & set__robot_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->robot_id = _arg;
    return *this;
  }
  Type & set__msg_type(
    const uint8_t & _arg)
  {
    this->msg_type = _arg;
    return *this;
  }
  Type & set__priority(
    const uint32_t & _arg)
  {
    this->priority = _arg;
    return *this;
  }
  Type & set__distance_to_choke(
    const double & _arg)
  {
    this->distance_to_choke = _arg;
    return *this;
  }
  Type & set__reason(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->reason = _arg;
    return *this;
  }
  Type & set__stamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->stamp = _arg;
    return *this;
  }

  // constant declarations
  static constexpr uint8_t REQUEST =
    0u;
  static constexpr uint8_t GRANT =
    1u;
  static constexpr uint8_t RELEASE =
    2u;
  static constexpr uint8_t HEARTBEAT =
    3u;

  // pointer types
  using RawPtr =
    amr_msgs::msg::ChokeRequest_<ContainerAllocator> *;
  using ConstRawPtr =
    const amr_msgs::msg::ChokeRequest_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<amr_msgs::msg::ChokeRequest_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<amr_msgs::msg::ChokeRequest_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      amr_msgs::msg::ChokeRequest_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<amr_msgs::msg::ChokeRequest_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      amr_msgs::msg::ChokeRequest_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<amr_msgs::msg::ChokeRequest_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<amr_msgs::msg::ChokeRequest_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<amr_msgs::msg::ChokeRequest_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__amr_msgs__msg__ChokeRequest
    std::shared_ptr<amr_msgs::msg::ChokeRequest_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__amr_msgs__msg__ChokeRequest
    std::shared_ptr<amr_msgs::msg::ChokeRequest_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ChokeRequest_ & other) const
  {
    if (this->robot_id != other.robot_id) {
      return false;
    }
    if (this->msg_type != other.msg_type) {
      return false;
    }
    if (this->priority != other.priority) {
      return false;
    }
    if (this->distance_to_choke != other.distance_to_choke) {
      return false;
    }
    if (this->reason != other.reason) {
      return false;
    }
    if (this->stamp != other.stamp) {
      return false;
    }
    return true;
  }
  bool operator!=(const ChokeRequest_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ChokeRequest_

// alias to use template instance with default allocator
using ChokeRequest =
  amr_msgs::msg::ChokeRequest_<std::allocator<void>>;

// constant definitions
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ChokeRequest_<ContainerAllocator>::REQUEST;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ChokeRequest_<ContainerAllocator>::GRANT;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ChokeRequest_<ContainerAllocator>::RELEASE;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ChokeRequest_<ContainerAllocator>::HEARTBEAT;
#endif  // __cplusplus < 201703L

}  // namespace msg

}  // namespace amr_msgs

#endif  // AMR_MSGS__MSG__DETAIL__CHOKE_REQUEST__STRUCT_HPP_

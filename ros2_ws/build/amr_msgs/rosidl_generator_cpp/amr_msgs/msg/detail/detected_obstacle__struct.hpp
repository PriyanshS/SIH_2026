// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from amr_msgs:msg/DetectedObstacle.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "amr_msgs/msg/detected_obstacle.hpp"


#ifndef AMR_MSGS__MSG__DETAIL__DETECTED_OBSTACLE__STRUCT_HPP_
#define AMR_MSGS__MSG__DETAIL__DETECTED_OBSTACLE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'position'
#include "geometry_msgs/msg/detail/point__struct.hpp"
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__amr_msgs__msg__DetectedObstacle __attribute__((deprecated))
#else
# define DEPRECATED__amr_msgs__msg__DetectedObstacle __declspec(deprecated)
#endif

namespace amr_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct DetectedObstacle_
{
  using Type = DetectedObstacle_<ContainerAllocator>;

  explicit DetectedObstacle_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : position(_init),
    stamp(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->reporter_id = "";
      this->radius = 0.0;
      this->ttl = 0.0;
    }
  }

  explicit DetectedObstacle_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : reporter_id(_alloc),
    position(_alloc, _init),
    stamp(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->reporter_id = "";
      this->radius = 0.0;
      this->ttl = 0.0;
    }
  }

  // field types and members
  using _reporter_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _reporter_id_type reporter_id;
  using _position_type =
    geometry_msgs::msg::Point_<ContainerAllocator>;
  _position_type position;
  using _radius_type =
    double;
  _radius_type radius;
  using _stamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _stamp_type stamp;
  using _ttl_type =
    double;
  _ttl_type ttl;

  // setters for named parameter idiom
  Type & set__reporter_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->reporter_id = _arg;
    return *this;
  }
  Type & set__position(
    const geometry_msgs::msg::Point_<ContainerAllocator> & _arg)
  {
    this->position = _arg;
    return *this;
  }
  Type & set__radius(
    const double & _arg)
  {
    this->radius = _arg;
    return *this;
  }
  Type & set__stamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->stamp = _arg;
    return *this;
  }
  Type & set__ttl(
    const double & _arg)
  {
    this->ttl = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    amr_msgs::msg::DetectedObstacle_<ContainerAllocator> *;
  using ConstRawPtr =
    const amr_msgs::msg::DetectedObstacle_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<amr_msgs::msg::DetectedObstacle_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<amr_msgs::msg::DetectedObstacle_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      amr_msgs::msg::DetectedObstacle_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<amr_msgs::msg::DetectedObstacle_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      amr_msgs::msg::DetectedObstacle_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<amr_msgs::msg::DetectedObstacle_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<amr_msgs::msg::DetectedObstacle_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<amr_msgs::msg::DetectedObstacle_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__amr_msgs__msg__DetectedObstacle
    std::shared_ptr<amr_msgs::msg::DetectedObstacle_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__amr_msgs__msg__DetectedObstacle
    std::shared_ptr<amr_msgs::msg::DetectedObstacle_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const DetectedObstacle_ & other) const
  {
    if (this->reporter_id != other.reporter_id) {
      return false;
    }
    if (this->position != other.position) {
      return false;
    }
    if (this->radius != other.radius) {
      return false;
    }
    if (this->stamp != other.stamp) {
      return false;
    }
    if (this->ttl != other.ttl) {
      return false;
    }
    return true;
  }
  bool operator!=(const DetectedObstacle_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct DetectedObstacle_

// alias to use template instance with default allocator
using DetectedObstacle =
  amr_msgs::msg::DetectedObstacle_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace amr_msgs

#endif  // AMR_MSGS__MSG__DETAIL__DETECTED_OBSTACLE__STRUCT_HPP_

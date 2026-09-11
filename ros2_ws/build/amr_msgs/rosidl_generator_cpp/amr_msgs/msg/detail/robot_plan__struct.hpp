// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from amr_msgs:msg/RobotPlan.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "amr_msgs/msg/robot_plan.hpp"


#ifndef AMR_MSGS__MSG__DETAIL__ROBOT_PLAN__STRUCT_HPP_
#define AMR_MSGS__MSG__DETAIL__ROBOT_PLAN__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'path'
#include "nav_msgs/msg/detail/path__struct.hpp"
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__amr_msgs__msg__RobotPlan __attribute__((deprecated))
#else
# define DEPRECATED__amr_msgs__msg__RobotPlan __declspec(deprecated)
#endif

namespace amr_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct RobotPlan_
{
  using Type = RobotPlan_<ContainerAllocator>;

  explicit RobotPlan_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : path(_init),
    stamp(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->robot_id = "";
      this->plan_seq = 0ul;
      this->estimated_velocity = 0.0;
    }
  }

  explicit RobotPlan_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : robot_id(_alloc),
    path(_alloc, _init),
    stamp(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->robot_id = "";
      this->plan_seq = 0ul;
      this->estimated_velocity = 0.0;
    }
  }

  // field types and members
  using _robot_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _robot_id_type robot_id;
  using _plan_seq_type =
    uint32_t;
  _plan_seq_type plan_seq;
  using _path_type =
    nav_msgs::msg::Path_<ContainerAllocator>;
  _path_type path;
  using _estimated_velocity_type =
    double;
  _estimated_velocity_type estimated_velocity;
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
  Type & set__plan_seq(
    const uint32_t & _arg)
  {
    this->plan_seq = _arg;
    return *this;
  }
  Type & set__path(
    const nav_msgs::msg::Path_<ContainerAllocator> & _arg)
  {
    this->path = _arg;
    return *this;
  }
  Type & set__estimated_velocity(
    const double & _arg)
  {
    this->estimated_velocity = _arg;
    return *this;
  }
  Type & set__stamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->stamp = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    amr_msgs::msg::RobotPlan_<ContainerAllocator> *;
  using ConstRawPtr =
    const amr_msgs::msg::RobotPlan_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<amr_msgs::msg::RobotPlan_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<amr_msgs::msg::RobotPlan_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      amr_msgs::msg::RobotPlan_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<amr_msgs::msg::RobotPlan_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      amr_msgs::msg::RobotPlan_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<amr_msgs::msg::RobotPlan_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<amr_msgs::msg::RobotPlan_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<amr_msgs::msg::RobotPlan_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__amr_msgs__msg__RobotPlan
    std::shared_ptr<amr_msgs::msg::RobotPlan_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__amr_msgs__msg__RobotPlan
    std::shared_ptr<amr_msgs::msg::RobotPlan_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const RobotPlan_ & other) const
  {
    if (this->robot_id != other.robot_id) {
      return false;
    }
    if (this->plan_seq != other.plan_seq) {
      return false;
    }
    if (this->path != other.path) {
      return false;
    }
    if (this->estimated_velocity != other.estimated_velocity) {
      return false;
    }
    if (this->stamp != other.stamp) {
      return false;
    }
    return true;
  }
  bool operator!=(const RobotPlan_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct RobotPlan_

// alias to use template instance with default allocator
using RobotPlan =
  amr_msgs::msg::RobotPlan_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace amr_msgs

#endif  // AMR_MSGS__MSG__DETAIL__ROBOT_PLAN__STRUCT_HPP_

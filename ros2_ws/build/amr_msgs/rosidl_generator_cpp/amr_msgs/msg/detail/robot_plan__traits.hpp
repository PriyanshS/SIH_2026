// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from amr_msgs:msg/RobotPlan.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "amr_msgs/msg/robot_plan.hpp"


#ifndef AMR_MSGS__MSG__DETAIL__ROBOT_PLAN__TRAITS_HPP_
#define AMR_MSGS__MSG__DETAIL__ROBOT_PLAN__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "amr_msgs/msg/detail/robot_plan__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'path'
#include "nav_msgs/msg/detail/path__traits.hpp"
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace amr_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const RobotPlan & msg,
  std::ostream & out)
{
  out << "{";
  // member: robot_id
  {
    out << "robot_id: ";
    rosidl_generator_traits::value_to_yaml(msg.robot_id, out);
    out << ", ";
  }

  // member: plan_seq
  {
    out << "plan_seq: ";
    rosidl_generator_traits::value_to_yaml(msg.plan_seq, out);
    out << ", ";
  }

  // member: path
  {
    out << "path: ";
    to_flow_style_yaml(msg.path, out);
    out << ", ";
  }

  // member: estimated_velocity
  {
    out << "estimated_velocity: ";
    rosidl_generator_traits::value_to_yaml(msg.estimated_velocity, out);
    out << ", ";
  }

  // member: stamp
  {
    out << "stamp: ";
    to_flow_style_yaml(msg.stamp, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const RobotPlan & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: robot_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "robot_id: ";
    rosidl_generator_traits::value_to_yaml(msg.robot_id, out);
    out << "\n";
  }

  // member: plan_seq
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "plan_seq: ";
    rosidl_generator_traits::value_to_yaml(msg.plan_seq, out);
    out << "\n";
  }

  // member: path
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "path:\n";
    to_block_style_yaml(msg.path, out, indentation + 2);
  }

  // member: estimated_velocity
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "estimated_velocity: ";
    rosidl_generator_traits::value_to_yaml(msg.estimated_velocity, out);
    out << "\n";
  }

  // member: stamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "stamp:\n";
    to_block_style_yaml(msg.stamp, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const RobotPlan & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace amr_msgs

namespace rosidl_generator_traits
{

[[deprecated("use amr_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const amr_msgs::msg::RobotPlan & msg,
  std::ostream & out, size_t indentation = 0)
{
  amr_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use amr_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const amr_msgs::msg::RobotPlan & msg)
{
  return amr_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<amr_msgs::msg::RobotPlan>()
{
  return "amr_msgs::msg::RobotPlan";
}

template<>
inline const char * name<amr_msgs::msg::RobotPlan>()
{
  return "amr_msgs/msg/RobotPlan";
}

template<>
struct has_fixed_size<amr_msgs::msg::RobotPlan>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<amr_msgs::msg::RobotPlan>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<amr_msgs::msg::RobotPlan>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // AMR_MSGS__MSG__DETAIL__ROBOT_PLAN__TRAITS_HPP_

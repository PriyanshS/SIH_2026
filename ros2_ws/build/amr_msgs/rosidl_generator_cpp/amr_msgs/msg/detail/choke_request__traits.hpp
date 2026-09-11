// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from amr_msgs:msg/ChokeRequest.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "amr_msgs/msg/choke_request.hpp"


#ifndef AMR_MSGS__MSG__DETAIL__CHOKE_REQUEST__TRAITS_HPP_
#define AMR_MSGS__MSG__DETAIL__CHOKE_REQUEST__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "amr_msgs/msg/detail/choke_request__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace amr_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const ChokeRequest & msg,
  std::ostream & out)
{
  out << "{";
  // member: robot_id
  {
    out << "robot_id: ";
    rosidl_generator_traits::value_to_yaml(msg.robot_id, out);
    out << ", ";
  }

  // member: msg_type
  {
    out << "msg_type: ";
    rosidl_generator_traits::value_to_yaml(msg.msg_type, out);
    out << ", ";
  }

  // member: priority
  {
    out << "priority: ";
    rosidl_generator_traits::value_to_yaml(msg.priority, out);
    out << ", ";
  }

  // member: distance_to_choke
  {
    out << "distance_to_choke: ";
    rosidl_generator_traits::value_to_yaml(msg.distance_to_choke, out);
    out << ", ";
  }

  // member: reason
  {
    out << "reason: ";
    rosidl_generator_traits::value_to_yaml(msg.reason, out);
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
  const ChokeRequest & msg,
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

  // member: msg_type
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "msg_type: ";
    rosidl_generator_traits::value_to_yaml(msg.msg_type, out);
    out << "\n";
  }

  // member: priority
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "priority: ";
    rosidl_generator_traits::value_to_yaml(msg.priority, out);
    out << "\n";
  }

  // member: distance_to_choke
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "distance_to_choke: ";
    rosidl_generator_traits::value_to_yaml(msg.distance_to_choke, out);
    out << "\n";
  }

  // member: reason
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "reason: ";
    rosidl_generator_traits::value_to_yaml(msg.reason, out);
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

inline std::string to_yaml(const ChokeRequest & msg, bool use_flow_style = false)
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
  const amr_msgs::msg::ChokeRequest & msg,
  std::ostream & out, size_t indentation = 0)
{
  amr_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use amr_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const amr_msgs::msg::ChokeRequest & msg)
{
  return amr_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<amr_msgs::msg::ChokeRequest>()
{
  return "amr_msgs::msg::ChokeRequest";
}

template<>
inline const char * name<amr_msgs::msg::ChokeRequest>()
{
  return "amr_msgs/msg/ChokeRequest";
}

template<>
struct has_fixed_size<amr_msgs::msg::ChokeRequest>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<amr_msgs::msg::ChokeRequest>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<amr_msgs::msg::ChokeRequest>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // AMR_MSGS__MSG__DETAIL__CHOKE_REQUEST__TRAITS_HPP_

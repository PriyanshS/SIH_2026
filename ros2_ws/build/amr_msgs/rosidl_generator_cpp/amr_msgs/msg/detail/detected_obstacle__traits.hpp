// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from amr_msgs:msg/DetectedObstacle.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "amr_msgs/msg/detected_obstacle.hpp"


#ifndef AMR_MSGS__MSG__DETAIL__DETECTED_OBSTACLE__TRAITS_HPP_
#define AMR_MSGS__MSG__DETAIL__DETECTED_OBSTACLE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "amr_msgs/msg/detail/detected_obstacle__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'position'
#include "geometry_msgs/msg/detail/point__traits.hpp"
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace amr_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const DetectedObstacle & msg,
  std::ostream & out)
{
  out << "{";
  // member: reporter_id
  {
    out << "reporter_id: ";
    rosidl_generator_traits::value_to_yaml(msg.reporter_id, out);
    out << ", ";
  }

  // member: position
  {
    out << "position: ";
    to_flow_style_yaml(msg.position, out);
    out << ", ";
  }

  // member: radius
  {
    out << "radius: ";
    rosidl_generator_traits::value_to_yaml(msg.radius, out);
    out << ", ";
  }

  // member: stamp
  {
    out << "stamp: ";
    to_flow_style_yaml(msg.stamp, out);
    out << ", ";
  }

  // member: ttl
  {
    out << "ttl: ";
    rosidl_generator_traits::value_to_yaml(msg.ttl, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const DetectedObstacle & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: reporter_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "reporter_id: ";
    rosidl_generator_traits::value_to_yaml(msg.reporter_id, out);
    out << "\n";
  }

  // member: position
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "position:\n";
    to_block_style_yaml(msg.position, out, indentation + 2);
  }

  // member: radius
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "radius: ";
    rosidl_generator_traits::value_to_yaml(msg.radius, out);
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

  // member: ttl
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "ttl: ";
    rosidl_generator_traits::value_to_yaml(msg.ttl, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const DetectedObstacle & msg, bool use_flow_style = false)
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
  const amr_msgs::msg::DetectedObstacle & msg,
  std::ostream & out, size_t indentation = 0)
{
  amr_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use amr_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const amr_msgs::msg::DetectedObstacle & msg)
{
  return amr_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<amr_msgs::msg::DetectedObstacle>()
{
  return "amr_msgs::msg::DetectedObstacle";
}

template<>
inline const char * name<amr_msgs::msg::DetectedObstacle>()
{
  return "amr_msgs/msg/DetectedObstacle";
}

template<>
struct has_fixed_size<amr_msgs::msg::DetectedObstacle>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<amr_msgs::msg::DetectedObstacle>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<amr_msgs::msg::DetectedObstacle>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // AMR_MSGS__MSG__DETAIL__DETECTED_OBSTACLE__TRAITS_HPP_

// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from amr_msgs:msg/DetectedObstacle.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "amr_msgs/msg/detected_obstacle.hpp"


#ifndef AMR_MSGS__MSG__DETAIL__DETECTED_OBSTACLE__BUILDER_HPP_
#define AMR_MSGS__MSG__DETAIL__DETECTED_OBSTACLE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "amr_msgs/msg/detail/detected_obstacle__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace amr_msgs
{

namespace msg
{

namespace builder
{

class Init_DetectedObstacle_ttl
{
public:
  explicit Init_DetectedObstacle_ttl(::amr_msgs::msg::DetectedObstacle & msg)
  : msg_(msg)
  {}
  ::amr_msgs::msg::DetectedObstacle ttl(::amr_msgs::msg::DetectedObstacle::_ttl_type arg)
  {
    msg_.ttl = std::move(arg);
    return std::move(msg_);
  }

private:
  ::amr_msgs::msg::DetectedObstacle msg_;
};

class Init_DetectedObstacle_stamp
{
public:
  explicit Init_DetectedObstacle_stamp(::amr_msgs::msg::DetectedObstacle & msg)
  : msg_(msg)
  {}
  Init_DetectedObstacle_ttl stamp(::amr_msgs::msg::DetectedObstacle::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return Init_DetectedObstacle_ttl(msg_);
  }

private:
  ::amr_msgs::msg::DetectedObstacle msg_;
};

class Init_DetectedObstacle_radius
{
public:
  explicit Init_DetectedObstacle_radius(::amr_msgs::msg::DetectedObstacle & msg)
  : msg_(msg)
  {}
  Init_DetectedObstacle_stamp radius(::amr_msgs::msg::DetectedObstacle::_radius_type arg)
  {
    msg_.radius = std::move(arg);
    return Init_DetectedObstacle_stamp(msg_);
  }

private:
  ::amr_msgs::msg::DetectedObstacle msg_;
};

class Init_DetectedObstacle_position
{
public:
  explicit Init_DetectedObstacle_position(::amr_msgs::msg::DetectedObstacle & msg)
  : msg_(msg)
  {}
  Init_DetectedObstacle_radius position(::amr_msgs::msg::DetectedObstacle::_position_type arg)
  {
    msg_.position = std::move(arg);
    return Init_DetectedObstacle_radius(msg_);
  }

private:
  ::amr_msgs::msg::DetectedObstacle msg_;
};

class Init_DetectedObstacle_reporter_id
{
public:
  Init_DetectedObstacle_reporter_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_DetectedObstacle_position reporter_id(::amr_msgs::msg::DetectedObstacle::_reporter_id_type arg)
  {
    msg_.reporter_id = std::move(arg);
    return Init_DetectedObstacle_position(msg_);
  }

private:
  ::amr_msgs::msg::DetectedObstacle msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::amr_msgs::msg::DetectedObstacle>()
{
  return amr_msgs::msg::builder::Init_DetectedObstacle_reporter_id();
}

}  // namespace amr_msgs

#endif  // AMR_MSGS__MSG__DETAIL__DETECTED_OBSTACLE__BUILDER_HPP_

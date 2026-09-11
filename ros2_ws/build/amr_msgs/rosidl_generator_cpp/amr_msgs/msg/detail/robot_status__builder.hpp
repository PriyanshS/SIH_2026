// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from amr_msgs:msg/RobotStatus.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "amr_msgs/msg/robot_status.hpp"


#ifndef AMR_MSGS__MSG__DETAIL__ROBOT_STATUS__BUILDER_HPP_
#define AMR_MSGS__MSG__DETAIL__ROBOT_STATUS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "amr_msgs/msg/detail/robot_status__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace amr_msgs
{

namespace msg
{

namespace builder
{

class Init_RobotStatus_stamp
{
public:
  explicit Init_RobotStatus_stamp(::amr_msgs::msg::RobotStatus & msg)
  : msg_(msg)
  {}
  ::amr_msgs::msg::RobotStatus stamp(::amr_msgs::msg::RobotStatus::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::amr_msgs::msg::RobotStatus msg_;
};

class Init_RobotStatus_pose_y
{
public:
  explicit Init_RobotStatus_pose_y(::amr_msgs::msg::RobotStatus & msg)
  : msg_(msg)
  {}
  Init_RobotStatus_stamp pose_y(::amr_msgs::msg::RobotStatus::_pose_y_type arg)
  {
    msg_.pose_y = std::move(arg);
    return Init_RobotStatus_stamp(msg_);
  }

private:
  ::amr_msgs::msg::RobotStatus msg_;
};

class Init_RobotStatus_pose_x
{
public:
  explicit Init_RobotStatus_pose_x(::amr_msgs::msg::RobotStatus & msg)
  : msg_(msg)
  {}
  Init_RobotStatus_pose_y pose_x(::amr_msgs::msg::RobotStatus::_pose_x_type arg)
  {
    msg_.pose_x = std::move(arg);
    return Init_RobotStatus_pose_y(msg_);
  }

private:
  ::amr_msgs::msg::RobotStatus msg_;
};

class Init_RobotStatus_status
{
public:
  explicit Init_RobotStatus_status(::amr_msgs::msg::RobotStatus & msg)
  : msg_(msg)
  {}
  Init_RobotStatus_pose_x status(::amr_msgs::msg::RobotStatus::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_RobotStatus_pose_x(msg_);
  }

private:
  ::amr_msgs::msg::RobotStatus msg_;
};

class Init_RobotStatus_robot_id
{
public:
  Init_RobotStatus_robot_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RobotStatus_status robot_id(::amr_msgs::msg::RobotStatus::_robot_id_type arg)
  {
    msg_.robot_id = std::move(arg);
    return Init_RobotStatus_status(msg_);
  }

private:
  ::amr_msgs::msg::RobotStatus msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::amr_msgs::msg::RobotStatus>()
{
  return amr_msgs::msg::builder::Init_RobotStatus_robot_id();
}

}  // namespace amr_msgs

#endif  // AMR_MSGS__MSG__DETAIL__ROBOT_STATUS__BUILDER_HPP_

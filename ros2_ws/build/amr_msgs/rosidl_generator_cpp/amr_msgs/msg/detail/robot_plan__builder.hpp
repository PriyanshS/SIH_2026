// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from amr_msgs:msg/RobotPlan.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "amr_msgs/msg/robot_plan.hpp"


#ifndef AMR_MSGS__MSG__DETAIL__ROBOT_PLAN__BUILDER_HPP_
#define AMR_MSGS__MSG__DETAIL__ROBOT_PLAN__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "amr_msgs/msg/detail/robot_plan__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace amr_msgs
{

namespace msg
{

namespace builder
{

class Init_RobotPlan_stamp
{
public:
  explicit Init_RobotPlan_stamp(::amr_msgs::msg::RobotPlan & msg)
  : msg_(msg)
  {}
  ::amr_msgs::msg::RobotPlan stamp(::amr_msgs::msg::RobotPlan::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::amr_msgs::msg::RobotPlan msg_;
};

class Init_RobotPlan_estimated_velocity
{
public:
  explicit Init_RobotPlan_estimated_velocity(::amr_msgs::msg::RobotPlan & msg)
  : msg_(msg)
  {}
  Init_RobotPlan_stamp estimated_velocity(::amr_msgs::msg::RobotPlan::_estimated_velocity_type arg)
  {
    msg_.estimated_velocity = std::move(arg);
    return Init_RobotPlan_stamp(msg_);
  }

private:
  ::amr_msgs::msg::RobotPlan msg_;
};

class Init_RobotPlan_path
{
public:
  explicit Init_RobotPlan_path(::amr_msgs::msg::RobotPlan & msg)
  : msg_(msg)
  {}
  Init_RobotPlan_estimated_velocity path(::amr_msgs::msg::RobotPlan::_path_type arg)
  {
    msg_.path = std::move(arg);
    return Init_RobotPlan_estimated_velocity(msg_);
  }

private:
  ::amr_msgs::msg::RobotPlan msg_;
};

class Init_RobotPlan_plan_seq
{
public:
  explicit Init_RobotPlan_plan_seq(::amr_msgs::msg::RobotPlan & msg)
  : msg_(msg)
  {}
  Init_RobotPlan_path plan_seq(::amr_msgs::msg::RobotPlan::_plan_seq_type arg)
  {
    msg_.plan_seq = std::move(arg);
    return Init_RobotPlan_path(msg_);
  }

private:
  ::amr_msgs::msg::RobotPlan msg_;
};

class Init_RobotPlan_robot_id
{
public:
  Init_RobotPlan_robot_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RobotPlan_plan_seq robot_id(::amr_msgs::msg::RobotPlan::_robot_id_type arg)
  {
    msg_.robot_id = std::move(arg);
    return Init_RobotPlan_plan_seq(msg_);
  }

private:
  ::amr_msgs::msg::RobotPlan msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::amr_msgs::msg::RobotPlan>()
{
  return amr_msgs::msg::builder::Init_RobotPlan_robot_id();
}

}  // namespace amr_msgs

#endif  // AMR_MSGS__MSG__DETAIL__ROBOT_PLAN__BUILDER_HPP_

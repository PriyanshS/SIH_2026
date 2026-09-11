// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from amr_msgs:msg/ChokeRequest.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "amr_msgs/msg/choke_request.hpp"


#ifndef AMR_MSGS__MSG__DETAIL__CHOKE_REQUEST__BUILDER_HPP_
#define AMR_MSGS__MSG__DETAIL__CHOKE_REQUEST__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "amr_msgs/msg/detail/choke_request__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace amr_msgs
{

namespace msg
{

namespace builder
{

class Init_ChokeRequest_stamp
{
public:
  explicit Init_ChokeRequest_stamp(::amr_msgs::msg::ChokeRequest & msg)
  : msg_(msg)
  {}
  ::amr_msgs::msg::ChokeRequest stamp(::amr_msgs::msg::ChokeRequest::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::amr_msgs::msg::ChokeRequest msg_;
};

class Init_ChokeRequest_reason
{
public:
  explicit Init_ChokeRequest_reason(::amr_msgs::msg::ChokeRequest & msg)
  : msg_(msg)
  {}
  Init_ChokeRequest_stamp reason(::amr_msgs::msg::ChokeRequest::_reason_type arg)
  {
    msg_.reason = std::move(arg);
    return Init_ChokeRequest_stamp(msg_);
  }

private:
  ::amr_msgs::msg::ChokeRequest msg_;
};

class Init_ChokeRequest_distance_to_choke
{
public:
  explicit Init_ChokeRequest_distance_to_choke(::amr_msgs::msg::ChokeRequest & msg)
  : msg_(msg)
  {}
  Init_ChokeRequest_reason distance_to_choke(::amr_msgs::msg::ChokeRequest::_distance_to_choke_type arg)
  {
    msg_.distance_to_choke = std::move(arg);
    return Init_ChokeRequest_reason(msg_);
  }

private:
  ::amr_msgs::msg::ChokeRequest msg_;
};

class Init_ChokeRequest_priority
{
public:
  explicit Init_ChokeRequest_priority(::amr_msgs::msg::ChokeRequest & msg)
  : msg_(msg)
  {}
  Init_ChokeRequest_distance_to_choke priority(::amr_msgs::msg::ChokeRequest::_priority_type arg)
  {
    msg_.priority = std::move(arg);
    return Init_ChokeRequest_distance_to_choke(msg_);
  }

private:
  ::amr_msgs::msg::ChokeRequest msg_;
};

class Init_ChokeRequest_msg_type
{
public:
  explicit Init_ChokeRequest_msg_type(::amr_msgs::msg::ChokeRequest & msg)
  : msg_(msg)
  {}
  Init_ChokeRequest_priority msg_type(::amr_msgs::msg::ChokeRequest::_msg_type_type arg)
  {
    msg_.msg_type = std::move(arg);
    return Init_ChokeRequest_priority(msg_);
  }

private:
  ::amr_msgs::msg::ChokeRequest msg_;
};

class Init_ChokeRequest_robot_id
{
public:
  Init_ChokeRequest_robot_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ChokeRequest_msg_type robot_id(::amr_msgs::msg::ChokeRequest::_robot_id_type arg)
  {
    msg_.robot_id = std::move(arg);
    return Init_ChokeRequest_msg_type(msg_);
  }

private:
  ::amr_msgs::msg::ChokeRequest msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::amr_msgs::msg::ChokeRequest>()
{
  return amr_msgs::msg::builder::Init_ChokeRequest_robot_id();
}

}  // namespace amr_msgs

#endif  // AMR_MSGS__MSG__DETAIL__CHOKE_REQUEST__BUILDER_HPP_

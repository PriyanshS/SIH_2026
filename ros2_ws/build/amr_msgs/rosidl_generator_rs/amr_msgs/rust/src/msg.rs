#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to amr_msgs__msg__RobotPlan
/// Robot's shared navigation plan

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotPlan {

    // This member is not documented.
    #[allow(missing_docs)]
    pub robot_id: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub plan_seq: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub path: nav_msgs::msg::Path,


    // This member is not documented.
    #[allow(missing_docs)]
    pub estimated_velocity: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::Time,

}



impl Default for RobotPlan {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::RobotPlan::default())
  }
}

impl rosidl_runtime_rs::Message for RobotPlan {
  type RmwMsg = super::msg::rmw::RobotPlan;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        robot_id: msg.robot_id.as_str().into(),
        plan_seq: msg.plan_seq,
        path: nav_msgs::msg::Path::into_rmw_message(std::borrow::Cow::Owned(msg.path)).into_owned(),
        estimated_velocity: msg.estimated_velocity,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.stamp)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        robot_id: msg.robot_id.as_str().into(),
      plan_seq: msg.plan_seq,
        path: nav_msgs::msg::Path::into_rmw_message(std::borrow::Cow::Borrowed(&msg.path)).into_owned(),
      estimated_velocity: msg.estimated_velocity,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.stamp)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      robot_id: msg.robot_id.to_string(),
      plan_seq: msg.plan_seq,
      path: nav_msgs::msg::Path::from_rmw_message(msg.path),
      estimated_velocity: msg.estimated_velocity,
      stamp: builtin_interfaces::msg::Time::from_rmw_message(msg.stamp),
    }
  }
}


// Corresponds to amr_msgs__msg__DetectedObstacle
/// Dynamic obstacle detected by a robot and relayed to peers

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DetectedObstacle {

    // This member is not documented.
    #[allow(missing_docs)]
    pub reporter_id: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub position: geometry_msgs::msg::Point,


    // This member is not documented.
    #[allow(missing_docs)]
    pub radius: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::Time,


    // This member is not documented.
    #[allow(missing_docs)]
    pub ttl: f64,

}



impl Default for DetectedObstacle {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::DetectedObstacle::default())
  }
}

impl rosidl_runtime_rs::Message for DetectedObstacle {
  type RmwMsg = super::msg::rmw::DetectedObstacle;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        reporter_id: msg.reporter_id.as_str().into(),
        position: geometry_msgs::msg::Point::into_rmw_message(std::borrow::Cow::Owned(msg.position)).into_owned(),
        radius: msg.radius,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.stamp)).into_owned(),
        ttl: msg.ttl,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        reporter_id: msg.reporter_id.as_str().into(),
        position: geometry_msgs::msg::Point::into_rmw_message(std::borrow::Cow::Borrowed(&msg.position)).into_owned(),
      radius: msg.radius,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.stamp)).into_owned(),
      ttl: msg.ttl,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      reporter_id: msg.reporter_id.to_string(),
      position: geometry_msgs::msg::Point::from_rmw_message(msg.position),
      radius: msg.radius,
      stamp: builtin_interfaces::msg::Time::from_rmw_message(msg.stamp),
      ttl: msg.ttl,
    }
  }
}


// Corresponds to amr_msgs__msg__ChokeRequest
/// Chokepoint negotiation protocol message

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ChokeRequest {

    // This member is not documented.
    #[allow(missing_docs)]
    pub robot_id: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub msg_type: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub priority: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub distance_to_choke: f64,

    /// human-readable yield reason e.g. "yielding to robot2, lower priority"
    pub reason: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::Time,

}

impl ChokeRequest {
    /// msg_type constants
    pub const REQUEST: u8 = 0;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const GRANT: u8 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const RELEASE: u8 = 2;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const HEARTBEAT: u8 = 3;

}


impl Default for ChokeRequest {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::ChokeRequest::default())
  }
}

impl rosidl_runtime_rs::Message for ChokeRequest {
  type RmwMsg = super::msg::rmw::ChokeRequest;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        robot_id: msg.robot_id.as_str().into(),
        msg_type: msg.msg_type,
        priority: msg.priority,
        distance_to_choke: msg.distance_to_choke,
        reason: msg.reason.as_str().into(),
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.stamp)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        robot_id: msg.robot_id.as_str().into(),
      msg_type: msg.msg_type,
      priority: msg.priority,
      distance_to_choke: msg.distance_to_choke,
        reason: msg.reason.as_str().into(),
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.stamp)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      robot_id: msg.robot_id.to_string(),
      msg_type: msg.msg_type,
      priority: msg.priority,
      distance_to_choke: msg.distance_to_choke,
      reason: msg.reason.to_string(),
      stamp: builtin_interfaces::msg::Time::from_rmw_message(msg.stamp),
    }
  }
}


// Corresponds to amr_msgs__msg__RobotStatus
/// Per-robot idle/busy state published for the goal dispatcher

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotStatus {

    // This member is not documented.
    #[allow(missing_docs)]
    pub robot_id: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub status: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pose_x: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pose_y: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::Time,

}

impl RobotStatus {
    /// status constants
    pub const IDLE: u8 = 0;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const BUSY: u8 = 1;

}


impl Default for RobotStatus {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::RobotStatus::default())
  }
}

impl rosidl_runtime_rs::Message for RobotStatus {
  type RmwMsg = super::msg::rmw::RobotStatus;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        robot_id: msg.robot_id.as_str().into(),
        status: msg.status,
        pose_x: msg.pose_x,
        pose_y: msg.pose_y,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.stamp)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        robot_id: msg.robot_id.as_str().into(),
      status: msg.status,
      pose_x: msg.pose_x,
      pose_y: msg.pose_y,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.stamp)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      robot_id: msg.robot_id.to_string(),
      status: msg.status,
      pose_x: msg.pose_x,
      pose_y: msg.pose_y,
      stamp: builtin_interfaces::msg::Time::from_rmw_message(msg.stamp),
    }
  }
}



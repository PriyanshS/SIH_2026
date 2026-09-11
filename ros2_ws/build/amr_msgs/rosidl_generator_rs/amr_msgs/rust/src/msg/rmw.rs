#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "amr_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__amr_msgs__msg__RobotPlan() -> *const std::ffi::c_void;
}

#[link(name = "amr_msgs__rosidl_generator_c")]
extern "C" {
    fn amr_msgs__msg__RobotPlan__init(msg: *mut RobotPlan) -> bool;
    fn amr_msgs__msg__RobotPlan__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RobotPlan>, size: usize) -> bool;
    fn amr_msgs__msg__RobotPlan__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RobotPlan>);
    fn amr_msgs__msg__RobotPlan__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RobotPlan>, out_seq: *mut rosidl_runtime_rs::Sequence<RobotPlan>) -> bool;
}

// Corresponds to amr_msgs__msg__RobotPlan
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Robot's shared navigation plan

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotPlan {

    // This member is not documented.
    #[allow(missing_docs)]
    pub robot_id: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub plan_seq: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub path: nav_msgs::msg::rmw::Path,


    // This member is not documented.
    #[allow(missing_docs)]
    pub estimated_velocity: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::rmw::Time,

}



impl Default for RobotPlan {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !amr_msgs__msg__RobotPlan__init(&mut msg as *mut _) {
        panic!("Call to amr_msgs__msg__RobotPlan__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RobotPlan {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { amr_msgs__msg__RobotPlan__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { amr_msgs__msg__RobotPlan__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { amr_msgs__msg__RobotPlan__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RobotPlan {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RobotPlan where Self: Sized {
  const TYPE_NAME: &'static str = "amr_msgs/msg/RobotPlan";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__amr_msgs__msg__RobotPlan() }
  }
}


#[link(name = "amr_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__amr_msgs__msg__DetectedObstacle() -> *const std::ffi::c_void;
}

#[link(name = "amr_msgs__rosidl_generator_c")]
extern "C" {
    fn amr_msgs__msg__DetectedObstacle__init(msg: *mut DetectedObstacle) -> bool;
    fn amr_msgs__msg__DetectedObstacle__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<DetectedObstacle>, size: usize) -> bool;
    fn amr_msgs__msg__DetectedObstacle__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<DetectedObstacle>);
    fn amr_msgs__msg__DetectedObstacle__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<DetectedObstacle>, out_seq: *mut rosidl_runtime_rs::Sequence<DetectedObstacle>) -> bool;
}

// Corresponds to amr_msgs__msg__DetectedObstacle
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Dynamic obstacle detected by a robot and relayed to peers

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DetectedObstacle {

    // This member is not documented.
    #[allow(missing_docs)]
    pub reporter_id: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub position: geometry_msgs::msg::rmw::Point,


    // This member is not documented.
    #[allow(missing_docs)]
    pub radius: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::rmw::Time,


    // This member is not documented.
    #[allow(missing_docs)]
    pub ttl: f64,

}



impl Default for DetectedObstacle {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !amr_msgs__msg__DetectedObstacle__init(&mut msg as *mut _) {
        panic!("Call to amr_msgs__msg__DetectedObstacle__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for DetectedObstacle {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { amr_msgs__msg__DetectedObstacle__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { amr_msgs__msg__DetectedObstacle__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { amr_msgs__msg__DetectedObstacle__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for DetectedObstacle {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for DetectedObstacle where Self: Sized {
  const TYPE_NAME: &'static str = "amr_msgs/msg/DetectedObstacle";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__amr_msgs__msg__DetectedObstacle() }
  }
}


#[link(name = "amr_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__amr_msgs__msg__ChokeRequest() -> *const std::ffi::c_void;
}

#[link(name = "amr_msgs__rosidl_generator_c")]
extern "C" {
    fn amr_msgs__msg__ChokeRequest__init(msg: *mut ChokeRequest) -> bool;
    fn amr_msgs__msg__ChokeRequest__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ChokeRequest>, size: usize) -> bool;
    fn amr_msgs__msg__ChokeRequest__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ChokeRequest>);
    fn amr_msgs__msg__ChokeRequest__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ChokeRequest>, out_seq: *mut rosidl_runtime_rs::Sequence<ChokeRequest>) -> bool;
}

// Corresponds to amr_msgs__msg__ChokeRequest
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Chokepoint negotiation protocol message

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ChokeRequest {

    // This member is not documented.
    #[allow(missing_docs)]
    pub robot_id: rosidl_runtime_rs::String,


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
    pub reason: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::rmw::Time,

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
    unsafe {
      let mut msg = std::mem::zeroed();
      if !amr_msgs__msg__ChokeRequest__init(&mut msg as *mut _) {
        panic!("Call to amr_msgs__msg__ChokeRequest__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ChokeRequest {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { amr_msgs__msg__ChokeRequest__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { amr_msgs__msg__ChokeRequest__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { amr_msgs__msg__ChokeRequest__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ChokeRequest {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ChokeRequest where Self: Sized {
  const TYPE_NAME: &'static str = "amr_msgs/msg/ChokeRequest";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__amr_msgs__msg__ChokeRequest() }
  }
}


#[link(name = "amr_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__amr_msgs__msg__RobotStatus() -> *const std::ffi::c_void;
}

#[link(name = "amr_msgs__rosidl_generator_c")]
extern "C" {
    fn amr_msgs__msg__RobotStatus__init(msg: *mut RobotStatus) -> bool;
    fn amr_msgs__msg__RobotStatus__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RobotStatus>, size: usize) -> bool;
    fn amr_msgs__msg__RobotStatus__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RobotStatus>);
    fn amr_msgs__msg__RobotStatus__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RobotStatus>, out_seq: *mut rosidl_runtime_rs::Sequence<RobotStatus>) -> bool;
}

// Corresponds to amr_msgs__msg__RobotStatus
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Per-robot idle/busy state published for the goal dispatcher

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotStatus {

    // This member is not documented.
    #[allow(missing_docs)]
    pub robot_id: rosidl_runtime_rs::String,


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
    pub stamp: builtin_interfaces::msg::rmw::Time,

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
    unsafe {
      let mut msg = std::mem::zeroed();
      if !amr_msgs__msg__RobotStatus__init(&mut msg as *mut _) {
        panic!("Call to amr_msgs__msg__RobotStatus__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RobotStatus {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { amr_msgs__msg__RobotStatus__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { amr_msgs__msg__RobotStatus__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { amr_msgs__msg__RobotStatus__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RobotStatus {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RobotStatus where Self: Sized {
  const TYPE_NAME: &'static str = "amr_msgs/msg/RobotStatus";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__amr_msgs__msg__RobotStatus() }
  }
}



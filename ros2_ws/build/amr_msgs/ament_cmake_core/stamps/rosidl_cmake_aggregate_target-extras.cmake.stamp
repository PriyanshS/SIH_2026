# generated from rosidl_cmake/cmake/rosidl_cmake_aggregate_target-extras.cmake.in

# Create a convenience aggregate target amr_msgs::amr_msgs
# that links all generated interface targets, so downstream packages can use
# a single modern CMake target name instead of ${amr_msgs_TARGETS}.
if(amr_msgs_TARGETS AND NOT TARGET amr_msgs::amr_msgs)
  add_library(amr_msgs::amr_msgs INTERFACE IMPORTED)
  set_target_properties(amr_msgs::amr_msgs PROPERTIES
    INTERFACE_LINK_LIBRARIES "${amr_msgs_TARGETS}")
endif()

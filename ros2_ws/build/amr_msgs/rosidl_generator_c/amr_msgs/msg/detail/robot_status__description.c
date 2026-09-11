// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from amr_msgs:msg/RobotStatus.idl
// generated code does not contain a copyright notice

#include "amr_msgs/msg/detail/robot_status__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_amr_msgs
const rosidl_type_hash_t *
amr_msgs__msg__RobotStatus__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xa6, 0x39, 0x19, 0xc7, 0x91, 0x72, 0x65, 0xdc,
      0xe3, 0x1f, 0xf6, 0x6a, 0x54, 0x3d, 0xeb, 0xa3,
      0x63, 0x6c, 0xde, 0x47, 0xe2, 0xee, 0xbc, 0x9d,
      0x22, 0x5c, 0x42, 0xac, 0xea, 0xce, 0xc4, 0x12,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types
#include "builtin_interfaces/msg/detail/time__functions.h"

// Hashes for external referenced types
#ifndef NDEBUG
static const rosidl_type_hash_t builtin_interfaces__msg__Time__EXPECTED_HASH = {1, {
    0xb1, 0x06, 0x23, 0x5e, 0x25, 0xa4, 0xc5, 0xed,
    0x35, 0x09, 0x8a, 0xa0, 0xa6, 0x1a, 0x3e, 0xe9,
    0xc9, 0xb1, 0x8d, 0x19, 0x7f, 0x39, 0x8b, 0x0e,
    0x42, 0x06, 0xce, 0xa9, 0xac, 0xf9, 0xc1, 0x97,
  }};
#endif

static char amr_msgs__msg__RobotStatus__TYPE_NAME[] = "amr_msgs/msg/RobotStatus";
static char builtin_interfaces__msg__Time__TYPE_NAME[] = "builtin_interfaces/msg/Time";

// Define type names, field names, and default values
static char amr_msgs__msg__RobotStatus__FIELD_NAME__robot_id[] = "robot_id";
static char amr_msgs__msg__RobotStatus__FIELD_NAME__status[] = "status";
static char amr_msgs__msg__RobotStatus__FIELD_NAME__pose_x[] = "pose_x";
static char amr_msgs__msg__RobotStatus__FIELD_NAME__pose_y[] = "pose_y";
static char amr_msgs__msg__RobotStatus__FIELD_NAME__stamp[] = "stamp";

static rosidl_runtime_c__type_description__Field amr_msgs__msg__RobotStatus__FIELDS[] = {
  {
    {amr_msgs__msg__RobotStatus__FIELD_NAME__robot_id, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {amr_msgs__msg__RobotStatus__FIELD_NAME__status, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT8,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {amr_msgs__msg__RobotStatus__FIELD_NAME__pose_x, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {amr_msgs__msg__RobotStatus__FIELD_NAME__pose_y, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {amr_msgs__msg__RobotStatus__FIELD_NAME__stamp, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription amr_msgs__msg__RobotStatus__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
amr_msgs__msg__RobotStatus__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {amr_msgs__msg__RobotStatus__TYPE_NAME, 24, 24},
      {amr_msgs__msg__RobotStatus__FIELDS, 5, 5},
    },
    {amr_msgs__msg__RobotStatus__REFERENCED_TYPE_DESCRIPTIONS, 1, 1},
  };
  if (!constructed) {
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "# Per-robot idle/busy state published for the goal dispatcher\n"
  "string  robot_id\n"
  "uint8   status\n"
  "float64 pose_x\n"
  "float64 pose_y\n"
  "builtin_interfaces/Time stamp\n"
  "\n"
  "# status constants\n"
  "uint8 IDLE=0\n"
  "uint8 BUSY=1";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
amr_msgs__msg__RobotStatus__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {amr_msgs__msg__RobotStatus__TYPE_NAME, 24, 24},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 200, 200},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
amr_msgs__msg__RobotStatus__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[2];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 2, 2};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *amr_msgs__msg__RobotStatus__get_individual_type_description_source(NULL),
    sources[1] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}

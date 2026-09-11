// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from amr_msgs:msg/DetectedObstacle.idl
// generated code does not contain a copyright notice

#include "amr_msgs/msg/detail/detected_obstacle__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_amr_msgs
const rosidl_type_hash_t *
amr_msgs__msg__DetectedObstacle__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xc9, 0xb0, 0x71, 0xa9, 0x18, 0x79, 0xbb, 0x34,
      0x14, 0xc7, 0x21, 0xf7, 0x1c, 0xfe, 0x08, 0xa6,
      0xb0, 0x68, 0x40, 0xae, 0x82, 0x09, 0x6e, 0x4f,
      0xf5, 0x5c, 0x06, 0x50, 0x21, 0x7f, 0xc2, 0x5f,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types
#include "builtin_interfaces/msg/detail/time__functions.h"
#include "geometry_msgs/msg/detail/point__functions.h"

// Hashes for external referenced types
#ifndef NDEBUG
static const rosidl_type_hash_t builtin_interfaces__msg__Time__EXPECTED_HASH = {1, {
    0xb1, 0x06, 0x23, 0x5e, 0x25, 0xa4, 0xc5, 0xed,
    0x35, 0x09, 0x8a, 0xa0, 0xa6, 0x1a, 0x3e, 0xe9,
    0xc9, 0xb1, 0x8d, 0x19, 0x7f, 0x39, 0x8b, 0x0e,
    0x42, 0x06, 0xce, 0xa9, 0xac, 0xf9, 0xc1, 0x97,
  }};
static const rosidl_type_hash_t geometry_msgs__msg__Point__EXPECTED_HASH = {1, {
    0x69, 0x63, 0x08, 0x48, 0x42, 0xa9, 0xb0, 0x44,
    0x94, 0xd6, 0xb2, 0x94, 0x1d, 0x11, 0x44, 0x47,
    0x08, 0xd8, 0x92, 0xda, 0x2f, 0x4b, 0x09, 0x84,
    0x3b, 0x9c, 0x43, 0xf4, 0x2a, 0x7f, 0x68, 0x81,
  }};
#endif

static char amr_msgs__msg__DetectedObstacle__TYPE_NAME[] = "amr_msgs/msg/DetectedObstacle";
static char builtin_interfaces__msg__Time__TYPE_NAME[] = "builtin_interfaces/msg/Time";
static char geometry_msgs__msg__Point__TYPE_NAME[] = "geometry_msgs/msg/Point";

// Define type names, field names, and default values
static char amr_msgs__msg__DetectedObstacle__FIELD_NAME__reporter_id[] = "reporter_id";
static char amr_msgs__msg__DetectedObstacle__FIELD_NAME__position[] = "position";
static char amr_msgs__msg__DetectedObstacle__FIELD_NAME__radius[] = "radius";
static char amr_msgs__msg__DetectedObstacle__FIELD_NAME__stamp[] = "stamp";
static char amr_msgs__msg__DetectedObstacle__FIELD_NAME__ttl[] = "ttl";

static rosidl_runtime_c__type_description__Field amr_msgs__msg__DetectedObstacle__FIELDS[] = {
  {
    {amr_msgs__msg__DetectedObstacle__FIELD_NAME__reporter_id, 11, 11},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {amr_msgs__msg__DetectedObstacle__FIELD_NAME__position, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {geometry_msgs__msg__Point__TYPE_NAME, 23, 23},
    },
    {NULL, 0, 0},
  },
  {
    {amr_msgs__msg__DetectedObstacle__FIELD_NAME__radius, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {amr_msgs__msg__DetectedObstacle__FIELD_NAME__stamp, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    },
    {NULL, 0, 0},
  },
  {
    {amr_msgs__msg__DetectedObstacle__FIELD_NAME__ttl, 3, 3},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription amr_msgs__msg__DetectedObstacle__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
  {
    {geometry_msgs__msg__Point__TYPE_NAME, 23, 23},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
amr_msgs__msg__DetectedObstacle__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {amr_msgs__msg__DetectedObstacle__TYPE_NAME, 29, 29},
      {amr_msgs__msg__DetectedObstacle__FIELDS, 5, 5},
    },
    {amr_msgs__msg__DetectedObstacle__REFERENCED_TYPE_DESCRIPTIONS, 2, 2},
  };
  if (!constructed) {
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&geometry_msgs__msg__Point__EXPECTED_HASH, geometry_msgs__msg__Point__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[1].fields = geometry_msgs__msg__Point__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "# Dynamic obstacle detected by a robot and relayed to peers\n"
  "string   reporter_id\n"
  "geometry_msgs/Point  position\n"
  "float64  radius\n"
  "builtin_interfaces/Time  stamp\n"
  "float64  ttl";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
amr_msgs__msg__DetectedObstacle__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {amr_msgs__msg__DetectedObstacle__TYPE_NAME, 29, 29},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 171, 171},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
amr_msgs__msg__DetectedObstacle__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[3];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 3, 3};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *amr_msgs__msg__DetectedObstacle__get_individual_type_description_source(NULL),
    sources[1] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[2] = *geometry_msgs__msg__Point__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}

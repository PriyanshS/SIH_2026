// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from amr_msgs:msg/ChokeRequest.idl
// generated code does not contain a copyright notice

#include "amr_msgs/msg/detail/choke_request__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_amr_msgs
const rosidl_type_hash_t *
amr_msgs__msg__ChokeRequest__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x9f, 0x0c, 0x1b, 0xc8, 0x6b, 0xfa, 0x42, 0x0c,
      0x6e, 0xf3, 0xd2, 0x6a, 0xa9, 0x0b, 0xc6, 0x4e,
      0x52, 0xe9, 0xc6, 0x45, 0x29, 0x67, 0x55, 0x74,
      0x9e, 0xff, 0x7d, 0x8a, 0xd6, 0xf2, 0x5e, 0x35,
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

static char amr_msgs__msg__ChokeRequest__TYPE_NAME[] = "amr_msgs/msg/ChokeRequest";
static char builtin_interfaces__msg__Time__TYPE_NAME[] = "builtin_interfaces/msg/Time";

// Define type names, field names, and default values
static char amr_msgs__msg__ChokeRequest__FIELD_NAME__robot_id[] = "robot_id";
static char amr_msgs__msg__ChokeRequest__FIELD_NAME__msg_type[] = "msg_type";
static char amr_msgs__msg__ChokeRequest__FIELD_NAME__priority[] = "priority";
static char amr_msgs__msg__ChokeRequest__FIELD_NAME__distance_to_choke[] = "distance_to_choke";
static char amr_msgs__msg__ChokeRequest__FIELD_NAME__reason[] = "reason";
static char amr_msgs__msg__ChokeRequest__FIELD_NAME__stamp[] = "stamp";

static rosidl_runtime_c__type_description__Field amr_msgs__msg__ChokeRequest__FIELDS[] = {
  {
    {amr_msgs__msg__ChokeRequest__FIELD_NAME__robot_id, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {amr_msgs__msg__ChokeRequest__FIELD_NAME__msg_type, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT8,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {amr_msgs__msg__ChokeRequest__FIELD_NAME__priority, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {amr_msgs__msg__ChokeRequest__FIELD_NAME__distance_to_choke, 17, 17},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {amr_msgs__msg__ChokeRequest__FIELD_NAME__reason, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {amr_msgs__msg__ChokeRequest__FIELD_NAME__stamp, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription amr_msgs__msg__ChokeRequest__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
amr_msgs__msg__ChokeRequest__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {amr_msgs__msg__ChokeRequest__TYPE_NAME, 25, 25},
      {amr_msgs__msg__ChokeRequest__FIELDS, 6, 6},
    },
    {amr_msgs__msg__ChokeRequest__REFERENCED_TYPE_DESCRIPTIONS, 1, 1},
  };
  if (!constructed) {
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "# Chokepoint negotiation protocol message\n"
  "string   robot_id\n"
  "uint8    msg_type\n"
  "uint32   priority\n"
  "float64  distance_to_choke\n"
  "string   reason        # human-readable yield reason e.g. \"yielding to robot2, lower priority\"\n"
  "builtin_interfaces/Time  stamp\n"
  "\n"
  "# msg_type constants\n"
  "uint8 REQUEST=0\n"
  "uint8 GRANT=1\n"
  "uint8 RELEASE=2\n"
  "uint8 HEARTBEAT=3";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
amr_msgs__msg__ChokeRequest__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {amr_msgs__msg__ChokeRequest__TYPE_NAME, 25, 25},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 335, 335},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
amr_msgs__msg__ChokeRequest__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[2];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 2, 2};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *amr_msgs__msg__ChokeRequest__get_individual_type_description_source(NULL),
    sources[1] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}

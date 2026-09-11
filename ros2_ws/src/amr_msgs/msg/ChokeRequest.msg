# Chokepoint negotiation protocol message
string   robot_id
uint8    msg_type
uint32   priority
float64  distance_to_choke
string   reason        # human-readable yield reason e.g. "yielding to robot2, lower priority"
builtin_interfaces/Time  stamp

# msg_type constants
uint8 REQUEST=0
uint8 GRANT=1
uint8 RELEASE=2
uint8 HEARTBEAT=3

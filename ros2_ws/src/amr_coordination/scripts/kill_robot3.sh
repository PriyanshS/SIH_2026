#!/usr/bin/env bash
# kill_robot3.sh — Terminates all robot3 coordination node processes.
#
# Use this during the "Live Kill-a-Robot" demo moment or as part of the
# robot_goes_silent.launch.py scenario.
#
# What the panel should see after running this:
#   - /choke_negotiation no longer shows robot3 HEARTBEATs
#   - robot1/robot2 print: "Peer robot3 heartbeat stale — treating choke as free"
#   - robot1 and robot2 continue their tasks unaffected
#
# Usage:
#   bash src/amr_coordination/scripts/kill_robot3.sh

set -euo pipefail

echo "[kill_robot3] Terminating all robot3 coordination nodes..."

NODES=(
    "robot3_choke_negotiator"
    "robot3_conflict_detector"
    "robot3_path_sharer"
    "robot3_obstacle_relay"
    "robot3_goal_sequencer"
)

for node in "${NODES[@]}"; do
    if ros2 node list | grep -q "/${node}"; then
        echo "[kill_robot3]   Killing: /${node}"
        # ros2 node kill is not standard — use pkill on the node executable
        pkill -f "choke_negotiator.*robot_id.*robot3"  2>/dev/null || true
        pkill -f "conflict_detector.*robot_id.*robot3" 2>/dev/null || true
        pkill -f "path_sharer.*robot_id.*robot3"       2>/dev/null || true
        pkill -f "obstacle_relay.*robot_id.*robot3"    2>/dev/null || true
        pkill -f "goal_sequencer.*robot_id.*robot3"    2>/dev/null || true
    else
        echo "[kill_robot3]   Node /${node} not found (may already be dead)"
    fi
done

# Alternative: kill all processes referencing robot3 namespace topics
# This is more aggressive and ensures nothing is left
pkill -f "robot3" 2>/dev/null || true

echo "[kill_robot3] Done. robot1 and robot2 should detect stale heartbeat within 3s."
echo "[kill_robot3] Watch: ros2 topic echo /choke_negotiation"

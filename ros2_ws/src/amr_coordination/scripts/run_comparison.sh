#!/bin/bash
# Run comparison between coordinated and baseline modes
# Usage: bash run_comparison.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WS_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"
RESULTS_DIR="$WS_DIR/results"

mkdir -p "$RESULTS_DIR"

echo "================================================"
echo "  Decentralized AMR Coordination - Comparison"
echo "================================================"
echo ""

# Source workspace
source "$WS_DIR/install/setup.bash"

echo "[1/2] Running COORDINATED mode..."
echo "     (This will launch Gazebo, Nav2, and coordination nodes)"
echo "     Waiting for all robots to complete..."
echo ""

timeout 180 ros2 launch amr_bringup full_demo.launch.py &
COORD_PID=$!

# Wait for completion or timeout
wait $COORD_PID 2>/dev/null || true

echo ""
echo "[2/2] Running BASELINE mode..."
echo "     (Same scenario with sequential stop-and-wait)"
echo ""

timeout 240 ros2 launch amr_bringup full_baseline.launch.py &
BASE_PID=$!

wait $BASE_PID 2>/dev/null || true

echo ""
echo "================================================"
echo "  Comparison complete!"
echo "  Results in: $RESULTS_DIR"
echo "================================================"

# Print results if available
if [ -f "$RESULTS_DIR/summary_coordinated.txt" ]; then
    echo ""
    cat "$RESULTS_DIR/summary_coordinated.txt"
fi
if [ -f "$RESULTS_DIR/summary_baseline.txt" ]; then
    echo ""
    cat "$RESULTS_DIR/summary_baseline.txt"
fi

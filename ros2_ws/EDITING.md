# Architecture & Design Decisions (EDITING.md)

This document maps the full architecture and documents every assumption and shortcut taken, for defending the design to a panel.

## System Architecture

### Package Dependency Graph

```
amr_bringup  ──► amr_gazebo     (Gazebo world, robot models)
             ──► amr_nav        (Nav2 config per robot)
             ──► amr_coordination (all Python coordination nodes)
             ──► amr_msgs       (custom ROS 2 messages)
```

### Node Map (per robot)

Each robot runs these nodes in its namespace:

| Node | File | Responsibility |
|------|------|---------------|
| `path_sharer` | `path_sharer.py` | Republish Nav2 plan to shared topic, store peer plans |
| `conflict_detector` | `conflict_detector.py` | Compare own plan vs. peers' for spatial-temporal overlap |
| `choke_negotiator` | `choke_negotiator.py` | REQUEST/GRANT/RELEASE protocol for chokepoint |
| `obstacle_relay` | `obstacle_relay.py` | Detect unexpected lidar returns, broadcast obstacles |
| `goal_sequencer` | `goal_sequencer.py` | Send waypoint sequence to Nav2, record timing |

Plus global fleet management nodes:

| Node | File | Responsibility |
|------|------|---------------|
| `metrics_logger` | `metrics_logger.py` | Collect timing events, print comparison |
| `goal_dispatcher` | `goal_dispatcher.py` | Assigns RViz clicks to nearest idle robot, manages queue |
| `send_goal` | `send_goal.py` | Interactive CLI for live dynamic custom goal injection |

### Communication Map

```
/shared_plans          ←  path_sharer × 3   →  conflict_detector × 3
/choke_negotiation     ←  choke_negotiator × 3  →  choke_negotiator × 3
/detected_obstacles    ←  obstacle_relay × 3 →  obstacle_relay × 3
/metrics              ←  goal_sequencer × 3  →  metrics_logger × 1
/clicked_point         ←  RViz Publish Point →  goal_dispatcher
/<ns>/plan            ←  Nav2 planner       →  path_sharer
/<ns>/scan            ←  Gazebo lidar       →  obstacle_relay + Nav2 costmap
/<ns>/cmd_vel         ←  Nav2 controller    →  Gazebo diff-drive
/<ns>/ground_truth_pose ← Gazebo pose pub   →  choke_negotiator, obstacle_relay, goal_sequencer
/<ns>/virtual_scan    ←  obstacle_relay     →  Nav2 local costmap
```

## Algorithms

### Conflict Detection
- Downsample both plans to ≤60 poses
- Assign elapsed time to each pose using distance/velocity
- Nested loop: flag if two robots will be within 0.8m at similar times (±3s window)
- Resolution: higher `robot_id` string yields (deterministic, no negotiation needed)
- Yielding = pause 3 seconds, then resume

### Chokepoint Negotiation (Token Protocol)
State machine: `IDLE → REQUESTING → GRANTED → IN_CHOKE → IDLE`

1. **IDLE**: Monitor distance to chokepoint centroid. If <3m and plan crosses choke → REQUEST
2. **REQUESTING**: Publish REQUEST at 2 Hz. If near choke boundary → stop robot via cmd_vel override
   - If higher-priority peer REQUESTs → reset grant timeout
   - On timeout (5s + priority×0.3s jitter) with no higher-priority contender → self-GRANT
3. **GRANTED**: Allow Nav2 to proceed. When inside polygon → IN_CHOKE
4. **IN_CHOKE**: Publish HEARTBEAT at 2 Hz. When outside polygon → RELEASE → IDLE

**Tie-breaking**: Lower priority number wins. Same priority → closer distance wins. Same distance → lower robot_id string wins.

**Crash handling**: If peer heartbeats go stale (>3s), assume they've exited/crashed, clear the choke.

### Obstacle Relay
1. Filter lidar returns to [0.3m, 3.0m] range
2. Transform to map frame using pose
3. Remove points matching known static map walls (occupancy grid lookup)
4. Cluster remaining points (greedy, eps=0.3m, min_size=3)
5. Broadcast cluster centroid + radius
6. Receiver creates a virtual LaserScan with hits at obstacle position → Nav2 costmap picks it up

## Assumptions & Shortcuts

### 1. Ground-Truth Localization (Simulating Industrial UWB)
**Active Strategy**: Robot absolute position comes directly from Gazebo's PosePublisher plugin via `/<ns>/ground_truth_pose`.
**Rationale**: 
- In modern automated warehouses, AMRs typically rely on Ultra-Wideband (UWB) infrastructure beacons or ceiling visual fiducials (AprilTags/QR grids) providing sub-decimeter global localization without scan-matching drift.
- Running online SLAM (e.g. `slam_toolbox`) or EKF sensor fusion in multi-robot simulation adds high CPU consumption, non-deterministic cold-start latency (15–30 s), and mapping distortions unrelated to the core problem.
- Ground-truth simulation matches the ideal, drift-free pose data that an industrial UWB tracking infrastructure provides, ensuring that coordination benchmarks purely measure decentralized arbitration efficiency.

### 2. Static Architectural Map (Nav2 map_server)
**Active Strategy**: The occupancy grid is loaded directly from `warehouse_map.yaml` by `nav2_map_server` for each robot namespace.
**Rationale**: Industrial facilities operate from CAD/architectural maps. Loading the pre-built map provides deterministic global costmaps, instantaneous initialization, and zero mapping artifacts across benchmark runs.

### 3. String Comparison for Priority (instead of consensus)
**Shortcut**: `robot1 < robot2 < robot3` → `robot1` always has highest priority.
**Why**: Deterministic, trivial to implement, and sufficient for 3 robots. No need for leader election overhead.
**To extend**: Use a Raft or Paxos-based priority rotation, or dynamic priority based on task urgency/battery level.

### 4. Camera Stub
**Shortcut**: Camera topic exists in the SDF but no detection logic processes the images.
**Why**: Object detection would require a trained model and adds significant complexity for marginal demo value.
**To extend**: Add a YOLO or MobileNet-SSD node subscribing to `/<ns>/camera/image_raw`.

### 5. Virtual Scan Injection (instead of custom costmap plugin)
**Shortcut**: Peer-reported obstacles are injected as virtual LaserScan messages that Nav2's obstacle_layer picks up.
**Why**: Writing a custom costmap plugin is time-consuming and fragile. Virtual scans leverage existing Nav2 infrastructure.
**To extend**: Write a custom costmap plugin that directly subscribes to `/detected_obstacles` and manages obstacle lifecycles.

### 6. Static TF for map→odom
**Active Strategy**: `map → <ns>/odom` is published by `static_transform_publisher` at each robot's spawn coordinate.
**Rationale**: Combined with Gazebo's differential drive odometry publishing `<ns>/odom → <ns>/base_link`, the TF tree (`map` → `<ns>/odom` → `<ns>/base_link` → `<ns>/lidar_link`) is consistent and drift-free.

### 7. Baseline Mode is Simplistic
**Shortcut**: Baseline uses fixed time delays (`(priority-1) * 10s`) instead of a real centralized coordinator.
**Why**: The goal is to show coordination is faster than a dumb sequential approach. A real centralized coordinator would be a separate system to implement.
**To extend**: Implement a central ROS 2 service that assigns time slots to robots.

## Known Limitations

1. **Three robots only**: Scaling beyond ~5 would require topic filtering or partitioned DDS domains.
2. **Single chokepoint**: Only one designated zone. Multiple chokepoints would need a per-zone negotiator.
3. **Fixed priority**: Robot1 always wins. Fair priority rotation is not implemented.
4. **No battery/energy modeling**: Robots never run out of charge.
5. **2D only**: No multi-floor warehouse support.
6. **No dynamic replanning from conflict_detector**: Conflict detector only pauses, doesn't trigger a full replan to find an alternate route.

## How to Modify

### Add a new robot
1. Add spawn position in `sim_world.launch.py`
2. Add waypoints in `waypoints.yaml`
3. Add Nav2 launch in `full_demo.launch.py`
4. Add coordination nodes in `coordination.launch.py`
5. Update `expected_robots` in metrics_logger

### Change the warehouse layout
1. Modify `warehouse.sdf` — add/remove walls and shelves
2. Regenerate `warehouse_map.pgm` to match
3. Update `chokepoint.yaml` polygon vertices

### Add a second chokepoint
1. Define a second polygon in `chokepoint.yaml`
2. Launch a second `choke_negotiator` per robot with the new polygon

### Switch to real localization
1. Remove `static_transform_publisher` for map→odom
2. Launch AMCL with the lidar scan
3. Change `ground_truth_pose` subscribers to use AMCL's `amcl_pose`

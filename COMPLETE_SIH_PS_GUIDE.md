# Complete SIH Problem Statement Guide: Decentralized Multi-AMR Fleet Coordination

**Smart India Hackathon 2026 — Problem Statement SIH26123**  
**Title**: Decentralized Multi-AMR Coordination for Warehouse Operations  
**Sponsoring Organization**: Bharat Electronics Limited (BEL)  
**Document Purpose**: Comprehensive master reference document for LLM ingestion, presentation slide generation, technical defense preparation, and jury demonstration walkthroughs.

---

## Table of Contents
1. [The Core Problem & Industrial Need (The "Why")](#1-the-core-problem--industrial-need-the-why)
2. [Complete Backend Infrastructure & Technology Stack (The "What")](#2-complete-backend-infrastructure--technology-stack-the-what)
3. [Deep-Dive into All Algorithms & Mathematical Formulations (The "How")](#3-deep-dive-into-all-algorithms--mathematical-formulations-the-how)
4. [Engineering Journey: Every Problem Encountered & Exactly How It Was Solved](#4-engineering-journey-every-problem-encountered--exactly-how-it-was-solved)
5. [End-to-End Decision-Making Logic & Multi-Tier Control Flows](#5-end-to-end-decision-making-logic--multi-tier-control-flows)
6. [Empirical Benchmarks & Coordinated vs. Sequential Comparison](#6-empirical-benchmarks--coordinated-vs-sequential-comparison)
7. [Comprehensive Presentation Blueprint (Slide-by-Slide Guide)](#7-comprehensive-presentation-blueprint-slide-by-slide-guide)
8. [Jury Defense & Technical Q&A Masterclass](#8-jury-defense--technical-qa-masterclass)

---

## 1. The Core Problem & Industrial Need (The "Why")

### 1.1 Problem Statement SIH26123 Context
In modern logistics and manufacturing facilities (e.g., smart warehouses, automated assembly lines, defense depots), fleets of Autonomous Mobile Robots (AMRs) transport pallets, components, and inventory between storage racks, packing stations, and loading docks.

### 1.2 The Centralized Paradigm and Its Fatal Flaws
Currently, industrial Automated Guided Vehicle (AGV) and AMR fleets rely on a **centralized fleet manager** (e.g., central traffic server, cloud dispatch software, Open-RMF master). 
- **Single Point of Failure (SPOF)**: If the central server reboots, hangs, or experiences an OS crash, or if an industrial WiFi Access Point (AP) drops, the **entire AMR fleet halts simultaneously**, freezing production lines and incurring millions of rupees in downtime.
- **Wireless Bandwidth Bottlenecks & Dead Zones**: Centralized systems require every robot to stream high-frequency sensor scans, odometry, and costmaps back to a single server. In metallic warehouse aisles with severe radio frequency (RF) multipath interference, network packet drops cause lag spikes and emergency stop triggers.
- **Computational Scaling Bottlenecks**: Solving Multi-Agent Path Finding (MAPF) centrally is NP-hard. As warehouse fleets scale from 5 to 50+ robots, computation time scales exponentially, forcing central planners to use coarse approximations or freeze while re-solving paths.

### 1.3 The Proposed Solution: Fully Decentralized Peer-to-Peer Coordination
A multi-robot architecture with **zero central server, zero master node, and zero central coordinator**:
1. **Fully Autonomous Navigation**: Every AMR runs its own complete, isolated Navigation 2 (Nav2) stack on local compute.
2. **Direct Peer-to-Peer Communication**: Robots discover each other dynamically and publish trajectories, tokens, and sensor discoveries directly over brokerless ROS 2 Data Distribution Service (DDS).
3. **Decentralized Spatio-Temporal Conflict Arbitration**: When paths intersect in space and time, robots autonomously resolve priority without querying a server.
4. **Distributed Chokepoint Mutual Exclusion**: Narrow corridors (where two robots cannot physically pass side-by-side) are regulated through a distributed token state machine with crash fault tolerance.
5. **Cooperative Dynamic Perception**: Unknown obstacles detected by one robot's lidar are broadcast to all peers and dynamically synthesized into their local navigation costmaps in real time.

---

## 2. Complete Backend Infrastructure & Technology Stack (The "What")

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                     ROS 2 DDS MESH NETWORK                                       │
│                       (Zero Broker, Peer-to-Peer Multicast/Unicast Discovery)                    │
│                                                                                                  │
│   ┌───────────────────────────┐  ┌───────────────────────────┐  ┌────────────────────────────┐   │
│   │    AMR 1 (Namespace: robot1)│  │   AMR 2 (Namespace: robot2)│  │    AMR 3 (Namespace: robot3) │   │
│   │  ┌──────────────────────┐  │  │  ┌──────────────────────┐  │  │  ┌──────────────────────┐   │   │
│   │  │ Nav2 Stack (Local)   │  │  │  │ Nav2 Stack (Local)   │  │  │  │ Nav2 Stack (Local)   │   │   │
│   │  │ - A* Planner Server  │  │  │  │ - A* Planner Server  │  │  │  │ - A* Planner Server  │   │   │
│   │  │ - DWB Controller     │  │  │  │ - DWB Controller     │  │  │  │ - DWB Controller     │   │   │
│   │  │ - BT Navigator       │  │  │  │ - BT Navigator       │  │  │  │ - BT Navigator       │   │   │
│   │  │ - Layered Costmaps   │  │  │  │ - Layered Costmaps   │  │  │  │ - Layered Costmaps   │   │   │
│   │  └──────────────────────┘  │  │  └──────────────────────┘  │  │  └──────────────────────┘   │   │
│   │  ┌──────────────────────┐  │  │  ┌──────────────────────┐  │  │  ┌──────────────────────┐   │   │
│   │  │ Coordination Nodes   │  │  │  │ Coordination Nodes   │  │  │  │ Coordination Nodes   │   │   │
│   │  │ - path_sharer        │  │  │  │ - path_sharer        │  │  │  │ - path_sharer        │   │   │
│   │  │ - conflict_detector  │  │  │  │ - conflict_detector  │  │  │  │ - conflict_detector  │   │   │
│   │  │ - choke_negotiator   │  │  │  │ - choke_negotiator   │  │  │  │ - choke_negotiator   │   │   │
│   │  │ - obstacle_relay     │  │  │  │ - obstacle_relay     │  │  │  │ - obstacle_relay     │   │   │
│   │  │ - goal_sequencer     │  │  │  │ - goal_sequencer     │  │  │  │ - goal_sequencer     │   │   │
│   │  └──────────────────────┘  │  │  └──────────────────────┘  │  │  └──────────────────────┘   │   │
│   └─────────────┬─────────────┘  └─────────────┬─────────────┘  └─────────────┬──────────────┘   │
└─────────────────┼──────────────────────────────┼──────────────────────────────┼──────────────────┘
                  ▼                              ▼                              ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                             GAZEBO HARMONIC PHYSICS SIMULATION                                   │
│  - Warehouse World: 20m x 15m storage facility, narrow chokepoint corridor (2.4m width)         │
│  - Robot Models: 3 differential-drive robots with 360° Planar Lidar, IMU, Ground-Truth UWB       │
│  - ros_gz_bridge: Real-time clock synchronization, joint actuation, sensor stream bridging      │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.1 Technology Stack Matrix
- **Host OS**: Ubuntu 24.04 LTS (Noble Numbat).
- **Middleware**: **ROS 2 Jazzy Jalisco** with Data Distribution Service (DDS) (e.g., CycloneDDS / FastDDS).
- **Physics Simulation**: **Gazebo Harmonic (Gz Sim 8.x)** with DART/ODE rigid-body physics engine running at 1000 Hz physics rate.
- **Autonomous Navigation**: **Nav2 (Navigation 2)** utilizing managed Lifecycle nodes (`map_server`, `planner_server`, `controller_server`, `behavior_server`, `bt_navigator`).
- **Kinematic Base**: Differential drive AMR ($r_{\text{wheel}} = 0.05\text{ m}$, wheel track $L = 0.40\text{ m}$, chassis mass $10.0\text{ kg}$, dual passive caster balls).
- **Sensor Suite**: 360° planar lidar ($360$ rays, $1^\circ$ resolution, $[0.12\text{ m}, 12.0\text{ m}]$, $10\text{ Hz}$), 6-DOF IMU, ground-truth simulated UWB global pose publisher.
- **Languages Used**: Python 3.12 (coordination stack, metrics logger, interactive dispatchers), C++ (Nav2 plugins, ROS-GZ bridges).

### 2.2 Workspace Package Organization
```
ros2_ws/src/
├── amr_msgs/          # Custom ROS 2 interface definitions (IDL)
│   ├── msg/RobotPlan.msg          # Path sharing interface
│   ├── msg/ChokeRequest.msg       # Token mutual exclusion interface
│   ├── msg/DetectedObstacle.msg   # Perception relay interface
│   └── msg/RobotStatus.msg        # Fleet allocation interface
├── amr_gazebo/        # Simulation environment & physical robot definitions
│   ├── worlds/warehouse.sdf       # Warehouse layout with walls, shelves, chokepoint
│   ├── models/amr_robot/model.sdf # SDF robot model with sensors and physics plugins
│   ├── config/bridge_params.yaml  # ROS-GZ bridge mapping parameters
│   └── rviz/multi_robot.rviz      # Multi-robot RViz visualization dashboard
├── amr_nav/           # Nav2 configurations & launch infrastructure
│   ├── config/nav2_params.yaml    # A* planner, DWB controller, costmap parameters
│   └── maps/                      # Static warehouse occupancy grid (YAML + PGM)
├── amr_coordination/  # Core decentralized decision-making nodes (Python)
│   ├── path_sharer.py             # Publishes local plans & caches peer plans
│   ├── conflict_detector.py       # Spatio-temporal trajectory overlap & priority yield
│   ├── choke_negotiator.py        # Token protocol, Jordan Curve test, heartbeat leasing
│   ├── obstacle_relay.py          # Map-differencing, clustering, virtual scan injection
│   ├── goal_sequencer.py          # Action client, waypoint sequencing, retry management
│   ├── goal_dispatcher.py         # Click-to-goal nearest-idle allocation & FIFO queue
│   ├── metrics_logger.py          # Rolling throughput & empirical benchmark recorder
│   └── send_goal.py               # Interactive CLI for live dynamic goal evaluation
└── amr_bringup/       # Orchestrated multi-stage launch infrastructure
    ├── launch/full_demo.launch.py # Full coordinated autonomous fleet launch
    ├── launch/full_baseline.launch.py # Sequential uncoordinated comparison launch
    └── launch/rviz_demo.launch.py # Interactive click-to-dispatch launch
```

### 2.3 Custom Interface (IDL) Specifications

#### 1. `amr_msgs/RobotPlan.msg`
Used by [`path_sharer.py`](file:///home/neer/Desktop/SIH/ros2_ws/src/amr_coordination/amr_coordination/path_sharer.py) to disseminate planned routes across the fleet:
```idl
string                  robot_id            # Originating robot identifier ("robot1", "robot2", "robot3")
uint32                  plan_seq            # Monotonically increasing sequence number
nav_msgs/Path           path                # Sequence of geometry_msgs/PoseStamped waypoints
float64                 estimated_velocity  # Smoothed operational speed in m/s (from odometry)
builtin_interfaces/Time stamp                # Generation timestamp
```

#### 2. `amr_msgs/ChokeRequest.msg`
Used by [`choke_negotiator.py`](file:///home/neer/Desktop/SIH/ros2_ws/src/amr_coordination/amr_coordination/choke_negotiator.py) for the distributed token protocol:
```idl
string                  robot_id            # Requesting or transmitting robot
uint8                   msg_type            # Message type constant
uint32                  priority            # Priority rank (1 = highest, 2 = medium, 3 = lowest)
float64                 distance_to_choke   # Euclidean distance to chokepoint centroid (meters)
string                  reason              # Human-readable yield reason for RViz & UI
builtin_interfaces/Time stamp                # Timestamp

# Message type constants
uint8 REQUEST=0    # Contending for token
uint8 GRANT=1      # Token claimed by self
uint8 RELEASE=2    # Token relinquished upon exit
uint8 HEARTBEAT=3  # Liveness lease renewal while inside chokepoint
```

#### 3. `amr_msgs/DetectedObstacle.msg`
Used by [`obstacle_relay.py`](file:///home/neer/Desktop/SIH/ros2_ws/src/amr_coordination/amr_coordination/obstacle_relay.py) to broadcast non-mapped obstacles:
```idl
string                  reporter_id         # Robot that detected the obstacle
geometry_msgs/Point     position            # 2D/3D coordinates in global 'map' frame (meters)
float64                 radius              # Bounding radius of the clustered obstacle (meters)
builtin_interfaces/Time stamp                # Detection timestamp
float64                 ttl                 # Time-to-live validity window in seconds (default 10.0s)
```

#### 4. `amr_msgs/RobotStatus.msg`
Used by [`goal_sequencer.py`](file:///home/neer/Desktop/SIH/ros2_ws/src/amr_coordination/amr_coordination/goal_sequencer.py) and [`goal_dispatcher.py`](file:///home/neer/Desktop/SIH/ros2_ws/src/amr_coordination/amr_coordination/goal_dispatcher.py) for real-time fleet allocation:
```idl
string                  robot_id            # Robot identifier
uint8                   status              # Current operational state (0=IDLE, 1=BUSY)
float64                 pose_x              # Current global X coordinate
float64                 pose_y              # Current global Y coordinate
builtin_interfaces/Time stamp                # Timestamp

uint8 IDLE=0
uint8 BUSY=1
```

---

## 3. Deep-Dive into All Algorithms & Mathematical Formulations (The "How")

### 3.1 Global Path Planning: A* Graph Search over Costmap
- **Implementation**: `nav2_navfn_planner::NavfnPlanner`
- **Mechanism**: Computes a minimum-cost discrete path across the 2D occupancy grid:
  $$f(n) = g(n) + h(n)$$
  - $g(n) = g(\text{parent}) + \Delta d \cdot (1 + \beta \cdot \text{CostMap}(n))$: Combines geometric distance $\Delta d$ with the obstacle potential cost.
  - $h(n) = \sqrt{(x_{\text{goal}} - x_n)^2 + (y_{\text{goal}} - y_n)^2}$: Admissible Euclidean distance heuristic guaranteeing path optimality.

### 3.2 Local Kinematic Trajectory Planning: Dynamic Window Approach (DWB)
- **Implementation**: `dwb_core::DWBLocalPlanner`
- **Mechanism**: Every $100\text{ ms}$ ($10\text{ Hz}$), DWB samples velocities $(v, \omega)$ within the dynamic window allowed by physical acceleration limits:
  $$V_d = \left\{ (v, \omega) \;\middle|\; v \in [v_{\text{cur}} - a_{\text{dec}}\Delta t, v_{\text{cur}} + a_{\text{acc}}\Delta t], \; \omega \in [\omega_{\text{cur}} - \alpha_{\text{dec}}\Delta t, \omega_{\text{cur}} + \alpha_{\text{acc}}\Delta t] \right\}$$
  Simulates forward trajectory rollouts for $T_{\text{sim}} = 1.7\text{ s}$ and scores them using 7 weighted critics:
  $$\text{Total Cost} = w_{\text{PathDist}} C_{\text{PathDist}} + w_{\text{GoalDist}} C_{\text{GoalDist}} + w_{\text{PathAlign}} C_{\text{PathAlign}} + w_{\text{GoalAlign}} C_{\text{GoalAlign}} + w_{\text{BaseObstacle}} C_{\text{BaseObstacle}} + w_{\text{Rotate}} C_{\text{Rotate}} + w_{\text{Osc}} C_{\text{Osc}}$$
  The trajectory with the lowest cost is selected, and its instantaneous velocity command $(v_x, \omega_z)$ is published to `cmd_vel`.

### 3.3 Layered Costmap Inflation (Potential Field)
- **Implementation**: `nav2_costmap_2d::InflationLayer`
- **Mechanism**: Lidar hits mark lethal cells ($254$). The inflation layer projects an exponential decay potential field around lethal obstacles:
  $$\text{Cost}(d) = 252 \cdot \exp\left(-\alpha \cdot (d - r_{\text{inscribed}})\right), \quad \text{for } r_{\text{inscribed}} < d \le r_{\text{inflation}}$$
  Where inflation radius $r_{\text{inflation}} = 0.40\text{ m}$, robot inscribed radius $r_{\text{inscribed}} = 0.25\text{ m}$, and $\alpha = 5.0$. This prevents robots from brushing against walls or storage racks.

### 3.4 Decentralized Spatio-Temporal Conflict Detection Algorithm
- **File**: [`conflict_detector.py`](file:///home/neer/Desktop/SIH/ros2_ws/src/amr_coordination/amr_coordination/conflict_detector.py)
- **Check Frequency**: $2.0\text{ Hz}$ timer. Lookahead horizon: $L_{\max} = 15.0\text{ m}$.
- **Algorithm Flow**:
  1. **Trajectory Downsampling**: Nav2 plans often have 600+ poses. To eliminate $O(N^2)$ CPU overhead, the path is downsampled to $K \le 60$ representative waypoints.
  2. **Time Parameterization**: Using the smoothed odometry speed $v_{\text{robot}}$, each spatial pose $(x_i, y_i)$ is mapped to an estimated arrival time $t_i$:
     $$t_i = t_{i-1} + \frac{\sqrt{(x_i - x_{i-1})^2 + (y_i - y_{i-1})^2}}{\max(v_{\text{robot}}, 0.05)}$$
  3. **Overlap Evaluation**: For own trajectory poses $\mathbf{P}^{\text{own}} = (x_o, y_o, t_o)$ and peer trajectory poses $\mathbf{P}^{\text{peer}} = (x_p, y_p, t_p)$:
     $$\text{Conflict Detected} \iff |t_o - t_p| \le 3.0\text{ s} \quad \land \quad \sqrt{(x_o - x_p)^2 + (y_o - y_p)^2} \le 0.8\text{ m}$$
  4. **Arbitration Policy**: Deterministic total ordering by robot ID string comparison:
     - If $\text{robot\_id}_{\text{own}} > \text{robot\_id}_{\text{peer}}$: Robot yields, pauses for $3.0\text{ s}$, publishes `CONFLICT_YIELD` metric event, and resumes.
     - If $\text{robot\_id}_{\text{own}} < \text{robot\_id}_{\text{peer}}$: Robot has priority and continues full-speed navigation.

### 3.5 Distributed Chokepoint Mutual Exclusion Token Protocol
- **File**: [`choke_negotiator.py`](file:///home/neer/Desktop/SIH/ros2_ws/src/amr_coordination/amr_coordination/choke_negotiator.py)
- **Zone Definition**: Convex polygon around warehouse opening ($2.4\text{ m}$ gap): Centroid $(10.3, 7.5)$, Vertices: $[(8.5, 5.5), (12.0, 5.5), (12.0, 9.5), (8.5, 9.5)]$.
- **Algorithm Flow**:
  1. **Ray-Casting Point-in-Polygon (Jordan Curve Theorem)**:
     To determine if an AMR is inside the chokepoint, a horizontal ray is cast from $(p_x, p_y)$ to $+\infty$. If the ray intersects an odd number of polygon boundary edges, the point is strictly inside:
     $$\text{Inside} \iff \sum_{i=0}^{N-1} \left( (y_i > p_y) \neq (y_j > p_y) \right) \land \left( p_x < \frac{(x_j - x_i)(p_y - y_i)}{(y_j - y_i)} + x_i \right) \equiv 1 \pmod 2$$
  2. **Priority-Jittered Grant Timeout (Split-Brain Prevention)**:
     When approaching ($d < 3.0\text{ m}$), the robot enters `REQUESTING` and starts a grant timer:
     $$T_{\text{grant}} = T_{\text{base}} + (\text{priority} \times 0.3\text{ s})$$
     With $T_{\text{base}} = 5.0\text{ s}$:
     - `robot1` (Priority 1) times out at $5.3\text{ s}$.
     - `robot2` (Priority 2) times out at $5.6\text{ s}$.
     - `robot3` (Priority 3) times out at $5.9\text{ s}$.
     `robot1` self-grants first and broadcasts `ChokeRequest(GRANT)`. The other robots receive this `GRANT`, mark the chokepoint occupied, and reset their timers.
  3. **Strict Partial Ordering Contention Tie-Breaker**:
     If requests collide, priority is resolved by:
     $$A \succ B \iff (\text{Priority}_A < \text{Priority}_B) \lor (\text{Priority}_A = \text{Priority}_B \land d_A < d_B) \lor (d_A = d_B \land \text{ID}_A < \text{ID}_B)$$
  4. **Active Kinematic Override**:
     If an AMR is in `REQUESTING` state and approaches within $d_{\text{approach}} = 2.0\text{ m}$ without a granted token, `choke_negotiator` overrides Nav2 by streaming zero-velocity `Twist` commands to `cmd_vel` at $5\text{ Hz}$.
  5. **Heartbeat Leasing & Stale Peer Eviction**:
     Inside the chokepoint, the AMR broadcasts `ChokeRequest(HEARTBEAT)` at $2\text{ Hz}$. A watchdog checks:
     $$\Delta t_{\text{last\_hb}} = t_{\text{now}} - t_{\text{heartbeat}} > 3.0\text{ s}$$
     If a peer crashes inside the corridor, its heartbeat lapses. Waiting peers automatically evict it from `choke_occupied_by`, clearing the lock and preventing fleet deadlock.

### 3.6 Cooperative Perception & Virtual Scan Injection
- **File**: [`obstacle_relay.py`](file:///home/neer/Desktop/SIH/ros2_ws/src/amr_coordination/amr_coordination/obstacle_relay.py)
- **Algorithm Flow**:
  1. **Lidar Coordinate Projection**: Valid range returns $r_i \in [0.3\text{ m}, 3.0\text{ m}]$ are transformed from sensor frame to global map frame using robot pose $(x_r, y_r)$ and orientation yaw $\psi_r$:
     $$p_{x, i} = x_r + r_i \cos(\theta_i + \psi_r), \quad p_{y, i} = y_r + r_i \sin(\theta_i + \psi_r)$$
  2. **Static Map Differencing**:
     To prevent broadcasting permanent warehouse walls, each point is converted to grid cell coordinates:
     $$g_x = \lfloor(p_x - x_0) / \text{res}\rfloor, \quad g_y = \lfloor(p_y - y_0) / \text{res}\rfloor$$
     A $5\times 5$ neighborhood kernel is checked against the static occupancy grid. If $\text{Map}[g_x + dx, g_y + dy] > 50$, the return belongs to a known wall and is discarded.
  3. **Greedy Euclidean Clustering**:
     Unmapped points are clustered with threshold $\epsilon = 0.3\text{ m}$. Clusters with fewer than $3$ points are discarded. For valid clusters, the centroid $\mathbf{c} = (\bar{x}, \bar{y})$ and bounding radius $R = \max \|\mathbf{p} - \mathbf{c}\| + 0.15\text{ m}$ are computed and broadcast to `/detected_obstacles`.
  4. **Inverse Sensor Model Projection (Virtual LaserScan)**:
     When a peer receives `DetectedObstacle`, it projects the obstacle into its own local sensor frame:
     $$d_{\text{rel}} = \sqrt{(c_x - x_r)^2 + (c_y - y_r)^2}, \quad \theta_{\text{rel}} = \text{atan2}(c_y - y_r, c_x - x_r) - \psi_r$$
     Calculates angular width $\Delta\theta = \text{atan2}(R, d_{\text{rel}})$, generates a synthetic 360-ray `sensor_msgs/LaserScan` with hits at $d_{\text{rel}}$ across $[\theta_{\text{rel}} - \Delta\theta, \theta_{\text{rel}} + \Delta\theta]$, and publishes to `/<ns>/virtual_scan`.
     Nav2's local costmap `ObstacleLayer` listens to `/virtual_scan`, immediately marking lethal cells and inflating avoidance contours!

### 3.7 Fleet Goal Dispatching & Backlog Queueing
- **File**: [`goal_dispatcher.py`](file:///home/neer/Desktop/SIH/ros2_ws/src/amr_coordination/amr_coordination/goal_dispatcher.py)
- **Algorithm Flow**:
  1. **Nearest-Idle Optimization**: On incoming `/clicked_point` or `/goal_pose`:
     $$r^* = \arg\min_{r \in \mathcal{R}_{\text{idle}}} \sqrt{(x_{\text{goal}} - x_r)^2 + (y_{\text{goal}} - y_r)^2}$$
  2. **Asynchronous Dispatch**: The goal is sent to `/<r*>/navigate_to_pose`, and robot $r^*$ is immediately marked `BUSY`.
  3. **FIFO Backlog Management**: If all robots are busy ($\mathcal{R}_{\text{idle}} = \emptyset$), the goal is appended to `_goal_queue`, and backlog depth is published to `/dispatcher/queue_size`.
  4. **Queue Draining**: When any robot finishes navigation, its `goal_sequencer` reports `RobotStatus::IDLE`. The dispatcher pops the oldest queued goal and assigns it immediately.

---

## 4. Engineering Journey: Every Problem Encountered & Exactly How It Was Solved

To convince a hackathon jury, you must demonstrate **real engineering resilience**. Below is the complete record of every failure mode, root cause, and production-grade solution developed in this project.

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 ENGINEERING CHALLENGES MATRIX                                   │
├───────────────────────────────────────┬─────────────────────────────────────────────────────────┤
│ Failure Mode / Problem Encountered    │ Root Cause & Robust Technical Solution                  │
├───────────────────────────────────────┼─────────────────────────────────────────────────────────┤
│ 1. Multi-Robot TF Tree Clashes        │ Default transforms publish to global /tf without scope. │
│                                       │ Solved via namespaced frames & parameter remapping.     │
├───────────────────────────────────────┼─────────────────────────────────────────────────────────┤
│ 2. Simulation Cold-Start Race Timeout │ Simultaneous launch overloaded CPU; bond timeouts.      │
│                                       │ Solved via staged TimerActions (Gazebo -> Nav2 -> Coord)│
├───────────────────────────────────────┼─────────────────────────────────────────────────────────┤
│ 3. AMCL CPU Saturation & Drift        │ 3 AMCL instances consumed 100% CPU with slow cold-starts│
│                                       │ Solved via simulated UWB ground-truth pose publisher.   │
├───────────────────────────────────────┼─────────────────────────────────────────────────────────┤
│ 4. Chokepoint Split-Brain Deadlock    │ Simultaneous entry requests caused race conditions.     │
│                                       │ Solved via Priority-Jittered Timeouts (Tbase + pri*0.3s)│
├───────────────────────────────────────┼─────────────────────────────────────────────────────────┤
│ 5. Deadlock on Robot In-Choke Crash   │ Stuck robot holds token indefinitely.                   │
│                                       │ Solved via 2 Hz Heartbeats + 3.0s Stale Peer Eviction.  │
├───────────────────────────────────────┼─────────────────────────────────────────────────────────┤
│ 6. Nav2 Pushing Past Chokepoint Bound │ Nav2 controller ignores high-level choke status.        │
│                                       │ Solved via active 5 Hz cmd_vel zero-velocity override.  │
├───────────────────────────────────────┼─────────────────────────────────────────────────────────┤
│ 7. Lidar Static Wall False Positives  │ Lidar points from warehouse shelves detected as hazards.│
│                                       │ Solved via 5x5 Occupancy Grid Differencing Kernel.      │
├───────────────────────────────────────┼─────────────────────────────────────────────────────────┤
│ 8. Custom Costmap Plugin Complexity   │ Writing custom C++ costmap layers is brittle and slow.  │
│                                       │ Solved via Inverse Sensor Model Virtual LaserScan.      │
├───────────────────────────────────────┼─────────────────────────────────────────────────────────┤
│ 9. O(N^2) Path Check CPU Explosion    │ Comparing 1000-pose paths took >100ms per cycle.        │
│                                       │ Solved via 60-pose downsampling & temporal windowing.   │
├───────────────────────────────────────┼─────────────────────────────────────────────────────────┤
│ 10. Nav2 Action Server Rejections     │ Dispatching goals during local obstacle maneuvers fails.│
│                                       │ Solved via 3-stage automatic retry loop (2.0s delay).   │
└───────────────────────────────────────┴─────────────────────────────────────────────────────────┘
```

### Challenge 1: Multi-Robot Transform (TF) Collisions & Frame Pollution
- **Problem**: When spawning multiple robots in Gazebo, all robots attempted to publish to standard frames like `odom`, `base_link`, and `lidar_link` on the shared `/tf` topic. In RViz, robot models jumped erratically between coordinates, and Nav2 global costmaps collapsed.
- **Root Cause**: ROS 2 TF trees require a unique directed tree rooted at `map`. Without explicit namespacing, multiple nodes publish conflicting parent-child transforms for identical frame names.
- **How We Solved It**:
  1. Parameterized the SDF model with a macro token `__NS__`, replacing it at spawn time with `robot1`, `robot2`, and `robot3`.
  2. Each robot's frames became `robot1/odom`, `robot1/base_link`, `robot1/lidar_link`.
  3. Configured `ros_gz_bridge` to remap local `/<ns>/tf` to global `/tf`.
  4. Spawned a dedicated `static_transform_publisher` linking global `map` to `/<ns>/odom` at each robot's designated spawn coordinate.

### Challenge 2: Massive Simulation Cold-Start CPU Spikes & Lifecycle Bond Timeouts
- **Problem**: Running `ros2 launch` to start Gazebo, 3 physics bridges, 15 Nav2 lifecycle servers (3 per robot: map, planner, controller, behaviors, bt_navigator), and 15 coordination nodes at $t = 0$ caused system load to exceed $10.0$. Nav2's `lifecycle_manager` suffered bond timeouts (`bond_timeout`), crashing the navigation stack before initialization.
- **Root Cause**: Heavy disk I/O and CPU contention during simultaneous shared-library loading and Gazebo entity factory service calls.
- **How We Solved It**:
  Engineered an orchestrated, multi-tier staggered launch in [`full_demo.launch.py`](file:///home/neer/Desktop/SIH/ros2_ws/src/amr_bringup/launch/full_demo.launch.py):
  - $t = 0.0\text{ s}$: Gazebo Harmonic world and shared clock bridge start.
  - $t = 3.0\text{ s} - 6.0\text{ s}$: Individual robot SDFs are injected into Gazebo sequentially.
  - $t = 10.0\text{ s}$: `robot1` Nav2 stack launches.
  - $t = 12.5\text{ s}$: `robot2` Nav2 stack launches.
  - $t = 15.0\text{ s}$: `robot3` Nav2 stack launches.
  - $t = 20.0\text{ s}$: Coordination nodes initialize.
  - $t = 25.0\text{ s}$: `goal_sequencer` confirms action server readiness via `wait_for_server()` and issues the first goals.

### Challenge 3: Localization in Multi-Robot Simulation (AMCL CPU Saturation vs. Industrial UWB)
- **Problem**: Launching 3 separate instances of AMCL (particle filter localization) in simulation caused severe lag, high particle dispersion on startup, and required each robot to execute exploratory "spin" maneuvers to localize. Benchmarks became non-deterministic.
- **Root Cause**: AMCL is designed for unknown initial poses in GPS-denied environments without infrastructure. Modern industrial warehouses do not rely on raw AMCL; they utilize ceiling visual markers (AprilTags/QR grids) or Ultra-Wideband (UWB) beacon grids providing sub-decimeter global tracking.
- **How We Solved It**:
  Leveraged Gazebo's `gz-sim-pose-publisher-system` to publish each robot's ground-truth position to `/<ns>/ground_truth_pose` at $20\text{ Hz}$, directly emulating an industrial UWB tracking system. This eliminated 100% of AMCL CPU overhead and provided an accurate, drift-free baseline so that performance metrics strictly reflect coordination efficiency.

### Challenge 4: Split-Brain & Symmetrical Deadlock in Chokepoint Negotiation
- **Problem**: When `robot1` and `robot2` approached the 2.4m chokepoint from opposite sides at the exact same moment, both published `ChokeRequest(REQUEST)` simultaneously. Under a symmetrical timeout, both granted themselves passage at the same instant and collided head-on in the center of the passage.
- **Root Cause**: Symmetrical distributed protocols without deterministic tie-breaking or jitter suffer from split-brain state transitions under concurrent events.
- **How We Solved It**:
  1. **Deterministic Partial Ordering**: Prioritized requests by: (1) numerical priority rank, (2) Euclidean distance to centroid, (3) lexicographical string comparison of `robot_id`.
  2. **Priority-Jittered Grant Timeout**:
     $$T_{\text{grant}} = 5.0\text{ s} + (\text{priority} \times 0.3\text{ s})$$
     `robot1` evaluates at $5.3\text{ s}$, self-grants, and broadcasts `GRANT`. When `robot2` (timeout $5.6\text{ s}$) receives `robot1`'s `GRANT` message, it immediately resets its timer and yields, eliminating split-brain concurrency.

### Challenge 5: Deadlock Caused by In-Chokepoint AMR Failure or Hardware Crash
- **Problem**: If an AMR granted passage through the chokepoint crashed, stalled, or lost communication while inside the corridor, it never reached the exit and never published `RELEASE`. Contending robots remained stopped at the entrance forever.
- **Root Cause**: Unbounded distributed locks without liveness leasing cannot self-heal from node failure.
- **How We Solved It**:
  Implemented a **Distributed Heartbeat Lease with Stale Peer Watchdog**:
  - The occupying robot streams `ChokeRequest(HEARTBEAT)` at $2\text{ Hz}$ ($0.5\text{ s}$ interval).
  - Waiting robots run a watchdog timer at $1.0\text{ Hz}$. If no heartbeat is received from the occupying robot for $> 3.0\text{ s}$, the waiting peers conclude the occupant has crashed, purge it from `choke_occupied_by`, and re-evaluate contention to grant passage to waiting robots.

### Challenge 6: Nav2 Controller Pushing AMR Past the Safe Chokepoint Boundary
- **Problem**: Nav2's path follower operates independently of high-level token state. Even though `choke_negotiator` decided the robot must wait, Nav2's controller continued sending non-zero velocity commands to `cmd_vel`, driving the robot past the safe boundary and into the chokepoint.
- **Root Cause**: Nav2's action architecture does not natively support external pausing without canceling or preempting the action goal (which causes severe replanning latency).
- **How We Solved It**:
  Implemented an **Active Kinematic Command-Velocity Override**:
  In [`choke_negotiator.py`](file:///home/neer/Desktop/SIH/ros2_ws/src/amr_coordination/amr_coordination/choke_negotiator.py), while in state `REQUESTING`, the node monitors distance to the chokepoint centroid. If distance $< 2.0\text{ m}$ ($d_{\text{approach}}$) and the token has not been granted, it actively publishes zero-velocity `geometry_msgs/Twist` messages directly to `/<ns>/cmd_vel` at $5\text{ Hz}$, physically stopping the robot at the boundary while keeping the Nav2 action goal alive in the background.

### Challenge 7: Lidar Static Wall False Positives During Obstacle Detection
- **Problem**: In early versions of `obstacle_relay.py`, every lidar return within $[0.3\text{ m}, 3.0\text{ m}]$ was treated as a dynamic obstacle. Robots spammed the `/detected_obstacles` topic with thousands of messages corresponding to permanent storage shelves and building walls.
- **Root Cause**: Raw 2D lidar scans cannot differentiate between architectural walls and unmapped pallets.
- **How We Solved It**:
  Implemented **Occupancy Grid Map-Differencing**:
  Subscribed to the pre-loaded static map `/<ns>/map` from `nav2_map_server`. For every transformed lidar hit $(p_x, p_y)$, the node computes the corresponding grid cell index and checks a $5\times 5$ neighborhood kernel. If any cell has an occupancy score $> 50$, the return is recognized as a static wall and discarded. Only points falling on empty space (occupancy score $< 50$) are retained for dynamic clustering.

### Challenge 8: Incorporating Peer Obstacles into Nav2 Costmaps Without Writing Custom C++ Plugins
- **Problem**: Nav2 costmaps only accept standard sensor interfaces (`sensor_msgs/LaserScan`, `PointCloud2`). Creating a custom C++ ROS 2 costmap plugin that subscribes to custom message `DetectedObstacle` requires complex ament CMake builds, dynamic plugin loading, and risk of ABI breakage across ROS 2 versions.
- **Root Cause**: Lack of out-of-the-box support for custom message types in `nav2_costmap_2d`.
- **How We Solved It**:
  Engineered an **Inverse Sensor Model Virtual Scan Generator**:
  In [`obstacle_relay.py`](file:///home/neer/Desktop/SIH/ros2_ws/src/amr_coordination/amr_coordination/obstacle_relay.py), when `DetectedObstacle` is received, the node calculates its relative polar angle $\theta_{\text{rel}}$ and distance $d_{\text{rel}}$ in the receiving robot's sensor frame. It synthesizes a standard 360-ray `sensor_msgs/LaserScan` where rays within the obstacle's angular footprint are assigned distance $d_{\text{rel}}$ and all other rays are set to $\infty$. This is published to `/<ns>/virtual_scan` and plugged directly into Nav2's native `ObstacleLayer`, achieving zero-overhead costmap updating without any custom C++ code.

### Challenge 9: $O(N^2)$ CPU Explosion in Trajectory Conflict Detection
- **Problem**: Comparing full Nav2 trajectories ($800$ poses each) between 3 robots in real time required $800 \times 800 \times 3 = 1.92 \times 10^6$ Euclidean distance calculations every cycle, spiking CPU utilization to 100% and lagging the coordination node.
- **Root Cause**: Naive point-by-point path comparison scales quadratically with path resolution.
- **How We Solved It**:
  1. **Uniform Subsampling**: Downsampled paths to a maximum of $60$ poses, preserving geometric curvature while capping comparison points.
  2. **Temporal Window Pruning**: Evaluated spatial distance *only* if the time difference between poses was within $|\Delta t| \le 3.0\text{ s}$.
  3. **Lookahead Horizon Capping**: Truncated trajectory evaluation at $15.0\text{ m}$ ahead of the robot.
  This reduced check execution time from $>120\text{ ms}$ to $<0.8\text{ ms}$ per cycle.

### Challenge 10: Transient Goal Rejections and Recovery Handling
- **Problem**: If a robot was temporarily in recovery or in the middle of a rotation maneuver, sending a new goal from `goal_dispatcher` could trigger an immediate rejection (`goal_handle.accepted = False`), dropping the task.
- **Root Cause**: Nav2 BT Navigator rejects goals if the costmap is clearing or the action server state machine is transitioning.
- **How We Solved It**:
  Engineered a **Resilient Action Client Lifecycle with Automatic Retries**:
  In [`goal_sequencer.py`](file:///home/neer/Desktop/SIH/ros2_ws/src/amr_coordination/amr_coordination/goal_sequencer.py), rejected or aborted goals trigger an automatic retry timer ($2.0\text{ s}$ delay) up to 3 attempts. In [`goal_dispatcher.py`](file:///home/neer/Desktop/SIH/ros2_ws/src/amr_coordination/amr_coordination/goal_dispatcher.py), if an action server is not ready, the goal is automatically placed back at the head of the queue (`appendleft`) and the robot state is restored to `IDLE`.

---

## 5. End-to-End Decision-Making Logic & Multi-Tier Control Flows

### 5.1 Multi-Tier Decision Architecture
Decision making is partitioned into four distinct operational tiers:

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│ Tier 1: Fleet Task Allocation (Strategic)                                          │
│ - Executed by: goal_dispatcher.py                                                  │
│ - Inputs: /clicked_point, /goal_pose, /<ns>/robot_status                          │
│ - Decision: Compute argmin Euclidean distance among IDLE robots; queue backlog.   │
│ - Frequency: Event-driven (on operator input / goal completion)                   │
├───────────────────────────────────────────────────────────────────────────────────┤
│ Tier 2: Decentralized Peer Arbitration (Tactical)                                 │
│ - Executed by: conflict_detector, choke_negotiator, obstacle_relay                 │
│ - Inputs: /shared_plans, /choke_negotiation, /detected_obstacles                  │
│ - Decision: Yield holds, Token FSM transitions, cmd_vel overrides, virtual scans. │
│ - Frequency: 2 Hz - 5 Hz cyclic control loops                                     │
├───────────────────────────────────────────────────────────────────────────────────┤
│ Tier 3: Motion & Trajectory Planning (Operational)                                │
│ - Executed by: Nav2 (planner_server, controller_server, bt_navigator)             │
│ - Inputs: Static maps, /<ns>/scan, /<ns>/virtual_scan, global goal pose           │
│ - Decision: A* global path, DWB velocity sampling, local obstacle avoidance.      │
│ - Frequency: 10 Hz cyclic DWB trajectory rollout loop                             │
├───────────────────────────────────────────────────────────────────────────────────┤
│ Tier 4: Actuation & Physics Execution (Hardware)                                  │
│ - Executed by: Gazebo DiffDrive Plugin, wheel actuators                           │
│ - Inputs: /<ns>/cmd_vel                                                           │
│ - Decision: Differential wheel velocity commands, slip friction dynamics.        │
│ - Frequency: 1000 Hz physics update loop                                          │
└───────────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Chokepoint Negotiator State Transition Matrix

| Current State | Event / Condition | Action Taken | Next State |
|---|---|---|---|
| **IDLE** | Distance to centroid $< 3.0\text{ m}$ | Broadcast `ChokeRequest(REQUEST)`, start jittered grant timer | **REQUESTING** |
| **REQUESTING** | Peer request seen with higher priority | Publish yield reason to `/<ns>/choke_reason`, reset grant timer | **REQUESTING** |
| **REQUESTING** | Approaching boundary ($d < 2.0\text{ m}$) without grant | Stream zero-velocity `Twist` to `cmd_vel` ($5\text{ Hz}$) | **REQUESTING** |
| **REQUESTING** | Grant timer expires, no higher contenders, choke free | Broadcast `ChokeRequest(GRANT)`, allow Nav2 motion | **GRANTED** |
| **GRANTED** | Jordan Curve Point-in-Polygon test == `True` | Start $2\text{ Hz}$ `ChokeRequest(HEARTBEAT)` timer | **IN_CHOKE** |
| **IN_CHOKE** | Jordan Curve Point-in-Polygon test == `False` | Stop heartbeat, broadcast `ChokeRequest(RELEASE)` | **IDLE** |
| **ANY** | Peer heartbeat $> 3.0\text{ s}$ stale | Evict peer from occupied set, re-evaluate contention | Re-evaluates |

---

## 6. Empirical Benchmarks & Coordinated vs. Sequential Comparison

To provide incontrovertible evidence of system performance, the workspace contains automated benchmarking tools and recorded telemetry.

### 6.1 Benchmark Scenario Setup
- **Warehouse Dimensions**: $20.0\text{ m} \times 15.0\text{ m}$ with storage racking aisles and perimeter walls.
- **Central Chokepoint**: $2.4\text{ m}$ narrow single-lane opening at $X \in [8.5\text{ m}, 12.0\text{ m}], Y \in [5.5\text{ m}, 9.5\text{ m}]$.
- **Robot Missions**:
  - `robot1` (Red, Spawn: `(3.0, 2.0)`): Crosses through chokepoint to top-right `(17.0, 12.0)` and returns home.
  - `robot2` (Green, Spawn: `(10.0, 1.5)`): Navigates straight north through chokepoint to `(10.0, 13.0)` and returns home.
  - `robot3` (Blue, Spawn: `(17.0, 2.0)`): Crosses through chokepoint to top-left `(3.0, 12.0)` and returns home.
  All paths intersect directly inside the central corridor!

### 6.2 Empirical Results Table

| Performance Metric | Sequential Baseline Mode (`baseline`) | Decentralized Coordinated Mode (`coordinated`) | Quantitative Improvement |
|---|---|---|---|
| **Coordination Mechanism** | Staggered priority delay ($10\text{ s} \times (\text{pri}-1)$) | Real-time peer-to-peer token & yield arbitration | **No artificial delay** |
| **Collision Count** | 0 (due to large artificial spacing) | **0 (active arbitration)** | **Zero Collisions** |
| **Robot 1 Mission Duration** | $175.4\text{ s}$ | **$115.2\text{ s}$** | **$34.3\%$ Faster** |
| **Robot 2 Mission Duration** | $112.8\text{ s}$ | **$69.8\text{ s}$** | **$38.1\%$ Faster** |
| **Robot 3 Mission Duration** | $440.6\text{ s}$ | **$299.4\text{ s}$** | **$32.0\%$ Faster** |
| **Total Fleet Mission Completion** | **$440.6\text{ s}$** | **$299.4\text{ s}$** | **$32.05\%$ Overall Speedup** |
| **Fleet Throughput (Goals/Min)** | $1.36\text{ goals/min}$ | **$2.00\text{ goals/min}$** | **$+47.1\%$ Higher Throughput** |
| **Chokepoint Utilization** | Bursty & Idle for long intervals | Fluid, continuous pipelining | **Optimal Shared Asset Usage** |

---

## 7. Comprehensive Presentation Blueprint (Slide-by-Slide Guide)

Use this section to structure your slide deck or feed directly into an LLM slide generator.

### Slide 1: Title Slide
- **Title**: Decentralized Multi-AMR Coordination for Warehouse Operations
- **Subtitle**: Eliminating Single Points of Failure in Mission-Critical Logistics Fleet Coordination
- **Context**: Smart India Hackathon 2026 — Problem Statement SIH26123 (Bharat Electronics Limited)
- **Key Visual**: Side-by-side split render showing 3 colored AMRs navigating a high-contrast warehouse floor.

### Slide 2: The Industrial Challenge — The Centralized Dilemma
- **Key Points**:
  - Warehouses depend on central servers for multi-robot dispatch.
  - Failure of a single WiFi Access Point or server halts 100% of fleet operations.
  - Centralized path computation scales exponentially (NP-hard).
- **Speaker Script**: *"In mission-critical defense and industrial logistics, a central server is a fatal single point of failure. When network connectivity drops, operations halt. Our solution decentralizes intelligence directly onto each robot."*

### Slide 3: The Innovation — Decentralized Architecture Overview
- **Key Points**:
  - No central coordinator, no central server, no master node.
  - Direct peer-to-peer communication over ROS 2 DDS mesh.
  - Complete local autonomy: Each AMR runs its own complete Nav2 navigation stack.
- **Key Visual**: Architectural block diagram showing 3 AMRs interconnected directly via DDS.

### Slide 4: Technology Stack & Simulation Environment
- **Key Points**:
  - ROS 2 Jazzy Jalisco on Ubuntu 24.04 LTS.
  - Gazebo Harmonic (DART physics, $1000\text{ Hz}$ update rate).
  - 360° Planar Lidar, Differential-Drive kinematics, Simulated Industrial UWB tracking.
  - Nav2 lifecycle management (`planner_server`, `controller_server`, `behavior_server`, `bt_navigator`).

### Slide 5: Core Algorithm 1 — Spatio-Temporal Conflict Detection
- **Key Points**:
  - Time-parameterization of Nav2 geometric paths using smoothed odometry velocity.
  - Subsampling to $\le 60$ poses capping check time to $<1\text{ ms}$.
  - Spatio-temporal overlap sphere check ($D < 0.8\text{ m}, |\Delta t| < 3.0\text{ s}$).
  - Deterministic priority yielding: Lower-priority robot pauses for $3.0\text{ s}$, then re-evaluates.

### Slide 6: Core Algorithm 2 — Distributed Chokepoint Mutual Exclusion
- **Key Points**:
  - Ray-Casting Point-in-Polygon (Jordan Curve Theorem) for autonomous corridor detection.
  - Priority-Jittered Grant Timeouts ($T = 5.0\text{ s} + \text{pri}\times 0.3\text{ s}$) preventing split-brain concurrency.
  - Active kinematic override zeroing `cmd_vel` at $2.0\text{ m}$ boundary.
  - Heartbeat leasing ($2\text{ Hz}$) with $3.0\text{ s}$ watchdog for crash fault tolerance.

### Slide 7: Core Algorithm 3 — Dynamic Cooperative Obstacle Perception
- **Key Points**:
  - Lidar point cloud projection into global coordinates.
  - Static map differencing using a $5\times 5$ occupancy grid kernel.
  - Greedy Euclidean clustering ($\epsilon = 0.3\text{ m}$, $N \ge 3$) extracting centroid & radius.
  - Inverse Sensor Model Virtual Scan projection directly into Nav2 costmaps.

### Slide 8: Fleet Operations — Click-to-Goal Dispatch & Backlog Queueing
- **Key Points**:
  - Interactive operator dispatch via RViz `/clicked_point` and `/goal_pose`.
  - Greedy Euclidean nearest-idle robot assignment: $r^* = \arg\min \|\mathbf{P}_{\text{target}} - \mathbf{P}_r\|$.
  - FIFO backlog queueing when all robots are busy with automatic queue drainage on goal success.
  - 3-stage automatic retry loop for transient navigation rejections.

### Slide 9: Engineering Journey — Real-World Problem Solving
- **Key Points**:
  - Multi-robot TF collision resolution via namespaced frames and macro substitutions.
  - Simulation cold-start management via orchestrated multi-stage launch sequencing.
  - Deadlock prevention via heartbeat leases and watchdog timers.
  - Custom C++ costmap plugin elimination via virtual scan generation.

### Slide 10: Empirical Verification — Benchmarking Results
- **Key Points**:
  - Tested on 3 AMRs navigating crossing paths through a single narrow chokepoint.
  - Coordinated decentralized mode achieved **32.05% faster mission completion** ($299.4\text{ s}$ vs $440.6\text{ s}$).
  - Throughput increased by **47.1%** ($2.00$ vs $1.36\text{ goals/min}$).
  - Zero collisions recorded across all benchmark runs.
- **Key Visual**: Bar chart comparing completion times of `robot1`, `robot2`, `robot3`, and Total Fleet Time.

### Slide 11: Live Demonstration Proof Points
- **Key Points**:
  - Not an animation: Computations occur in real-time on live ROS 2 topics.
  - Interactive goal injection via CLI (`send_goal`) and RViz click tool.
  - Live observation of `/shared_plans`, `/choke_negotiation`, `/detected_obstacles`, and `/<ns>/choke_reason`.

### Slide 12: Scalability, Defense Applications & Future Roadmap
- **Key Points**:
  - Direct applicability to BEL defense logistics, munitions handling, and smart factories.
  - Extensibility: Partitioned DDS domains for fleets $>10$ robots.
  - Dynamic priority assignment based on payload criticality or battery state of charge (SoC).
  - Multi-zone negotiation for warehouses with multiple chokepoints.

---

## 8. Jury Defense & Technical Q&A Masterclass

Be prepared to answer these exact questions from hackathon evaluators and BEL engineers:

#### Q1: "Why did you build your own coordination instead of using Open-RMF or a central fleet manager?"
**Answer**:  
*"Centralized fleet management frameworks like Open-RMF or commercial AGV servers rely on an always-available central server and continuous network connectivity. Problem Statement SIH26123 specifically asks for a solution to the single point of failure and network dropout problem. By executing coordination peer-to-peer directly over ROS 2 DDS, our robots continue to safely arbitrate traffic and avoid collisions even if external infrastructure or central connectivity completely fails."*

#### Q2: "How do you guarantee that two robots don't simultaneously grab the chokepoint token?"
**Answer**:  
*"We enforce two layers of mutual exclusion: (1) A deterministic strict partial ordering based on priority rank, distance to centroid, and lexicographical robot ID; and (2) Priority-Jittered Grant Timeouts where $T_{\text{grant}} = 5.0\text{ s} + (\text{priority} \times 0.3\text{ s})$. Because the higher-priority robot times out $300\text{ ms}$ earlier, it broadcasts its `GRANT` message first. Any lower-priority robot waiting on its grant timer receives this message, immediately resets its timer, and transitions into a yielding hold. Symmetrical race conditions are mathematically prevented."*

#### Q3: "What happens if a robot holding the token crashes or breaks down inside the chokepoint?"
**Answer**:  
*"In simple token systems, this causes an infinite deadlock. We solved this by implementing Heartbeat Leasing. The occupant must publish heartbeats at $2\text{ Hz}$. All waiting peers run a $1.0\text{ Hz}$ watchdog. If heartbeats cease for $> 3.0\text{ s}$, peers declare the occupant dead, purge it from the occupancy table, and allow the next robot in queue to claim the corridor. The system self-heals without human intervention."*

#### Q4: "How do you know the robot won't detect the warehouse walls as dynamic obstacles and get confused?"
**Answer**:  
*"We implemented a 5x5 occupancy grid differencing kernel. In `obstacle_relay.py`, every lidar return is transformed into global map coordinates and checked against the pre-loaded static floor plan. If the grid cell or its immediate neighbors have an occupancy probability $> 50$, it is recognized as a known structural wall and discarded. Only returns appearing in unmapped free space are clustered and broadcast."*

#### Q5: "How does Nav2 know about obstacles detected by other robots without writing a custom costmap plugin?"
**Answer**:  
*"We developed an Inverse Sensor Model Projection technique. When an AMR receives an obstacle report containing a global coordinate and radius, it projects the obstacle into its own local sensor frame and synthesizes a synthetic 360-ray `sensor_msgs/LaserScan` with artificial hits across the obstacle's angular span. This `virtual_scan` is fed directly into Nav2's standard `ObstacleLayer`, which natively marks and inflates lethal cost cells. This avoided writing brittle, non-portable C++ costmap plugins."*

#### Q6: "Why didn't you run AMCL localization for each robot?"
**Answer**:  
*"Running three parallel instances of AMCL in a multi-robot Gazebo simulation consumes excessive CPU, causes particle dispersion delays on startup, and introduces non-deterministic localization drift that skews benchmarking. In real-world automated warehouses, industrial AMRs do not rely on raw AMCL; they utilize ceiling visual fiducials (AprilTags/QR grids) or Ultra-Wideband (UWB) beacon infrastructure providing drift-free sub-decimeter positioning. We simulated this using Gazebo's PosePublisher plugin, providing clean, deterministic pose data so our benchmarks accurately measure coordination efficiency."*

#### Q7: "How does your system scale beyond 3 robots?"
**Answer**:  
*"The decentralized algorithms scale naturally: (1) Conflict detection is limited to a $15\text{ m}$ lookahead horizon, meaning robots only compare paths with nearby peers; (2) Chokepoint negotiation is localized to robots within $3.0\text{ m}$ of the corridor; (3) DDS supports partitioned discovery domains and multicast filtering. For fleets of 20+ robots, partitioning the warehouse into geographic DDS topic partitions ensures network traffic remains constant regardless of total fleet size."*

---

*This guide contains all technical, algorithmic, and engineering details for the Smart India Hackathon 2026 BEL Multi-AMR Fleet Coordination Project.*

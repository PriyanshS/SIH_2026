# Decentralized Multi-AMR Fleet Coordination for Warehouse Operations

**Smart India Hackathon 2026 — Problem Statement SIH26123**  
**Sponsoring Organization**: Bharat Electronics Limited (BEL)  
**Domain**: Autonomous Mobile Robots (AMRs), Distributed Robotics, Mission-Critical Logistics

---

## Executive Overview

Industrial Automated Guided Vehicle (AGV) and Autonomous Mobile Robot (AMR) fleets traditionally depend on a centralized fleet management server. This creates a catastrophic **Single Point of Failure (SPOF)**, suffers from severe RF multipath degradation in metallic warehouses, and faces computational intractability when centrally computing Multi-Agent Path Finding (MAPF).

This project implements a **fully decentralized, peer-to-peer (P2P) multi-AMR coordination system** with **zero central coordinator, zero master node, and zero external broker**:
- **Fully Autonomous Navigation**: Every AMR runs its own isolated Navigation 2 (Nav2) stack with local A* global search and DWB local controller.
- **Decentralized Spatio-Temporal Conflict Arbitration**: Trajectory envelopes ($\Delta t \le 3.0\,\text{s}, D \le 0.8\,\text{m}$) resolve crossing paths deterministically with mathematical deadlock-free guarantees.
- **Distributed Chokepoint Mutual Exclusion**: Single-lane passages are governed by a 4-state token protocol with Jordan Curve polygon containment, Raft-inspired priority-jittered grant timeouts, active kinematic command-velocity overrides, and 2 Hz heartbeat leasing with 3.0 s crash fault eviction.
- **Cooperative Dynamic Perception**: Non-mapped obstacles detected by one robot's 360° lidar are filtered against known architectural walls ($5\times 5$ occupancy kernel), clustered, and injected as synthetic virtual laser scans into peer costmaps without custom C++ plugins.
- **Interactive Web Fleet UI**: Real-time browser-based dashboard featuring an interactive 2D top-down warehouse map, click-to-dispatch, live KPI counters, chokepoint lock visualizer, and live P2P event logs.

---

## Repository Structure & Categorization

```
SIH_2026/
├── docs/                                  # Comprehensive Documentation
│   ├── guides/
│   │   ├── COMPLETE_SIH_PS_GUIDE.md       # Master SIH Problem Statement & Jury Defense Blueprint
│   │   ├── DECENTRALIZED_P2P_GUIDE.md     # Algorithmic theory, proofs & multi-laptop deployment
│   │   └── RUNNING_AND_DEMO_GUIDE.md      # Setup, commands & live presentation walkthroughs
│   ├── architecture/
│   │   ├── ALGORITHMS_AND_BACKEND.md      # Deep dive into all math, FSMs & control loops
│   │   └── SYSTEM_DESIGN_AND_DECISIONS.md # Engineering tradeoffs, assumptions & shortcuts
│   └── whitepaper/
│       └── DECENTRALIZED_MULTI_AMR_WHITE_PAPER.tex # Publication-grade LaTeX paper
├── web_ui/                                # Modern Web Fleet Dashboard & Bridge
│   ├── frontend/                          # HTML5 Canvas map, modern dark CSS, JavaScript client
│   │   ├── index.html
│   │   ├── style.css
│   │   └── app.js
│   └── backend/                           # Standalone launcher for the web bridge
│       └── web_bridge_node.py
└── ros2_ws/                               # Core ROS 2 Jazzy Workspace
    ├── src/
    │   ├── amr_bringup/                   # Multi-stage launch files & benchmark scenarios
    │   ├── amr_coordination/              # Core P2P Python coordination nodes & web bridge
    │   ├── amr_gazebo/                    # 20x15m warehouse SDF, robot models & RViz config
    │   ├── amr_msgs/                      # Custom ROS 2 IDLs (RobotPlan, ChokeRequest, etc.)
    │   └── amr_nav/                       # Namespaced Nav2 configurations & static maps
    └── README.md                          # ROS 2 workspace quickstart
```

---

## Documentation Quick Index

| Category | Document | Description |
| :--- | :--- | :--- |
| **Guides** | [`COMPLETE_SIH_PS_GUIDE.md`](docs/guides/COMPLETE_SIH_PS_GUIDE.md) | Master reference for LLM ingestion, slide deck generation, and jury defense Q&A. |
| **Guides** | [`DECENTRALIZED_P2P_GUIDE.md`](docs/guides/DECENTRALIZED_P2P_GUIDE.md) | Theoretical proofs, Chaos Testing, and 2–3 physical laptop deployment guide. |
| **Guides** | [`RUNNING_AND_DEMO_GUIDE.md`](docs/guides/RUNNING_AND_DEMO_GUIDE.md) | Step-by-step instructions for simulation, RViz dispatch, and CLI tools. |
| **Architecture** | [`ALGORITHMS_AND_BACKEND.md`](docs/architecture/ALGORITHMS_AND_BACKEND.md) | In-depth breakdown of all algorithms, equations, state machines, and QoS matrix. |
| **Architecture** | [`SYSTEM_DESIGN_AND_DECISIONS.md`](docs/architecture/SYSTEM_DESIGN_AND_DECISIONS.md) | Design rationale, pragmatic shortcuts (e.g. simulated UWB vs AMCL), and extensibility. |
| **White Paper** | [`DECENTRALIZED_MULTI_AMR_WHITE_PAPER.tex`](docs/whitepaper/DECENTRALIZED_MULTI_AMR_WHITE_PAPER.tex) | Complete academic white paper in LaTeX ready for Overleaf or local compilation. |

---

## Quickstart: Running the System

### 1. Prerequisites
- **Operating System**: Ubuntu 24.04 LTS
- **Middleware**: ROS 2 Jazzy Jalisco (`ros-jazzy-desktop`, Nav2, ros-gz-bridge)
- **Physics**: Gazebo Harmonic (`gz-harmonic`)

### 2. Build the Workspace
```bash
cd ros2_ws
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
source install/setup.bash
```

### 3. Launch Modes

#### Mode A: Full Coordinated Fleet + Interactive Web UI (Recommended)
Launches Gazebo Harmonic, 3 namespaced Nav2 stacks, all peer coordination nodes, and the real-time Web Dashboard:
```bash
ros2 launch amr_bringup web_demo.launch.py
```
Open **`http://localhost:8090`** in any browser (desktop, tablet, or smartphone) to view the live top-down map, monitor metrics, and click to dispatch AMRs!

#### Mode B: Full Coordinated Fleet + RViz Console
```bash
ros2 launch amr_bringup rviz_demo.launch.py
```

#### Mode C: Benchmark Comparison (Coordinated vs. Sequential Baseline)
```bash
bash ros2_ws/src/amr_coordination/scripts/run_comparison.sh
```

---

## Empirical Benchmark Results

| Metric | Sequential Baseline | Decentralized Coordinated Mode | Improvement |
| :--- | :--- | :--- | :--- |
| **Collision Count** | 0 (via artificial spacing) | **0 (active arbitration)** | **Zero Collisions** |
| **Fleet Mission Makespan** | $440.6\,\text{s}$ | **$299.4\,\text{s}$** | **$32.05\%$ Faster** |
| **Fleet Throughput** | $1.36\,\text{goals/min}$ | **$2.00\,\text{goals/min}$** | **$+47.1\%$ Higher** |
| **Crash Recovery** | Indefinite deadlock | Self-heals in **$3.0\,\text{s}$** via lease eviction | **Fault Tolerant** |

# Decentralized Multi-AMR Coordination for Warehouse Operations

**Smart India Hackathon 2026 — Problem Statement SIH26123**
**Bharat Electronics Ltd.**

## Problem

Warehouse Autonomous Mobile Robots (AMRs) currently depend on a central server for routing and coordination. When the network drops, the entire fleet stops. This creates a single point of failure that is unacceptable for mission-critical warehouse operations.

## Solution

A fully **decentralized** coordination system where robots communicate directly with each other — **no central server, no coordinator node**. Each robot:

1. Runs its own complete navigation stack (Nav2)
2. Shares its planned path with peers via ROS 2 topics
3. Detects and resolves path conflicts using priority-based arbitration
4. Negotiates passage through narrow chokepoints using a distributed token protocol
5. Relays dynamically detected obstacles to all peers in real-time

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    ROS 2 DDS Network                     │
│              (No Central Server/Coordinator)             │
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   Robot 1    │  │   Robot 2    │  │   Robot 3    │    │
│  │  ┌────────┐  │  │  ┌────────┐  │  │  ┌────────┐  │    │
│  │  │ Nav2   │  │  │  │ Nav2   │  │  │  │ Nav2   │  │    │
│  │  │ Stack  │  │  │  │ Stack  │  │  │  │ Stack  │  │    │
│  │  └────────┘  │  │  └────────┘  │  │  └────────┘  │    │
│  │  ┌────────┐  │  │  ┌────────┐  │  │  ┌────────┐  │    │
│  │  │Path    │◄─┼──┼─►│Path    │◄─┼──┼─►│Path    │  │    │
│  │  │Sharer  │  │  │  │Sharer  │  │  │  │Sharer  │  │    │
│  │  └────────┘  │  │  └────────┘  │  │  └────────┘  │    │
│  │  ┌────────┐  │  │  ┌────────┐  │  │  ┌────────┐  │    │
│  │  │Conflict│  │  │  │Conflict│  │  │  │Conflict│  │    │
│  │  │Detector│  │  │  │Detector│  │  │  │Detector│  │    │
│  │  └────────┘  │  │  └────────┘  │  │  └────────┘  │    │
│  │  ┌────────┐  │  │  ┌────────┐  │  │  ┌────────┐  │    │
│  │  │Choke   │◄─┼──┼─►│Choke   │◄─┼──┼─►│Choke   │  │    │
│  │  │Negot.  │  │  │  │Negot.  │  │  │  │Negot.  │  │    │
│  │  └────────┘  │  │  └────────┘  │  │  └────────┘  │    │
│  │  ┌────────┐  │  │  ┌────────┐  │  │  ┌────────┐  │    │
│  │  │Obstacle│◄─┼──┼─►│Obstacle│◄─┼──┼─►│Obstacle│  │    │
│  │  │Relay   │  │  │  │Relay   │  │  │  │Relay   │  │    │
│  │  └────────┘  │  │  └────────┘  │  │  └────────┘  │    │
│  └─────────────┘  └─────────────┘  └─────────────┘    │
└─────────────────────────────────────────────────────────┘
```

## Key Features

| Feature | Description |
|---------|-------------|
| **Decentralized** | No central server. Every robot is autonomous and coordinates via peer-to-peer ROS 2 topics. |
| **Path Sharing** | Each robot publishes its Nav2 plan. Peers subscribe and check for conflicts. |
| **Conflict Detection** | Spatial + temporal overlap detection with priority-based yielding. |
| **Chokepoint Negotiation** | REQUEST/GRANT/RELEASE token protocol for narrow passages with heartbeat-based crash detection. |
| **Dynamic Obstacle Relay** | Unknown obstacles detected by lidar are broadcast to peers who inject them into their costmaps. |
| **Metrics & Comparison** | Side-by-side comparison with a sequential baseline proves coordination efficiency. |

## Tech Stack

- **ROS 2 Jazzy** — Robot middleware
- **Gazebo Harmonic** — Physics simulation
- **Nav2** — Autonomous navigation
- **DDS** — Decentralized communication (no broker)

## Quick Start

See [RUNNING.md](RUNNING.md) for complete setup and run instructions.

## Demo Scenario

Three robots navigate deliberately crossing paths through a single narrow chokepoint:

1. **Coordinated Mode**: Robots negotiate passage using the distributed protocol. One passes at a time. Zero collisions.
2. **Baseline Mode**: Robots use simple sequential stop-and-wait. Significantly slower.

The metrics logger prints a hard comparison: coordinated mode typically achieves **30-40% faster completion** than the sequential baseline.

## Project Structure

```
ros2_ws/src/
├── amr_msgs/          # Custom ROS 2 messages (RobotPlan, DetectedObstacle, ChokeRequest)
├── amr_gazebo/        # Gazebo world, robot models, bridges
├── amr_nav/           # Nav2 configuration and per-robot nav launch
├── amr_coordination/  # All coordination nodes (Python)
└── amr_bringup/       # Top-level launch files
```

## Architecture & Technical Documentation

- See [ALGORITHMS_AND_BACKEND.md](ALGORITHMS_AND_BACKEND.md) for an in-depth breakdown of all algorithms, mathematical formulations, backend infrastructure, and decision-making logic.
- See [EDITING.md](EDITING.md) for detailed architecture, engineering assumptions, shortcuts, and extensibility notes.
- See [RUNNING.md](RUNNING.md) for setup, execution, RViz dispatching, and live demo instructions.

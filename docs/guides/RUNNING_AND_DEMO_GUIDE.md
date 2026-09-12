# Running the Decentralized AMR Demo

Step-by-step instructions for someone who has never used ROS 2.

## Prerequisites

### Operating System
- **Ubuntu 24.04 LTS** (required for ROS 2 Jazzy)

### Install ROS 2 Jazzy

Follow the official guide: https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html

Quick summary:
```bash
# Add ROS 2 apt repository
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
sudo apt update
sudo apt install ros-jazzy-desktop
```

### Install Gazebo Harmonic

```bash
sudo apt install gz-harmonic
```

### Install Nav2 and Dependencies

```bash
sudo apt install -y \
  ros-jazzy-nav2-bringup \
  ros-jazzy-nav2-bt-navigator \
  ros-jazzy-nav2-controller \
  ros-jazzy-nav2-planner \
  ros-jazzy-nav2-behaviors \
  ros-jazzy-nav2-costmap-2d \
  ros-jazzy-nav2-map-server \
  ros-jazzy-nav2-lifecycle-manager \
  ros-jazzy-nav2-msgs \
  ros-jazzy-ros-gz \
  ros-jazzy-ros-gz-bridge \
  ros-jazzy-ros-gz-sim \
  ros-jazzy-tf2-ros \
  ros-jazzy-tf2-geometry-msgs \
  python3-colcon-common-extensions
```

## Build the Project

```bash
# Source ROS 2
source /opt/ros/jazzy/setup.bash

# Navigate to workspace
cd ~/Desktop/SIH/ros2_ws

# Build all packages
colcon build --symlink-install

# Source the workspace
source install/setup.bash
```

If the build fails, try building packages individually:
```bash
colcon build --packages-select amr_msgs
colcon build --packages-select amr_gazebo amr_nav
colcon build --packages-select amr_coordination
colcon build --packages-select amr_bringup
source install/setup.bash
```

## Run the Coordinated Demo

This launches everything in one command: Gazebo simulation, Nav2 for all 3 robots, and all coordination nodes.

```bash
# 1. Clean up any previous simulator instances
pkill -9 -f "gz sim|ros2|nav2" || true

# 2. Navigate to the workspace and source ROS 2
cd /home/neer/Desktop/SIH/ros2_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash

# 3. Launch the simulation and coordination
ros2 launch amr_bringup full_demo.launch.py
```

**What to expect:**
1. Gazebo window opens with the warehouse and 3 colored robots (red `robot1`, green `robot2`, blue `robot3`)
2. At 10s–15s, Nav2 stacks initialize and activate for each robot with static map and ground-truth localization
3. At ~25 seconds, peer coordination nodes initialize and issue navigation goals
4. **All 3 robots start driving!**
5. Robot 2 drives straight through the central chokepoint, while Robot 1 and Robot 3 negotiate passage peer-to-peer
6. Terminal prints completion times when all robots finish their round trips

## Run the Baseline (Sequential) Demo

```bash
pkill -9 -f "gz sim|ros2|nav2" || true
cd /home/neer/Desktop/SIH/ros2_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch amr_bringup full_baseline.launch.py
```

**What to expect:**
- Same scenario but robots use staggered sequential navigation without peer coordination
- Total completion time is noticeably longer

## Visualize in RViz (Optional)

In a separate terminal:
```bash
cd /home/neer/Desktop/SIH/ros2_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
rviz2 -d src/amr_gazebo/rviz/multi_robot.rviz
```

## Custom Goal Setting & Live Presentation

To prove to evaluators that navigation is computed dynamically in real time (and **not a pre-made animation**), you can send live custom goals using three methods:

### Method 1: Interactive Goal Tool (Recommended for Presentations)

Open a new terminal while the simulation is running:
```bash
cd ~/Desktop/SIH/ros2_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash

# Interactive prompt (prompts you to select a robot and coordinates):
ros2 run amr_coordination send_goal

# Or pass coordinates directly on the command line:
ros2 run amr_coordination send_goal --robot robot1 --x 14.0 --y 8.0 --yaw 0.0
ros2 run amr_coordination send_goal --robot robot2 --x 5.0 --y 12.0
ros2 run amr_coordination send_goal --robot robot3 --x 16.0 --y 4.0
```
- **Warehouse Dimensions**: X: `1.0` to `19.0` m, Y: `1.0` to `14.0` m.
- **Central Chokepoint**: X: `9.0` to `11.0` m, Y: `6.0` to `8.5` m.
- You can command two robots to cross through the chokepoint in opposite directions. You will watch them actively detect the path intersection, communicate over DDS topics (`/shared_plans` and `/choke_negotiation`), yield by priority, and safely navigate.

### Method 2: Click-to-Goal via RViz (Live Interactive Dispatch)

In this mode, the robots start in **IDLE** state without running any pre-programmed waypoints. They stay parked at their starting positions until you click in RViz.

#### Option A: One-Command Launch (Sim + Nav2 + RViz)
Launch everything (Gazebo, all 3 Nav2 stacks, peer coordination, and RViz) in one terminal:
```bash
pkill -9 -f "gz sim|ros2|nav2" || true
cd ~/Desktop/SIH/ros2_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash

ros2 launch amr_bringup rviz_demo.launch.py
```
*(Alternatively: `ros2 launch amr_bringup full_demo.launch.py mode:=dispatcher rviz:=true`)*

#### Option B: Two-Terminal Launch
If you prefer running the simulation and RViz in separate windows:
- **Terminal 1 (Simulation & Nav2):**
  ```bash
  ros2 launch amr_bringup full_demo.launch.py mode:=dispatcher
  ```
- **Terminal 2 (RViz):**
  ```bash
  rviz2 -d src/amr_gazebo/rviz/multi_robot.rviz
  ```

#### What RViz Shows:
- **Warehouse Map**: High-contrast occupancy grid showing all external perimeter walls, storage aisles, and the central chokepoint corridor.
- **Robot Positions (Live Arrows & Footprints)**:
  - 🔴 **Robot 1 (Red)**: Spawned at `(3.0, 2.0)`
  - 🟢 **Robot 2 (Green)**: Spawned at `(10.0, 1.5)`
  - 🔵 **Robot 3 (Blue)**: Spawned at `(17.0, 2.0)`
- **Lidar Laser Scans**: Red, Green, and Blue points outlining obstacles and walls detected by each AMR's 360° lidar in real time.
- **Planned Paths**: Trajectory lines showing the global path each robot is actively following.
- **Top Toolbar Tools**:
  - **Publish Point**: Single-click goal assignment.
  - **2D Goal Pose**: Click and drag to specify target position + orientation heading.

#### How to Dispatch Robots in RViz:
1. **Using Publish Point (hotkey `p`):**
   - Click the **Publish Point** button in the RViz top toolbar (or press `p`).
   - Click anywhere on the warehouse floor (e.g., inside an aisle or near a corner).
   - `goal_dispatcher` instantly finds the nearest idle robot and commands it to drive to that spot.
2. **Using 2D Goal Pose (hotkey `g`):**
   - Click the **2D Goal Pose** tool in the RViz toolbar (or press `g`).
   - Click on the destination, drag in the direction you want the robot to face upon arrival, and release.
   - The nearest idle robot plans a path and navigates to the exact pose and heading.
3. **Queueing Multiple Dispatches:**
   - Click 3 or 4 points across the warehouse in rapid succession.
   - The dispatcher assigns the available robots first and queues the remaining points. As each robot reaches its goal, it transitions back to IDLE and automatically claims the next goal in the queue!

### Method 3: Customize Waypoints in Config File

If you want a different set of automated goals for the default demo:
1. Open [`src/amr_coordination/config/waypoints.yaml`](file:///home/neer/Desktop/SIH/ros2_ws/src/amr_coordination/config/waypoints.yaml)
2. Edit the coordinates for each robot:
   ```yaml
   robot1:
     spawn: [3.0, 2.0, 0.0]
     goals:
       - [17.0, 12.0, 0.0]    # goal 1: [X, Y, yaw_radians]
       - [3.0, 2.0, 0.0]      # return goal
   ```
3. Re-run `ros2 launch amr_bringup full_demo.launch.py`.

## Monitor Topics (Debugging)

```bash
# See all active topics
ros2 topic list

# Watch ground-truth poses (from Gazebo PosePublisher)
ros2 topic echo /robot1/ground_truth_pose

# Watch path sharing
ros2 topic echo /shared_plans

# Watch chokepoint negotiation
ros2 topic echo /choke_negotiation

# Watch obstacle broadcasts
ros2 topic echo /detected_obstacles

# Watch metrics events
ros2 topic echo /metrics

# Check a robot's laser scan
ros2 topic echo /robot1/scan --once

# Check TF tree
ros2 run tf2_tools view_frames
```

## Run Comparison Script

```bash
bash src/amr_coordination/scripts/run_comparison.sh
```

This runs both modes sequentially and prints the comparison results.

## Troubleshooting

### Gazebo doesn't open
- Make sure you have `gz-harmonic` installed
- Check: `gz sim --version` should show version 8.x

### Robots don't move
- Wait ~25 seconds after launch for Nav2 to initialize and coordination nodes to issue goals
- Check if Nav2 lifecycle nodes are active:
  ```bash
  ros2 lifecycle get /robot1/bt_navigator
  # Expected: active [3]
  ```
  Or check all managed servers:
  ```bash
  for n in map_server controller_server planner_server behavior_server bt_navigator; do echo -n "$n: "; ros2 lifecycle get /robot1/$n; done
  ```
  Or check a managed server's transition event:
  ```bash
  ros2 topic echo /robot1/controller_server/transition_event
  ```
  *(Note: In ROS 2 Nav2, `lifecycle_manager` is an orchestrator client that manages the servers; the managed servers publish the `/transition_event` topics, while the manager provides the `/robot1/lifecycle_manager/is_active` service).*
- Make sure `ROS_DOMAIN_ID` is the same (default 0) in all terminals
- Source both `/opt/ros/jazzy/setup.bash` and `install/setup.bash`

### TF errors
- Check TF tree: `ros2 run tf2_tools view_frames`
- Expected: `map` → `robot1/odom` → `robot1/base_link`

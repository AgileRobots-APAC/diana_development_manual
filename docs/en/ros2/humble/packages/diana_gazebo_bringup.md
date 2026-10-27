# `diana_gazebo_bringup`

## Installation

See [Development Setup](../development.md). Before using Gazebo simulation, also complete "Install Gazebo Simulation Dependencies (Optional)" there.

## Package Overview

`diana_gazebo_bringup` lives under the `diana_gazebo/` directory of the source tree and, together with `diana_gazebo_hardware`, forms the Gazebo simulation support of the Humble branch. It provides:

- `launch/`: two launch files, `visualize_diana_robot.launch.py` and `gazebo_diana_arm_example_controller.launch.py`.
- `config/`: controller configurations for the three robot types, `diana3_gazebo_controllers.yaml`, `diana7_gazebo_controllers.yaml` and `diana7g2_gazebo_controllers.yaml`.
- `urdf/`: `diana_arm.gazebo.xacro` (the Gazebo entry xacro).

The launch files start Gazebo through `ros_gz_sim` (Humble corresponds to Ignition Fortress), spawn the robot from the `/robot_description` topic with `ros_gz_sim create`, and start `robot_state_publisher`, the controllers and RViz. The robot model comes from the external package `diana_description`, imported through the `dependency.repos` file in the source tree, see [Development Setup](../development.md).

```{note}
Gazebo uses a simulated hardware interface, not the `diana_hardware` of the real robot. With `gazebo_effort` set to `true` the `diana_gazebo_hardware` plugin is used, see the section of the same name below.
```

```{figure} ../../../../_static/images/ros2-humble-gazebo-launch-en.png
:alt: Launch structure of the Gazebo simulation with an example controller
:width: 70%

What `gazebo_diana_arm_example_controller.launch.py` starts and how the parts relate.
```

## Usage

### Model Visualization

```bash
ros2 launch diana_gazebo_bringup visualize_diana_robot.launch.py robot_type:=diana7
```

This file starts Gazebo (`empty.sdf -r`, hard-coded in the file), `robot_state_publisher` (using `robots/<robot_type>/<robot_type>.urdf.xacro` of `diana_description` with `gazebo:=true`), spawns the robot, starts RViz (`rviz/visualize_diana.rviz` of `diana_description`, fixed frame `base_link`), activates `joint_state_broadcaster` with `ros2 control load_controller` after the spawn finishes, and starts `joint_state_publisher`. It loads no motion controller.

| Argument | Default | Description |
| --- | --- | --- |
| `robot_type` | Required | `diana3`, `diana7` or `diana7g2`, matching your robot |
| `namespace` | empty | Namespace of the spawn node and RViz |

### Simulation with an Example Controller

```bash
ros2 launch diana_gazebo_bringup gazebo_diana_arm_example_controller.launch.py robot_type:=diana7 controller:=joint_impedance_example_controller
```

| Argument | Default | Description |
| --- | --- | --- |
| `robot_type` | Required | `diana3`, `diana7` or `diana7g2`, matching your robot; selects `config/<robot_type>_gazebo_controllers.yaml` |
| `controller` | `gravity_compensation_example_controller` | Controller to start, taken from [diana_example_controllers](diana_example_controllers.md); it must be configured in the yaml described in the next section |
| `namespace` | empty | Namespace of the RViz node only |
| `gz_args` | `empty.sdf -r` | Gazebo arguments forwarded to `gz_sim.launch.py` |
| `rviz` | `true` | Whether to start RViz (fixed frame `world`) |

```{figure} ../../../../_static/images/ros2-humble-gazebo-diana7-joint-impedance.png
:alt: diana7 running the joint impedance example controller in Gazebo and RViz
:width: 100%

`diana7` running `joint_impedance_example_controller`: Gazebo (left) and RViz (right). The Gazebo entity tree shows `ground_plane`, `sun`, and `diana7`.
```

What this launch file does:

1. Sets `GZ_SIM_RESOURCE_PATH` (the parent directory of `diana_description` and this package's share directory) and starts Gazebo.
2. Generates and publishes the robot description from `urdf/diana_arm.gazebo.xacro` (`gazebo:=true`, `gazebo_effort:=true`).
3. After the robot is spawned, starts `joint_state_broadcaster` and the selected controller with the `controller_manager spawner`, using parameters from the matching yaml.
4. On shutdown, sends `SIGINT` to the `ruby` processes so Gazebo exits cleanly.

```{important}
`controller` must be a name registered in the yaml files above; `diana_robot_state_broadcaster`, the `*_move_to_start` controllers and others are not configured in them.
```

## Controller Configuration

`config/<robot_type>_gazebo_controllers.yaml` is loaded by the `gz_ros2_control` plugin in `diana_arm.gazebo.xacro` and by the spawner in the launch file. The three files share one structure, set the controller manager update rate to 1000 Hz and register these controllers:

| Controller name | Type |
| --- | --- |
| `joint_state_broadcaster` | `joint_state_broadcaster/JointStateBroadcaster` |
| `joint_position_example_controller` | `diana_example_controllers/JointPositionExampleController` |
| `joint_velocity_example_controller` | `diana_example_controllers/JointVelocityExampleController` |
| `joint_impedance_example_controller` | `diana_example_controllers/JointImpedanceExampleController` |
| `gravity_compensation_example_controller` | `diana_example_controllers/GravityCompensationExampleController` |
| `model_example_controller` | `diana_example_controllers/ModelExampleController` |

Differences between robot types:

- The `robot_type` parameter is set to `diana3`, `diana7` or `diana7g2` respectively (for `joint_position_example_controller`, `joint_velocity_example_controller`, `joint_impedance_example_controller` and `model_example_controller`); the position and velocity controllers additionally have `gazebo: true`, and `model_example_controller` has `arm_prefix: ''`.
- Stiffness and damping gains of `joint_impedance_example_controller` (joints 1 to 7):

| Robot type | `k_gains` | `d_gains` |
| --- | --- | --- |
| `diana3` | 24, 24, 24, 24, 10, 6, 2 | 2, 2, 2, 1, 1, 1, 0.5 |
| `diana7` | 48, 48, 48, 48, 20, 16, 12 | 4, 4, 4, 2, 2, 2, 1.5 |
| `diana7g2` | 48, 48, 48, 48, 20, 16, 12 | 4, 4, 4, 2, 2, 2, 1.5 |

## `diana_gazebo_hardware`

`diana_gazebo_hardware` is a `gz_ros2_control` system plugin with the class name `diana_gazebo_hardware/DianaGazeboHardwareInterface` (base class `gz_ros2_control::GazeboSimSystemInterface`, library `diana_gz_hardware_plugins`). It wraps the stock `gz_ros2_control/GazeboSimSystem`, forwards all joint and sensor logic to it, and adds:

- **Gravity compensation**: builds a `pinocchio` model from the URDF and adds the gravity torque to the torque (`effort`) commands in `write()`, so effort-controlled joints stay gravity-compensated in simulation.
- **Model and state interfaces**: exports the `robot_model` and `robot_state` state interfaces under `<prefix><robot_type>`, so model-based controllers (such as `model_example_controller`) can activate in simulation.
- **TCP force/torque interfaces**: exports six state interfaces under `<prefix><robot_type>_tcp`: `force.x`, `force.y`, `force.z`, `torque.x`, `torque.y`, `torque.z`, filled with an external wrench estimated from the measured-torque residual.
- **Cartesian pose interfaces**: exports 16 `<prefix><i>/cartesian_pose_state` state interfaces (the column-major 4x4 `O_T_EE`).

Command interfaces come unchanged from the wrapped system.

`diana_arm.gazebo.xacro` uses this plugin when `gazebo_effort` is `true` (the setting of `gazebo_diana_arm_example_controller.launch.py`), and `gz_ros2_control/GazeboSimSystem` otherwise.

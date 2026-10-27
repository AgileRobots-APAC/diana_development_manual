# Gazebo Simulation

Package name: `diana_gazebo_bringup`

## Installation

See [Development Setup](../development.md). Gazebo simulation also needs the runtime dependencies that `diana_gazebo_bringup` declares in its `package.xml`: `ros_gz`, `sdformat_urdf`, `joint_state_publisher_gui`, `gz_ros2_control`, `ros2controlcli`, plus `diana_gazebo_hardware`, `diana_description`, `franka_hardware` and `franka_example_controllers`. `rosdep install` installs the apt part of them.

## Package Overview

`diana_gazebo_bringup` lives under the `diana_gazebo/` directory of the source tree and, together with `diana_gazebo_hardware`, forms the Gazebo simulation support of the Jazzy branch. It provides:

- `launch/`: the launch files `diana.launch.py` (model visualization) and `diana.example_controller.launch.py` (simulation with an example controller).
- `config/controllers.yaml`: one controller configuration shared by all robot types.
- `urdf/`: the Gazebo entry xacro `diana.gazebo.urdf.xacro` and the `diana_gazebo_hardware_plugins.xacro` and `diana_gazebo_transmissions.xacro` it includes.
- `rviz/diana.visualize.rviz`: the RViz configuration.

The launch files start Gazebo Sim through `gz_sim.launch.py` of `ros_gz_sim`, spawn the robot from the `/robot_description` topic with `ros_gz_sim create`, bridge `/clock` with the `parameter_bridge` of `ros_gz_bridge`, and start `robot_state_publisher`, the controllers and RViz. The robot model comes from `diana_description`, imported through the `dependency.repos` file in the source tree, see [Development Setup](../development.md).

```{note}
Gazebo uses a simulated hardware interface, not the hardware interface of the real robot. With `gazebo_effort` set to `true` the `diana_gazebo_hardware` plugin is used, see the section of the same name below.
```

## Usage

### Model Visualization

```bash
ros2 launch diana_gazebo_bringup diana.launch.py robot_type:=diana7
```

This file starts Gazebo (`empty.sdf -r`, fixed in the file), `robot_state_publisher` (using `robots/<robot_type>/<robot_type>.urdf.xacro` of `diana_description` with `gazebo:=true`, `ros2_control:=true` and `connected_to:=world`), spawns the robot, starts RViz (`rviz/diana.visualize.rviz`, fixed frame `world`), activates `joint_state_broadcaster` with `ros2 control load_controller --set-state active joint_state_broadcaster` once the spawn process has exited, and starts `joint_state_publisher`. It loads no motion controller.

| Argument | Default | Description |
| --- | --- | --- |
| `robot_type` | `diana7` (pass explicitly) | `diana3`, `diana7` or `diana7g2`, matching your robot type |
| `namespace` | empty | Namespace of the spawn node, RViz and `joint_state_publisher` |

### Simulation with an Example Controller

```bash
ros2 launch diana_gazebo_bringup diana.example_controller.launch.py robot_type:=diana7 controller:=joint_impedance_example_controller
```

| Argument | Default | Description |
| --- | --- | --- |
| `robot_type` | `diana7` (pass explicitly) | `diana3`, `diana7` or `diana7g2`, matching your robot type |
| `controller` | `gravity_compensation_example_controller` | Name of the controller to start, taken from [franka_example_controllers](franka_example_controllers.md); it must be configured in `controllers.yaml` (next section) |
| `namespace` | empty | Namespace of the spawn node and RViz |
| `gz_args` | `-r empty.sdf` | Gazebo arguments forwarded to `gz_sim.launch.py` |
| `rviz` | `true` | Whether to start RViz (fixed frame `world`) |
| `gazebo_effort` | `true` | Whether to add `effort` to the command interfaces; when `true` the `diana_gazebo_hardware` plugin is used |

What this launch file does:

1. Sets `GZ_SIM_RESOURCE_PATH` (the parent of the directory that holds `diana_description`) and starts Gazebo.
2. Generates and publishes the robot description from `urdf/diana.gazebo.urdf.xacro` (passing `robot_type` and `gazebo_effort`).
3. Once the spawn process has exited, starts `joint_state_broadcaster` and the selected controller with `controller_manager spawner`, with parameters taken from `config/controllers.yaml`.

```{important}
`controller` must be a name registered in `controllers.yaml`, see the next section.
```

## Controller Configuration

`config/controllers.yaml` is loaded by the `gz_ros2_control` plugin in `diana_gazebo_hardware_plugins.xacro` and by the spawner in the launch file; all robot types share this one file. The controller manager update rate is 1000 Hz. The controllers in the file that are relevant to single-arm simulation are (types come from [franka_example_controllers](franka_example_controllers.md) and `joint_state_broadcaster`):

| Controller name | Type |
| --- | --- |
| `joint_state_broadcaster` | `joint_state_broadcaster/JointStateBroadcaster` |
| `joint_position_example_controller` | `franka_example_controllers/JointPositionExampleController` |
| `joint_velocity_example_controller` | `franka_example_controllers/JointVelocityExampleController` |
| `joint_impedance_example_controller` | `franka_example_controllers/JointImpedanceExampleController` |
| `gravity_compensation_example_controller` | `franka_example_controllers/GravityCompensationExampleController` |
| `model_example_controller` | `franka_example_controllers/ModelExampleController` |
| `cartesian_impedance_example_controller` | `franka_example_controllers/CartesianImpedanceExampleController` |
| `move_to_start_example_controller` | `franka_example_controllers/MoveToStartExampleController` |
| `franka_robot_state_broadcaster` | `franka_robot_state_broadcaster/FrankaRobotStateBroadcaster` |

`joint_position_example_controller` and `joint_velocity_example_controller` have their parameter `gazebo` set to `true`.

## `diana_gazebo_hardware`

`diana_gazebo_hardware` is a `gz_ros2_control` system plugin with the class name `diana_gazebo_hardware/DianaGazeboHardwareInterface` (base class `gz_ros2_control::GazeboSimSystemInterface`, library `diana_gz_hardware_plugins`). It wraps the stock `gz_ros2_control/GazeboSimSystem`, forwards all joint and sensor logic to it, and adds:

- **Gravity compensation**: based on the robot model (built with `pinocchio`), `write()` adds the gravity torque to the torque (`effort`) commands, so torque-controlled joints stay gravity-compensated in simulation.
- **Model and state interfaces**: exports the `robot_model` and `robot_state` state interfaces under `<prefix><robot_type>`, so model-dependent controllers (such as `model_example_controller`) can be activated in simulation. The model is generated from `robots/<robot_type>/<robot_type>.urdf.xacro` of `diana_description`.
- **TCP force/torque interfaces**: exports the six state interfaces `force.x`, `force.y`, `force.z`, `torque.x`, `torque.y`, `torque.z` under `<prefix><robot_type>_tcp`, with data from the external force estimated from the measured torque residual.
- **Cartesian pose interfaces**: exports 16 state interfaces `<prefix><i>/cartesian_pose_state` (the column-major 4x4 `O_T_EE`).

The command interfaces come unchanged from the wrapped system.

`diana.gazebo.urdf.xacro` uses this plugin when `gazebo_effort` is `true` (the default of `diana.example_controller.launch.py`) and `gz_ros2_control/GazeboSimSystem` otherwise.

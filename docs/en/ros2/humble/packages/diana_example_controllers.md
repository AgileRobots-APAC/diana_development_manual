# `diana_example_controllers`

`diana_example_controllers` is a set of `ros2_control` example controller plugins that show how to implement joint, Cartesian, and elbow control on the Diana hardware interface, and how to read the robot model. They are meant for learning and reference, not as production controllers.

## Installation

See [Development Setup](../development.md).

## Package Overview

The package builds a single controller plugin library, `diana_example_controllers`. Plugin types are registered in `diana_example_controllers.xml`, with `controller_interface::ControllerInterface` as the base class. Controller names, their types, the update rate, and the gain parameters are all provided by `config/controllers.yaml` of [diana_bringup](diana_bringup.md): the controller manager's `update_rate` is `1000` (Hz) and `thread_priority` is `98`.

The examples access the Cartesian pose, Cartesian velocity, and robot model interfaces through `diana_semantic_components`, and call the parameter services of `diana_hardware` through `diana_msgs`. They depend on `pinocchio`; the joint-impedance IK example also depends on MoveIt.

## Example Controllers

Every example is started the same way. Replace the name with one from the sections below (written as `controller_names:=...` on the command line):

```bash
ros2 launch diana_bringup example.launch.py controller_names:=gravity_compensation_example_controller
```

For the arguments, namespace, and multi-robot usage of `example.launch.py`, see [diana_bringup](diana_bringup.md). The launch file reads the robot configuration from `diana.config.yaml`; before running, change its `robot_type` to your own model (`diana3`, `diana7`, or `diana7g2`).

```{warning}
Except for `model_example_controller`, these controllers send torque, velocity, or position commands to the robot, and the arm really moves. Before running one, make sure the workspace is clear of people and obstacles, the emergency stop is reachable, and the robot is in a state that allows external control. Read [Safety Boundaries](../../../reference/safety.md) first; for FCI and network prerequisites see the [FCI overview](../../../fci/overview.md). Start from a conservative pose for the first run and be ready to press the emergency stop at any time.
```

```{note}
According to the header comment of `example.launch.py`, the elbow and Cartesian examples call services (for example `set_full_collision_behavior`) and use interfaces such as `robot_time` and `elbow_state`, which only the real `diana_hardware` provides. They need `use_fake_hardware` set to `"false"` and a reachable robot. With `mock_components` simulated hardware, the comment recommends the joint-level examples (`gravity_compensation_example_controller`, `joint_impedance_example_controller`). Unless stated otherwise below, treat an example as requiring real hardware.
```

```{note}
The sources of `cartesian_*`, `joint_impedance_*`, and others live under `src/diana3/`, but apart from the `*_move_to_start_example_controller` ones the code does not check the robot model. They are written for 7 joints, and the robot name comes from `robot_description` (or from the `robot_type` parameter passed by the launch file).
```

The table below summarizes all example controllers; each controller is described in detail in the sections that follow:

| Example controller | Description | Needs real hardware |
|---|---|---|
| <a href="#gravity-compensation-example-controller"><code>gravity_compensation_example_controller</code></a> | Zero-torque gravity-compensated hover; prints the external force estimate | No (runs on fake hardware) |
| <a href="#joint-impedance-example-controller"><code>joint_impedance_example_controller</code></a> | Joint impedance law; joints 4 and 5 move slowly and periodically | No (runs on fake hardware) |
| <a href="#joint-impedance-with-ik-example-controller"><code>joint_impedance_with_ik_example_controller</code></a> | Solves IK through MoveIt `compute_ik`; the end effector traces an arc in x and z | Yes |
| <a href="#joint-position-example-controller"><code>joint_position_example_controller</code></a> | Joint position commands with a periodic offset | Yes |
| <a href="#joint-velocity-example-controller"><code>joint_velocity_example_controller</code></a> | Joint velocity commands; joints 4 and 5 move back and forth | Yes |
| <a href="#cartesian-velocity-example-controller"><code>cartesian_velocity_example_controller</code></a> | Cartesian velocity commands; back-and-forth motion in x and z | Yes |
| <a href="#cartesian-pose-example-controller"><code>cartesian_pose_example_controller</code></a> | Cartesian pose commands; an arc in x and z | Yes |
| <a href="#cartesian-orientation-example-controller"><code>cartesian_orientation_example_controller</code></a> | Cartesian pose commands; periodic rotation about the x axis | Yes |
| <a href="#cartesian-elbow-example-controller"><code>cartesian_elbow_example_controller</code></a> | Holds the end-effector pose while the elbow (null space) varies periodically | Yes |
| <a href="#elbow-example-controller"><code>elbow_example_controller</code></a> | Moves only the elbow (null space) in velocity mode | Yes |
| <a href="#model-example-controller"><code>model_example_controller</code></a> | Reads and prints the robot model; sends no commands | Yes (needs the model interface) |
| <a href="#diana3-move-to-start-example-controller"><code>diana3_move_to_start_example_controller</code></a> | Smoothly moves to a start joint configuration; `diana3` only | Yes |
| <a href="#diana7-move-to-start-example-controller"><code>diana7_move_to_start_example_controller</code></a> | Smoothly moves to a start joint configuration; `diana7` only | Yes |
| <a href="#diana7g2-move-to-start-example-controller"><code>diana7g2_move_to_start_example_controller</code></a> | Smoothly moves to a start joint configuration; `diana7g2` only | Yes |

### `gravity_compensation_example_controller`

Writes zero torque to the `effort` interfaces of all 7 joints so that the robot's internal gravity compensation holds it in place (the arm can be pushed by hand), and logs the estimated external force and torque in the stiffness frame every 100 control cycles. It needs the `<robot_type>_tcp` force/torque sensor state interfaces.

```bash
ros2 launch diana_bringup example.launch.py controller_names:=gravity_compensation_example_controller
```

```{warning}
The arm is in zero-torque mode and does not actively hold its position; it moves when force is applied. Support the arm and its payload first, and keep a hand within reach of the emergency stop.
```

### `joint_impedance_example_controller`

Outputs torque with a joint impedance law so that joints 4 and 5 perform a slow periodic motion of about π/8 rad amplitude while the other joints stay at their initial positions. `k_gains` and `d_gains` (7 values each) are read from `controllers.yaml`; the defaults are `50, 50, 50, 50, 20, 10, 5` for `k_gains` and `4, 4, 4, 2, 2, 2, 1` for `d_gains`, which is quite compliant.

```bash
ros2 launch diana_bringup example.launch.py controller_names:=joint_impedance_example_controller
```

```{warning}
This controller outputs torque and moves the arm. Make sure the motion range of joints 4 and 5 is free of obstacles.
```

### `joint_impedance_with_ik_example_controller`

Moves the end effector along a small circular arc of radius 0.1 m in x and z, solves inverse kinematics through the MoveIt `compute_ik` service (OrocosKDL LMA), and outputs torque with a joint impedance law plus Coriolis compensation. The default gains are in `controllers.yaml`: `k_gains` is `600, 600, 600, 600, 250, 150, 50` and `d_gains` is `30, 30, 30, 30, 10, 10, 5`. It needs the `compute_ik` and `set_full_collision_behavior` services, so use the dedicated launch file, which also starts MoveIt:

```bash
ros2 launch diana_bringup joint_impedance_with_ik_example_controller.launch.py
```

```{warning}
This controller outputs torque and moves the arm in Cartesian space. It needs real hardware and a working `compute_ik` service. For the launch file details and prerequisites see [diana_bringup](diana_bringup.md).
```

### `joint_position_example_controller`

Writes position commands to the `position` interfaces of all 7 joints: a slow periodic offset is added to the initial position, with joints 4 and 5 offset in the opposite direction from the others. It keeps time with the `robot_time` state interface; the parameter `gazebo` (default `false`) is for Gazebo simulation, where the control period is used for timing instead.

```bash
ros2 launch diana_bringup example.launch.py controller_names:=joint_position_example_controller
```

```{warning}
This controller moves all joints at the same time. Make sure the entire workspace is free of obstacles.
```

### `joint_velocity_example_controller`

Writes velocity commands to the `velocity` interfaces of all 7 joints: joints 4 and 5 move in opposite directions with a back-and-forth angular velocity of at most 0.1 rad/s and a period of 8 seconds, while the other joints have zero velocity. The `gazebo` parameter (default `false`) is the same as in the position example.

```bash
ros2 launch diana_bringup example.launch.py controller_names:=joint_velocity_example_controller
```

```{warning}
This controller moves the arm through the velocity interface. Make sure the motion range of joints 4 and 5 is free of obstacles.
```

### `cartesian_velocity_example_controller`

Commands a linear velocity in x and z through the Cartesian velocity GPIO interfaces (direction angle π/4, at most 0.05 m/s, reversing every 4 seconds) with zero angular velocity.

```bash
ros2 launch diana_bringup example.launch.py controller_names:=cartesian_velocity_example_controller
```

```{warning}
The end effector moves back and forth in x and z. Make sure there is enough clearance around it.
```

### `cartesian_pose_example_controller`

Uses Cartesian pose commands to move the end effector along a circular arc of radius 0.1 m in x and z (period about 10 seconds) while keeping the orientation unchanged.

```bash
ros2 launch diana_bringup example.launch.py controller_names:=cartesian_pose_example_controller
```

```{warning}
The end effector moves about 0.1 m in x and z. Make sure there is enough clearance around it.
```

### `cartesian_orientation_example_controller`

Uses Cartesian pose commands to keep the end-effector position fixed while rotating its orientation periodically around the x axis by up to about π/4 rad.

```bash
ros2 launch diana_bringup example.launch.py controller_names:=cartesian_orientation_example_controller
```

```{warning}
The end-effector orientation rotates noticeably. Make sure there is enough space around the tool and cables.
```

### `cartesian_elbow_example_controller`

Uses Cartesian pose commands to keep the end-effector pose fixed while the elbow (joint 3 position) varies periodically around its initial value (maximum offset about 2π/15 rad), so only the null space moves. `controllers.yaml` also contains an alias of the same type, `cartesian_pose_elbow_example_controller`; both use the same class.

```bash
ros2 launch diana_bringup example.launch.py controller_names:=cartesian_elbow_example_controller
```

```{warning}
The elbow swings noticeably. Make sure there is enough space around the elbow. This controller needs the elbow command interface of real hardware.
```

### `elbow_example_controller`

Commands zero linear and angular velocity through the Cartesian velocity interface while varying the elbow position in the same way as `cartesian_elbow_example_controller`, that is, it moves the null space in velocity mode.

```bash
ros2 launch diana_bringup example.launch.py controller_names:=elbow_example_controller
```

```{warning}
The elbow swings noticeably. Make sure there is enough space around the elbow. This controller needs the elbow command interface of real hardware.
```

### `model_example_controller`

Sends no commands. It only reads the robot model interface and logs, about once per second, the mass matrix, Coriolis vector, gravity vector, the pose and Jacobian of joint 4, and the end-effector Jacobian, to demonstrate how to use `DianaRobotModel`. Configuration fails if the given `robot_type` does not match the loaded `robot_description`.

```bash
ros2 launch diana_bringup example.launch.py controller_names:=model_example_controller
```

### `diana3_move_to_start_example_controller`

Outputs torque with a joint impedance law to move the arm smoothly to a start joint configuration (parameter `start_joint_configuration`, default `0, -π/4, 0, 3π/4, 0, π/2, 0`; motion limits are scaled to 0.2 of their maximum). When it arrives it outputs zero torque and sets the parameter `process_finished` to `true`. It supports only robots whose `robot_type` is `diana3`, otherwise configuration fails; `k_gains` and `d_gains` must have 7 values each (provided in `controllers.yaml`).

```bash
ros2 launch diana_bringup example.launch.py controller_names:=diana3_move_to_start_example_controller
```

```{warning}
The arm moves from its current pose to the start pose, and any joint along the path may move a lot. Make sure the entire workspace is free of obstacles.
```

### `diana7_move_to_start_example_controller`

Identical to the previous controller, but it supports only robots whose `robot_type` is `diana7`, and the default start configuration is `0, -π/4, 0, 3π/4, 0, -π/2, 0` (joint 6 has the opposite sign compared with Diana3).

```bash
ros2 launch diana_bringup example.launch.py controller_names:=diana7_move_to_start_example_controller
```

```{warning}
The arm moves from its current pose to the start pose. Make sure the entire workspace is free of obstacles.
```

### `diana7g2_move_to_start_example_controller`

Identical to the previous controller, but it supports only robots whose `robot_type` is `diana7g2`, and the default start configuration is `0, -π/4, 0, 3π/4, 0, π/2, 0`.

```bash
ros2 launch diana_bringup example.launch.py controller_names:=diana7g2_move_to_start_example_controller
```

```{warning}
The arm moves from its current pose to the start pose. Make sure the entire workspace is free of obstacles.
```

## Writing Custom Controllers

A custom controller lists the interfaces it needs in `command_interface_configuration()` and `state_interface_configuration()`. The interfaces the Diana hardware interface actually provides are determined by `diana_hardware/ros2_control/diana_arm.ros2_control.xacro` and the hardware interface source (in the table below, `arm_prefix` is the `arm_prefix` parameter plus an underscore, or empty when there is no prefix).

| Interface | Name | Description |
| --- | --- | --- |
| Joint command | `<robot_type>_joint<1..7>/position`, `/velocity`, `/effort` | Joint position, velocity, torque; the xacro in `diana_bringup` includes the effort command by default |
| Joint state | `<robot_type>_joint<1..7>/position`, `/velocity`, `/effort` | Joint state |
| Cartesian velocity command | `cartesian_velocity` under `vx`, `vy`, `vz`, `wx`, `wy`, `wz` (each with `arm_prefix`) | 6 GPIO entries |
| Cartesian pose command | `cartesian_pose_command` under `0` to `15` (with `arm_prefix`) | 16 GPIO entries, a 4x4 pose matrix |
| Elbow command | `elbow_command` under `joint_3_position`, `joint_4_sign` (with `arm_prefix`) | Must be claimed together with a Cartesian pose or velocity command |
| Cartesian pose state | `cartesian_pose_state` under `0` to `15` (with `arm_prefix`) | Current pose matrix |
| Elbow state | `elbow_state` under `joint_3_position`, `joint_4_sign` (with `arm_prefix`) | Current elbow configuration |
| Robot state and model | `robot_state`, `robot_model`, `robot_time` under `arm_prefix` + `<robot_type>` | Full robot state, dynamic model handle, and robot time |
| Force/torque sensor | `force.x`, `force.y`, `force.z`, `torque.x`, `torque.y`, `torque.z` under `arm_prefix` + `<robot_type>_tcp` | Estimated external force and torque in the stiffness frame |

```{important}
State interfaces such as `robot_state`, `robot_model`, and `robot_time`, and the actual behavior of the elbow and Cartesian GPIOs, are provided by `diana_hardware/DianaHardwareInterface`. Simulated hardware (`mock_components/GenericSystem`) does not provide them, so controllers that depend on them can only run on real hardware. For hardware interface details see [diana_hardware](diana_hardware.md).
```

```{important}
Handle-type interfaces such as `robot_state` and `robot_model` cannot be used directly as plain `double` values, and it is not recommended to assemble the names of the pose, elbow, and model interfaces yourself. Use the semantic components from `diana_semantic_components` (`DianaRobotState`, `DianaRobotModel`, `DianaCartesianPoseInterface`, `DianaCartesianVelocityInterface`); they generate the interface names and read and write the data, which is how the example controllers do it. See [diana_semantic_components](diana_semantic_components.md). Robot state is also available as topics through [diana_robot_state_broadcaster](diana_robot_state_broadcaster.md).
```

When writing one, follow the approach of the example controllers:

- declare parameters such as `arm_prefix` in `on_init()` and read them in `on_configure()`;
- resolve the robot name from the `robot_description` parameter of `robot_state_publisher`, so that interface names match the loaded model;
- bind interfaces with the semantic component's `assign_loaned_*_interfaces()` in `on_activate()` and call `release_interfaces()` in `on_deactivate()`;
- to set non-realtime parameters such as the collision behavior, call the `service_server/...` services (see [diana_bringup](diana_bringup.md));
- `diana_hardware` accepts only one control mode at a time, so avoid designs in which several controllers claim command interfaces of different modes.

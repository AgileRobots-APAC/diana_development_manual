# Example Controllers

Package name: `franka_example_controllers`

`franka_example_controllers` is a set of `ros2_control` example controller plugins. They show how to implement joint torque, joint position/velocity, Cartesian pose/velocity, and elbow control on the Diana hardware interface, and how to read the robot model. They are meant for learning and reference, not as production controllers.

```{note}
This package is adapted from `franka_ros2` by Franka Robotics and keeps the `franka_` package name. See the NOTICE page of this manual for the third-party notice.
```

## Installation

See [Development Setup](../development.md).

## Package Overview

The package builds a single controller plugin library, `franka_example_controllers`. Plugin types are registered in `franka_example_controllers.xml`, with `controller_interface::ControllerInterface` as the base class. Controller names, their types, the update rate, and the gain parameters are provided by `config/controllers.yaml` of [diana_bringup](diana_bringup.md): the controller manager's `update_rate` is `1000` (Hz) and `thread_priority` is `97`.

The examples access the Cartesian pose, Cartesian velocity, force/torque, and robot model interfaces through [franka_semantic_components](franka_semantic_components.md), and call services of [franka_hardware](franka_hardware.md) through [franka_msgs](franka_msgs.md). The package depends on `pinocchio`; the joint-impedance IK example also depends on MoveIt (`moveit_core`, `moveit_msgs`).

Besides the controller plugins, the package contains one executable, `ptp_motion_example_node` (see below). It is a plain node, not a controller.

## Starting the Example Controllers

### Single-Arm Examples

Single-arm examples are started with `diana.example_controllers.launch.py` of [diana_bringup](diana_bringup.md). The launch file reads the model and IP from a robot configuration file (by default `diana_bringup/config/diana.config.yaml`), starts the basic nodes (robot description, `ros2_control_node`, `joint_state_broadcaster`, and so on), and then loads the controllers given in `controller_names` with a `spawner`.

| Launch argument | Default | Description |
|---|---|---|
| `controller_names` | none (required) | Controller names to load; separate several names with commas, one name per robot entry of the configuration file |
| `robot_config_file` | `diana.config.yaml` | Configuration file name (looked up in `diana_bringup/config/`) or full path |
| `robot_ips` | empty | Optional comma-separated IP list; when not empty it overrides `robot_ip` in the configuration file |

The model `robot_type` (`diana3`, `diana7`, or `diana7g2`) and `robot_ip` both come from the configuration file, so you must set them to your own values before running. It is best to copy the default file and edit the copy:

```bash
cp $(ros2 pkg prefix diana_bringup)/share/diana_bringup/config/diana.config.yaml ~/diana_ros2_ws/my_robot.config.yaml
```

In the copy, set at least `robot_type` and `robot_ip`; to connect to a real robot, set `use_fake_hardware` to `"false"` (boolean values must be quoted), and keep the other keys as they are in the default file. Then start with the command below, replacing `<controller-name>` with a name from the sections that follow:

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
    robot_config_file:=$HOME/diana_ros2_ws/my_robot.config.yaml \
    robot_ips:=192.168.10.75 \
    controller_names:=<controller-name>
```

The default IP of a Diana robot is `192.168.10.75` (the A network port of the controller). If the `namespace` key of the configuration file is not empty, the controllers, services, and topics live in that namespace; see the next section.

Entries whose name contains `controller` are loaded by the `spawner` as `ros2_control` controllers; entries without `controller` (for example `ptp_motion_example_node`) are run as plain nodes.

### Joint Impedance IK Example

`joint_impedance_with_ik_example_controller` needs the MoveIt `compute_ik` service, which is provided by `move_group` of [diana_moveit_config](diana_moveit_config.md) and must be available before the controller is used. The interfaces, parameters, and requirements of the controller itself are described in its own section below.

### Diana Duo Example

The dual-arm example `diana_duo_joint_impedance_example_controller` is started with `diana_duo.launch.py`, using the arguments `controller_name` (singular, only one controller is loaded) and `robot_config_file` (default `diana_duo.config.yaml`):

```bash
ros2 launch diana_bringup diana_duo.launch.py \
    robot_config_file:=$HOME/diana_ros2_ws/my_duo.config.yaml \
    controller_name:=diana_duo_joint_impedance_example_controller
```

In the dual-arm configuration file, `robot_types`, `arm_prefixes`, and `robot_ips` are stringified lists of equal length (for example `"['diana7','diana7']"`), the values of `arm_prefixes` must be unique, and you must set your own models and IPs before running. The dual-arm setup currently supports only the torque (`effort`) command interface.

## Interface and Parameter Conventions

The example controllers share the conventions below.

**Interface names.** Let `<name>` be `<arm_prefix>_<robot_type>` (just `<robot_type>`, for example `diana7`, when `arm_prefix` is empty). Joint interfaces are `position`, `velocity`, and `effort` under `<name>_joint1` to `<name>_joint7`; the robot time interface is `<name>/robot_time`. The Cartesian pose, Cartesian velocity, and elbow interfaces come from the semantic components and are named as follows (with `<arm_prefix>_` prepended when `arm_prefix` is not empty):

| Interface | Name |
|---|---|
| Pose command (16) | `0/cartesian_pose_command` to `15/cartesian_pose_command` |
| Pose state (16) | `0/cartesian_pose_state` to `15/cartesian_pose_state` |
| Velocity command (6) | `cartesian_velocity` under `vx`, `vy`, `vz`, `wx`, `wy`, `wz` |
| Elbow command (2) | `joint_3_position/elbow_command`, `joint_4_sign/elbow_command` |
| Elbow state (2) | `joint_3_position/elbow_state`, `joint_4_sign/elbow_state` |

All examples are written for 7 joints.

**Common parameters.** `arm_prefix` (string, default empty) exists on almost every controller. `robot_type` is set on `ros2_control_node` by `diana.launch.py`; some controllers read it directly, while others resolve the robot name from the `robot_description` parameter of `robot_state_publisher` during configuration, so the model must match the loaded description. Parameters specific to a controller are given in its section.

**Namespaces.** Services called by the controllers use relative names, for example `service_server/set_full_collision_behavior`; this is the name as is when `namespace` in the configuration file is empty, and `/<namespace>/service_server/set_full_collision_behavior` otherwise. The same applies to the `collision_detected` topic subscribed by `diana_duo_joint_impedance_example_controller`.

**Default collision behavior.** The Cartesian, elbow, joint velocity, and joint-impedance IK examples call `service_server/set_full_collision_behavior` (type `franka_msgs/srv/SetFullCollisionBehavior`) during configuration and set the collision thresholds to the defaults in the code: lower joint torque thresholds (nominal and acceleration) `25, 25, 22, 20, 19, 17, 14` Nm and upper thresholds `35, 35, 32, 30, 29, 27, 24` Nm; lower Cartesian force/torque thresholds `30, 30, 30, 25, 25, 25` and upper thresholds `40, 40, 40, 35, 35, 35` (N for forces, Nm for torques). If the call fails, configuration fails and the controller is not activated. The service is provided by the real `franka_hardware`.

```{warning}
Except for `model_example_controller`, these examples send torque, velocity, or position commands to the robot, and the arm really moves. Before running one, make sure the workspace is clear of people and obstacles, the emergency stop is reachable, and the robot is in a state that allows external control. Read [Safety Boundaries](../../../reference/safety.md) first; for FCI and network prerequisites see the [FCI overview](../../../fci/overview.md). Start from a conservative pose for the first run and be ready to press the emergency stop at any time.
```

## Controller List

The table below summarizes all examples; details are in the sections that follow. The "Extra requirements" column lists what the code depends on beyond the joint interfaces; these are provided by the real `franka_hardware` (or MoveIt).

| Example controller | Description | Command interfaces | Extra requirements |
|---|---|---|---|
| <a href="#gravity-compensation-example-controller"><code>gravity_compensation_example_controller</code></a> | Zero-torque gravity compensation, prints the external wrench estimate | Joint `effort` | TCP force/torque state interfaces |
| <a href="#joint-impedance-example-controller"><code>joint_impedance_example_controller</code></a> | Joint impedance law, joints 4 and 5 move periodically | Joint `effort` | None |
| <a href="#joint-impedance-with-ik-example-controller"><code>joint_impedance_with_ik_example_controller</code></a> | MoveIt inverse kinematics + joint impedance law, end effector draws an arc | Joint `effort` | `compute_ik`, collision behavior service, model and pose interfaces |
| <a href="#joint-position-example-controller"><code>joint_position_example_controller</code></a> | Joint position commands, periodic offset | Joint `position` | `robot_time` |
| <a href="#joint-velocity-example-controller"><code>joint_velocity_example_controller</code></a> | Joint velocity commands, joints 4 and 5 oscillate | Joint `velocity` | Collision behavior service |
| <a href="#cartesian-velocity-example-controller"><code>cartesian_velocity_example_controller</code></a> | Cartesian velocity commands, oscillation in x and z | Cartesian velocity | Collision behavior service |
| <a href="#cartesian-pose-example-controller"><code>cartesian_pose_example_controller</code></a> | Cartesian pose commands, arc in the x-z plane | Cartesian pose | Collision behavior service, `robot_time` |
| <a href="#cartesian-orientation-example-controller"><code>cartesian_orientation_example_controller</code></a> | Cartesian pose commands, orientation rotates periodically about x | Cartesian pose | Collision behavior service, `robot_time` |
| <a href="#cartesian-elbow-example-controller"><code>cartesian_elbow_example_controller</code></a> | Holds the end-effector pose, elbow varies periodically | Cartesian pose + elbow | Collision behavior service, `robot_time` |
| <a href="#elbow-example-controller"><code>elbow_example_controller</code></a> | Moves only the elbow, in velocity mode | Cartesian velocity + elbow | Collision behavior service, `robot_time` |
| <a href="#model-example-controller"><code>model_example_controller</code></a> | Reads and prints the robot model only | None | Robot model interfaces |
| <a href="#move-to-start-example-controller"><code>move_to_start_example_controller</code></a> | Smoothly moves to a start joint configuration | Joint `effort` | None |
| <a href="#diana-duo-joint-impedance-example-controller"><code>diana_duo_joint_impedance_example_controller</code></a> | Dual-arm joint impedance, joints 4 and 5 of both arms move periodically | Joint `effort` of both arms | `collision_detected` topic |
| <a href="#ptp-motion-example-node"><code>ptp_motion_example_node</code></a> | Sends a series of joint goals to the PTP motion action (a node, not a controller) | None | `action_server/ptp_motion` |

### `gravity_compensation_example_controller`

Type `franka_example_controllers/GravityCompensationExampleController`. It only writes zero torque to the `effort` interfaces of the 7 joints so that the robot just compensates its own weight, and prints the external force and torque estimate in the stiffness frame once every 1000 control cycles.

- Command interfaces: `effort` of `<name>_joint1` to `<name>_joint7`.
- State interfaces: the force/torque sensor interfaces of `<name>_tcp` (`force.x/y/z`, `torque.x/y/z`; `<arm_prefix>_` is prepended to the name when `arm_prefix` is not empty).
- Parameters: `robot_type`, `arm_prefix` (default empty).

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
    robot_config_file:=$HOME/diana_ros2_ws/my_robot.config.yaml \
    robot_ips:=192.168.10.75 \
    controller_names:=gravity_compensation_example_controller
```

```{warning}
The arm is in zero-torque mode and does not actively hold its position; it moves when pushed. Support the arm and the end load first, and keep a hand within reach of the emergency stop.
```

### `joint_impedance_example_controller`

Type `franka_example_controllers/JointImpedanceExampleController`. It outputs torques with a joint impedance law so that joints 4 and 5 move slowly with an amplitude of about π/4 rad and a period of 5 seconds, while the other joints stay at their initial positions from activation. The overall behavior is compliant.

- Command interfaces: `effort` of the 7 joints.
- State interfaces: `position` and `velocity` of the 7 joints.
- Parameters: `robot_type`, `arm_prefix`, `k_gains`, `d_gains` (7 values each; they must be set, and configuration fails if they are empty or have the wrong length). In `controllers.yaml`, `k_gains` is `24, 24, 24, 24, 10, 6, 2` and `d_gains` is `2, 2, 2, 1, 1, 1, 0.5`.

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
    robot_config_file:=$HOME/diana_ros2_ws/my_robot.config.yaml \
    robot_ips:=192.168.10.75 \
    controller_names:=joint_impedance_example_controller
```

```{warning}
This controller outputs torques and moves the arm. Make sure there are no obstacles within the range of motion of joints 4 and 5.
```

### `joint_impedance_with_ik_example_controller`

Type `franka_example_controllers/JointImpedanceWithIKExampleController`. It moves the end-effector position along an arc of radius 0.1 m in the x-z plane (period 10 seconds) while keeping the orientation unchanged. In every control cycle it asks the MoveIt `compute_ik` service (`moveit_msgs/srv/GetPositionIK`) for a joint solution of the target pose, and outputs torques with a joint impedance law plus Coriolis compensation. The request uses the planning group `<name>_arm` and the pose reference frame `<name>_link0`.

- Command interfaces: `effort` of the 7 joints.
- State interfaces: the Cartesian pose state, `position`, `velocity`, and `effort` of the 7 joints, the robot model interfaces, and `robot_time`.
- Parameters: `arm_prefix`, `k_gains`, `d_gains`. In `controllers.yaml`, `k_gains` is `600, 600, 600, 600, 250, 150, 50` and `d_gains` is `30, 30, 30, 30, 10, 10, 5`.
- Requirements: during configuration the controller waits for the `compute_ik` and `service_server/set_full_collision_behavior` services for about 10 seconds at most and fails to configure on timeout, so the MoveIt `move_group` must be started first. The solver can be replaced in `kinematics.yaml` of [diana_moveit_config](diana_moveit_config.md).

```{warning}
This controller outputs torques and moves the arm in Cartesian space; it needs real hardware and a working `compute_ik` service. When an inverse kinematics request fails, the controller keeps using the last joint solution it received.
```

### `joint_position_example_controller`

Type `franka_example_controllers/JointPositionExampleController`. It writes position commands to the `position` interfaces of the 7 joints: a slow periodic offset (at most about π/40 rad, period 10 seconds) is added to the initial positions at activation, with joint 5 offset in the opposite direction to the other joints.

- Command interfaces: `position` of the 7 joints.
- State interfaces: `position` of the 7 joints and `robot_time`.
- Parameters: `arm_prefix`; `gazebo` (boolean, default `false`): when `true`, `robot_time` is not read and time is accumulated from the control period instead, for use in simulation.

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
    robot_config_file:=$HOME/diana_ros2_ws/my_robot.config.yaml \
    robot_ips:=192.168.10.75 \
    controller_names:=joint_position_example_controller
```

```{warning}
This controller moves all joints at the same time. Make sure the whole workspace is free of obstacles.
```

### `joint_velocity_example_controller`

Type `franka_example_controllers/JointVelocityExampleController`. It writes velocity commands to the `velocity` interfaces of the 7 joints: joints 4 and 5 move with a peak angular velocity of 0.1 rad/s and a period of 8 seconds, reversing direction every period, and the other joints have zero velocity.

- Command interfaces: `velocity` of the 7 joints.
- State interfaces: `position` and `velocity` of the 7 joints.
- Parameters: `arm_prefix`; `gazebo` (boolean, default `false`): when `true`, the collision behavior service is not called.
- When `gazebo` is `false`, the default collision behavior is set during configuration.

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
    robot_config_file:=$HOME/diana_ros2_ws/my_robot.config.yaml \
    robot_ips:=192.168.10.75 \
    controller_names:=joint_velocity_example_controller
```

```{warning}
This controller moves the arm through the velocity interface. Make sure there are no obstacles within the range of motion of joints 4 and 5.
```

### `cartesian_velocity_example_controller`

Type `franka_example_controllers/CartesianVelocityExampleController`. It gives a linear velocity in the x and z directions through the Cartesian velocity interface: direction angle π/4, peak 0.05 m/s, period 4 seconds, reversing every period. The angular velocity is zero and the elbow interfaces are not used.

- Command interfaces: `cartesian_velocity` of `vx`, `vy`, `vz`, `wx`, `wy`, `wz`.
- State interfaces: none.
- Parameters: `arm_prefix`. The default collision behavior is set during configuration.

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
    robot_config_file:=$HOME/diana_ros2_ws/my_robot.config.yaml \
    robot_ips:=192.168.10.75 \
    controller_names:=cartesian_velocity_example_controller
```

```{warning}
The end effector oscillates in the x and z directions. Make sure there is enough clearance around it.
```

### `cartesian_pose_example_controller`

Type `franka_example_controllers/CartesianPoseExampleController`. It moves the end effector along an arc of radius 0.1 m in the x-z plane (period 10 seconds) through Cartesian pose commands, keeping the orientation it had at activation.

- Command interfaces: the 16 Cartesian pose command interfaces.
- State interfaces: the 16 Cartesian pose state interfaces and `robot_time`.
- Parameters: `arm_prefix`. The default collision behavior is set during configuration.

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
    robot_config_file:=$HOME/diana_ros2_ws/my_robot.config.yaml \
    robot_ips:=192.168.10.75 \
    controller_names:=cartesian_pose_example_controller
```

```{warning}
The end effector moves by about 0.1 m in x and z. Make sure there is enough clearance around it.
```

### `cartesian_orientation_example_controller`

Type `franka_example_controllers/CartesianOrientationExampleController`. It keeps the end-effector position fixed through Cartesian pose commands and rotates the orientation periodically about the x axis of the base frame, by at most about π/4 rad with a period of 10 seconds.

- Command interfaces: the 16 Cartesian pose command interfaces.
- State interfaces: the 16 Cartesian pose state interfaces and `robot_time`.
- Parameters: `arm_prefix`. The default collision behavior is set during configuration.

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
    robot_config_file:=$HOME/diana_ros2_ws/my_robot.config.yaml \
    robot_ips:=192.168.10.75 \
    controller_names:=cartesian_orientation_example_controller
```

```{warning}
The end-effector orientation changes noticeably. Make sure there is enough space around the tool and cables.
```

### `cartesian_elbow_example_controller`

Type `franka_example_controllers/CartesianElbowExampleController`. It keeps the end-effector pose fixed through Cartesian pose commands while the elbow (`joint_3_position`) varies periodically around its initial value (at most about 2π/15 rad, period 10 seconds); in other words, only the nullspace moves. `controllers.yaml` also contains a second name for the same type, `cartesian_pose_elbow_example_controller`, which is used in the same way.

- Command interfaces: the 16 Cartesian pose command interfaces and the 2 elbow command interfaces.
- State interfaces: the 16 Cartesian pose state interfaces, the 2 elbow state interfaces, and `robot_time`.
- Parameters: `arm_prefix`. The default collision behavior is set during configuration.

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
    robot_config_file:=$HOME/diana_ros2_ws/my_robot.config.yaml \
    robot_ips:=192.168.10.75 \
    controller_names:=cartesian_elbow_example_controller
```

```{warning}
The elbow swings noticeably. Make sure there is enough space around the elbow. This controller needs the elbow command interfaces of the real hardware.
```

### `elbow_example_controller`

Type `franka_example_controllers/ElbowExampleController`. It gives zero linear and angular velocity through the Cartesian velocity interface while the elbow position follows the same periodic variation as `cartesian_elbow_example_controller`; that is, it moves the nullspace in velocity mode.

- Command interfaces: the 6 Cartesian velocity command interfaces and the 2 elbow command interfaces.
- State interfaces: the 2 elbow state interfaces and `robot_time`.
- Parameters: `arm_prefix`. The default collision behavior is set during configuration.

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
    robot_config_file:=$HOME/diana_ros2_ws/my_robot.config.yaml \
    robot_ips:=192.168.10.75 \
    controller_names:=elbow_example_controller
```

```{warning}
The elbow swings noticeably. Make sure there is enough space around the elbow. This controller needs the elbow command interfaces of the real hardware.
```

### `model_example_controller`

Type `franka_example_controllers/ModelExampleController`. It sends no commands and only reads the robot model interfaces. About once per second it prints the mass matrix, the Coriolis vector, the gravity vector, the pose of joint 4, the body Jacobian of joint 4, and the end-effector Jacobian with respect to the base frame, demonstrating the `FrankaRobotModel` semantic component.

- Command interfaces: none.
- State interfaces: the robot model interfaces for `<name>/robot_model` and `<name>/robot_state`.
- Parameters: `robot_type`, `arm_prefix` (default empty).

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
    robot_config_file:=$HOME/diana_ros2_ws/my_robot.config.yaml \
    robot_ips:=192.168.10.75 \
    controller_names:=model_example_controller
```

### `move_to_start_example_controller`

Type `franka_example_controllers/MoveToStartExampleController`. It outputs torques with a joint impedance law and smoothly moves the arm to a start joint configuration. The motion is generated by `MotionGenerator`, with velocity and acceleration limits at 0.2 times the maximum. When the goal is reached it outputs zero torque and sets the parameter `process_finished` to `true`; the controller stays active.

- Command interfaces: `effort` of the 7 joints.
- State interfaces: `position` and `velocity` of the 7 joints.
- Parameters:

| Parameter | Default | Description |
|---|---|---|
| `robot_type` | `diana7` | Robot model, used to build the interface names |
| `arm_prefix` | empty | Arm prefix |
| `k_gains`, `d_gains` | empty, must be set | 7 values each; in `controllers.yaml` they are `600, 600, 600, 600, 250, 150, 50` and `30, 30, 30, 30, 10, 10, 5` |
| `start_joint_configuration` | `-π/4, 0, 0, π/2, 0, -π/2, π/4` | Goal joint angles (rad) |
| `process_finished` | `false` | Set to `true` by the controller when the motion has finished |

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
    robot_config_file:=$HOME/diana_ros2_ws/my_robot.config.yaml \
    robot_ips:=192.168.10.75 \
    controller_names:=move_to_start_example_controller
```

```{warning}
The arm moves from its current pose to the goal pose, and any joint may move a large distance. Make sure the whole workspace is free of obstacles. The default goal joint angles are fixed values in the code; confirm they suit your model before running and change `start_joint_configuration` in `controllers.yaml` if needed. After the motion finishes the controller outputs zero torque, so be ready to support the arm.
```

### `diana_duo_joint_impedance_example_controller`

Type `franka_example_controllers/DianaDuoJointImpedanceExampleController`. It runs the joint impedance law on both arms of a dual-arm system at the same time; joints 4 and 5 of each arm follow the same periodic motion as in `joint_impedance_example_controller`. The controller also subscribes to `collision_detected` (`std_msgs/msg/Bool`, `SensorDataQoS`) and treats it as the result of self-collision checking: a publisher must already exist at activation, and while running, receiving no message for more than 0.5 seconds or receiving `true` makes the controller return an error and stop.

- Command interfaces: `effort` of 7 joints per arm, named `<arm_prefix>_<robot_type>_joint<i>/effort`.
- State interfaces: `position` and `velocity` of 7 joints per arm.
- Parameters: `robot_types`, `arm_prefixes` (string arrays, set by `diana_duo.launch.py` from the configuration file); `k_gains`, `d_gains` (7 values each, shared by both arms). In `controllers.yaml`, `k_gains` is `24, 24, 24, 24, 10, 6, 2`, `d_gains` is `2, 2, 2, 1, 1, 1, 0.5`, and `update_rate` is `1000`.
- Requirements: the `collision_detected` topic needs a publisher, see [diana_selfcollision](diana_selfcollision.md); the topic name is relative, so it must be in the same namespace as the controller.

```bash
ros2 launch diana_bringup diana_duo.launch.py \
    robot_config_file:=$HOME/diana_ros2_ws/my_duo.config.yaml \
    controller_name:=diana_duo_joint_impedance_example_controller
```

```{warning}
Both arms move at the same time. Make sure there are no people or obstacles in the workspace of each arm and between the two arms. The controller cannot be activated without a self-collision publisher.
```

### `ptp_motion_example_node`

The executable `ptp_motion_example_node` (node name `ptp_motion_example`) is not a controller plugin. It is an action client that sends goals in sequence to `action_server/ptp_motion` (type `franka_msgs/action/PTPMotion`, provided by [franka_hardware](franka_hardware.md)): first a fixed initial joint configuration `-0.5, -π/4, 0, -3π/4, 0, π/2, π/4` (rad), then 20 goals that move joints 1 and 3 alternately to both sides (with growing amplitude); the last goal returns these two joints to 0. All goals use a maximum joint velocity of 1.0 rad/s and a tolerance of 0.01.

Because its name does not contain `controller`, `diana.example_controllers.launch.py` runs it as a plain node and no controller is needed:

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
    robot_config_file:=$HOME/diana_ros2_ws/my_robot.config.yaml \
    robot_ips:=192.168.10.75 \
    controller_names:=ptp_motion_example_node
```

```{warning}
The goal joint configuration and the motion amplitude are fixed values in the code, and the arm moves a large distance. Before running, confirm that these joint angles suit your model, that the whole workspace is free of people and obstacles, and that the emergency stop is within reach.
```

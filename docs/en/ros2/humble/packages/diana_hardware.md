# `diana_hardware`

## Installation

See [Development Setup](../development.md).

## Package Overview

`diana_hardware` is the `ros2_control` hardware plugin for Diana robots. It implements the `hardware_interface::SystemInterface` plugin `diana_hardware/DianaHardwareInterface` (registered through `diana_hardware.xml`) on top of libfranka-compatible robot communication, and also ships the `ros2_control` xacro macro library that declares the interfaces the plugin exports.

The package provides:

- **The hardware plugin**: reads the full robot state every control cycle and writes one of the supported command modes (joint effort, joint velocity, joint position, Cartesian velocity, Cartesian pose, each optionally with elbow).
- **The xacro macro library** in `ros2_control/`: `diana_arm.ros2_control.xacro` and `diana_ros2_control_macros.xacro`.
- **A parameter service node** (`service_server`) that wraps the `Set*` services from [diana_msgs](diana_msgs.md).
- **An action server node** (`action_server`) that serves the `ErrorRecovery` action.
- **A libfranka logger bridge** that forwards libfranka log messages to the ROS 2 logger.

The plugin is normally loaded by the `ros2_control_node` that [diana_bringup](diana_bringup.md) starts. Controllers should not talk to the plugin directly; use the [semantic components](diana_semantic_components.md) instead of raw interface names.

```{figure} ../../../../_static/images/ros2-humble-hardware-dataflow-en.png
:alt: Data flow between the hardware plugin, the controllers and the robot
:width: 100%

Data flow of `DianaHardwareInterface`: controllers send commands through command interfaces and read state through state interfaces; the parameter services and the error-recovery action are two nodes inside the plugin that talk to the robot directly.
```

```{important}
Commanding a real robot moves it. Before activating any controller, make sure the workspace is clear, the emergency stop is within reach, and the robot is ready for external control as described in [Safety Boundaries](../../../reference/safety.md) and the [FCI overview](../../../fci/overview.md).
```

## Hardware Interfaces

In the names below, `<P>` is the arm prefix (`modified_prefix` in the xacro, empty by default) and `<T>` is the `robot_type` (`diana3`, `diana7` or `diana7g2`). All interfaces are of type `double`. The interface set below is what the xacro declares and what `export_state_interfaces()` / `export_command_interfaces()` register in `diana_hardware_interface.cpp`.

### Joint Interfaces

Seven joints are exported, `<P><T>_joint1` to `<P><T>_joint7`. The joint count is fixed to 7 in the plugin.

| Interface | Direction | Source / meaning |
| --- | --- | --- |
| `<P><T>_jointN/position` | state | measured joint position `q` (rad) |
| `<P><T>_jointN/velocity` | state | measured joint velocity `dq` (rad/s) |
| `<P><T>_jointN/effort` | state | measured joint torque `tau_J` (Nm) |
| `<P><T>_jointN/position` | command | joint position command |
| `<P><T>_jointN/velocity` | command | joint velocity command |
| `<P><T>_jointN/effort` | command | joint torque command; declared when `include_effort_command` is true (the bringup xacro sets it to `true`) |

The `initial_value` of the position state interface (used by mock hardware) is `0`, `-pi/4`, `0`, `3*pi/4`, `0`, `-pi/2` (`diana7`) or `pi/2` (other types), `0` for joints 1 to 7.

### Cartesian Command Interfaces

Cartesian commands are exported as GPIO entries whose `index` parameter selects the slot of the underlying command array.

| Interface | Count | Meaning |
| --- | --- | --- |
| `<P>vx/cartesian_velocity`, `<P>vy/...`, `<P>vz/...`, `<P>wx/...`, `<P>wy/...`, `<P>wz/...` | 6 (index 0 to 5) | desired end-effector twist in the base frame; linear in m/s, angular in rad/s |
| `<P>0/cartesian_pose_command` ... `<P>15/cartesian_pose_command` | 16 (index 0 to 15) | desired end-effector pose as a column-major 4x4 homogeneous transform |
| `<P>0/cartesian_pose_state` ... `<P>15/cartesian_pose_state` | 16 (state) | measured end-effector pose `O_T_EE`, column-major |

### Elbow Interfaces

| Interface | Direction | Meaning |
| --- | --- | --- |
| `<P>joint_3_position/elbow_command` | command (index 0) | desired position of joint 3 (rad) |
| `<P>joint_4_sign/elbow_command` | command (index 1) | desired flip direction of the elbow (joint 4) |
| `<P>joint_3_position/elbow_state` | state | current joint 3 position of the elbow |
| `<P>joint_4_sign/elbow_state` | state | current elbow flip direction |

The elbow command can only be claimed together with the Cartesian velocity or the Cartesian pose command interfaces; otherwise `perform_command_mode_switch` fails with a fatal log message.

### Force/Torque Sensor Interfaces

The xacro declares one sensor named `<P><T>_tcp` with the state interfaces `force.x`, `force.y`, `force.z`, `torque.x`, `torque.y`, `torque.z`. The plugin fills them from the estimated external wrench in the stiffness frame (`K_F_ext_hat_K`), in the order declared in the xacro.

## Additional State Interfaces

Besides the joint, pose, elbow and sensor interfaces, the plugin exports three robot-level state interfaces that carry data not representable as plain numbers:

| Interface | Content |
| --- | --- |
| `<P><T>/robot_state` | the address of the full robot state structure (`franka::RobotState`), stored in the `double` slot; consumed by [DianaRobotState](diana_semantic_components.md) and [diana_robot_state_broadcaster](diana_robot_state_broadcaster.md) |
| `<P><T>/robot_model` | the address of the model object (`diana_hardware::Model`), consumed by `DianaRobotModel` |
| `<P><T>/robot_time` | robot time in seconds, a plain `double` |

```{warning}
`robot_state` and `robot_model` are pointers stored in a `double` and are only meaningful inside the same process. Never read them as numbers, and do not use them from another process; use the semantic component classes which perform the conversion.
```

## ros2_control Macro Library

The macros live in `ros2_control/` of the package and are installed to `share/diana_hardware/ros2_control`.

### diana_arm.ros2_control.xacro

Defines the macro `diana_arm_ros2_control` which emits one `ros2_control` block named `<arm_prefix>DianaHardwareInterface` of type `system`.

| Argument | Default | Use |
| --- | --- | --- |
| `robot_type` | required | written to the hardware parameter `robot_type` and used in joint, sensor and interface names |
| `include_effort_command` | `true` | declare the `effort` command interface on every joint |
| `arm_prefix` | `''` | prefix of joint and GPIO names; written to the hardware parameter `prefix` |
| `is_async` | `false` | passed to `ros2_control` as `is_async`; when true an `async` properties block is added |
| `thread_priority` | `50` | thread priority of the async block (only used if `is_async` is true) |
| `hardware_plugin` (block parameter) | required | the `plugin` tag and its parameters, inserted into `hardware` |

The macro always writes the parameter `version` with value `1.1.0` and then calls `configure_arm_interfaces` with the elbow, Cartesian pose and sensor options enabled (`sensor_name` is `<arm_prefix><robot_type>_tcp`).

### diana_ros2_control_macros.xacro

| Macro | Purpose |
| --- | --- |
| `configure_arm_joint` | one joint with `position`, `velocity` and (optional) `effort` command interfaces and `position`, `velocity`, `effort` state interfaces |
| `configure_arm_joints` | joints 1 to 7 with the initial positions listed above |
| `general_purpose_io` | one GPIO entry with a single command interface and an `index` parameter |
| `cartesian_velocity_io` | the six `vx` ... `wz` GPIO entries |
| `cartesian_pose_loop` | recursive macro that emits the 16 `cartesian_pose_command` GPIO entries |
| `configure_arm_interfaces` | complete per-arm set: joints, Cartesian velocity, optional elbow, optional Cartesian pose, optional sensor |

### Using the Macro in a Robot Description

The single-arm entry point `diana_bringup/urdf/diana_arm.urdf.xacro` includes the macro and selects the plugin:

```xml
<xacro:diana_arm_ros2_control
    robot_type="$(arg robot_type)"
    include_effort_command="true"
    arm_prefix="${modified_prefix}"
    is_async="$(arg is_async)"
    thread_priority="$(arg thread_priority)">
  <hardware_plugin>
    <xacro:if value="$(arg use_fake_hardware)">
      <plugin>mock_components/GenericSystem</plugin>
      <param name="mock_sensor_commands">$(arg fake_sensor_commands)</param>
      <param name="state_following_offset">0.0</param>
    </xacro:if>
    <xacro:unless value="$(arg use_fake_hardware)">
      <plugin>diana_hardware/DianaHardwareInterface</plugin>
      <param name="robot_ip">$(arg robot_ip)</param>
      <param name="arm_prefix">${modified_prefix}</param>
    </xacro:unless>
  </hardware_plugin>
</xacro:diana_arm_ros2_control>
```

`robot_type` (required: `diana3`, `diana7` or `diana7g2`, matching your robot model), `arm_prefix`, `robot_ip` and `use_fake_hardware` are xacro arguments of that file. `modified_prefix` is derived from `arm_prefix` in the `diana_description` package, which is not part of this package. With `use_fake_hardware:=true` the generic mock system is used instead of `DianaHardwareInterface`, and no robot connection is made.

## Configuration

### Hardware Plugin Parameters

The plugin reads these parameters from the `hardware` block in `on_init`:

| Parameter | Required | Description |
| --- | --- | --- |
| `version` | yes | version of the `ros2_control` interface description, `major.minor.patch`. The major version must be `1`; otherwise initialization fails with a message asking you to update the URDF (`diana_description`) |
| `robot_ip` | yes | hostname or IP address of the robot; initialization fails if it is missing or the connection cannot be established |
| `robot_type` | yes | one of `diana3`, `diana7` or `diana7g2`; must equal the robot name reported by the connected robot, otherwise initialization fails |
| `prefix` | no | prefix of the robot-level interface names (`<P><T>/robot_state`, ...); empty if unset. The bringup xacro macro sets it from `arm_prefix` |


During `on_init` the plugin also starts two ROS 2 nodes in its own executor thread (see the Parameter Services and Action Server sections below).

### Command Rate Limiting and Filtering

`robot.hpp` holds fixed (compile-time) defaults for optional command post-processing. There is no ROS parameter for them:

| Setting | Default |
| --- | --- |
| torque command rate limiter | on |
| joint velocity rate limiter | off |
| joint position rate limiter and low-pass filter | off |
| Cartesian velocity rate limiter and low-pass filter | off |
| Cartesian pose rate limiter and low-pass filter | off |
| low-pass cut-off frequency | 100 Hz |

```{note}
If the process is not running on a real-time kernel, the plugin logs a notice and continues with real-time enforcement disabled. A real-time kernel is strongly recommended; see [Real-time Network](../../../fci/realtime_network.md).
```

## Parameter Services

The plugin hosts a node named `service_server` that serves the following services. Message definitions are in [diana_msgs](diana_msgs.md). The service names carry the namespace the robot was launched with: the table lists them without a namespace, and with the default `NS_1` of `diana.config.yaml` they take the form `/NS_1/service_server/set_joint_stiffness`.

| Service | Type |
| --- | --- |
| `/service_server/set_joint_stiffness` | `diana_msgs/srv/SetJointStiffness` |
| `/service_server/set_cartesian_stiffness` | `diana_msgs/srv/SetCartesianStiffness` |
| `/service_server/set_tcp_frame` | `diana_msgs/srv/SetTCPFrame` |
| `/service_server/set_stiffness_frame` | `diana_msgs/srv/SetStiffnessFrame` |
| `/service_server/set_force_torque_collision_behavior` | `diana_msgs/srv/SetForceTorqueCollisionBehavior` |
| `/service_server/set_full_collision_behavior` | `diana_msgs/srv/SetFullCollisionBehavior` |
| `/service_server/set_load` | `diana_msgs/srv/SetLoad` |

Each response contains `success` and an `error` string; library exceptions are reported there instead of crashing the plugin.

## Error Recovery

### Behavior on Error

- If reading the robot state raises a control exception, `read()` logs the message, stops the active control session and returns `ERROR`.
- If any command value is not finite, `write()` returns `ERROR`.
- A runtime error raised while writing during a command mode switch is logged as a warning and skipped, so that a mode switch does not take down all hardware.
- When a control session is started (`initializeTorqueInterface` and the equivalents) and the robot reports a control exception, the plugin runs one automatic error recovery and retries once.
- `on_deactivate` stops the robot control session.

```{important}
The plugin itself never deactivates controllers. Do not rely on the controller manager of your Humble release to deactivate or restart controllers after the hardware reports an error: after an error, check the controller states yourself and re-activate the controllers explicitly as described below.
```

### Recovery Steps

```{warning}
Re-activating a motion controller starts commanding the robot again. Remove the cause of the error, make sure the workspace is clear and the emergency stop is within reach before you start. Do not simply repeat the recovery in a loop; see [Safety Boundaries](../../../reference/safety.md).
```

1. Find out why the robot stopped (the `robot_mode`, `current_errors` and `last_motion_errors` fields of the [robot state](diana_robot_state_broadcaster.md)) and remove the cause.
2. Check which controllers are still active (when the robot runs in a namespace, add `-c /<namespace>/controller_manager` to every `ros2 control` command):

   ```bash
   ros2 control list_controllers
   ```

3. Deactivate the motion controllers that were running, so they can claim their interfaces again later (use `-c /<namespace>/controller_manager` if the robot runs in a namespace):

   ```bash
   ros2 control switch_controllers --deactivate <controller-name>
   ```

4. Send the error recovery goal (with a namespace, prefix the action name with it; the example uses `NS_1`):

   ```bash
   ros2 action send_goal /NS_1/action_server/error_recovery diana_msgs/action/ErrorRecovery {}
   ```

5. Re-activate the controller:

   ```bash
   ros2 control switch_controllers --activate <controller-name>
   ```

6. Verify with `ros2 control list_hardware_components` that the hardware component is `active`.

### Action Server

The node `action_server` serves one action:

| Action | Type | Behavior |
| --- | --- | --- |
| `/action_server/error_recovery` | `diana_msgs/action/ErrorRecovery` | accepts every goal, runs the robot's automatic error recovery; the goal succeeds when the recovery returns, and is aborted if it raises an exception. Goal, result and feedback are empty |

```{note}
The plugin creates these two nodes inside the `ros2_control_node` process, and their names carry the namespace the robot was launched with. For example, with the default `NS_1` of `diana.config.yaml` the services are `/NS_1/service_server/...` and the action is `/NS_1/action_server/error_recovery`. List the actual names with:

~~~bash
ros2 service list | grep service_server
ros2 action list | grep action_server
~~~
```

## Usage with Controllers

A controller claims interfaces in `command_interface_configuration()`. The plugin derives the control mode from the claimed command interfaces, in this priority order:

| Claimed command interfaces | Control mode |
| --- | --- |
| all 7 joints `effort` | joint torque |
| all 7 joints `velocity` | joint velocity |
| all 7 joints `position` | joint position |
| 16 `cartesian_pose_command` (+ 2 `elbow_command`) | Cartesian pose (with elbow) |
| 6 `cartesian_velocity` (+ 2 `elbow_command`) | Cartesian velocity (with elbow) |

Rules enforced by `prepare_command_mode_switch`:

- An interface group must be claimed or released completely (7, 6, 16 or 2 interfaces). A partial claim raises an error such as `Invalid number of ... interfaces to start`.
- Elbow commands require a Cartesian pose or velocity claim.
- Every mode switch stops the current control session and starts a new one. For position, pose and elbow modes the plugin initializes the command from the current robot state first, and ignores commands until that is done.

```{tip}
Use the classes in [diana_semantic_components](diana_semantic_components.md) (`DianaRobotState`, `DianaRobotModel`, `DianaCartesianPoseInterface`, `DianaCartesianVelocityInterface`) in your controllers instead of listing raw interface names; they build the correct prefixed names for you.
```

To inspect what the running plugin exports:

```bash
ros2 control list_hardware_interfaces
ros2 control list_hardware_components
```

```{note}
The code excerpts on this page are adapted from `diana_ros2`, whose source follows the structure of franka_ros2 and carries the Franka Robotics GmbH copyright notice (Copyright (c) 2023 Franka Robotics GmbH, Apache License 2.0); the adapted parts are Copyright (c) 2026 Agile Robots SE. See "License and Third-Party Notices" in the [Manual Overview](/about/overview.md).
```

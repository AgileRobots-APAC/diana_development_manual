# Hardware Interface

Package name: `franka_hardware`

## Installation

See [Development Setup](../development.md).

## Package Overview

`franka_hardware` is the `ros2_control` hardware plugin for Diana robots. Built on libfranka, it implements the `hardware_interface::SystemInterface` plugin `franka_hardware/FrankaHardwareInterface` (registered through `franka_hardware.xml`) and also ships the `ros2_control` xacro macro library that declares the interfaces the plugin exports.

The package contains:

- **The hardware plugin**: every control cycle it reads the full robot state and writes one of the supported command modes (joint torque, joint velocity, joint position, Cartesian velocity, Cartesian pose; the last two optionally with the elbow).
- **The xacro macro library** under `ros2_control/`: `diana_arm.ros2_control.xacro`, `diana_arm_hardware_plugins.xacro` and `diana_ros2_control_macros.xacro`.
- **The parameter service node** (`service_server`): wraps the `Set*` services from [franka_msgs](franka_msgs.md).
- **The action server node** (`action_server`): provides the `ErrorRecovery` and `PTPMotion` actions.
- **A libfranka log bridge**: forwards libfranka log output to the ROS 2 logger.

The plugin is normally loaded by the `ros2_control_node` started by [diana_bringup](diana_bringup.md). Controllers should not talk to the plugin directly; use the [semantic components](franka_semantic_components.md) instead of hand-written raw interface names.

```{important}
Sending commands to a real robot makes it move. Before activating any controller, make sure the workspace is clear of people and obstacles, the emergency stop is within reach, and the external-control prerequisites described in [Safety Boundaries](../../../reference/safety.md) and the [FCI Overview](../../../fci/overview.md) are met.
```

## Exported Interfaces

In the tables below, `<P>` is the arm prefix (`arm_prefix` in the xacro, `modified_prefix` in bringup; empty when no prefix is set, otherwise something like `left_`) and `<T>` is `robot_type` (`diana3`, `diana7` or `diana7g2`). All interface types are `double`. The interface set comes from the xacro declarations and from the registrations in `export_state_interfaces()` / `export_command_interfaces()` in `franka_hardware_interface.cpp`.

### Joint Interfaces

Seven joints are exported: `<P><T>_joint1` to `<P><T>_joint7`. The number of joints in the plugin is fixed at 7.

| Interface | Direction | Source / meaning |
| --- | --- | --- |
| `<P><T>_jointN/position` | state | Measured joint position `q` (rad) |
| `<P><T>_jointN/velocity` | state | Measured joint velocity `dq` (rad/s) |
| `<P><T>_jointN/effort` | state | Measured joint torque `tau_J` (Nm) |
| `<P><T>_jointN/position` | command | Joint position command (rad) |
| `<P><T>_jointN/velocity` | command | Joint velocity command (rad/s) |
| `<P><T>_jointN/effort` | command | Joint torque command (Nm); declared when `include_effort_command` is true (bringup sets it to `true`) |

The `initial_value` of the position state interfaces (used by mock hardware) is, for joints 1 to 7: `0`, `-pi/4`, `0`, `3*pi/4`, `0`, `-pi/2`, `pi/4`.

### Cartesian Command Interfaces

Cartesian commands are exported as GPIO entries whose `index` parameter selects the position in the underlying command array.

| Interface | Count | Meaning |
| --- | --- | --- |
| `<P>vx/cartesian_velocity`, `<P>vy/...`, `<P>vz/...`, `<P>wx/...`, `<P>wy/...`, `<P>wz/...` | 6 (index 0 to 5) | Desired end-effector velocity in the base frame; linear in m/s, angular in rad/s |
| `<P>0/cartesian_pose_command` ... `<P>15/cartesian_pose_command` | 16 (index 0 to 15) | Desired end-effector pose as a 4x4 homogeneous transform in column-major order |
| `<P>0/cartesian_pose_state` ... `<P>15/cartesian_pose_state` | 16 (state) | Measured end-effector pose `O_T_EE`, column-major |

### Elbow Interfaces

| Interface | Direction | Meaning |
| --- | --- | --- |
| `<P>joint_3_position/elbow_command` | command (index 0) | Desired position of joint 3 |
| `<P>joint_4_sign/elbow_command` | command (index 1) | Desired flip direction of the elbow (joint 4) |
| `<P>joint_3_position/elbow_state` | state | Current joint 3 position of the elbow |
| `<P>joint_4_sign/elbow_state` | state | Current flip direction of the elbow |

Elbow commands can only be claimed together with the Cartesian velocity or Cartesian pose command interfaces; otherwise `perform_command_mode_switch` fails with a fatal log message.

### Force/Torque Sensor Interfaces

The xacro declares a sensor named `<P><T>_tcp` with the state interfaces `force.x`, `force.y`, `force.z`, `torque.x`, `torque.y` and `torque.z`. The plugin fills them, in the order declared in the xacro, with the estimated external wrench in the stiffness frame (`K_F_ext_hat_K`).

## Additional State Interfaces

Besides the joint, pose, elbow and sensor interfaces, the plugin exports two robot-level state interfaces that carry data which cannot be expressed as plain numbers, plus a robot-time interface:

| Interface | Content |
| --- | --- |
| `<P><T>/robot_state` | Address of the full robot state structure (`franka::RobotState`) stored in a `double` slot; used by [franka_semantic_components](franka_semantic_components.md) and [franka_robot_state_broadcaster](franka_robot_state_broadcaster.md) |
| `<P><T>/robot_model` | Address of the model object, used by the robot model class in the semantic components |
| `<P><T>/robot_time` | Robot time in seconds, a plain `double` |

```{warning}
`robot_state` and `robot_model` are pointers stored in a `double` and are only meaningful inside the same process. Do not read them as numbers and do not use them across processes; use the semantic component classes to convert them.
```

## ros2_control Macro Library

The macro files live in the package's `ros2_control/` directory and are installed to `share/franka_hardware/ros2_control`.

### diana_arm.ros2_control.xacro

Defines the macro `diana_arm_ros2_control`, which generates a `ros2_control` block of type `system` named `<arm_prefix>FrankaHardwareInterface`.

| Argument | Default | Purpose |
| --- | --- | --- |
| `robot_type` | required | Written to the hardware parameter `robot_type` and used to name joints, the sensor and interfaces |
| `include_effort_command` | `true` | Declares the `effort` command interface for every joint |
| `arm_prefix` | `''` | Prefix for joint and GPIO names; written to the hardware parameter `prefix` |
| `is_async` | `false` | Passed to `ros2_control` as `is_async`; when true, an `async` properties block is added |
| `thread_priority` | `98` | Thread priority of the async block (only used when `is_async` is true) |
| `hardware_plugin` (block parameter) | required | The `plugin` tag and its parameters, inserted into `hardware` |

The macro always writes the parameter `version` with the value `1.1.0`, then calls `configure_arm_interfaces` with the elbow, Cartesian pose and sensor options enabled (`sensor_name` is `<arm_prefix><robot_type>_tcp`).

### diana_arm_hardware_plugins.xacro

Provides macros that emit only the `plugin` tag and its parameters, for use in the `hardware_plugin` block above.

| Macro | Purpose |
| --- | --- |
| `diana_real_hardware_plugin` | Real robot: plugin `franka_hardware/FrankaHardwareInterface` with the parameters `robot_ip` and `arm_prefix` (both default to an empty string) |
| `diana_mock_hardware_plugin` | The generic mock system `mock_components/GenericSystem`; the argument `fake_sensor_commands` (default `false`) is written to `mock_sensor_commands`, and `state_following_offset` is `0.0` |
| `diana_selected_arm_hardware_plugin` | Chooses one of the two above based on `use_fake_hardware` |

### diana_ros2_control_macros.xacro

| Macro | Purpose |
| --- | --- |
| `configure_arm_joint` | One joint: `position`, `velocity` and (optionally) `effort` command interfaces, plus `position`, `velocity` and `effort` state interfaces |
| `configure_arm_joints` | Joints 1 to 7, using the initial positions listed above |
| `general_purpose_io` | One GPIO entry with a single command interface and an `index` parameter |
| `cartesian_velocity_io` | The six `vx` ... `wz` GPIO entries |
| `cartesian_pose_loop` | Recursive macro that generates the 16 `cartesian_pose_command` GPIO entries |
| `configure_arm_interfaces` | The complete single-arm interface set: joints, Cartesian velocity, optional elbow, optional Cartesian pose, optional sensor |

### Using the Macro in a Robot Description

The single-arm entry file `diana_bringup/urdf/diana.urdf.xacro` includes these macros and selects the plugin:

```xml
<xacro:diana_arm_ros2_control
    robot_type="$(arg robot_type)"
    include_effort_command="true"
    arm_prefix="${modified_prefix}"
    is_async="$(arg is_async)"
    thread_priority="$(arg thread_priority)">
  <hardware_plugin>
    <xacro:if value="$(arg use_fake_hardware)">
      <xacro:diana_mock_hardware_plugin fake_sensor_commands="$(arg fake_sensor_commands)"/>
    </xacro:if>
    <xacro:unless value="$(arg use_fake_hardware)">
      <xacro:diana_real_hardware_plugin robot_ip="$(arg robot_ip)" arm_prefix="${modified_prefix}"/>
    </xacro:unless>
  </hardware_plugin>
</xacro:diana_arm_ros2_control>
```

`robot_type` (required; `diana3`, `diana7` or `diana7g2`, matching your model), `robot_ip` (required for a real robot; the default address of the Diana controller's A network port is `192.168.10.75`), `use_fake_hardware`, `is_async` and `thread_priority` are xacro arguments of this file. `modified_prefix` is derived from `prefix` by the `diana_description` package (an underscore is appended when it is non-empty); that package is not part of this one. With `use_fake_hardware:=true` the generic mock system is used instead of `FrankaHardwareInterface` and no robot connection is made.

## Configuration

### Hardware Plugin Parameters

The plugin reads the following parameters from the `hardware` block in `on_init`:

| Parameter | Required | Description |
| --- | --- | --- |
| `version` | yes | `ros2_control` interface description version in the form `major.minor.patch`. The major version must be `1`, otherwise initialization fails and asks you to update the URDF |
| `robot_ip` | yes | Hostname or IP address of the robot; initialization fails if it is missing or the connection cannot be established |
| `robot_type` | yes (always written by the xacro macro) | `diana3`, `diana7` or `diana7g2`; used to compose the robot-level interface names (`<P><T>/robot_state` etc.) |
| `prefix` | no | Prefix for the robot-level interface names; it also determines the namespace of the parameter and action server nodes (see below). Empty when not set |

During `on_init` the plugin also starts two ROS 2 nodes in its own executor thread (see the Parameter Services and Action Services sections below).

### Command Rate Limiting and Filtering

`robot.hpp` holds optional command post-processing defaults as compile-time constants; there are no corresponding ROS parameters:

| Setting | Default |
| --- | --- |
| Torque command rate limiting | on |
| Joint velocity rate limiting | off |
| Joint position rate limiting and low-pass filter | off |
| Cartesian velocity rate limiting and low-pass filter | off |
| Cartesian pose rate limiting and low-pass filter | off |
| Low-pass cut-off frequency | 100 Hz |

```{note}
Running on a real-time kernel is strongly recommended; see [Real-time Network](../../../fci/realtime_network.md).
```

## Parameter Services

The plugin runs a node named `service_server` that provides the services below. Message definitions are in [franka_msgs](franka_msgs.md). The node namespace is derived from the hardware parameter `prefix`: the trailing underscore is removed and the rest is used as the namespace; without a prefix there is no namespace. The table lists the names without a namespace; with the prefix `left_` they take the form `/left/service_server/set_joint_stiffness`.

| Service | Type |
| --- | --- |
| `/service_server/set_joint_stiffness` | `franka_msgs/srv/SetJointStiffness` |
| `/service_server/set_cartesian_stiffness` | `franka_msgs/srv/SetCartesianStiffness` |
| `/service_server/set_tcp_frame` | `franka_msgs/srv/SetTCPFrame` |
| `/service_server/set_stiffness_frame` | `franka_msgs/srv/SetStiffnessFrame` |
| `/service_server/set_force_torque_collision_behavior` | `franka_msgs/srv/SetForceTorqueCollisionBehavior` |
| `/service_server/set_full_collision_behavior` | `franka_msgs/srv/SetFullCollisionBehavior` |
| `/service_server/set_load` | `franka_msgs/srv/SetLoad` |

Every response contains `success` and an `error` string; exceptions from the underlying library are reported there instead of crashing the plugin.

## Action Services

The plugin runs a node named `action_server`, with the same namespace rule as `service_server`. It provides two actions:

| Action | Type | Behavior |
| --- | --- | --- |
| `/action_server/error_recovery` | `franka_msgs/action/ErrorRecovery` | Accepts every goal and runs the robot's automatic error recovery; the goal succeeds when recovery returns and is aborted if an exception is thrown. Goal, result and feedback are empty |
| `/action_server/ptp_motion` | `franka_msgs/action/PTPMotion` | Accepts every goal and runs a point-to-point joint motion using the joint configuration, maximum joint velocities and tolerance from the goal, publishing `TargetStatus` as feedback; the goal succeeds when the target is reached and is aborted on error. Cancelling the goal stops the motion |

With the prefix `left_` the action names are `/left/action_server/error_recovery` and `/left/action_server/ptp_motion`. The action definitions are in [franka_msgs](franka_msgs.md).

The vectors in a `PTPMotion` goal must have the same length as the number of joints, otherwise the goal is aborted with an error message.

```{note}
Both nodes are created by the plugin inside the `ros2_control_node` process. You can list their actual names with:

~~~bash
ros2 service list | grep service_server
ros2 action list | grep action_server
~~~
```

## Error Recovery

### Behavior on Error

- If a control exception is thrown while reading or writing (for example a reflex triggered by a collision or a violated joint limit), the plugin logs it and latches the fault: `read()` stops refreshing the robot state (the exported state interfaces keep their pre-fault values), the next `write()` returns `DEACTIVATE`, and the controller manager moves the hardware component to the inactive state. The process does not exit.
- Once the hardware component is inactive, `on_deactivate` stops the robot control session, clears the fault latch and resets the active control mode; the state keeps being read afterwards, and `robot_mode`, `current_errors` and `last_motion_errors` in the robot state reflect the actual reflex condition.
- A network exception thrown while reading or writing returns `ERROR`.
- `write()` returns `ERROR` if any command value is not a finite number.
- A runtime error during a write while a command mode switch is in progress only logs a warning and skips that write.
- When starting a control session (`initializeTorqueInterface` and similar functions), if the robot reports a control exception the plugin runs one automatic error recovery and retries once.
- `on_activate` reads the robot state once first; if a fault is still latched, or the robot is in reflex mode or has active errors, activation fails and the log asks you to clear the robot error first.

```{important}
The plugin itself does not deactivate controllers. After an error, check the controller state yourself and follow the steps below to clear the error and explicitly reactivate the hardware component and the controllers.
```

### Recovery Steps

```{warning}
Reactivating a motion controller commands the robot again. Before you start, remove the cause of the error and make sure the workspace is clear of people and obstacles and the emergency stop is within reach. Do not retry recovery in a loop; see [Safety Boundaries](../../../reference/safety.md).
```

1. Find out why the robot stopped (the `robot_mode`, `current_errors` and `last_motion_errors` fields in the [robot state](franka_robot_state_broadcaster.md)) and remove the cause.
2. Send an error recovery goal to clear the robot error (with a prefix, put the namespace in front of the action name, for example `/left/action_server/error_recovery`):

   ```bash
   ros2 action send_goal /action_server/error_recovery franka_msgs/action/ErrorRecovery {}
   ```

3. Switch the hardware component back to the active state. The component name is `<arm_prefix>FrankaHardwareInterface`; you can look it up with `ros2 control list_hardware_components`:

   ```bash
   ros2 control set_hardware_component_state FrankaHardwareInterface active
   ```

4. Reactivate the command controller that should resume controlling the robot:

   ```bash
   ros2 control switch_controllers --activate <controller-name>
   ```

5. Confirm with `ros2 control list_hardware_components` that the hardware component is `active`.

```{note}
The order matters: the robot error must be cleared before the hardware component can be reactivated, and the hardware component must be active before controllers can be activated. Reactivating the hardware component before clearing the error fails and the log asks you to clear the robot error first.
```

## Control Modes

Controllers claim interfaces in `command_interface_configuration()`. The plugin infers the control mode from the claimed command interfaces, in the following priority order:

| Claimed command interfaces | Control mode |
| --- | --- |
| `effort` of all 7 joints | Joint torque |
| `velocity` of all 7 joints | Joint velocity |
| `position` of all 7 joints | Joint position |
| 16 `cartesian_pose_command` (+ 2 `elbow_command`) | Cartesian pose (optionally with elbow) |
| 6 `cartesian_velocity` (+ 2 `elbow_command`) | Cartesian velocity (optionally with elbow) |

Rules enforced by `prepare_command_mode_switch`:

- A group of interfaces must be claimed or released as a whole (7, 6, 16 or 2 interfaces). Claiming only part of a group reports an error such as `Invalid number of ... interfaces to start`.
- Elbow commands must be claimed together with Cartesian pose or velocity.
- Every mode switch stops the current control session and starts a new one. In the position, pose and elbow modes the plugin first initializes the commands from the current robot state; until then no commands are written to the robot.

```{tip}
In controllers, use the classes from [franka_semantic_components](franka_semantic_components.md) instead of listing raw interface names; they generate the correctly prefixed names for you.
```

To see what the plugin currently exports:

```bash
ros2 control list_hardware_interfaces
ros2 control list_hardware_components
```

```{note}
The code snippets on this page are adapted from `diana_ros2`, whose source follows the franka_ros2 structure and carries the copyright notice of Franka Robotics GmbH (Copyright (c) 2023 Franka Robotics GmbH, Apache License 2.0); the adapted parts are Copyright (c) 2026 Agile Robots SE. See "License and Third-Party Notices" in the [Manual Overview](/about/overview.md).
```

# `diana_robot_state_broadcaster`

## Installation

See [Development Setup](../development.md).

## Package Overview

`diana_robot_state_broadcaster` is a `ros2_control` controller plugin (`diana_robot_state_broadcaster/DianaRobotStateBroadcaster`) that publishes the full robot state of a Diana robot. It claims the `robot_state` state interface (its name is built from the `robot_type` and `arm_prefix` parameters), exported by [diana_hardware](diana_hardware.md), converts it with [DianaRobotState](diana_semantic_components.md) into a `diana_msgs/msg/DianaRobotState` message and publishes it. It claims no command interfaces.

Implementation notes taken from the source:

- `update()` runs in the real-time loop and only copies the state into a lock-free triple buffer; publishing happens in a separate thread so that the control loop is never blocked.
- The publish thread requests `SCHED_FIFO` priority 50. If this is not permitted, a warning is logged and the thread runs at normal priority; messages may then be coalesced. Granting `CAP_SYS_NICE` (or running with sufficient rights) enables real-time scheduling.
- The controller assumes a controller manager `update_rate` of 1000 Hz (constant `kUpdateRate`).

```{figure} ../../../../_static/images/ros2-humble-broadcaster-flow-en.png
:alt: Data flow of the robot state broadcaster
:width: 100%

Data flow: `update()` only copies the state into a lock-free buffer in the real-time loop, and a separate publisher thread publishes the full state and the convenience topics.
```

## Published Topics

All topics are relative to the controller node (`~/`), so with no namespace they are `/diana_robot_state_broadcaster/<name>`, and `/<namespace>/diana_robot_state_broadcaster/<name>` with a namespace.

### Full Robot State

| Topic | Type | Rate | QoS |
| --- | --- | --- | --- |
| `~/robot_state` | `diana_msgs/msg/DianaRobotState` | controller update rate (1000 Hz) | system default |

The full state is always published at the controller update rate, independent of the parameter `convenience_publish_rate`.

### Convenience Topics

Each convenience topic republishes one field of the same sample, with QoS best effort and history depth 1:

| Topic | Type | Source field |
| --- | --- | --- |
| `~/current_pose` | `geometry_msgs/msg/PoseStamped` | `o_t_ee` |
| `~/last_desired_pose` | `geometry_msgs/msg/PoseStamped` | `o_t_ee_d` |
| `~/desired_end_effector_twist` | `geometry_msgs/msg/TwistStamped` | `o_dp_ee_d` |
| `~/measured_joint_states` | `sensor_msgs/msg/JointState` | `measured_joint_state` |
| `~/desired_joint_states` | `sensor_msgs/msg/JointState` | `desired_joint_state` |
| `~/external_joint_torques` | `sensor_msgs/msg/JointState` | `tau_ext_hat_filtered` |
| `~/external_wrench_in_stiffness_frame` | `geometry_msgs/msg/WrenchStamped` | `k_f_ext_hat_k` |
| `~/external_wrench_in_base_frame` | `geometry_msgs/msg/WrenchStamped` | `o_f_ext_hat_k` |

Their rate is `convenience_publish_rate` Hz, limited to 1000 Hz: the broadcaster publishes every N-th cycle with `N = max(1, 1000 / convenience_publish_rate)`. If the requested rate does not divide 1000 evenly, a warning is logged and the effective rate is `1000 / N`. For example, `300` gives `N = 3` and an effective 333 Hz.

```{note}
Subscribers of the convenience topics must use a compatible QoS (best effort) to receive messages, for example `ros2 topic echo --qos-reliability best_effort`.
```

## Parameters

Defined in `src/diana_robot_state_broadcaster_parameters.yaml` (generated with `generate_parameter_library`):

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `robot_type` | string | required | set it to your robot model (`diana3`, `diana7` or `diana7g2`); used to build the claimed interface name |
| `arm_prefix` | string | `""` | arm prefix, used to build the interface name |
| `convenience_publish_rate` | int | `1000` | publish rate in Hz of the convenience topics; must be at least 1 |

The `controllers.yaml` of [diana_bringup](diana_bringup.md) sets `convenience_publish_rate: 1000` for the controller.

```{important}
`robot_type` and `arm_prefix` must match the hardware interface names: set `robot_type` to your robot model (`diana3`, `diana7` or `diana7g2`), and if you use an `arm_prefix`, set the same `arm_prefix` for this broadcaster. Set these parameters in your controller parameter file; otherwise the claimed interface name will not match the hardware.
```

## Usage

### Starting the Broadcaster

`diana.launch.py` of [diana_bringup](diana_bringup.md) spawns the broadcaster with the controller manager spawner, together with `joint_state_broadcaster`. It does so only when `use_fake_hardware` is not `true`, because the `robot_state` interface exists only in the real hardware plugin:

```bash
ros2 launch diana_bringup diana.launch.py robot_type:=diana3 robot_ip:=<robot-ip>
```

### Inspecting the Topics

```bash
ros2 topic list | grep diana_robot_state_broadcaster
ros2 topic hz /diana_robot_state_broadcaster/robot_state
ros2 topic echo /diana_robot_state_broadcaster/current_pose --qos-reliability best_effort
ros2 topic echo /diana_robot_state_broadcaster/external_wrench_in_stiffness_frame --qos-reliability best_effort
ros2 topic echo --field robot_mode /diana_robot_state_broadcaster/robot_state
```

The full state is large and published at 1 kHz; prefer `--field`, `--once` or `ros2 topic hz` over echoing the whole message.

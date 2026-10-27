# Robot State Broadcaster

Package name: `franka_robot_state_broadcaster`

## Installation

See [Development Setup](../development.md).

## Package Overview

`franka_robot_state_broadcaster` is a `ros2_control` controller plugin (`franka_robot_state_broadcaster/FrankaRobotStateBroadcaster`) that publishes the full robot state. It claims the `robot_state` state interface exported by [franka_hardware](franka_hardware.md), converts it with [FrankaRobotState](franka_semantic_components.md) into a `franka_msgs/msg/FrankaRobotState` message (see [franka_msgs](franka_msgs.md)) and publishes it. It also republishes several fields of that state as standard ROS messages on convenience topics. It claims no command interfaces.

The claimed state interface is named `<arm_prefix>_<robot_type>/robot_state`, or `<robot_type>/robot_state` when `arm_prefix` is empty.

## Published Topics

All topics are relative to the controller node (`~/`): `/franka_robot_state_broadcaster/<name>` without a namespace, `/<namespace>/franka_robot_state_broadcaster/<name>` with one.

### Full Robot State

| Topic | Type | Rate | QoS |
| --- | --- | --- | --- |
| `~/robot_state` | `franka_msgs/msg/FrankaRobotState` | controller update rate | system defaults |

The full state is published once per controller update cycle, independent of the `convenience_publish_rate` parameter. The header stamp is the `update()` time of that cycle. In the `controllers.yaml` of [diana_bringup](diana_bringup.md) the controller manager `update_rate` is 1000 Hz.

### Convenience Topics

Each convenience topic republishes one field of the same sample, with best-effort QoS and history depth 1:

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

Convenience topics are published every N-th new sample, where `N = max(1, update_rate / min(convenience_publish_rate, update_rate))` and `update_rate` is the update rate of this controller; the effective rate is `update_rate / N`. If the requested rate does not divide the update rate evenly, a warning is logged and the effective rate applies. For example, with a 1000 Hz update rate and `convenience_publish_rate` set to `300`, `N = 3` and the effective rate is about 333 Hz.

```{note}
Subscribers to the convenience topics must use a compatible QoS (best effort) to receive messages, for example `ros2 topic echo --qos-reliability best_effort`.
```

## Parameters

Defined in `src/franka_robot_state_broadcaster_parameters.yaml` (generated with `generate_parameter_library`):

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `robot_type` | string | Required | Used to build the claimed interface name; set it to your robot model (`diana3`, `diana7` or `diana7g2`) |
| `arm_prefix` | string | `""` | Arm prefix; when non-empty the interface name is `<arm_prefix>_<robot_type>/robot_state` |
| `convenience_publish_rate` | int | `1000` | Publish rate of the convenience topics in Hz, at least 1; values above the update rate are treated as the update rate and rounded down to a whole divisor of it |

The `controllers.yaml` of [diana_bringup](diana_bringup.md) sets `convenience_publish_rate: 1000` for this controller.

```{important}
`robot_type` and `arm_prefix` must match the hardware interface names. Otherwise the claimed interface does not match what [franka_hardware](franka_hardware.md) exports and the controller cannot be activated. Set `robot_type` to your robot model, and when you use `arm_prefix`, set the same `arm_prefix` for this broadcaster.
```

## Threading and Real-Time Behavior

- `update()` runs in the controller manager loop: it reads the `robot_state` interface, writes the state into an internal triple buffer (`AsyncBuffer`), wakes the publish thread and returns. All publishing happens on a dedicated publish thread, so the publish cost does not take time from the control loop.
- The publish thread is started in `on_activate()` and stopped in `on_deactivate()`. On start the buffer is drained so that state left over from a previous activation is not published.
- The publish thread requests `SCHED_FIFO` priority 30 (`kPublishThreadPriority`), below the controller manager real-time loop. Without permission a warning is logged and it runs at normal priority; messages may then be coalesced. Grant `CAP_SYS_NICE` (or run with sufficient privileges) to enable real-time scheduling.
- Keep the controller synchronous (`is_async: false`) so that it shares the controller manager thread with model-based controllers that also read the robot state; running it asynchronously logs a warning.

## Usage

### Starting the Broadcaster

`diana.launch.py` of [diana_bringup](diana_bringup.md) starts the broadcaster through the controller manager spawner. The launch argument `load_franka_robot_state_broadcaster` (default `true`) controls this; it is not started when `use_fake_hardware` is `true`, because the `robot_state` interface only exists in the real hardware plugin. `robot_type` and `robot_ip` are required arguments and must be passed explicitly:

```bash
ros2 launch diana_bringup diana.launch.py robot_type:=diana3 robot_ip:=192.168.10.75
```

### Inspecting the Topics

```bash
ros2 topic list | grep franka_robot_state_broadcaster
ros2 topic hz /franka_robot_state_broadcaster/robot_state
ros2 topic echo /franka_robot_state_broadcaster/current_pose --qos-reliability best_effort
ros2 topic echo /franka_robot_state_broadcaster/external_wrench_in_stiffness_frame --qos-reliability best_effort
ros2 topic echo --field robot_mode /franka_robot_state_broadcaster/robot_state
```

With a namespace (for example `namespace:=NS1`), prefix the topics with `/NS1`. The full state is large and published at the update rate; use `--field`, `--once` or `ros2 topic hz` instead of printing whole messages.

```{note}
This page is adapted from `franka_ros2`, whose source carries the Franka Robotics GmbH copyright notice (Copyright (c) 2023 Franka Robotics GmbH, Apache License 2.0). See "License and third-party notices" in the [manual overview](/about/overview.md).
```

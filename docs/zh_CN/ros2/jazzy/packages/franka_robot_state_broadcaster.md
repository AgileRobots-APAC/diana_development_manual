# 机器人状态广播器

软件包名称：`franka_robot_state_broadcaster`

## 安装

请参阅 [开发准备](../development.md)。

## 软件包概述

`franka_robot_state_broadcaster` 是一个 `ros2_control` 控制器插件（`franka_robot_state_broadcaster/FrankaRobotStateBroadcaster`），用于发布机器人的完整状态。它申请由 [franka_hardware](franka_hardware.md) 导出的 `robot_state` 状态接口，经 [FrankaRobotState](franka_semantic_components.md) 转换为 `franka_msgs/msg/FrankaRobotState` 消息（见 [franka_msgs](franka_msgs.md)）后发布，同时把状态中的若干字段重新发布为标准 ROS 消息的便捷话题。它不申请任何命令接口。

所申请的状态接口名为 `<arm_prefix>_<robot_type>/robot_state`；`arm_prefix` 为空时为 `<robot_type>/robot_state`。

## 发布的话题

所有话题都相对于控制器节点（`~/`）：无命名空间时为 `/franka_robot_state_broadcaster/<name>`，有命名空间时为 `/<namespace>/franka_robot_state_broadcaster/<name>`。

### 完整机器人状态

| 话题 | 类型 | 频率 | QoS |
| --- | --- | --- | --- |
| `~/robot_state` | `franka_msgs/msg/FrankaRobotState` | 控制器更新频率 | 系统默认 |

完整状态在每个控制器更新周期发布一次，与参数 `convenience_publish_rate` 无关；消息头的时间戳取自该周期的 `update()` 时间。[diana_bringup](diana_bringup.md) 的 `controllers.yaml` 中 controller manager 的 `update_rate` 为 1000 Hz。

### 便捷话题

每个便捷话题重新发布同一采样中的一个字段，QoS 为 best effort，历史深度为 1：

| 话题 | 类型 | 来源字段 |
| --- | --- | --- |
| `~/current_pose` | `geometry_msgs/msg/PoseStamped` | `o_t_ee` |
| `~/last_desired_pose` | `geometry_msgs/msg/PoseStamped` | `o_t_ee_d` |
| `~/desired_end_effector_twist` | `geometry_msgs/msg/TwistStamped` | `o_dp_ee_d` |
| `~/measured_joint_states` | `sensor_msgs/msg/JointState` | `measured_joint_state` |
| `~/desired_joint_states` | `sensor_msgs/msg/JointState` | `desired_joint_state` |
| `~/external_joint_torques` | `sensor_msgs/msg/JointState` | `tau_ext_hat_filtered` |
| `~/external_wrench_in_stiffness_frame` | `geometry_msgs/msg/WrenchStamped` | `k_f_ext_hat_k` |
| `~/external_wrench_in_base_frame` | `geometry_msgs/msg/WrenchStamped` | `o_f_ext_hat_k` |

便捷话题每 N 个新采样发布一次，其中 `N = max(1, update_rate / min(convenience_publish_rate, update_rate))`，`update_rate` 为该控制器的更新频率，实际频率为 `update_rate / N`。若所设频率不能整除更新频率，会记录警告并按实际频率发布。例如更新频率为 1000 Hz、`convenience_publish_rate` 设为 `300` 时，`N = 3`，实际约 333 Hz。

```{note}
便捷话题的订阅方必须使用兼容的 QoS（best effort）才能收到消息，例如 `ros2 topic echo --qos-reliability best_effort`。
```

## 参数

定义于 `src/franka_robot_state_broadcaster_parameters.yaml`（由 `generate_parameter_library` 生成）：

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `robot_type` | string | 必填 | 用于拼出所申请的接口名；请设为你的机器人型号（`diana3`、`diana7` 或 `diana7g2`） |
| `arm_prefix` | string | `""` | 机械臂前缀，非空时接口名为 `<arm_prefix>_<robot_type>/robot_state` |
| `convenience_publish_rate` | int | `1000` | 便捷话题的发布频率（Hz），不得小于 1；超过更新频率时按更新频率处理，并向下取为其整除频率 |

[diana_bringup](diana_bringup.md) 的 `controllers.yaml` 为该控制器设置了 `convenience_publish_rate: 1000`。

```{important}
`robot_type` 和 `arm_prefix` 必须与硬件接口名一致，否则所申请的接口名将与 [franka_hardware](franka_hardware.md) 导出的接口不匹配，控制器无法激活。请把 `robot_type` 设为你的机器人型号；使用了 `arm_prefix` 时，也要为该广播器设置相同的 `arm_prefix`。
```

## 线程与实时行为

- `update()` 在 controller manager 的循环中运行：它读取 `robot_state` 接口、把状态写入内部三重缓冲区（`AsyncBuffer`）并唤醒发布线程，随即返回。所有话题的发布都在独立的发布线程中完成，因此发布开销不会占用控制循环。
- 发布线程在 `on_activate()` 时启动，在 `on_deactivate()` 时停止。启动时会清空缓冲区中的旧数据，避免发布上一次激活留下的状态。
- 发布线程请求 `SCHED_FIFO` 优先级 30（`kPublishThreadPriority`），低于 controller manager 的实时循环。若无权限，会记录警告并以普通优先级运行，此时消息可能被合并。授予 `CAP_SYS_NICE`（或以足够权限运行）即可启用实时调度。
- 建议保持控制器同步运行（`is_async: false`），使其与同样读取机器人状态的基于模型的控制器共用 controller manager 线程；以异步方式运行时会记录警告。

## 使用

### 启动广播器

[diana_bringup](diana_bringup.md) 的 `diana.launch.py` 通过 controller manager 的 spawner 启动该广播器。启动参数 `load_franka_robot_state_broadcaster`（默认 `true`）控制是否启动；`use_fake_hardware` 为 `true` 时不会启动，因为 `robot_state` 接口只存在于真实硬件插件中。`robot_type` 与 `robot_ip` 为必须显式给出的参数：

```bash
ros2 launch diana_bringup diana.launch.py robot_type:=diana3 robot_ip:=192.168.10.75
```

### 查看话题

```bash
ros2 topic list | grep franka_robot_state_broadcaster
ros2 topic hz /franka_robot_state_broadcaster/robot_state
ros2 topic echo /franka_robot_state_broadcaster/current_pose --qos-reliability best_effort
ros2 topic echo /franka_robot_state_broadcaster/external_wrench_in_stiffness_frame --qos-reliability best_effort
ros2 topic echo --field robot_mode /franka_robot_state_broadcaster/robot_state
```

使用命名空间（例如 `namespace:=NS1`）时，话题前需加上 `/NS1`。完整状态数据量大且按更新频率发布；建议使用 `--field`、`--once` 或 `ros2 topic hz`，不要直接打印整条消息。

```{note}
本页内容改编自 `franka_ros2`，其源码带有 Franka Robotics GmbH 的版权声明（Copyright (c) 2023 Franka Robotics GmbH，Apache License 2.0）。详见[手册概述](/about/overview.md)中的“许可证与第三方声明”。
```

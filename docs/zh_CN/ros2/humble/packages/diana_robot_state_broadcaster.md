# 机器人状态广播器

软件包名称：`diana_robot_state_broadcaster`

## 安装

请参阅 [开发准备](../development.md)。

## 软件包概述

`diana_robot_state_broadcaster` 是一个 `ros2_control` 控制器插件（`diana_robot_state_broadcaster/DianaRobotStateBroadcaster`），用于发布 Diana 机器人的完整状态。它申请由 [diana_hardware](diana_hardware.md) 导出的 `robot_state` 状态接口（接口名由 `robot_type` 与 `arm_prefix` 参数拼出），经 [DianaRobotState](diana_semantic_components.md) 转换为 `diana_msgs/msg/DianaRobotState` 消息后发布。它不申请任何命令接口。

以下实现要点来自源码：

- `update()` 在实时循环中运行，只把状态拷贝到无锁三重缓冲区；发布在独立线程中完成，因此控制循环不会被阻塞。
- 发布线程请求 `SCHED_FIFO` 优先级 50。若无权限，会记录警告并以普通优先级运行，此时消息可能被合并。授予 `CAP_SYS_NICE`（或以足够权限运行）即可启用实时调度。
- 控制器假定 controller manager 的 `update_rate` 为 1000 Hz（常量 `kUpdateRate`）。

```{figure} ../../../../_static/images/ros2-humble-broadcaster-flow-zh.png
:alt: 机器人状态广播器的数据流
:width: 100%

数据流：`update()` 在实时循环中只把状态拷贝到无锁缓冲区，由独立的发布线程发布完整状态和便捷话题。
```

## 发布的话题

所有话题都相对于控制器节点（`~/`）：无命名空间时为 `/diana_robot_state_broadcaster/<name>`，有命名空间时为 `/<namespace>/diana_robot_state_broadcaster/<name>`。

### 完整机器人状态

| 话题 | 类型 | 频率 | QoS |
| --- | --- | --- | --- |
| `~/robot_state` | `diana_msgs/msg/DianaRobotState` | 控制器更新频率（1000 Hz） | 系统默认 |

完整状态始终按控制器更新频率发布，与参数 `convenience_publish_rate` 无关。

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

其频率为 `convenience_publish_rate` Hz，上限 1000 Hz：广播器每 N 个周期发布一次，`N = max(1, 1000 / convenience_publish_rate)`。若所设频率不能整除 1000，会记录警告，实际频率为 `1000 / N`。例如设为 `300` 时 `N = 3`，实际约 333 Hz。

```{note}
便捷话题的订阅方必须使用兼容的 QoS（best effort）才能收到消息，例如 `ros2 topic echo --qos-reliability best_effort`。
```

## 参数

定义于 `src/diana_robot_state_broadcaster_parameters.yaml`（由 `generate_parameter_library` 生成）：

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `robot_type` | string | 必填 | 设为你的机器人型号（`diana3`、`diana7` 或 `diana7g2`），用于拼出所申请的接口名 |
| `arm_prefix` | string | `""` | 机械臂前缀，用于拼出接口名 |
| `convenience_publish_rate` | int | `1000` | 便捷话题的发布频率（Hz）；不得小于 1 |

[diana_bringup](diana_bringup.md) 的 `controllers.yaml` 为该控制器设置了 `convenience_publish_rate: 1000`。

```{important}
`robot_type` 和 `arm_prefix` 必须与硬件接口名一致：请把 `robot_type` 设为你的机器人型号（`diana3`、`diana7` 或 `diana7g2`）；使用了 `arm_prefix` 时，也要为该广播器设置相同的 `arm_prefix`。请在你的控制器参数文件中设置这些参数，否则所申请的接口名将与硬件不匹配。
```

## 使用

### 启动广播器

[diana_bringup](diana_bringup.md) 的 `diana.launch.py` 通过 controller manager 的 spawner 启动该广播器，同时启动 `joint_state_broadcaster`。仅当 `use_fake_hardware` 不为 `true` 时才会启动，因为 `robot_state` 接口只存在于真实硬件插件中：

```bash
ros2 launch diana_bringup diana.launch.py robot_type:=diana3 robot_ip:=<robot-ip>
```

### 查看话题

```bash
ros2 topic list | grep diana_robot_state_broadcaster
ros2 topic hz /diana_robot_state_broadcaster/robot_state
ros2 topic echo /diana_robot_state_broadcaster/current_pose --qos-reliability best_effort
ros2 topic echo /diana_robot_state_broadcaster/external_wrench_in_stiffness_frame --qos-reliability best_effort
ros2 topic echo --field robot_mode /diana_robot_state_broadcaster/robot_state
```

完整状态数据量大且以 1 kHz 发布；建议使用 `--field`、`--once` 或 `ros2 topic hz`，不要直接打印整条消息。

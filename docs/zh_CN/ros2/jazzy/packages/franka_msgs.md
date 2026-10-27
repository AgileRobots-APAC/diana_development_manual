# 消息、服务与动作

软件包名称：`franka_msgs`

## 安装

请参阅 [开发准备](../development.md)。

## 软件包概述

`franka_msgs` 包含 Diana ROS 2 各软件包共用的消息、服务和动作定义，本身不含节点。依赖 `builtin_interfaces`、`std_msgs`、`action_msgs`、`sensor_msgs` 和 `geometry_msgs`。

| 类别 | 定义 |
| --- | --- |
| 消息 | `FrankaRobotState`、`CollisionIndicators`、`Elbow`、`Errors`、`TargetStatus` |
| 服务 | `SetCartesianStiffness`、`SetForceTorqueCollisionBehavior`、`SetFullCollisionBehavior`、`SetJointStiffness`、`SetLoad`、`SetStiffnessFrame`、`SetTCPFrame` |
| 动作 | `ErrorRecovery`、`PTPMotion` |

使用者：[franka_hardware](franka_hardware.md)（服务以及 `ErrorRecovery`、`PTPMotion` 动作）、[franka_semantic_components](franka_semantic_components.md) 和 [franka_robot_state_broadcaster](franka_robot_state_broadcaster.md)（`FrankaRobotState`）。

## 消息

### FrankaRobotState

`franka_msgs/msg/FrankaRobotState` 携带完整的机器人状态，由 [franka_robot_state_broadcaster](franka_robot_state_broadcaster.md) 发布。字段名均为小写。力旋量、位姿、速度旋量和惯量字段使用带时间戳的 geometry 消息类型。

| 分组 | 字段 | 类型 | 含义 |
| --- | --- | --- | --- |
| 消息头 | `header` | `std_msgs/Header` | 采样时间戳 |
| 碰撞 | `collision_indicators` | `CollisionIndicators` | 当前接触与碰撞标志 |
| 关节空间 | `measured_joint_state` | `sensor_msgs/JointState` | 测量位置 `q`、速度 `dq`、力矩 `tau_J` |
| 关节空间 | `desired_joint_state` | `sensor_msgs/JointState` | 期望位置 `q_d`、速度 `dq_d`、力矩 `tau_J_d` |
| 关节空间 | `measured_joint_motor_state` | `sensor_msgs/JointState` | 电机位置 `theta` 和速度 `dtheta` |
| 关节空间 | `ddq_d` | `float64[7]` | 期望关节加速度 |
| 关节空间 | `dtau_j` | `float64[7]` | 测量力矩信号的导数 |
| 关节空间 | `tau_ext_hat_filtered` | `sensor_msgs/JointState` | 滤波后的外部力矩（在 `effort` 中） |
| 肘部 | `elbow` | `Elbow` | 肘部状态、期望值与命令值 |
| 外力旋量 | `k_f_ext_hat_k` | `geometry_msgs/WrenchStamped` | 刚度坐标系下估计的外力旋量 |
| 外力旋量 | `o_f_ext_hat_k` | `geometry_msgs/WrenchStamped` | 基坐标系下估计的外力旋量 |
| 惯量 | `inertia_ee` | `geometry_msgs/InertiaStamped` | 末端执行器惯量 |
| 惯量 | `inertia_load` | `geometry_msgs/InertiaStamped` | 负载惯量 |
| 惯量 | `inertia_total` | `geometry_msgs/InertiaStamped` | 总惯量（末端 + 负载） |
| 位姿 | `o_t_ee` | `geometry_msgs/PoseStamped` | 基坐标系下末端测量位姿 |
| 位姿 | `o_t_ee_d` | `geometry_msgs/PoseStamped` | 运动生成最近一次的期望末端位姿 |
| 位姿 | `o_t_ee_c` | `geometry_msgs/PoseStamped` | 运动生成最近一次的命令末端位姿 |
| 位姿 | `f_t_ee` | `geometry_msgs/PoseStamped` | 法兰到末端坐标系 |
| 位姿 | `ee_t_k` | `geometry_msgs/PoseStamped` | 末端到刚度坐标系 |
| 速度 / 加速度 | `o_dp_ee_d` | `geometry_msgs/TwistStamped` | 基坐标系下末端期望速度旋量 |
| 速度 / 加速度 | `o_dp_ee_c` | `geometry_msgs/TwistStamped` | 基坐标系下最近一次命令的末端速度旋量 |
| 速度 / 加速度 | `o_ddp_ee_c` | `geometry_msgs/AccelStamped` | 基坐标系下最近一次命令的末端加速度 |
| 附加信息 | `time` | `float64` | 机器人时间（秒） |
| 附加信息 | `control_command_success_rate` | `float64` | 控制命令成功率 |
| 附加信息 | `robot_mode` | `uint8` | 下表 `ROBOT_MODE_*` 常量之一 |
| 错误 | `current_errors` | `Errors` | 当前处于激活状态的错误 |
| 错误 | `last_motion_errors` | `Errors` | 导致上一次运动停止的错误 |
| 加速度计 | `accelerometer_top` | `geometry_msgs/Vector3Stamped[6]` | 关节 1 至 6 上安装的加速度计的平移加速度 |
| 加速度计 | `accelerometer_bottom` | `geometry_msgs/Vector3Stamped[6]` | 关节 1 至 6 上安装的加速度计的平移加速度 |

关节 1 至 6 分别安装在连杆 0 至 5 上，关节 7 没有加速度计。每个元素的数据在其 `header` 中所标明的 `<prefix>link<i>_accelerometer_<side>` 坐标系下表示。

`robot_mode` 的常量：

| 常量 | 值 |
| --- | --- |
| `ROBOT_MODE_OTHER` | 0 |
| `ROBOT_MODE_IDLE` | 1 |
| `ROBOT_MODE_MOVE` | 2 |
| `ROBOT_MODE_GUIDING` | 3 |
| `ROBOT_MODE_REFLEX` | 4 |
| `ROBOT_MODE_USER_STOPPED` | 5 |
| `ROBOT_MODE_AUTOMATIC_ERROR_RECOVERY` | 6 |

### 辅助消息

| 消息 | 字段 | 用途 |
| --- | --- | --- |
| `CollisionIndicators` | `is_cartesian_linear_collision`、`is_cartesian_angular_collision`、`is_cartesian_linear_contact`、`is_cartesian_angular_contact`（均为 `geometry_msgs/Vector3`）；`is_joint_collision`、`is_joint_contact`（均为 `float64[7]`） | 哪些笛卡尔方向和关节存在碰撞或接触标志 |
| `Elbow` | `position`、`desired_position`、`commanded_position`、`commanded_velocity`、`commanded_acceleration`（均为 `float64[2]`） | 各量对应的肘部配置，格式为 `[joint_3_position, joint_4_sign]` |
| `Errors` | 36 个 `bool` 标志，例如 `joint_position_limits_violation`、`cartesian_velocity_violation`、`joint_reflex`、`cartesian_reflex`、`communication_constraints_violation`、`power_limit_violation`、`instability_detected` | 每个控制器或运动生成器错误对应一个标志；完整列表见 `msg/Errors.msg` |
| `TargetStatus` | `status`（`uint8`）；常量 `IDLE`=0、`EXECUTING`=1、`TARGET_REACHED`=2、`ABORTED`=3 | 运动动作的状态 |

## 服务

所有服务的响应相同：`bool success` 和 `string error`。数组均为固定长度。这些服务由 [franka_hardware](franka_hardware.md) 插件中的 `service_server` 节点提供。

### 服务定义

| 服务 | 请求字段 | 含义 |
| --- | --- | --- |
| `SetJointStiffness` | `float64[7] joint_stiffness` | 内部控制器中各关节的阻抗 |
| `SetCartesianStiffness` | `float64[6] cartesian_stiffness` | 刚度坐标系下的笛卡尔刚度（x、y、z、roll、pitch、yaw） |
| `SetTCPFrame` | `float64[16] transformation` | 描述 TCP 坐标系与末端执行器坐标系之间关系的 4x4 列主序变换 |
| `SetStiffnessFrame` | `float64[16] transformation` | 刚度坐标系相对 TCP 坐标系的 4x4 列主序变换 |
| `SetLoad` | `float64 mass`、`float64[3] center_of_mass`、`float64[9] load_inertia` | 负载质量、质心以及 3x3 列主序惯量 |
| `SetForceTorqueCollisionBehavior` | `float64[7] lower_torque_thresholds_nominal`、`float64[7] upper_torque_thresholds_nominal`、`float64[6] lower_force_thresholds_nominal`、`float64[6] upper_force_thresholds_nominal` | 碰撞与接触阈值 |
| `SetFullCollisionBehavior` | 上述四个字段，外加 `lower_torque_thresholds_acceleration`、`upper_torque_thresholds_acceleration`（`float64[7]`）、`lower_force_thresholds_acceleration`、`upper_force_thresholds_acceleration`（`float64[6]`） | 包含加速度相关阈值在内的碰撞与接触阈值 |

```{warning}
这些服务会修改机器人控制器的阻抗、工具坐标系、负载和碰撞阈值。数值不当会改变机器人对接触的反应，可能导致意外运动或漏检碰撞。请设置与实际工具和工作空间相符的值，并保持急停触手可及，参见[安全边界](../../../reference/safety.md)。
```

### 调用服务

示例按不带命名空间的服务名书写；设置了机械臂前缀（例如 `left_`）时，服务名前加命名空间，如 `/left/service_server/set_load`，详见 [franka_hardware](franka_hardware.md)。

设置负载（质量 kg，质心 m，惯量 kg m^2）：

```bash
ros2 service call /service_server/set_load franka_msgs/srv/SetLoad \
  "{mass: 0.5, center_of_mass: [0.0, 0.0, 0.05], load_inertia: [0.001, 0.0, 0.0, 0.0, 0.001, 0.0, 0.0, 0.0, 0.001]}"
```

设置关节刚度：

```bash
ros2 service call /service_server/set_joint_stiffness franka_msgs/srv/SetJointStiffness \
  "{joint_stiffness: [600.0, 600.0, 600.0, 600.0, 250.0, 150.0, 50.0]}"
```

把 TCP 坐标系设为与末端执行器坐标系重合（单位变换，列主序）：

```bash
ros2 service call /service_server/set_tcp_frame franka_msgs/srv/SetTCPFrame \
  "{transformation: [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0]}"
```

```{note}
以上数值仅用于说明参数格式。有效范围取决于你的机器人型号和工具。
```

## 动作

### 动作定义

| 动作 | 目标 | 结果 | 反馈 |
| --- | --- | --- | --- |
| `ErrorRecovery` | 空 | 空 | 空 |
| `PTPMotion` | `float64[] goal_joint_configuration`（rad）、`float64[] maximum_joint_velocities`（rad/s）、`float64 goal_tolerance`（rad） | `TargetStatus target_status`、`string error_message` | `TargetStatus target_status` |

`PTPMotion` 在以下两个条件同时满足时判定为到达目标：各关节当前位置与目标位置之差的绝对值在 `goal_tolerance` 之内，且关节速度低于一个很小的阈值。`error_message` 在失败时给出原因。

这两个动作由 [franka_hardware](franka_hardware.md) 插件中的 `action_server` 节点提供；`ErrorRecovery` 的使用步骤见该页的“错误恢复”一节。

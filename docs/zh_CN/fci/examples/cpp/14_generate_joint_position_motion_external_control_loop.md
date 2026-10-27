# 14 关节位置外部控制循环

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

源文件：`libfranka/examples/<model>/generate_joint_position_motion_external_control_loop.cpp`。

以外部控制循环发送关节位置目标，并在写入前对目标进行速度、加速度和加加速度限幅。

`<model>` 为已应用补丁的 `diana3`、`diana7` 或 `diana7G2`。

```bash
./build/libfranka/examples/<model>/generate_joint_position_motion_external_control_loop <robot-ip>
```

| 使用的接口 | 本示例中的用途 |
|---|---|
| `startJointPositionControl()` | 启动关节位置外部控制会话。 |
| `getLowerJointVelocityLimits()` | 按参考关节位置获取关节速度下限。 |
| `getUpperJointVelocityLimits()` | 按参考关节位置获取关节速度上限。 |
| `limitRate()` | 对目标关节位置进行速度、加速度和加加速度限幅。 |
## Example 调用流程

移至初始姿态 → startJointPositionControl() → 每周期 readOnce() → 按参考关节位置获取关节速度上下限 → limitRate() → writeOnce()。

### 关键源码片段

```cpp
auto upper_velocity_limits = robot.getUpperJointVelocityLimits(reference_joint_position);
auto lower_velocity_limits = robot.getLowerJointVelocityLimits(reference_joint_position);
auto rate_limited_positions_array =
    franka::limitRate(upper_velocity_limits, lower_velocity_limits,
                      franka::kMaxJointAcceleration, franka::kMaxJointJerk, target_positions,
                      reference_joint_position, robot_state.dq_d, robot_state.ddq_d);
auto active_control = robot.startJointPositionControl(
    research_interface::robot::Move::ControllerMode::kJointImpedance);
active_control->writeOnce(joint_positions);
```

(fci-zh-cpp-14_generate_joint_position_motion_external_control_loop-api)=
## 逐项 API 用法与调用案例
(fci-zh-cpp-14_generate_joint_position_motion_external_control_loop-api-50)=
### `startJointPositionControl()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Robot::startJointPositionControl()` | `std::unique_ptr<ActiveControlBase> startJointPositionControl(const research_interface::robot::Move::ControllerMode& control_type)` | 返回主动控制对象；控制冲突、网络中断或机器人错误会抛出 `ControlException`。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `control_type` | 输入，`research_interface::robot::Move::ControllerMode` | 内部控制器模式，常用 `kJointImpedance` 或 `kCartesianImpedance`。 |

`startJointPositionControl()` 启动外部控制模式。启动后示例每周期调用 `readOnce()` 读取状态和周期时间，再用 `writeOnce(JointPositions)` 写入目标命令。

```{rubric} 调用案例
```

```cpp
auto active_control = robot.startJointPositionControl(
    research_interface::robot::Move::ControllerMode::kJointImpedance);
```


````
(fci-zh-cpp-14_generate_joint_position_motion_external_control_loop-api-51)=
### `getLowerJointVelocityLimits()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Robot::getLowerJointVelocityLimits` | `auto getLowerJointVelocityLimits(const std::array<double, kNumJoints>& joint_positions) -> std::array<double, kNumJoints>` | 返回 7 轴关节速度下限，单位 rad/s。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `joint_positions` | 输入，`std::array<double,7>` | 计算速度限值所依据的关节位置，单位 rad。 |

该函数是 `Robot` 的成员函数，根据给定关节位置计算关节速度下限。示例在第一个周期传入 `robot_state.q`，之后传入 `robot_state.q_d`，并在写入命令前把结果交给 `limitRate()` 做速度/加速度约束。

```{rubric} 调用案例
```

```cpp
auto lower_velocity_limits = robot.getLowerJointVelocityLimits(reference_joint_position);
```


````
(fci-zh-cpp-14_generate_joint_position_motion_external_control_loop-api-52)=
### `getUpperJointVelocityLimits()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Robot::getUpperJointVelocityLimits` | `auto getUpperJointVelocityLimits(const std::array<double, kNumJoints>& joint_positions) -> std::array<double, kNumJoints>` | 返回 7 轴关节速度上限，单位 rad/s。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `joint_positions` | 输入，`std::array<double,7>` | 计算速度限值所依据的关节位置，单位 rad。 |

该函数是 `Robot` 的成员函数，根据给定关节位置计算关节速度上限。示例把上下限一起传给 `limitRate()`。

```{rubric} 调用案例
```

```cpp
auto upper_velocity_limits = robot.getUpperJointVelocityLimits(reference_joint_position);
```


````
(fci-zh-cpp-14_generate_joint_position_motion_external_control_loop-api-53)=
### `limitRate()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `franka::limitRate` | `std::array<double, 7> limitRate(const std::array<double, 7>& upper_limits_velocity, const std::array<double, 7>& lower_limits_velocity, const std::array<double, 7>& max_acceleration, const std::array<double, 7>& max_jerk, const std::array<double, 7>& commanded_positions, const std::array<double, 7>& last_commanded_positions, const std::array<double, 7>& last_commanded_velocities, const std::array<double, 7>& last_commanded_accelerations)` | 返回限幅后的 7 轴目标关节位置；`commanded_positions` 含无穷大或 NaN 时抛出 `std::invalid_argument`。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `upper_limits_velocity` / `lower_limits_velocity` | 输入，`std::array<double,7>` | 关节速度上限 / 下限。 |
| `max_acceleration` / `max_jerk` | 输入，`std::array<double,7>` | 最大关节加速度 / 加加速度，示例使用 `franka::kMaxJointAcceleration` 和 `franka::kMaxJointJerk`。 |
| `commanded_positions` | 输入，`std::array<double,7>` | 当前周期期望关节位置。 |
| `last_commanded_positions` / `last_commanded_velocities` / `last_commanded_accelerations` | 输入，`std::array<double,7>` | 上一周期的命令关节位置、速度和加速度；示例使用参考关节位置、`robot_state.dq_d` 和 `robot_state.ddq_d`。 |

`limitRate()` 按机型限制约束目标命令变化率；头文件中另有针对关节速度、笛卡尔速度、笛卡尔位姿和力矩的重载。示例在外部控制循环中对目标关节位置做限幅后再 `writeOnce()`。

```{rubric} 调用案例
```

```cpp
auto rate_limited_positions_array =
    franka::limitRate(upper_velocity_limits, lower_velocity_limits,
                      franka::kMaxJointAcceleration, franka::kMaxJointJerk, target_positions,
                      reference_joint_position, robot_state.dq_d, robot_state.ddq_d);
```


````

```{note}
本页的代码片段改编自 libfranka 的示例（Copyright (c) 2023 Franka Robotics GmbH，Apache License 2.0），已针对 Diana 机械臂做了修改；改编部分 Copyright (c) 2026 Agile Robots SE。详见[手册概述](/about/overview.md)中的“许可证与第三方声明”。
```

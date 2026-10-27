# 12 笛卡尔位姿外部控制循环

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

源文件：`libfranka/examples/<model>/generate_cartesian_pose_motion_external_control_loop.cpp`。

使用显式的 active-control 读写循环发送笛卡尔位姿，而非将回调交给 Robot::control()。

`<model>` 为已应用补丁的 `diana3`、`diana7` 或 `diana7G2`。

```bash
./build/libfranka/examples/<model>/generate_cartesian_pose_motion_external_control_loop <robot-ip>
```

| 使用的接口 | 本示例中的用途 |
|---|---|
| `startCartesianPoseControl()` | 启动笛卡尔位姿外部控制会话。 |
| `ActiveControl::readOnce()` | 读取当前状态和周期时间。 |
| `ActiveControl::writeOnce()` | 写入本周期笛卡尔位姿命令。 |
## Example 调用流程

移至初始姿态 → startCartesianPoseControl() → 循环 readOnce() → 生成 CartesianPose → writeOnce() 至完成。

### 关键源码片段

```cpp
auto active_control = robot.startCartesianPoseControl(
    research_interface::robot::Move::ControllerMode::kJointImpedance);
auto [robot_state, duration] = active_control->readOnce();
auto command = callback_control(robot_state, duration);
active_control->writeOnce(command);
```

(fci-zh-cpp-12_generate_cartesian_pose_motion_external_control_loop-api)=
## 逐项 API 用法与调用案例
(fci-zh-cpp-12_generate_cartesian_pose_motion_external_control_loop-api-41)=
### `startCartesianPoseControl()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Robot::startCartesianPoseControl()` | `std::unique_ptr<ActiveControlBase> startCartesianPoseControl(const research_interface::robot::Move::ControllerMode& control_type)` | 返回主动控制对象；控制冲突、网络中断或机器人错误会抛出 `ControlException`。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `control_type` | 输入，`research_interface::robot::Move::ControllerMode` | 内部控制器模式，常用 `kJointImpedance` 或 `kCartesianImpedance`。 |

`startCartesianPoseControl()` 启动外部控制模式。启动后示例每周期调用 `readOnce()` 读取状态和周期时间，再用 `writeOnce(CartesianPose)` 写入目标命令。

```{rubric} 调用案例
```

```cpp
auto active_control = robot.startCartesianPoseControl(
    research_interface::robot::Move::ControllerMode::kJointImpedance);
```


````
(fci-zh-cpp-12_generate_cartesian_pose_motion_external_control_loop-api-42)=
### `ActiveControl::readOnce()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `ActiveControlBase::readOnce` | `virtual std::pair<RobotState, Duration> readOnce()` | 返回当前 `RobotState` 与距离上次读取的 `Duration`；网络、协议或机器人错误会抛出异常。 |

`readOnce()` 是外部控制循环的读周期入口。它会等待新状态，并给出本周期持续时间；示例随后根据状态计算下一帧命令。

```{rubric} 调用案例
```

```cpp
auto [robot_state, period] = active_control->readOnce();
```


````
(fci-zh-cpp-12_generate_cartesian_pose_motion_external_control_loop-api-43)=
### `ActiveControl::writeOnce()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `ActiveControlBase::writeOnce` | `virtual void writeOnce(const CartesianPose& motion_generator_input) = 0` | 无返回值；命令类型与当前控制模式不匹配会抛出 `ControlException`。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `motion_generator_input` | 输入，`const CartesianPose&` | 本周期的末端目标位姿命令（使用内部控制器）。 |

`writeOnce()` 是外部控制循环的写周期入口。它必须和启动的控制模式匹配：关节位置模式写 `JointPositions`，关节速度模式写 `JointVelocities`，笛卡尔模式写对应命令，力矩模式写 `Torques`。本例由 `startCartesianPoseControl()` 启动，因此写入 `CartesianPose`。 同名的双参数重载 `writeOnce(const CartesianPose&, const std::optional<const Torques>&)` 可同时附带力矩命令，本例未使用。

```{rubric} 调用案例
```

```cpp
active_control->writeOnce(command);
```


````

```{warning}
风险级别：运动。该示例会发送控制命令；运行前请确认工作空间、急停与碰撞阈值。
```

```{note}
本页的代码片段改编自 libfranka 的示例（Copyright (c) 2023 Franka Robotics GmbH，Apache License 2.0），已针对 Diana 机械臂做了修改；改编部分 Copyright (c) 2026 Agile Robots SE。详见[手册概述](/about/overview.md)中的“许可证与第三方声明”。
```

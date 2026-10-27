# 15 关节速度外部控制循环

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

源文件：`libfranka/examples/<model>/generate_joint_velocity_motion_external_control_loop.cpp`。

以显式读写循环发送关节速度命令，并在回调结束时停止控制。

`<model>` 为已应用补丁的 `diana3`、`diana7` 或 `diana7G2`。

```bash
./build/libfranka/examples/<model>/generate_joint_velocity_motion_external_control_loop <robot-ip>
```

| 使用的接口 | 本示例中的用途 |
|---|---|
| `startJointVelocityControl()` | 启动关节速度外部控制会话。 |
## Example 调用流程

移至初始姿态 → startJointVelocityControl() → 循环读取状态/周期 → 写入 JointVelocities。

### 关键源码片段

```cpp
auto active_control = robot.startJointVelocityControl(
    research_interface::robot::Move::ControllerMode::kJointImpedance);
auto [robot_state, duration] = active_control->readOnce();
auto command = callback_control(robot_state, duration);
active_control->writeOnce(command);
```

(fci-zh-cpp-15_generate_joint_velocity_motion_external_control_loop-api)=
## 逐项 API 用法与调用案例
(fci-zh-cpp-15_generate_joint_velocity_motion_external_control_loop-api-55)=
### `startJointVelocityControl()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Robot::startJointVelocityControl()` | `std::unique_ptr<ActiveControlBase> startJointVelocityControl(const research_interface::robot::Move::ControllerMode& control_type)` | 返回主动控制对象；控制冲突、网络中断或机器人错误会抛出 `ControlException`。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `control_type` | 输入，`research_interface::robot::Move::ControllerMode` | 内部控制器模式，常用 `kJointImpedance` 或 `kCartesianImpedance`。 |

`startJointVelocityControl()` 启动外部控制模式。启动后示例每周期调用 `readOnce()` 读取状态和周期时间，再用 `writeOnce(JointVelocities)` 写入目标命令。

```{rubric} 调用案例
```

```cpp
auto active_control = robot.startJointVelocityControl(
    research_interface::robot::Move::ControllerMode::kJointImpedance);
```


````

```{note}
本页的代码片段改编自 libfranka 的示例（Copyright (c) 2023 Franka Robotics GmbH，Apache License 2.0），已针对 Diana 机械臂做了修改；改编部分 Copyright (c) 2026 Agile Robots SE。详见[手册概述](/about/overview.md)中的“许可证与第三方声明”。
```

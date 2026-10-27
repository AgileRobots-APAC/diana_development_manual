# 13 笛卡尔速度外部控制循环

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

源文件：`libfranka/examples/<model>/generate_cartesian_velocity_motion_external_control_loop.cpp`。

使用显式外部控制循环发送笛卡尔速度指令。

`<model>` 为已应用补丁的 `diana3`、`diana7` 或 `diana7G2`。

```bash
./build/libfranka/examples/<model>/generate_cartesian_velocity_motion_external_control_loop <robot-ip>
```

| 使用的接口 | 本示例中的用途 |
|---|---|
| `setJointImpedance()` | 设置内部关节阻抗刚度。 |
| `startCartesianVelocityControl()` | 启动笛卡尔速度外部控制会话。 |
## Example 调用流程

移至初始姿态并设置关节阻抗 → startCartesianVelocityControl() → readOnce() / writeOnce() 循环。

### 关键源码片段

```cpp
auto active_control = robot.startCartesianVelocityControl(
    research_interface::robot::Move::ControllerMode::kJointImpedance);
auto [robot_state, duration] = active_control->readOnce();
active_control->writeOnce(callback_control(robot_state, duration));
```

(fci-zh-cpp-13_generate_cartesian_velocity_motion_external_control_loop-api)=
## 逐项 API 用法与调用案例
(fci-zh-cpp-13_generate_cartesian_velocity_motion_external_control_loop-api-45)=
### `setJointImpedance()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Robot::setJointImpedance` | `void setJointImpedance(const std::array<double, 7>& K_theta)` | 无返回值；网络中断或控制器拒绝配置会抛出异常。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `K_theta` | 输入，`std::array<double,7>` | 七个关节刚度参数。 |

`setJointImpedance()` 设置内部关节阻抗控制器的各关节刚度。笛卡尔速度和阻抗类示例在控制前设置它，用于调整内部控制器行为；它不会改变用户发送的力矩命令本身。

补丁版示例中，`diana3` 目录将该调用的刚度改为 `{{600, 600, 400, 100, 100, 100, 100}}`；`diana7` 和 `diana7G2` 目录的该示例已移除这次调用。

```{rubric} 调用案例
```

```cpp
robot.setJointImpedance({{3000, 3000, 3000, 2500, 2500, 2000, 2000}});
```


````
(fci-zh-cpp-13_generate_cartesian_velocity_motion_external_control_loop-api-46)=
### `startCartesianVelocityControl()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Robot::startCartesianVelocityControl()` | `std::unique_ptr<ActiveControlBase> startCartesianVelocityControl(const research_interface::robot::Move::ControllerMode& control_type)` | 返回主动控制对象；控制冲突、网络中断或机器人错误会抛出 `ControlException`。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `control_type` | 输入，`research_interface::robot::Move::ControllerMode` | 内部控制器模式，常用 `kJointImpedance` 或 `kCartesianImpedance`。 |

`startCartesianVelocityControl()` 启动外部控制模式。启动后示例每周期调用 `readOnce()` 读取状态和周期时间，再用 `writeOnce(CartesianVelocities)` 写入目标命令。

```{rubric} 调用案例
```

```cpp
auto active_control = robot.startCartesianVelocityControl(
    research_interface::robot::Move::ControllerMode::kJointImpedance);
```


````

```{note}
本页的代码片段改编自 libfranka 的示例（Copyright (c) 2023 Franka Robotics GmbH，Apache License 2.0），已针对 Diana 机械臂做了修改；改编部分 Copyright (c) 2026 Agile Robots SE。详见[手册概述](/about/overview.md)中的“许可证与第三方声明”。
```

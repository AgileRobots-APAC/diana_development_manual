# 02 通信性能检查

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

源文件：`libfranka/examples/<model>/communication_test.cpp`。

该程序统计 `control_command_success_rate`、丢失周期和成功率统计值。它不是只读程序：会先移动到初始姿态，然后进入零力矩控制会话。

`<model>` 为已应用补丁的 `diana3`、`diana7` 或 `diana7G2`。

```bash
./build/libfranka/examples/<model>/communication_test <robot-ip>
```

| 使用的接口 | 本示例中的用途 |
|---|---|
| `MotionGenerator` | 生成并执行测试初始姿态运动。 |
| `Robot::control()` | 移动至测试初始姿态。 |
| `startTorqueControl()` | 建立力矩读写控制会话。 |
| `readOnce()` | 每周期读取状态和周期时间。 |
| `writeOnce()` | 每周期写入零力矩命令。 |
| `control_command_success_rate` | 统计控制通信成功率。 |
## Example 调用流程

解析机器人地址 → 创建 Robot → 移动到初始姿态 → 开启力矩控制 → 读取状态并写入零力矩 → 汇总通信指标 → 结束会话。

### 关键源码片段

```cpp
franka::Torques zero_torques{{0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0}};
auto rw_interface = robot.startTorqueControl();

while (!zero_torques.motion_finished) {
  std::tie(robot_state, period) = rw_interface->readOnce();
  time += period.toMSec();
  zero_torques.motion_finished = time >= 10000;
  rw_interface->writeOnce(zero_torques);
}
```

(fci-zh-cpp-02_communication_test-api)=
## 逐项 API 用法与调用案例
(fci-zh-cpp-02_communication_test-api-1)=
### `Robot::startTorqueControl()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Robot::startTorqueControl` | `std::unique_ptr<ActiveControlBase> startTorqueControl()` | 返回主动控制对象；控制冲突、网络中断或机器人错误会抛出 `ControlException`。 |

`startTorqueControl()` 启动力矩外部控制模式。调用后通过返回的 `ActiveControlBase` 周期性 `readOnce()` / `writeOnce(Torques)` 完成读写。

```{rubric} 调用案例
```

```cpp
auto active_control = robot.startTorqueControl();
```


````
(fci-zh-cpp-02_communication_test-api-2)=
### `readOnce()`

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
(fci-zh-cpp-02_communication_test-api-3)=
### `writeOnce()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `ActiveControlBase::writeOnce` | `virtual void writeOnce(const Torques& control_input) = 0` | 无返回值；命令类型与当前控制模式不匹配会抛出 `ControlException`。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `control_input` | 输入，`const Torques&` | 本周期的关节力矩命令；本例每周期写入零力矩。 |

`writeOnce()` 是外部控制循环的写周期入口。它必须和启动的控制模式匹配：关节位置模式写 `JointPositions`，关节速度模式写 `JointVelocities`，笛卡尔模式写对应命令，力矩模式写 `Torques`。 本例由 `startTorqueControl()` 启动，因此调用只接受 `Torques` 的重载。其余重载接受 `JointPositions`、`JointVelocities`、`CartesianPose` 或 `CartesianVelocities`，并可附带可选的 `std::optional<const Torques>`。

```{rubric} 调用案例
```

```cpp
active_control->writeOnce(zero_torques);
```


````
(fci-zh-cpp-02_communication_test-api-128)=
### `control_command_success_rate`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `RobotState::control_command_success_rate` | `double control_command_success_rate` | 字段值为最近 100 条控制命令中被机器人成功接收的比例，范围 `[0, 1]`；没有控制或运动生成循环运行时为 0。 |

`control_command_success_rate` 是 `RobotState` 中的通信质量字段。示例在每个周期读取该值，累计最大值、最小值和平均值，并在结束时根据平均成功率给出网络/主机配置建议。

```{rubric} 调用案例
```

```cpp
avg_success_rate += robot_state.control_command_success_rate;
if (robot_state.control_command_success_rate > max_success_rate) {
  max_success_rate = robot_state.control_command_success_rate;
}
if (robot_state.control_command_success_rate < min_success_rate) {
  min_success_rate = robot_state.control_command_success_rate;
}
```


````

```{warning}
风险级别：力矩 / 运动。该程序会先移动到初始姿态，再进入力矩控制；仅在现场安全条件确认后运行，并确认工作空间、急停与碰撞阈值。
```

```{note}
本页的代码片段改编自 libfranka 的示例（Copyright (c) 2023 Franka Robotics GmbH，Apache License 2.0），已针对 Diana 机械臂做了修改；改编部分 Copyright (c) 2026 Agile Robots SE。详见[手册概述](/about/overview.md)中的“许可证与第三方声明”。
```

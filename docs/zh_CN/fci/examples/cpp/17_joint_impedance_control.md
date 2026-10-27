# 17 关节阻抗控制

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

源文件：`libfranka/examples/<model>/joint_impedance_control.cpp`。

用模型科氏力补偿的关节阻抗律跟踪由笛卡尔轨迹反解得到的关节目标。

`<model>` 为已应用补丁的 `diana3`、`diana7` 或 `diana7G2`。

```bash
./build/libfranka/examples/<model>/joint_impedance_control <robot-ip>
```

| 使用的接口 | 本示例中的用途 |
|---|---|
| `Model::coriolis()` | 计算科氏力和离心力补偿项。 |
| `Model::gravity()` | 计算重力项，用于打印实际力矩。 |
| `Robot::control()` | 同时启动力矩控制回调和笛卡尔位姿运动生成回调。 |
## Example 调用流程

加载模型 → 位姿回调产生圆轨迹 → 力矩回调计算刚度、阻尼、科氏补偿 → 限幅后组合控制。

### 关键源码片段

```cpp
auto coriolis = model.coriolis(state);
tau_d_calculated[i] = k_gains[i] * (state.q_d[i] - state.q[i])
                    - d_gains[i] * state.dq[i] + coriolis[i];
return franka::limitRate(franka::kMaxTorqueRate,
                         tau_d_calculated, state.tau_J_d);
```

(fci-zh-cpp-17_joint_impedance_control-api)=
## 逐项 API 用法与调用案例
(fci-zh-cpp-17_joint_impedance_control-api-67)=
### `Model::coriolis()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Model::coriolis` | `std::array<double, 7> coriolis(const franka::RobotState& robot_state) const noexcept` | 返回 7 维 Coriolis/离心力矩数组，单位 Nm。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `robot_state` | 输入，`const franka::RobotState&` | 用于计算的机器人状态。 |

`coriolis()` 根据当前状态计算补偿项。本示例把它加到关节阻抗控制律输出上，形成发送给机器人控制接口的关节力矩。

```{rubric} 调用案例
```

```cpp
std::array<double, 7> coriolis = model.coriolis(state);
```


````
(fci-zh-cpp-17_joint_impedance_control-api-68)=
### `Model::gravity()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Model::gravity` | `std::array<double, 7> gravity(const franka::RobotState& robot_state) const noexcept` | 返回 7 维重力力矩数组，单位 Nm。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `robot_state` | 输入，`const franka::RobotState&` | 用于计算的机器人状态。 |

`gravity()` 根据当前位形计算重力项。本示例不把它加入力矩命令，只在打印时与限幅后的力矩相加，显示实际关节力矩。

```{rubric} 调用案例
```

```cpp
print_data.gravity = model.gravity(state);
```


````
(fci-zh-cpp-17_joint_impedance_control-api-71)=
### `Robot::control()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Robot::control` | `void control(std::function<Torques(const RobotState&, franka::Duration)> control_callback, std::function<CartesianPose(const RobotState&, franka::Duration)> motion_generator_callback, bool limit_rate = false, double cutoff_frequency = kDefaultCutoffFrequency)` | 无返回值；控制结束由回调返回 `MotionFinished(...)` 表示；控制冲突、实时配置失败、网络中断或命令非法会抛出异常。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `control_callback` | 输入，`std::function` | 每个控制周期返回 `Torques` 力矩命令。 |
| `motion_generator_callback` | 输入，`std::function` | 每个控制周期返回 `CartesianPose` 运动生成命令。 |
| `limit_rate` | 输入，`bool`，默认 `false` | 是否启用限幅；可能改变轨迹。 |
| `cutoff_frequency` | 输入，`double` | 低通滤波截止频率。 |

`control()` 启动 1 kHz FCI 控制循环。本示例使用“力矩控制 + 笛卡尔位姿运动生成”重载：位姿回调给出目标位姿，由内部逆解得到的 `q_d` 供力矩回调跟踪。一次只能有一个控制/运动生成循环处于活动状态。

```{rubric} 调用案例
```

```cpp
robot.control(impedance_control_callback, cartesian_pose_callback);
```


````

```{warning}
风险级别：力矩。该示例会发送控制命令；运行前请确认工作空间、急停与碰撞阈值。
```

```{note}
本页的代码片段改编自 libfranka 的示例（Copyright (c) 2023 Franka Robotics GmbH，Apache License 2.0），已针对 Diana 机械臂做了修改；改编部分 Copyright (c) 2026 Agile Robots SE。详见[手册概述](/about/overview.md)中的“许可证与第三方声明”。
```

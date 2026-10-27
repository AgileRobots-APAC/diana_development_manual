# 07 生成关节速度运动

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

源文件：`libfranka/examples/<model>/generate_joint_velocity_motion.cpp`。

在实时回调中输出关节速度命令，并在指定时长后标记运动结束。

`<model>` 为已应用补丁的 `diana3`、`diana7` 或 `diana7G2`。

```bash
./build/libfranka/examples/<model>/generate_joint_velocity_motion <robot-ip>
```

| 使用的接口 | 本示例中的用途 |
|---|---|
| `Robot::control()` | 启动关节速度实时控制回调。 |
| `JointVelocities` | 封装每周期的七轴目标关节速度。 |
## Example 调用流程

先移至初始姿态 → 控制回调依据 Duration 计算速度 → 返回 JointVelocities / MotionFinished()。

与上游 libfranka 相比，Diana 补丁版本删除了 `setCollisionBehavior()` 调用。

第 4 轴速度因机型而异：diana3 为 `-omega`，diana7 与 diana7G2 为 `omega / 2`（下方代码为 diana7 取值）。

### 关键源码片段

```cpp
double cycle = std::floor(std::pow(-1.0, (time - std::fmod(time, time_max)) / time_max));
double omega = cycle * omega_max / 2.0 * (1.0 - std::cos(2.0 * M_PI / time_max * time));

franka::JointVelocities velocities = {{0.0, 0.0, 0.0, omega / 2, omega, omega, omega}};

if (time >= 2 * time_max) {
  return franka::MotionFinished(velocities);
}
return velocities;
```

(fci-zh-cpp-07_generate_joint_velocity_motion-api)=
## 逐项 API 用法与调用案例
(fci-zh-cpp-07_generate_joint_velocity_motion-api-17)=
### `Robot::control()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Robot::control` | `void control(std::function<JointVelocities(const RobotState&, Duration)> callback, ControllerMode controller_mode = ControllerMode::kJointImpedance, bool limit_rate = false, double cutoff_frequency = kDefaultCutoffFrequency)` | 无返回值；控制结束由回调返回 `MotionFinished(...)` 表示；控制冲突、实时配置失败、网络中断或命令非法会抛出异常。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `callback` | 输入，`std::function` | 每个控制周期生成目标命令。 |
| `controller_mode` | 输入，`ControllerMode`，默认 `kJointImpedance` | 内部控制器模式。 |
| `limit_rate` | 输入，`bool`，默认 `false` | 是否启用限幅；可能改变轨迹。 |
| `cutoff_frequency` | 输入，`double` | 低通滤波截止频率。 |

`control()` 启动 1 kHz FCI 控制循环。回调每周期接收 `RobotState` 和 `Duration`，返回 `JointPositions`、`JointVelocities`、`CartesianPose`、`CartesianVelocities` 或 `Torques` 等命令。一次只能有一个控制/运动生成循环处于活动状态。

```{rubric} 调用案例
```

```cpp
robot.control([&](const franka::RobotState& state,
                  franka::Duration period) -> franka::JointVelocities {
  time += period.toSec();
  franka::JointVelocities output = {{0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0}};
  if (time >= 2.0) {
    return franka::MotionFinished(output);
  }
  return output;
});
```


````
(fci-zh-cpp-07_generate_joint_velocity_motion-api-19)=
### `JointVelocities`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `franka::JointVelocities` | `JointVelocities(const std::array<double, 7>& joint_velocities)` | 返回关节速度命令对象；initializer list 数量错误时会抛出 `std::invalid_argument`。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `joint_velocities` | 输入，`std::array<double,7>` | 目标关节速度，单位 rad/s。 |

`JointVelocities` 封装 7 轴目标关节速度，单位 rad/s。速度运动生成器示例每周期返回该对象，结束时用 `MotionFinished()` 标记。

```{rubric} 调用案例
```

```cpp
franka::JointVelocities velocities = {{0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0}};
```


````

```{note}
本页的代码片段改编自 libfranka 的示例（Copyright (c) 2023 Franka Robotics GmbH，Apache License 2.0），已针对 Diana 机械臂做了修改；改编部分 Copyright (c) 2026 Agile Robots SE。详见[手册概述](/about/overview.md)中的“许可证与第三方声明”。
```

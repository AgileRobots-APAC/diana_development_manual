# 05 关节点到点运动

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

源文件：`libfranka/examples/<model>/joint_point_to_point_motion.cpp`。

通过示例公共的 MotionGenerator 移动至命令行给出的七轴目标关节角。

`<model>` 为已应用补丁的 `diana3`、`diana7` 或 `diana7G2`。

```bash
./build/libfranka/examples/<model>/joint_point_to_point_motion <robot-ip>
```

| 使用的接口 | 本示例中的用途 |
|---|---|
| `MotionGenerator` | 根据目标关节角和速度因子生成平滑的关节位置命令。 |
| `Robot::setCollisionBehavior()` | 配置运动前的碰撞与接触阈值。 |
| `Robot::control()` | 启动实时控制循环并执行运动生成器。 |
## Example 调用流程

读取七个关节目标和速度因子 → 设置碰撞阈值 → 构造 MotionGenerator → robot.control()。

机型差异：diana3 的补丁版本删除了 `setCollisionBehavior()` 调用；diana7 与 diana7G2 保留该调用，但将加速阶段和名义阶段两组笛卡尔力上阈值的第 6 个分量改为 30.0。

### 关键源码片段

```cpp
std::array<double, 7> q_goal = {/* 从命令行读取的 7 个关节目标 */};
MotionGenerator motion_generator(speed_factor, q_goal);
robot.control(motion_generator);
```

(fci-zh-cpp-05_joint_point_to_point_motion-api)=
## 逐项 API 用法与调用案例
(fci-zh-cpp-05_joint_point_to_point_motion-api-9)=
### `MotionGenerator`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `MotionGenerator` | `MotionGenerator(double speed_factor, const std::array<double, 7>& q_goal)` | 构造示例辅助对象；回调返回 `franka::JointPositions`。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `speed_factor` | 输入，`double` | 速度比例，通常在 0 到 1 之间。 |
| `q_goal` | 输入，`std::array<double,7>` | 目标关节角，单位 rad。 |

`MotionGenerator` 是 libfranka 示例里的轨迹辅助类，不是机器人控制器接口。它根据目标关节角和速度比例生成平滑关节位置命令，随后传给 `Robot::control()`。本例目标为命令行给出的七个关节角。

```{rubric} 调用案例
```

```cpp
MotionGenerator motion_generator(0.5, q_goal);
robot.control(motion_generator);
```


````
(fci-zh-cpp-05_joint_point_to_point_motion-api-10)=
### `Robot::setCollisionBehavior()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Robot::setCollisionBehavior` | `void setCollisionBehavior(const std::array<double, 7>& lower_torque_thresholds, const std::array<double, 7>& upper_torque_thresholds, const std::array<double, 6>& lower_force_thresholds, const std::array<double, 6>& upper_force_thresholds)` | 无返回值；参数非法、网络中断或机器人拒绝配置会抛出异常。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `lower_torque_thresholds` | 输入，`std::array<double,7>` | 各关节接触下阈值，单位 Nm。 |
| `upper_torque_thresholds` | 输入，`std::array<double,7>` | 各关节碰撞上阈值，单位 Nm。 |
| `lower_force_thresholds` | 输入，`std::array<double,6>` | 笛卡尔接触下阈值。 |
| `upper_force_thresholds` | 输入，`std::array<double,6>` | 笛卡尔碰撞上阈值。 |

`setCollisionBehavior()` 配置碰撞/接触阈值。阈值不是安全边界的替代；示例在运动前设置较保守的阈值，便于触发控制器保护。

```{rubric} 调用案例
```

```cpp
robot.setCollisionBehavior(
    {{20.0, 20.0, 18.0, 18.0, 16.0, 14.0, 12.0}},
    {{20.0, 20.0, 18.0, 18.0, 16.0, 14.0, 12.0}},
    {{20.0, 20.0, 20.0, 25.0, 25.0, 25.0}},
    {{20.0, 20.0, 20.0, 25.0, 25.0, 25.0}});
```


````
(fci-zh-cpp-05_joint_point_to_point_motion-api-11)=
### `Robot::control()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Robot::control` | `void control(std::function<JointPositions(const RobotState&, Duration)> callback, ControllerMode controller_mode = ControllerMode::kJointImpedance, bool limit_rate = false, double cutoff_frequency = kDefaultCutoffFrequency)` | 无返回值；控制结束由回调返回 `MotionFinished(...)` 表示；控制冲突、实时配置失败、网络中断或命令非法会抛出异常。 |

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

```{warning}
风险级别：运动。该示例会发送控制命令；运行前请确认工作空间、急停与碰撞阈值。
```

```{note}
本页的代码片段改编自 libfranka 的示例（Copyright (c) 2023 Franka Robotics GmbH，Apache License 2.0），已针对 Diana 机械臂做了修改；改编部分 Copyright (c) 2026 Agile Robots SE。详见[手册概述](/about/overview.md)中的“许可证与第三方声明”。
```

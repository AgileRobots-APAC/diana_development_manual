# 10 生成笛卡尔位姿运动

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

源文件：`libfranka/examples/<model>/generate_cartesian_pose_motion.cpp`。

在实时回调中让末端执行器沿圆形轨迹运动并发送笛卡尔位姿目标。

`<model>` 为已应用补丁的 `diana3`、`diana7` 或 `diana7G2`。

```bash
./build/libfranka/examples/<model>/generate_cartesian_pose_motion <robot-ip>
```

| 使用的接口 | 本示例中的用途 |
|---|---|
| `Robot::control()` | 启动笛卡尔位姿实时控制回调。 |
| `CartesianPose` | 封装每周期的末端目标位姿。 |
| `MotionFinished()` | 标记最后一帧命令并结束控制循环。 |
## Example 调用流程

移至初始姿态 → 读取 O_T_EE → 更新位姿矩阵平移项 → MotionFinished()。

与上游 libfranka 相比，Diana 补丁版本删除了 `setCollisionBehavior()` 调用。

### 关键源码片段

```cpp
constexpr double kRadius = 0.3;
double angle = M_PI / 4 * (1 - std::cos(M_PI / 5.0 * time));
double delta_x = kRadius * std::sin(angle);
double delta_z = kRadius * (std::cos(angle) - 1);

std::array<double, 16> new_pose = initial_pose;
new_pose[12] += delta_x;
new_pose[14] += delta_z;

if (time >= 10.0) {
  return franka::MotionFinished(new_pose);
}
return new_pose;
```

(fci-zh-cpp-10_generate_cartesian_pose_motion-api)=
## 逐项 API 用法与调用案例
(fci-zh-cpp-10_generate_cartesian_pose_motion-api-157)=
### `Robot::control()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Robot::control` | `void control(std::function<CartesianPose(const RobotState&, Duration)> callback, ControllerMode controller_mode = ControllerMode::kJointImpedance, bool limit_rate = false, double cutoff_frequency = kDefaultCutoffFrequency)` | 无返回值；控制结束由回调返回 `MotionFinished(...)` 表示；控制冲突、实时配置失败、网络中断或命令非法会抛出异常。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `callback` | 输入，`std::function` | 每个控制周期生成目标命令。 |
| `controller_mode` | 输入，`ControllerMode`，默认 `kJointImpedance` | 内部控制器模式。 |
| `limit_rate` | 输入，`bool`，默认 `false` | 是否启用限幅；可能改变轨迹。 |
| `cutoff_frequency` | 输入，`double` | 低通滤波截止频率。 |

`control()` 启动 1 kHz FCI 控制循环。回调每周期接收 `RobotState` 和 `Duration`，返回 `JointPositions`、`JointVelocities`、`CartesianPose`、`CartesianVelocities` 或 `Torques` 等命令。一次只能有一个控制/运动生成循环处于活动状态。本例的回调返回 `CartesianPose`。

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

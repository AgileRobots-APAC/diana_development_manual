# 06 生成关节位置运动

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

源文件：`libfranka/examples/<model>/generate_joint_position_motion.cpp`。

在实时回调中生成第 4、5、7 轴的平滑位置变化，约 5 秒后结束。

`<model>` 为已应用补丁的 `diana3`、`diana7` 或 `diana7G2`。

```bash
./build/libfranka/examples/<model>/generate_joint_position_motion <robot-ip>
```

| 使用的接口 | 本示例中的用途 |
|---|---|
| `Robot::control()` | 启动关节位置实时控制回调。 |
| `RobotState::q` | 读取当前关节角作为运动起点。 |
| `Duration::toSec()` | 累加控制周期时间生成轨迹相位。 |
| `JointPositions` | 封装每周期的七轴目标关节角。 |
| `MotionFinished()` | 标记最后一帧命令并结束控制循环。 |
## Example 调用流程

先移至初始姿态 → robot.control(位置回调) → 按周期累加时间并返回 JointPositions → MotionFinished()。

与上游 libfranka 相比，Diana 补丁版本删除了 `setCollisionBehavior()` 调用，并将第 4 轴偏移改为 `delta_angle / 2`。

### 关键源码片段

```cpp
double delta_angle = M_PI / 8.0 * (1 - std::cos(M_PI / 2.5 * time));

franka::JointPositions output = {{initial_position[0], initial_position[1],
                                  initial_position[2], initial_position[3] + delta_angle / 2,
                                  initial_position[4] + delta_angle, initial_position[5],
                                  initial_position[6] + delta_angle}};

if (time >= 5.0) {
  return franka::MotionFinished(output);
}
return output;
```

(fci-zh-cpp-06_generate_joint_position_motion-api)=
## 逐项 API 用法与调用案例
(fci-zh-cpp-06_generate_joint_position_motion-api-12)=
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
(fci-zh-cpp-06_generate_joint_position_motion-api-13)=
### `RobotState::q`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `RobotState::q` | `std::array<double, 7> q` | 字段值为当前测量关节角，单位 rad。 |

`q` 是 `RobotState` 中的当前关节位置数组。关节位置控制示例通常以 `q` 作为起点，在其基础上生成平滑目标，避免从假定零位直接下发命令。

```{rubric} 调用案例
```

```cpp
std::array<double, 7> initial_position = robot_state.q;
```


````
(fci-zh-cpp-06_generate_joint_position_motion-api-14)=
### `Duration::toSec()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Duration::toSec` | `double toSec() const noexcept` | 返回持续时间，单位 s。 |

`Duration::toSec()` 把控制周期时间转换为秒。示例用它累加轨迹时间，按时间生成正弦或分段运动。

```{rubric} 调用案例
```

```cpp
time += period.toSec();
```


````
(fci-zh-cpp-06_generate_joint_position_motion-api-15)=
### `JointPositions`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `franka::JointPositions` | `JointPositions(const std::array<double, 7>& joint_positions) noexcept` | 返回关节位置命令对象；另有 `JointPositions(std::initializer_list<double>)` 重载，initializer list 数量错误时会抛出 `std::invalid_argument`。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `joint_positions` | 输入，`std::array<double,7>` | 目标关节角，单位 rad。 |

`JointPositions` 封装 7 轴目标关节角，单位 rad。位置运动生成器或外部控制循环把它作为每周期的目标命令。

```{rubric} 调用案例
```

```cpp
franka::JointPositions output = {{q0, q1, q2, q3, q4, q5, q6}};
```


````
(fci-zh-cpp-06_generate_joint_position_motion-api-16)=
### `MotionFinished()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `franka::MotionFinished` | `Command MotionFinished(Command command) noexcept` | 返回同类型命令对象，并将其 `motion_finished` 标志置为 `true`。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `command` | 输入/输出，命令对象 | 要作为最后一帧发送的命令对象。 |

`MotionFinished()` 用于告诉 `Robot::control()` 或外部控制循环：当前返回的命令是最后一个命令，控制循环可以结束。它支持 `Torques`、`JointPositions`、`JointVelocities`、`CartesianPose` 和 `CartesianVelocities`。

```{rubric} 调用案例
```

```cpp
if (time >= motion_time) {
  return franka::MotionFinished(output);
}
```


````

```{warning}
风险级别：运动。该示例会发送控制命令；运行前请确认工作空间、急停与碰撞阈值。
```

```{note}
本页的代码片段改编自 libfranka 的示例（Copyright (c) 2023 Franka Robotics GmbH，Apache License 2.0），已针对 Diana 机械臂做了修改；改编部分 Copyright (c) 2026 Agile Robots SE。详见[手册概述](/about/overview.md)中的“许可证与第三方声明”。
```

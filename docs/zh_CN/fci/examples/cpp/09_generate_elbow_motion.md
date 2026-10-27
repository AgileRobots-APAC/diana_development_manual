# 09 生成带肘部冗余参数的笛卡尔运动

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

源文件：`libfranka/examples/<model>/generate_elbow_motion.cpp`。

在笛卡尔位姿目标中同时设置 elbow 冗余参数，展示七自由度冗余位形控制。

`<model>` 为已应用补丁的 `diana3`、`diana7` 或 `diana7G2`。

```bash
./build/libfranka/examples/<model>/generate_elbow_motion <robot-ip>
```

| 使用的接口 | 本示例中的用途 |
|---|---|
| `Robot::control()` | 启动笛卡尔位姿实时控制回调。 |
| `CartesianPose` | 封装末端目标位姿和 elbow 构型。 |
| `RobotState::O_T_EE` | 读取当前测量位姿作为轨迹起点。 |
## Example 调用流程

移至初始姿态 → 回调保持初始 O_T_EE 位姿并逐步增加 elbow[0] → 返回 CartesianPose / MotionFinished()。

与上游 libfranka 相比，Diana 补丁版本删除了 `setCollisionBehavior()` 调用。

elbow 摆动幅值因机型而异：diana3 与 diana7 为 `M_PI / 16.0`，diana7G2 为 `M_PI / 20.0`（下方代码为 diana7 取值）。

### 关键源码片段

```cpp
double angle = M_PI / 16.0 * (1.0 - std::cos(M_PI / 5.0 * time));

auto elbow = initial_elbow;
elbow[0] += angle;

if (time >= 10.0) {
  return franka::MotionFinished({initial_pose, elbow});
}
return {initial_pose, elbow};
```

(fci-zh-cpp-09_generate_elbow_motion-api)=
## 逐项 API 用法与调用案例
(fci-zh-cpp-09_generate_elbow_motion-api-26)=
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
(fci-zh-cpp-09_generate_elbow_motion-api-27)=
### `CartesianPose`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `franka::CartesianPose` | `CartesianPose(const std::array<double, 16>& cartesian_pose, const std::array<double, 2>& elbow) noexcept` | 返回笛卡尔位姿命令对象；另有仅含位姿的单参数重载，以及 `std::initializer_list<double>` 重载（元素数量错误时会抛出 `std::invalid_argument`）。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `cartesian_pose` | 输入，`std::array<double,16>` | 目标 4x4 位姿矩阵，列主序。 |
| `elbow` | 输入，`std::array<double,2>` | 肘部构型：`elbow[0]` 为第三关节位置（rad），`elbow[1]` 为第四关节翻转方向（+1 / 0 / -1）。 |

`CartesianPose` 封装末端相对于 base frame `O` 的目标齐次变换矩阵，按列主序展开。带 elbow 构造时还会指定肘部构型。

```{rubric} 调用案例
```

```cpp
franka::CartesianPose pose_desired(initial_pose);
pose_desired.O_T_EE[13] += 0.05;
```


````
(fci-zh-cpp-09_generate_elbow_motion-api-28)=
### `RobotState::O_T_EE`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `RobotState::O_T_EE` | `std::array<double, 16> O_T_EE` | 字段值为当前测量末端位姿，4x4 齐次矩阵按列主序展开。 |

`O_T_EE` 表示当前测量的末端执行器位姿，坐标系为 base frame `O` 到 end-effector frame `EE`。笛卡尔位姿示例以它为起点，只修改平移或肘部相关目标。

```{rubric} 调用案例
```

```cpp
initial_pose = robot_state.O_T_EE;
```


````

```{warning}
风险级别：运动。该示例会发送控制命令；运行前请确认工作空间、急停与碰撞阈值。
```

```{note}
本页的代码片段改编自 libfranka 的示例（Copyright (c) 2023 Franka Robotics GmbH，Apache License 2.0），已针对 Diana 机械臂做了修改；改编部分 Copyright (c) 2026 Agile Robots SE。详见[手册概述](/about/overview.md)中的“许可证与第三方声明”。
```

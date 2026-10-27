# 控制模式与数据流（以C++为例）

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

补丁后的 `libfranka/examples/<型号>/` 通过 `franka::Robot::control()` 进入实时控制回调。每个周期接收 `franka::RobotState` 与 `franka::Duration`，并返回目标命令；以 `franka::MotionFinished(...)` 包装命令可受控退出。

## 示例覆盖的控制输入

| 控制输入 | 当前示例文件 | 返回类型 |
|---|---|---|
| 关节位置 | [`joint_point_to_point_motion`](examples/cpp/05_joint_point_to_point_motion.md)、[`generate_joint_position_motion`](examples/cpp/06_generate_joint_position_motion.md)、[`generate_joint_position_motion_external_control_loop`](examples/cpp/14_generate_joint_position_motion_external_control_loop.md) | `franka::JointPositions` |
| 关节速度 | [`generate_joint_velocity_motion`](examples/cpp/07_generate_joint_velocity_motion.md)、[`generate_consecutive_motions`](examples/cpp/08_generate_consecutive_motions.md)、[`generate_joint_velocity_motion_external_control_loop`](examples/cpp/15_generate_joint_velocity_motion_external_control_loop.md) | `franka::JointVelocities` |
| 笛卡尔位姿 | [`generate_cartesian_pose_motion`](examples/cpp/10_generate_cartesian_pose_motion.md)、[`generate_elbow_motion`](examples/cpp/09_generate_elbow_motion.md)、[`generate_cartesian_pose_motion_external_control_loop`](examples/cpp/12_generate_cartesian_pose_motion_external_control_loop.md) | `franka::CartesianPose` |
| 笛卡尔速度 | [`generate_cartesian_velocity_motion`](examples/cpp/11_generate_cartesian_velocity_motion.md)、[`generate_cartesian_velocity_motion_external_control_loop`](examples/cpp/13_generate_cartesian_velocity_motion_external_control_loop.md) | `franka::CartesianVelocities` |
| 关节力矩 | [`joint_impedance_control`](examples/cpp/17_joint_impedance_control.md)、[`cartesian_impedance_control`](examples/cpp/18_cartesian_impedance_control.md)、[`force_control`](examples/cpp/19_force_control.md)、[`motion_with_control`](examples/cpp/20_motion_with_control.md)、[`motion_with_control_external_control_loop`](examples/cpp/16_motion_with_control_external_control_loop.md) | `franka::Torques` |

`*_external_control_loop` 文件是相应控制类型的外部控制循环变体。所有文件都必须从选定机型补丁后的 `libfranka/examples/<型号>/` 读取。

## 状态与模型数据

| 数据 | 来源 | 典型用途 |
|---|---|---|
| `franka::RobotState` | `read()`、`readOnce()` 或控制回调 | 关节、末端、速度、力矩和反馈 |
| `franka::Model` | `robot.loadModel()` | 重力、科氏项、末端位姿、雅可比 |
| `franka::Duration` | 控制回调参数 | 积分时间与周期目标 |

## 控制回调原则

1. 第一拍目标必须连续，避免相对于当前状态突变。
2. 回调内不要打印、网络访问、文件 I/O、动态大内存分配或长时间锁等待。
3. 每个控制器应有明确停止条件，并以零速度或受控力矩结束。
4. 力矩控制从低增益开始，并结合限幅和变化率限制。

```{warning}
FCI 控制模式的切换方式与普通 C++ SDK 运动命令不同。不要在实时控制回调中混用阻塞式普通 SDK 运动 API。运行任何运动或力矩示例前，必须完成现场安全确认。
```

# Control Modes and Data Flow

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

The patched `libfranka/examples/<model>/` enter realtime control through `franka::Robot::control()`. Each cycle receives `franka::RobotState` and `franka::Duration`, then returns the target command; wrapping the command in `franka::MotionFinished(...)` ends control in a controlled way.

## Control Inputs Covered by the Examples

| Control input | Examples | Return type |
|---|---|---|
| Joint position | [`joint_point_to_point_motion`](examples/cpp/05_joint_point_to_point_motion.md), [`generate_joint_position_motion`](examples/cpp/06_generate_joint_position_motion.md), [`generate_joint_position_motion_external_control_loop`](examples/cpp/14_generate_joint_position_motion_external_control_loop.md) | `franka::JointPositions` |
| Joint velocity | [`generate_joint_velocity_motion`](examples/cpp/07_generate_joint_velocity_motion.md), [`generate_consecutive_motions`](examples/cpp/08_generate_consecutive_motions.md), [`generate_joint_velocity_motion_external_control_loop`](examples/cpp/15_generate_joint_velocity_motion_external_control_loop.md) | `franka::JointVelocities` |
| Cartesian pose | [`generate_cartesian_pose_motion`](examples/cpp/10_generate_cartesian_pose_motion.md), [`generate_elbow_motion`](examples/cpp/09_generate_elbow_motion.md), [`generate_cartesian_pose_motion_external_control_loop`](examples/cpp/12_generate_cartesian_pose_motion_external_control_loop.md) | `franka::CartesianPose` |
| Cartesian velocity | [`generate_cartesian_velocity_motion`](examples/cpp/11_generate_cartesian_velocity_motion.md), [`generate_cartesian_velocity_motion_external_control_loop`](examples/cpp/13_generate_cartesian_velocity_motion_external_control_loop.md) | `franka::CartesianVelocities` |
| Joint torque | [`joint_impedance_control`](examples/cpp/17_joint_impedance_control.md), [`cartesian_impedance_control`](examples/cpp/18_cartesian_impedance_control.md), [`force_control`](examples/cpp/19_force_control.md), [`motion_with_control`](examples/cpp/20_motion_with_control.md), [`motion_with_control_external_control_loop`](examples/cpp/16_motion_with_control_external_control_loop.md) | `franka::Torques` |

The `*_external_control_loop` files are external-control-loop variants of the corresponding control type. All files must be read from the patched `libfranka/examples/<model>/` of the selected robot.

## State and Model Data

| Data | Source | Typical Use |
|---|---|---|
| `franka::RobotState` | `read()`, `readOnce()`, or the control callback argument | Joint, end-effector, velocity, torque, and external-torque estimates |
| `franka::Model` | `robot.loadModel()` | Gravity, Coriolis terms, end-effector pose, Jacobian |
| `franka::Duration` | Control callback argument | Time integration and periodic target generation |

## Callback Principles

1. Keep targets continuous; the first command should not jump away from the current state.
2. Avoid logging, network requests, file I/O, large dynamic allocations, and long lock waits in callbacks.
3. Give every example a clear stop condition and end with zero velocity or controlled torque.
4. Use torque and rate limits for torque control, and start with conservative gains.

```{warning}
FCI control-mode switching differs from ordinary C++ SDK motion commands. Do not mix blocking ordinary SDK motion APIs inside realtime callbacks. Complete an on-site safety check before running any motion or torque example.
```

# 12 Cartesian Pose External Control Loop

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

Source: `libfranka/examples/<model>/generate_cartesian_pose_motion_external_control_loop.cpp`.

Sends Cartesian poses through an explicit active-control read/write loop instead of handing a callback to Robot::control().

`<model>` is the selected patched robot directory: `diana3`, `diana7`, or `diana7G2`.

```bash
./build/libfranka/examples/<model>/generate_cartesian_pose_motion_external_control_loop <robot-ip>
```

| Used API | Purpose in this example |
|---|---|
| `startCartesianPoseControl()` | Starts the Cartesian-pose external-control session. |
| `ActiveControl::readOnce()` | Reads the current state and cycle period. |
| `ActiveControl::writeOnce()` | Writes the Cartesian-pose command for this cycle. |
## Example flow

Move to the initial pose → startCartesianPoseControl() → loop readOnce() → generate CartesianPose → writeOnce() until finished.

### Key source excerpt

```cpp
auto active_control = robot.startCartesianPoseControl(
    research_interface::robot::Move::ControllerMode::kJointImpedance);
auto [robot_state, duration] = active_control->readOnce();
auto command = callback_control(robot_state, duration);
active_control->writeOnce(command);
```

(fci-en-cpp-12_generate_cartesian_pose_motion_external_control_loop-api)=
## API usage and call examples

(fci-en-cpp-12_generate_cartesian_pose_motion_external_control_loop-api-165)=
### `startCartesianPoseControl()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Robot::startCartesianPoseControl()` | `std::unique_ptr<ActiveControlBase> startCartesianPoseControl(const research_interface::robot::Move::ControllerMode& control_type)` | Returns the active-control object; control conflicts, network interruptions or robot errors throw `ControlException`. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `control_type` | Input, `research_interface::robot::Move::ControllerMode` | Internal controller mode, commonly `kJointImpedance` or `kCartesianImpedance`. |

`startCartesianPoseControl()` starts the external-control mode. After it starts, the example calls `readOnce()` every cycle to read the state and cycle period, and then writes the target command with `writeOnce(CartesianPose)`.

```{rubric} Call example
```

```cpp
auto active_control = robot.startCartesianPoseControl(
    research_interface::robot::Move::ControllerMode::kJointImpedance);
```


````

(fci-en-cpp-12_generate_cartesian_pose_motion_external_control_loop-api-166)=
### `ActiveControl::readOnce()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `ActiveControlBase::readOnce` | `virtual std::pair<RobotState, Duration> readOnce()` | Returns the current `RobotState` and the `Duration` since the previous read; network, protocol or robot errors throw exceptions. |

`readOnce()` is the read entry point of each external-control-loop cycle. It waits for a new state and returns the duration of this cycle; the example then computes the next command from the state.

```{rubric} Call example
```

```cpp
auto [robot_state, period] = active_control->readOnce();
```


````

(fci-en-cpp-12_generate_cartesian_pose_motion_external_control_loop-api-167)=
### `ActiveControl::writeOnce()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `ActiveControlBase::writeOnce` | `virtual void writeOnce(const CartesianPose& motion_generator_input) = 0` | No return value; a command type that does not match the current control mode throws `ControlException`. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `motion_generator_input` | Input, `const CartesianPose&` | End-effector target pose command for this cycle (internal controller). |

`writeOnce()` is the write entry point of each external-control-loop cycle. It must match the control mode that was started: joint-position mode writes `JointPositions`, joint-velocity mode writes `JointVelocities`, Cartesian modes write the corresponding command, and torque mode writes `Torques`. This example is started with `startCartesianPoseControl()`, so it writes `CartesianPose`. A two-argument overload `writeOnce(const CartesianPose&, const std::optional<const Torques>&)` can additionally carry a torque command; this example does not use it.

```{rubric} Call example
```

```cpp
active_control->writeOnce(command);
```


````

```{warning}
Risk: Motion. This example sends control commands; confirm the workspace, emergency stop, and collision thresholds before running it.
```

```{note}
The code excerpts on this page are adapted from the libfranka examples (Copyright (c) 2023 Franka Robotics GmbH, Apache License 2.0) and modified for Diana robots; the adapted parts are Copyright (c) 2026 Agile Robots SE. See "License and Third-Party Notices" in the [Manual Overview](/about/overview.md).
```

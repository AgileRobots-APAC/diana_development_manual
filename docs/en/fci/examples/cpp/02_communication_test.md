# 02 Communication Performance Check

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

Source: `libfranka/examples/<model>/communication_test.cpp`.

The program collects statistics on `control_command_success_rate`, lost cycles and the success rate. It is not read-only: it first moves to an initial pose and then enters a zero-torque control session.

`<model>` is the selected patched robot directory: `diana3`, `diana7`, or `diana7G2`.

```bash
./build/libfranka/examples/<model>/communication_test <robot-ip>
```

| Used API | Purpose in this example |
|---|---|
| `MotionGenerator` | Generates and executes the motion to the test initial pose. |
| `Robot::control()` | Moves to the test initial pose. |
| `startTorqueControl()` | Opens the torque read/write control session. |
| `readOnce()` | Reads the state and cycle period every cycle. |
| `writeOnce()` | Writes a zero-torque command every cycle. |
| `control_command_success_rate` | Measures the control-communication success rate. |
## Example flow

Parse the robot address → create Robot → move to the initial pose → start torque control → read the state and write zero torques → aggregate communication metrics → end the session.

### Key source excerpt

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

(fci-en-cpp-02_communication_test-api)=
## API usage and call examples

(fci-en-cpp-02_communication_test-api-125)=
### `Robot::startTorqueControl()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Robot::startTorqueControl` | `std::unique_ptr<ActiveControlBase> startTorqueControl()` | Returns the active-control object; control conflicts, network interruptions or robot errors throw `ControlException`. |

`startTorqueControl()` starts the torque external-control mode. After the call, the returned `ActiveControlBase` is used to periodically call `readOnce()` / `writeOnce(Torques)` for reading and writing.

```{rubric} Call example
```

```cpp
auto active_control = robot.startTorqueControl();
```


````

(fci-en-cpp-02_communication_test-api-126)=
### `readOnce()`

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

(fci-en-cpp-02_communication_test-api-127)=
### `writeOnce()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `ActiveControlBase::writeOnce` | `virtual void writeOnce(const Torques& control_input) = 0` | No return value; a command type that does not match the current control mode throws `ControlException`. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `control_input` | Input, `const Torques&` | Joint-torque command for this cycle; this example writes zero torque every cycle. |

`writeOnce()` is the write entry point of each external-control-loop cycle. It must match the control mode that was started: joint-position mode writes `JointPositions`, joint-velocity mode writes `JointVelocities`, Cartesian modes write the corresponding command, and torque mode writes `Torques`. This example is started with `startTorqueControl()`, so it calls the overload that takes only `Torques`. The other overloads take `JointPositions`, `JointVelocities`, `CartesianPose`, or `CartesianVelocities`, optionally together with a `std::optional<const Torques>`.

```{rubric} Call example
```

```cpp
active_control->writeOnce(zero_torques);
```


````

(fci-en-cpp-02_communication_test-api-128)=
### `control_command_success_rate`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `RobotState::control_command_success_rate` | `double control_command_success_rate` | Field value is the fraction of the last 100 control commands successfully received by the robot, range `[0, 1]`; it is 0 when no control or motion-generator loop is running. |

`control_command_success_rate` is the communication-quality field in `RobotState`. The example reads it every cycle, accumulates the maximum, minimum and average, and at the end gives network/host configuration advice based on the average success rate.

```{rubric} Call example
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
Risk: Torque / motion. The program first moves to an initial pose and then enters torque control; run it only after on-site safety conditions are confirmed, and check the workspace, emergency stop, and collision thresholds.
```

```{note}
The code excerpts on this page are adapted from the libfranka examples (Copyright (c) 2023 Franka Robotics GmbH, Apache License 2.0) and modified for Diana robots; the adapted parts are Copyright (c) 2026 Agile Robots SE. See "License and Third-Party Notices" in the [Manual Overview](/about/overview.md).
```

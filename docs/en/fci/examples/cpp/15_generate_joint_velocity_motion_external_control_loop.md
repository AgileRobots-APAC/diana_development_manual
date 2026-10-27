# 15 generate_joint_velocity_motion_external_control_loop

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

Source: `libfranka/examples/<model>/generate_joint_velocity_motion_external_control_loop.cpp`.

Sends joint-velocity commands through an explicit read/write loop and stops control when the callback finishes.

`<model>` is the selected patched robot directory: `diana3`, `diana7`, or `diana7G2`.

```bash
./build/libfranka/examples/<model>/generate_joint_velocity_motion_external_control_loop <robot-ip>
```

| Used API | Purpose in this example |
|---|---|
| `startJointVelocityControl()` | Starts the joint-velocity external-control session. |
## Example flow

Move to the initial pose → startJointVelocityControl() → read state/period in a loop → write JointVelocities.

### Key source excerpt

```cpp
auto active_control = robot.startJointVelocityControl(
    research_interface::robot::Move::ControllerMode::kJointImpedance);
auto [robot_state, duration] = active_control->readOnce();
auto command = callback_control(robot_state, duration);
active_control->writeOnce(command);
```

(fci-en-cpp-15_generate_joint_velocity_motion_external_control_loop-api)=
## API usage and call examples

(fci-en-cpp-15_generate_joint_velocity_motion_external_control_loop-api-177)=
### `startJointVelocityControl()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Robot::startJointVelocityControl()` | `std::unique_ptr<ActiveControlBase> startJointVelocityControl(const research_interface::robot::Move::ControllerMode& control_type)` | Returns an active-control object; control conflicts, network interruptions or robot errors throw `ControlException`. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `control_type` | Input, `research_interface::robot::Move::ControllerMode` | Internal controller mode, commonly `kJointImpedance` or `kCartesianImpedance`. |

`startJointVelocityControl()` starts the external-control mode. After it starts, the example calls `readOnce()` every cycle to read the state and period, then writes the target command with `writeOnce(JointVelocities)`.

```{rubric} Call example
```

```cpp
auto active_control = robot.startJointVelocityControl(
    research_interface::robot::Move::ControllerMode::kJointImpedance);
```


````

```{note}
The code excerpts on this page are adapted from the libfranka examples (Copyright (c) 2023 Franka Robotics GmbH, Apache License 2.0) and modified for Diana robots; the adapted parts are Copyright (c) 2026 Agile Robots SE. See "License and Third-Party Notices" in the [Manual Overview](/about/overview.md).
```

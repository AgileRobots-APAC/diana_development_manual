# 10 Generate Cartesian Pose Motion

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

Source: `libfranka/examples/<model>/generate_cartesian_pose_motion.cpp`.

Moves the end effector along a circular trajectory in the real-time callback and sends Cartesian pose targets.

`<model>` is the selected patched robot directory: `diana3`, `diana7`, or `diana7G2`.

```bash
./build/libfranka/examples/<model>/generate_cartesian_pose_motion <robot-ip>
```

| Used API | Purpose in this example |
|---|---|
| `Robot::control()` | Starts the Cartesian-pose real-time control callback. |
| `CartesianPose` | Wraps the end-effector target pose for each cycle. |
| `MotionFinished()` | Marks the last command frame and ends the control loop. |
## Example flow

Move to the initial pose → read O_T_EE → update the translation terms of the pose matrix → MotionFinished().

Compared with upstream libfranka, the Diana patched versions remove the `setCollisionBehavior()` call.

### Key source excerpt

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

(fci-en-cpp-10_generate_cartesian_pose_motion-api)=
## API usage and call examples

(fci-en-cpp-10_generate_cartesian_pose_motion-api-157)=
### `Robot::control()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Robot::control` | `void control(std::function<CartesianPose(const RobotState&, Duration)> callback, ControllerMode controller_mode = ControllerMode::kJointImpedance, bool limit_rate = false, double cutoff_frequency = kDefaultCutoffFrequency)` | No return value; the end of control is signalled by the callback returning `MotionFinished(...)`; control conflicts, realtime configuration failures, network interruptions or invalid commands throw exceptions. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `callback` | Input, `std::function` | Generates the target command in every control cycle. |
| `controller_mode` | Input, `ControllerMode`, default `kJointImpedance` | Internal controller mode. |
| `limit_rate` | Input, `bool`, default `false` | Whether rate limiting is enabled; may alter the trajectory. |
| `cutoff_frequency` | Input, `double` | Low-pass filter cutoff frequency. |

`control()` starts the 1 kHz FCI control loop. In every cycle the callback receives `RobotState` and `Duration` and returns a command such as `JointPositions`, `JointVelocities`, `CartesianPose`, `CartesianVelocities` or `Torques`. Only one control/motion-generation loop can be active at a time. In this example the callback returns `CartesianPose`.

```{rubric} Call example
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
Risk: Motion. This example sends control commands; confirm the workspace, emergency stop, and collision thresholds before running it.
```

```{note}
The code excerpts on this page are adapted from the libfranka examples (Copyright (c) 2023 Franka Robotics GmbH, Apache License 2.0) and modified for Diana robots; the adapted parts are Copyright (c) 2026 Agile Robots SE. See "License and Third-Party Notices" in the [Manual Overview](/about/overview.md).
```

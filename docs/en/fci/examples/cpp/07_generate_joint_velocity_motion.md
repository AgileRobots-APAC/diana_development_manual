# 07 generate_joint_velocity_motion

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

Source: `libfranka/examples/<model>/generate_joint_velocity_motion.cpp`.

Outputs joint-velocity commands in the real-time callback and marks the motion as finished after the given duration.

`<model>` is the selected patched robot directory: `diana3`, `diana7`, or `diana7G2`.

```bash
./build/libfranka/examples/<model>/generate_joint_velocity_motion <robot-ip>
```

| Used API | Purpose in this example |
|---|---|
| `Robot::control()` | Starts the joint-velocity real-time control callback. |
| `JointVelocities` | Wraps the seven-axis target joint velocities for each cycle. |
## Example flow

Move to the initial pose → the control callback computes velocities from Duration → return JointVelocities / MotionFinished().

Compared with upstream libfranka, the Diana patched versions remove the `setCollisionBehavior()` call.

The joint-4 velocity differs per model: `-omega` on diana3 and `omega / 2` on diana7 and diana7G2 (the code below shows the diana7 value).

### Key source excerpt

```cpp
double cycle = std::floor(std::pow(-1.0, (time - std::fmod(time, time_max)) / time_max));
double omega = cycle * omega_max / 2.0 * (1.0 - std::cos(2.0 * M_PI / time_max * time));

franka::JointVelocities velocities = {{0.0, 0.0, 0.0, omega / 2, omega, omega, omega}};

if (time >= 2 * time_max) {
  return franka::MotionFinished(velocities);
}
return velocities;
```

(fci-en-cpp-07_generate_joint_velocity_motion-api)=
## API usage and call examples

(fci-en-cpp-07_generate_joint_velocity_motion-api-145)=
### `Robot::control()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Robot::control` | `void control(std::function<JointVelocities(const RobotState&, Duration)> callback, ControllerMode controller_mode = ControllerMode::kJointImpedance, bool limit_rate = false, double cutoff_frequency = kDefaultCutoffFrequency)` | No return value; the end of control is signaled by the callback returning `MotionFinished(...)`; control conflicts, realtime configuration failures, network interruptions or invalid commands throw exceptions. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `callback` | Input, `std::function` | Generates the target command in each control cycle. |
| `controller_mode` | Input, `ControllerMode`, default `kJointImpedance` | Internal controller mode. |
| `limit_rate` | Input, `bool`, default `false` | Whether to enable rate limiting; may alter the trajectory. |
| `cutoff_frequency` | Input, `double` | Cutoff frequency of the low-pass filter. |

`control()` starts the 1 kHz FCI control loop. In each cycle the callback receives a `RobotState` and a `Duration` and returns a command such as `JointPositions`, `JointVelocities`, `CartesianPose`, `CartesianVelocities` or `Torques`. Only one control/motion-generation loop can be active at a time.

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

(fci-en-cpp-07_generate_joint_velocity_motion-api-147)=
### `JointVelocities`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `franka::JointVelocities` | `JointVelocities(const std::array<double, 7>& joint_velocities)` | Returns a joint-velocity command object; throws `std::invalid_argument` if an initializer list has the wrong number of elements. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `joint_velocities` | Input, `std::array<double,7>` | Target joint velocities, in rad/s. |

`JointVelocities` wraps the seven-axis target joint velocities, in rad/s. The velocity motion-generator example returns this object every cycle and marks the end with `MotionFinished()`.

```{rubric} Call example
```

```cpp
franka::JointVelocities velocities = {{0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0}};
```


````

```{note}
The code excerpts on this page are adapted from the libfranka examples (Copyright (c) 2023 Franka Robotics GmbH, Apache License 2.0) and modified for Diana robots; the adapted parts are Copyright (c) 2026 Agile Robots SE. See "License and Third-Party Notices" in the [Manual Overview](/about/overview.md).
```

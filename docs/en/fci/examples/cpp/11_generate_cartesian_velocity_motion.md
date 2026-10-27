# 11 generate_cartesian_velocity_motion

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

Source: `libfranka/examples/<model>/generate_cartesian_velocity_motion.cpp`.

Outputs end-effector Cartesian velocities in the real-time callback and completes the motion in joint-impedance mode.

`<model>` is the selected patched robot directory: `diana3`, `diana7`, or `diana7G2`.

```bash
./build/libfranka/examples/<model>/generate_cartesian_velocity_motion <robot-ip>
```

| Used API | Purpose in this example |
|---|---|
| `Robot::control()` | Starts the Cartesian-velocity real-time control callback. |
| `CartesianVelocities` | Wraps the end-effector linear and angular velocity command. |
## Example flow

Move to the initial pose → the callback computes velocities per cycle → return CartesianVelocities.

Compared with upstream libfranka, the Diana patched versions remove the `setJointImpedance()` and `setCollisionBehavior()` calls.

### Key source excerpt

```cpp
double cycle = std::floor(pow(-1.0, (time - std::fmod(time, time_max)) / time_max));
double velocity = cycle * v_max / 2.0 * (1.0 - std::cos(2.0 * M_PI / time_max * time));
double velocity_x = std::cos(angle) * velocity;
double velocity_z = -std::sin(angle) * velocity;

franka::CartesianVelocities output = {{velocity_x, 0.0, velocity_z, 0.0, 0.0, 0.0}};
if (time >= 2 * time_max) {
  return franka::MotionFinished(output);
}
return output;
```

(fci-en-cpp-11_generate_cartesian_velocity_motion-api)=
## API usage and call examples

(fci-en-cpp-11_generate_cartesian_velocity_motion-api-162)=
### `Robot::control()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Robot::control` | `void control(std::function<CartesianVelocities(const RobotState&, Duration)> callback, ControllerMode controller_mode = ControllerMode::kJointImpedance, bool limit_rate = false, double cutoff_frequency = kDefaultCutoffFrequency)` | No return value; the end of control is signaled by the callback returning `MotionFinished(...)`; control conflicts, realtime configuration failures, network interruptions or invalid commands throw exceptions. |

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

(fci-en-cpp-11_generate_cartesian_velocity_motion-api-163)=
### `CartesianVelocities`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `franka::CartesianVelocities` | `CartesianVelocities(const std::array<double, 6>& cartesian_velocities, const std::array<double, 2>& elbow = {})` | Returns a Cartesian-velocity command object; throws `std::invalid_argument` if an initializer list has the wrong number of elements. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `cartesian_velocities` | Input, `std::array<double,6>` | `x/y/z` linear velocities and `wx/wy/wz` angular velocities. |
| `elbow` | Input, `std::array<double,2>`, optional | Elbow configuration. |

`CartesianVelocities` wraps the end-effector Cartesian velocity: the first three entries are linear velocities in m/s, the last three are angular velocities in rad/s, expressed in the base frame.

```{rubric} Call example
```

```cpp
franka::CartesianVelocities velocity = {{0.0, 0.0, 0.05, 0.0, 0.0, 0.0}};
```


````

```{note}
The code excerpts on this page are adapted from the libfranka examples (Copyright (c) 2023 Franka Robotics GmbH, Apache License 2.0) and modified for Diana robots; the adapted parts are Copyright (c) 2026 Agile Robots SE. See "License and Third-Party Notices" in the [Manual Overview](/about/overview.md).
```

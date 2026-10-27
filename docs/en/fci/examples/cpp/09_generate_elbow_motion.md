# 09 Generate Cartesian Motion with Elbow Redundancy

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

Source: `libfranka/examples/<model>/generate_elbow_motion.cpp`.

Sets the elbow redundancy parameter together with the Cartesian pose target, demonstrating redundant-configuration control of a 7-DoF arm.

`<model>` is the selected patched robot directory: `diana3`, `diana7`, or `diana7G2`.

```bash
./build/libfranka/examples/<model>/generate_elbow_motion <robot-ip>
```

| Used API | Purpose in this example |
|---|---|
| `Robot::control()` | Starts the Cartesian-pose real-time control callback. |
| `CartesianPose` | Wraps the end-effector target pose and the elbow configuration. |
| `RobotState::O_T_EE` | Reads the current measured pose as the trajectory start point. |
## Example flow

Move to the initial pose → the callback keeps the initial O_T_EE pose and gradually increases elbow[0] → return CartesianPose / MotionFinished().

Compared with upstream libfranka, the Diana patched versions remove the `setCollisionBehavior()` call.

The elbow swing amplitude differs per model: `M_PI / 16.0` on diana3 and diana7, `M_PI / 20.0` on diana7G2 (the code below shows the diana7 value).

### Key source excerpt

```cpp
double angle = M_PI / 16.0 * (1.0 - std::cos(M_PI / 5.0 * time));

auto elbow = initial_elbow;
elbow[0] += angle;

if (time >= 10.0) {
  return franka::MotionFinished({initial_pose, elbow});
}
return {initial_pose, elbow};
```

(fci-en-cpp-09_generate_elbow_motion-api)=
## API usage and call examples

(fci-en-cpp-09_generate_elbow_motion-api-155)=
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

`control()` starts the 1 kHz FCI control loop. In every cycle the callback receives `RobotState` and `Duration` and returns a command such as `JointPositions`, `JointVelocities`, `CartesianPose`, `CartesianVelocities` or `Torques`. Only one control/motion-generation loop can be active at a time.

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

(fci-en-cpp-09_generate_elbow_motion-api-153)=
### `CartesianPose`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `franka::CartesianPose` | `CartesianPose(const std::array<double, 16>& cartesian_pose, const std::array<double, 2>& elbow) noexcept` | Returns a Cartesian-pose command object; there is also a pose-only single-argument overload and `std::initializer_list<double>` overloads (which throw `std::invalid_argument` if the number of elements is wrong). |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `cartesian_pose` | Input, `std::array<double,16>` | Target 4x4 pose matrix, column-major. |
| `elbow` | Input, `std::array<double,2>` | Elbow configuration: `elbow[0]` is the 3rd joint position (rad), `elbow[1]` is the flip direction of the 4th joint (+1 / 0 / -1). |

`CartesianPose` wraps the target homogeneous transformation matrix of the end effector relative to base frame `O`, flattened in column-major order. When constructed with an elbow, it also specifies the elbow configuration.

```{rubric} Call example
```

```cpp
franka::CartesianPose pose_desired(initial_pose);
pose_desired.O_T_EE[13] += 0.05;
```


````

(fci-en-cpp-09_generate_elbow_motion-api-154)=
### `RobotState::O_T_EE`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `RobotState::O_T_EE` | `std::array<double, 16> O_T_EE` | Field value is the current measured end-effector pose, a 4x4 homogeneous matrix flattened in column-major order. |

`O_T_EE` is the currently measured end-effector pose, from base frame `O` to end-effector frame `EE`. Cartesian-pose examples use it as the start point and only modify the translation or elbow-related targets.

```{rubric} Call example
```

```cpp
initial_pose = robot_state.O_T_EE;
```


````

```{warning}
Risk: Motion. This example sends control commands; confirm the workspace, emergency stop, and collision thresholds before running it.
```

```{note}
The code excerpts on this page are adapted from the libfranka examples (Copyright (c) 2023 Franka Robotics GmbH, Apache License 2.0) and modified for Diana robots; the adapted parts are Copyright (c) 2026 Agile Robots SE. See "License and Third-Party Notices" in the [Manual Overview](/about/overview.md).
```

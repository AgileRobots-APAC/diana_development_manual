# 06 Generate Joint Position Motion

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

Source: `libfranka/examples/<model>/generate_joint_position_motion.cpp`.

Generates smooth position changes on joints 4, 5 and 7 in the real-time callback and finishes after about 5 seconds.

`<model>` is the selected patched robot directory: `diana3`, `diana7`, or `diana7G2`.

```bash
./build/libfranka/examples/<model>/generate_joint_position_motion <robot-ip>
```

| Used API | Purpose in this example |
|---|---|
| `Robot::control()` | Starts the joint-position real-time control callback. |
| `RobotState::q` | Reads the current joint angles as the motion start point. |
| `Duration::toSec()` | Accumulates control-period time to build the trajectory phase. |
| `JointPositions` | Wraps the seven-axis target joint angles for each cycle. |
| `MotionFinished()` | Marks the last command frame and ends the control loop. |
## Example flow

Move to the initial pose → robot.control(position callback) → accumulate time each cycle and return JointPositions → MotionFinished().

Compared with upstream libfranka, the Diana patched versions remove the `setCollisionBehavior()` call and change the joint-4 offset to `delta_angle / 2`.

### Key source excerpt

```cpp
double delta_angle = M_PI / 8.0 * (1 - std::cos(M_PI / 2.5 * time));

franka::JointPositions output = {{initial_position[0], initial_position[1],
                                  initial_position[2], initial_position[3] + delta_angle / 2,
                                  initial_position[4] + delta_angle, initial_position[5],
                                  initial_position[6] + delta_angle}};

if (time >= 5.0) {
  return franka::MotionFinished(output);
}
return output;
```

(fci-en-cpp-06_generate_joint_position_motion-api)=
## API usage and call examples

(fci-en-cpp-06_generate_joint_position_motion-api-140)=
### `Robot::control()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Robot::control` | `void control(std::function<JointPositions(const RobotState&, Duration)> callback, ControllerMode controller_mode = ControllerMode::kJointImpedance, bool limit_rate = false, double cutoff_frequency = kDefaultCutoffFrequency)` | No return value; the end of control is signalled by the callback returning `MotionFinished(...)`; control conflicts, realtime configuration failures, network interruptions or invalid commands throw exceptions. |

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

(fci-en-cpp-06_generate_joint_position_motion-api-141)=
### `RobotState::q`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `RobotState::q` | `std::array<double, 7> q` | Field value is the current measured joint angles, in rad. |

`q` is the current joint-position array in `RobotState`. Joint-position control examples usually take `q` as the start point and generate smooth targets from it, instead of sending commands directly from an assumed zero position.

```{rubric} Call example
```

```cpp
std::array<double, 7> initial_position = robot_state.q;
```


````

(fci-en-cpp-06_generate_joint_position_motion-api-142)=
### `Duration::toSec()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Duration::toSec` | `double toSec() const noexcept` | Returns the duration in s. |

`Duration::toSec()` converts the control-period duration to seconds. The example uses it to accumulate trajectory time and generate sinusoidal or piecewise motion as a function of time.

```{rubric} Call example
```

```cpp
time += period.toSec();
```


````

(fci-en-cpp-06_generate_joint_position_motion-api-143)=
### `JointPositions`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `franka::JointPositions` | `JointPositions(const std::array<double, 7>& joint_positions) noexcept` | Returns a joint-position command object; there is also a `JointPositions(std::initializer_list<double>)` overload, which throws `std::invalid_argument` if the initializer list has the wrong number of elements. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `joint_positions` | Input, `std::array<double,7>` | Target joint angles, in rad. |

`JointPositions` wraps the seven target joint angles, in rad. A position motion generator or an external control loop uses it as the target command for each cycle.

```{rubric} Call example
```

```cpp
franka::JointPositions output = {{q0, q1, q2, q3, q4, q5, q6}};
```


````

(fci-en-cpp-06_generate_joint_position_motion-api-144)=
### `MotionFinished()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `franka::MotionFinished` | `Command MotionFinished(Command command) noexcept` | Returns a command object of the same type with its `motion_finished` flag set to `true`. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `command` | Input/output, command object | The command object to send as the last frame. |

`MotionFinished()` tells `Robot::control()` or an external control loop that the command being returned is the last one and the control loop can end. It supports `Torques`, `JointPositions`, `JointVelocities`, `CartesianPose` and `CartesianVelocities`.

```{rubric} Call example
```

```cpp
if (time >= motion_time) {
  return franka::MotionFinished(output);
}
```


````

```{warning}
Risk: Motion. This example sends control commands; confirm the workspace, emergency stop, and collision thresholds before running it.
```

```{note}
The code excerpts on this page are adapted from the libfranka examples (Copyright (c) 2023 Franka Robotics GmbH, Apache License 2.0) and modified for Diana robots; the adapted parts are Copyright (c) 2026 Agile Robots SE. See "License and Third-Party Notices" in the [Manual Overview](/about/overview.md).
```

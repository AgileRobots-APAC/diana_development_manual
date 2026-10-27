# 05 joint_point_to_point_motion

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

Source: `libfranka/examples/<model>/joint_point_to_point_motion.cpp`.

Uses the shared example MotionGenerator to move to the seven-axis target joint angles given on the command line.

`<model>` is the selected patched robot directory: `diana3`, `diana7`, or `diana7G2`.

```bash
./build/libfranka/examples/<model>/joint_point_to_point_motion <robot-ip>
```

| Used API | Purpose in this example |
|---|---|
| `MotionGenerator` | Generates smooth joint-position commands from the target joint angles and the speed factor. |
| `Robot::setCollisionBehavior()` | Configures the collision and contact thresholds before the motion. |
| `Robot::control()` | Starts the real-time control loop and executes the motion generator. |
## Example flow

Read the seven joint targets and the speed factor → set collision thresholds → construct MotionGenerator → robot.control().

Model differences: the diana3 patched version removes the `setCollisionBehavior()` call; diana7 and diana7G2 keep it but change the sixth component of both upper Cartesian force thresholds (acceleration and nominal) to 30.0.

### Key source excerpt

```cpp
std::array<double, 7> q_goal = {/* 7 joint targets read from the command line */};
MotionGenerator motion_generator(speed_factor, q_goal);
robot.control(motion_generator);
```

(fci-en-cpp-05_joint_point_to_point_motion-api)=
## API usage and call examples

(fci-en-cpp-05_joint_point_to_point_motion-api-137)=
### `MotionGenerator`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `MotionGenerator` | `MotionGenerator(double speed_factor, const std::array<double, 7>& q_goal)` | Constructs the example helper object; its callback returns `franka::JointPositions`. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `speed_factor` | Input, `double` | Speed scaling factor, usually between 0 and 1. |
| `q_goal` | Input, `std::array<double,7>` | Target joint angles, in rad. |

`MotionGenerator` is a trajectory helper class from the libfranka examples, not a robot-controller interface. It generates smooth joint-position commands from the target joint angles and the speed factor, and is then passed to `Robot::control()`. In this example the target is the seven joint angles given on the command line.

```{rubric} Call example
```

```cpp
MotionGenerator motion_generator(0.5, q_goal);
robot.control(motion_generator);
```


````

(fci-en-cpp-05_joint_point_to_point_motion-api-138)=
### `Robot::setCollisionBehavior()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Robot::setCollisionBehavior` | `void setCollisionBehavior(const std::array<double, 7>& lower_torque_thresholds, const std::array<double, 7>& upper_torque_thresholds, const std::array<double, 6>& lower_force_thresholds, const std::array<double, 6>& upper_force_thresholds)` | No return value; throws an exception on invalid arguments, network interruption, or if the robot rejects the configuration. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `lower_torque_thresholds` | Input, `std::array<double,7>` | Per-joint lower contact thresholds, in Nm. |
| `upper_torque_thresholds` | Input, `std::array<double,7>` | Per-joint upper collision thresholds, in Nm. |
| `lower_force_thresholds` | Input, `std::array<double,6>` | Cartesian lower contact thresholds. |
| `upper_force_thresholds` | Input, `std::array<double,6>` | Cartesian upper collision thresholds. |

`setCollisionBehavior()` configures the collision/contact thresholds. The thresholds are not a substitute for safety limits; the example sets fairly conservative thresholds before the motion so that the controller protection triggers easily.

```{rubric} Call example
```

```cpp
robot.setCollisionBehavior(
    {{20.0, 20.0, 18.0, 18.0, 16.0, 14.0, 12.0}},
    {{20.0, 20.0, 18.0, 18.0, 16.0, 14.0, 12.0}},
    {{20.0, 20.0, 20.0, 25.0, 25.0, 25.0}},
    {{20.0, 20.0, 20.0, 25.0, 25.0, 25.0}});
```


````

(fci-en-cpp-05_joint_point_to_point_motion-api-139)=
### `Robot::control()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Robot::control` | `void control(std::function<JointPositions(const RobotState&, Duration)> callback, ControllerMode controller_mode = ControllerMode::kJointImpedance, bool limit_rate = false, double cutoff_frequency = kDefaultCutoffFrequency)` | No return value; the end of control is signaled by the callback returning `MotionFinished(...)`; control conflicts, realtime configuration failures, network interruptions or invalid commands throw exceptions. |

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


```{warning}
Risk: Motion. This example sends control commands. Confirm workspace, emergency stop, and collision thresholds before running it.
```

```{note}
The code excerpts on this page are adapted from the libfranka examples (Copyright (c) 2023 Franka Robotics GmbH, Apache License 2.0) and modified for Diana robots; the adapted parts are Copyright (c) 2026 Agile Robots SE. See "License and Third-Party Notices" in the [Manual Overview](/about/overview.md).
```

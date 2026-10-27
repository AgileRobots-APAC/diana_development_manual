# 20 motion_with_control

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

Source: `libfranka/examples/<model>/motion_with_control.cpp`.

Combines joint-velocity motion generation and torque control in one control session, and exports the log records on a control exception.

`<model>` is the selected patched robot directory: `diana3`, `diana7`, or `diana7G2`.

```bash
./build/libfranka/examples/<model>/motion_with_control <robot-ip>
```

| Used API | Purpose in this example |
|---|---|
| `Robot::control()` | Starts the combined motion-generator and torque-control callbacks. |
| `Record` | Log records carried by the control exception, exported as CSV on failure. |
## Example flow

Move to the initial pose → define velocity and torque callbacks → combined robot.control() → catch ControlException → export e.log with logToCSV().

### Key source excerpt

```cpp
try {
  robot.control(
      [&](const franka::RobotState& robot_state, franka::Duration) -> franka::Torques {
        return controller.step(robot_state);
      },
      [&](const franka::RobotState&, franka::Duration period) -> franka::JointVelocities {
        // ... joint-velocity trajectory ...
      });
} catch (const franka::ControlException& e) {
  writeLogToFile(e.log);  // log_stream << franka::logToCSV(log);
}
```

(fci-en-cpp-20_motion_with_control-api)=
## API usage and call examples

(fci-en-cpp-20_motion_with_control-api-198)=
### `Robot::control()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Robot::control` | `void control(std::function<Torques(const RobotState&, franka::Duration)> control_callback, std::function<JointVelocities(const RobotState&, franka::Duration)> motion_generator_callback, bool limit_rate = false, double cutoff_frequency = kDefaultCutoffFrequency)` | No return value; the callback ends control by returning `MotionFinished(...)`; throws an exception on a control conflict, real-time configuration failure, network interruption, or invalid command. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `control_callback` | Input, `std::function` | Returns a `Torques` command every control cycle. |
| `motion_generator_callback` | Input, `std::function` | Returns a `JointVelocities` motion-generator command every control cycle. |
| `limit_rate` | Input, `bool`, default `false` | Whether to enable rate limiting; this can change the trajectory. |
| `cutoff_frequency` | Input, `double` | Low-pass filter cutoff frequency. |

`control()` starts the 1 kHz FCI control loop. This example uses the "torque control + joint-velocity motion generation" overload: the motion-generator callback commands a velocity for a single joint from a pre-generated trajectory, and the torque callback computes joint torques with the example's controller. Only one control/motion-generation loop can be active at a time.

```{rubric} Call example
```

```cpp
robot.control(
    [&](const franka::RobotState& robot_state, franka::Duration) -> franka::Torques {
      return controller.step(robot_state);
    },
    [&](const franka::RobotState&, franka::Duration period) -> franka::JointVelocities {
      index += period.toMSec();
      if (index >= trajectory.size()) {
        index = trajectory.size() - 1;
      }
      franka::JointVelocities velocities{{0, 0, 0, 0, 0, 0, 0}};
      velocities.dq[joint_number] = trajectory[index];
      if (index >= trajectory.size() - 1) {
        return franka::MotionFinished(velocities);
      }
      return velocities;
    });
```


````

(fci-en-cpp-20_motion_with_control-api-199)=
### `Record`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `franka::Record` | `struct Record { RobotState state; RobotCommand command; }` | Data structure; no return value. |

| Member | Type | Meaning |
| --- | --- | --- |
| `state` | `RobotState` | Robot state of time step n+1. |
| `command` | `RobotCommand` | Robot command of time step n (after rate limiting, if enabled). |

`Record` is the libfranka log-record structure defined in `franka/logging/robot_state_log.hpp`. When control fails, the thrown `ControlException` carries the most recent records in its `log` member (`std::vector<franka::Record>`); after catching the exception, the example calls `franka::logToCSV(log)` to convert it to a CSV string and writes it to a log file in the temporary directory.

```{rubric} Call example
```

```cpp
} catch (const franka::ControlException& e) {
  std::cout << e.what() << std::endl;
  writeLogToFile(e.log);  // const std::vector<franka::Record>&
  return -1;
}
// in writeLogToFile():
log_stream << franka::logToCSV(log);
```


````

```{note}
The code excerpts on this page are adapted from the libfranka examples (Copyright (c) 2023 Franka Robotics GmbH, Apache License 2.0) and modified for Diana robots; the adapted parts are Copyright (c) 2026 Agile Robots SE. See "License and Third-Party Notices" in the [Manual Overview](/about/overview.md).
```

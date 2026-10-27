# 01 Continuous State Reading

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

Source: `libfranka/examples/<model>/echo_robot_state.cpp`.

The program uses `robot.read()` to continuously read and print `franka::RobotState`, and exits after about 101 callbacks. It does not call `control()` and sends no motion or torque commands.

`<model>` is the selected patched robot directory: `diana3`, `diana7`, or `diana7G2`.

```bash
./build/libfranka/examples/<model>/echo_robot_state <robot-ip>
```

| Used API | Purpose in this example |
|---|---|
| `franka::Robot` | Establishes the FCI session. |
| `Robot::read()` | Continuously receives state data. |
| `franka::RobotState` | Provides and prints the robot state. |
## Example flow

Parse the robot address → create `franka::Robot` → enter the `read()` callback → print the state → stop when the callback count is reached → release the session.

### Key source excerpt

```cpp
size_t count = 0;
robot.read([&count](const franka::RobotState& robot_state) {
  std::cout << robot_state << std::endl;
  return count++ < 100;
});
```

(fci-en-cpp-01_echo_robot_state-api)=
## API usage and call examples

(fci-en-cpp-01_echo_robot_state-api-122)=
### `franka::Robot`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `franka::Robot` | `explicit Robot(const std::string& franka_address, RealtimeConfig realtime_config = RealtimeConfig::kEnforce, size_t log_size = 50)` | On success, yields the robot connection object; on failure, throws network-, version- or realtime-configuration-related exceptions. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `franka_address` | Input, `const std::string&` | IP address or hostname of the robot controller. |
| `realtime_config` | Input, `RealtimeConfig`, default `kEnforce` | Whether the current thread is required to be able to set realtime priority. |
| `log_size` | Input, `size_t`, default `50` | Number of recent state log entries kept when a `ControlException` occurs. |

`franka::Robot` maintains the network connection to the robot controller and provides the entry points for state reading, model loading and control. `realtime_config` defaults to enforced realtime; if realtime permissions are not configured, the example can be changed to `RealtimeConfig::kIgnore` as needed.

```{rubric} Call example
```

```cpp
franka::Robot robot(argv[1]);
```


````

(fci-en-cpp-01_echo_robot_state-api-123)=
### `Robot::read()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Robot::read` | `void read(std::function<bool(const RobotState&)> read_callback)` | No return value; reading continues while the callback returns `true` and stops when it returns `false`; control conflicts, network interruptions or robot errors throw exceptions. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `read_callback` | Input, `std::function<bool(const RobotState&)>` | Called once per received state frame; return `true` to keep reading, `false` to stop. |

`read()` continuously receives robot state and sends no motion or torque commands. The callback argument is the current `RobotState`; the example prints the state in the callback and returns a boolean that decides whether the loop continues.

```{rubric} Call example
```

```cpp
robot.read([](const franka::RobotState& state) {
  std::cout << state << std::endl;
  return true;
});
```


````

(fci-en-cpp-01_echo_robot_state-api-124)=
### `franka::RobotState`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `franka::RobotState` | `struct RobotState` | The state struct itself has no function return value; it is provided by `Robot::readOnce()`, `Robot::read()` or control callbacks. |
| `operator<<` | `std::ostream& operator<<(std::ostream& ostream, const franka::RobotState& robot_state)` | Returns the given output stream, allowing chained output. |

`RobotState` is a snapshot of the robot state, containing joint positions, velocities, torques, pose matrices, collision/contact flags and other fields. In the `read()` callback this example prints the whole state struct to standard output via `operator<<` and does not modify the object.

```{rubric} Call example
```

```cpp
robot.read([&count](const franka::RobotState& robot_state) {
  std::cout << robot_state << std::endl;
  return count++ < 100;
});
```


````

```{warning}
Risk: Read-only. This example only reads state and sends no motion or torque commands.
```

```{note}
The code excerpts on this page are adapted from the libfranka examples (Copyright (c) 2023 Franka Robotics GmbH, Apache License 2.0) and modified for Diana robots; the adapted parts are Copyright (c) 2026 Agile Robots SE. See "License and Third-Party Notices" in the [Manual Overview](/about/overview.md).
```

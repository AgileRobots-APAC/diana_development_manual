# 16 motion_with_control_external_control_loop

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

Source: `libfranka/examples/<model>/motion_with_control_external_control_loop.cpp`.

Combines joint-velocity motion generation and torque control in the same explicit external loop and records a control log.

`<model>` is the selected patched robot directory: `diana3`, `diana7`, or `diana7G2`.

```bash
./build/libfranka/examples/<model>/motion_with_control_external_control_loop <robot-ip>
```

| Used API | Purpose in this example |
|---|---|
| `Torques` | Wraps the torque control command. |
| `logToCSV()` | Exports the records after control finishes. |
## Example flow

Move to the initial pose → startJointVelocityControl() → each cycle read the state, compute velocities/torques and write the commands → record Records and export CSV.

### Key source excerpt

```cpp
auto [state, period] = active_control->readOnce();
auto velocities = motion_callback(state, period);
auto torques = torque_callback(state, period);
active_control->writeOnce(velocities, torques);
```

(fci-en-cpp-16_motion_with_control_external_control_loop-api)=
## API usage and call examples

(fci-en-cpp-16_motion_with_control_external_control_loop-api-183)=
### `Torques`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `franka::Torques` | `Torques(const std::array<double, 7>& torques)` | Returns a joint-torque command object; throws `std::invalid_argument` if an initializer list has the wrong number of elements. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `torques` | Input, `std::array<double,7>` | Desired joint torques, in Nm. |

`Torques` wraps the seven-axis joint-torque command, in Nm. The header notes that this command does not include gravity and friction compensation; the examples usually combine model terms with a control law to generate the target torques.

```{rubric} Call example
```

```cpp
franka::Torques tau_d(tau_d_array);
```


````

(fci-en-cpp-16_motion_with_control_external_control_loop-api-184)=
### `logToCSV()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `franka::logToCSV` | `std::string logToCSV(const std::vector<Record>& log)` | Returns the log as a CSV-formatted string; writing it to a file is up to the caller. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `log` | Input, `const std::vector<franka::Record>&` | Records to export, usually taken from `franka::ControlException::log`. |

`franka::logToCSV()` is provided by libfranka in `franka/logging/robot_state_log.hpp` and converts the `Record` log to a CSV string. After catching a `ControlException`, the example writes the result to a temporary log file. It does not take part in real-time control and should be called after control finishes, to avoid blocking the 1 kHz callback.

```{rubric} Call example
```

```cpp
std::ofstream log_stream(log_file.path().c_str());
log_stream << franka::logToCSV(e.log);
```


````


```{warning}
Risk: Torque. This example sends control commands. Confirm workspace, emergency stop, and collision thresholds before running it.
```

```{note}
The code excerpts on this page are adapted from the libfranka examples (Copyright (c) 2023 Franka Robotics GmbH, Apache License 2.0) and modified for Diana robots; the adapted parts are Copyright (c) 2026 Agile Robots SE. See "License and Third-Party Notices" in the [Manual Overview](/about/overview.md).
```

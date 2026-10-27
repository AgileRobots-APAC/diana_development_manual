# 08 generate_consecutive_motions

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

Source: `libfranka/examples/<model>/generate_consecutive_motions.cpp`.

Runs several joint-velocity trajectories in succession and demonstrates automatic recovery after a control exception.

`<model>` is the selected patched robot directory: `diana3`, `diana7`, or `diana7G2`.

```bash
./build/libfranka/examples/<model>/generate_consecutive_motions <robot-ip>
```

| Used API | Purpose in this example |
|---|---|
| `ControlException` | Catches exceptions raised during control. |
| `automaticErrorRecovery()` | Requests automatic error recovery after an exception. |
## Example flow

Preparation and collision configuration → call the control callback several times → catch ControlException → automaticErrorRecovery(), then continue with the next segment.

### Key source excerpt

```cpp
try {
  robot.control(velocity_callback);
} catch (const franka::ControlException& e) {
  std::cout << e.what() << std::endl;
  robot.automaticErrorRecovery();
}
```

(fci-en-cpp-08_generate_consecutive_motions-api)=
## API usage and call examples

(fci-en-cpp-08_generate_consecutive_motions-api-151)=
### `ControlException`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `franka::ControlException` | `class ControlException : public Exception` | Exception object; after catching it, `what()` and the state log can be read. |

`ControlException` indicates that an error occurred during control or motion generation. The consecutive-motion example catches this exception and performs error recovery, so the robot is not left in an error state.

```{rubric} Call example
```

```cpp
try {
  robot.control(callback);
} catch (const franka::ControlException& e) {
  std::cerr << e.what() << std::endl;
}
```


````

(fci-en-cpp-08_generate_consecutive_motions-api-152)=
### `automaticErrorRecovery()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Robot::automaticErrorRecovery` | `void automaticErrorRecovery()` | No return value; throws an exception on network interruption or if recovery fails. |

`automaticErrorRecovery()` requests the robot to recover from a recoverable error state. The example calls it only after catching a control exception and confirming that the site is safe.

```{rubric} Call example
```

```cpp
robot.automaticErrorRecovery();
```


````


```{warning}
Risk: Motion. This example sends control commands. Confirm workspace, emergency stop, and collision thresholds before running it.
```

```{note}
The code excerpts on this page are adapted from the libfranka examples (Copyright (c) 2023 Franka Robotics GmbH, Apache License 2.0) and modified for Diana robots; the adapted parts are Copyright (c) 2026 Agile Robots SE. See "License and Third-Party Notices" in the [Manual Overview](/about/overview.md).
```

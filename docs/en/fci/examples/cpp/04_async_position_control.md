# 04 async_position_control

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

Source: `libfranka/examples/<model>/async_position_control.cpp`.

Sends seven-axis position targets to the experimental asynchronous position controller at 50 Hz and stops after ten seconds.

`<model>` is the selected patched robot directory: `diana3`, `diana7`, or `diana7G2`.

```bash
./build/libfranka/examples/<model>/async_position_control <robot-ip>
```

| Used API | Purpose in this example |
|---|---|
| `AsyncPositionControlHandler::configure()` | Creates the asynchronous joint-position control handler. |
| `getTargetFeedback()` | Queries the execution status of the asynchronous target. |
| `setJointPositionTarget()` | Sends the next seven-axis joint-position target. |
| `stopControl()` | Stops the asynchronous position control. |
## Example flow

Create Robot(..., RealtimeConfig::kIgnore) → configure AsyncPositionControlHandler → every 20 ms get feedback and send a JointPositionTarget → stopControl().

### Key source excerpt

```cpp
auto result = franka::AsyncPositionControlHandler::configure(
    robot, joint_position_control_configuration);
auto target = calculate_joint_position_target(time_step);
auto command_result = result.handler->setJointPositionTarget(target);
```

(fci-en-cpp-04_async_position_control-api)=
## API usage and call examples

(fci-en-cpp-04_async_position_control-api-133)=
### `AsyncPositionControlHandler::configure()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `AsyncPositionControlHandler::configure` | `static ConfigurationResult configure(const std::shared_ptr<Robot>& robot, const Configuration& configuration)` | Returns a `ConfigurationResult`; on success `handler` holds a value, on failure `error_message` describes the reason. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `robot` | Input, `std::shared_ptr<Robot>` | Shared robot connection object. |
| `configuration` | Input, `Configuration` | Configuration such as maximum joint velocity and target tolerance. |

`configure()` creates the asynchronous joint-position control handler. `Configuration` can set the maximum joint velocity and the target tolerance; asynchronous control is suited to querying the target status while sending the next set of joint positions.

```{rubric} Call example
```

```cpp
auto result = franka::AsyncPositionControlHandler::configure(robot, configuration);
if (result.error_message) {
  throw std::runtime_error(*result.error_message);
}
auto handler = result.handler;
```


````

(fci-en-cpp-04_async_position_control-api-134)=
### `getTargetFeedback()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `AsyncPositionControlHandler::getTargetFeedback` | `TargetFeedback getTargetFeedback()` | Returns a `TargetFeedback` containing the `TargetStatus` and an optional error message. |

`getTargetFeedback()` queries the execution status of the asynchronous target. The example uses states such as `kExecuting`, `kTargetReached` and `kAborted` to decide whether to keep waiting, send a new target or stop.

```{rubric} Call example
```

```cpp
auto feedback = handler->getTargetFeedback();
if (feedback.status == franka::TargetStatus::kTargetReached) {
  // target reached
}
```


````

(fci-en-cpp-04_async_position_control-api-135)=
### `setJointPositionTarget()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `AsyncPositionControlHandler::setJointPositionTarget` | `CommandResult setJointPositionTarget(const JointPositionTarget& target)` | Returns a `CommandResult`; on success `was_successful=true` and it may contain a `motion_uuid`; on failure it contains an `error_message`. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `target` | Input, `JointPositionTarget` | Target joint-position array, in rad. |

`setJointPositionTarget()` sends the next set of joint-position targets to the asynchronous controller. The example checks the returned status and stops control on failure.

```{rubric} Call example
```

```cpp
franka::AsyncPositionControlHandler::JointPositionTarget target;
target.joint_positions = q_goal;
auto command = handler->setJointPositionTarget(target);
```


````

(fci-en-cpp-04_async_position_control-api-136)=
### `stopControl()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `AsyncPositionControlHandler::stopControl` | `void stopControl()` | No return value. |

`stopControl()` stops the asynchronous joint-position control. The example calls it when the target is completed, on error, or before exiting, to release the control flow.

```{rubric} Call example
```

```cpp
handler->stopControl();
```


````


```{warning}
Risk: Motion. This example sends control commands. Confirm workspace, emergency stop, and collision thresholds before running it.
```

```{note}
The code excerpts on this page are adapted from the libfranka examples (Copyright (c) 2023 Franka Robotics GmbH, Apache License 2.0) and modified for Diana robots; the adapted parts are Copyright (c) 2026 Agile Robots SE. See "License and Third-Party Notices" in the [Manual Overview](/about/overview.md).
```

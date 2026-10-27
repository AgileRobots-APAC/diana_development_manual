# 14 generate_joint_position_motion_external_control_loop

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

Source: `libfranka/examples/<model>/generate_joint_position_motion_external_control_loop.cpp`.

Sends rate-limited joint positions from an external control loop.

`<model>` is the selected patched robot directory: `diana3`, `diana7`, or `diana7G2`.

```bash
./build/libfranka/examples/<model>/generate_joint_position_motion_external_control_loop <robot-ip>
```

| Used API | Purpose in this example |
|---|---|
| `startJointPositionControl()` | Starts the joint-position external-control session. |
| `getLowerJointVelocityLimits()` | Reads the lower joint-velocity limits for the reference joint position. |
| `getUpperJointVelocityLimits()` | Reads the upper joint-velocity limits for the reference joint position. |
| `limitRate()` | Limits the velocity, acceleration, and jerk of the target joint positions. |
## Example flow

Move to the initial pose → startJointPositionControl() → readOnce() each cycle → read the joint-velocity limits for the reference joint position → limitRate() → writeOnce().

### Key source excerpt

```cpp
auto upper_velocity_limits = robot.getUpperJointVelocityLimits(reference_joint_position);
auto lower_velocity_limits = robot.getLowerJointVelocityLimits(reference_joint_position);
auto rate_limited_positions_array =
    franka::limitRate(upper_velocity_limits, lower_velocity_limits,
                      franka::kMaxJointAcceleration, franka::kMaxJointJerk, target_positions,
                      reference_joint_position, robot_state.dq_d, robot_state.ddq_d);
auto active_control = robot.startJointPositionControl(
    research_interface::robot::Move::ControllerMode::kJointImpedance);
active_control->writeOnce(joint_positions);
```

(fci-en-cpp-14_generate_joint_position_motion_external_control_loop-api)=
## API usage and call examples

(fci-en-cpp-14_generate_joint_position_motion_external_control_loop-api-173)=
### `startJointPositionControl()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Robot::startJointPositionControl()` | `std::unique_ptr<ActiveControlBase> startJointPositionControl(const research_interface::robot::Move::ControllerMode& control_type)` | Returns an active-control object; throws `ControlException` on a control conflict, network interruption, or robot error. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `control_type` | Input, `research_interface::robot::Move::ControllerMode` | Internal controller mode, typically `kJointImpedance` or `kCartesianImpedance`. |

`startJointPositionControl()` starts external-control mode. After it starts, the example calls `readOnce()` every cycle to read the state and cycle duration, then writes the target command with `writeOnce(JointPositions)`.

```{rubric} Call example
```

```cpp
auto active_control = robot.startJointPositionControl(
    research_interface::robot::Move::ControllerMode::kJointImpedance);
```


````

(fci-en-cpp-14_generate_joint_position_motion_external_control_loop-api-174)=
### `getLowerJointVelocityLimits()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Robot::getLowerJointVelocityLimits` | `auto getLowerJointVelocityLimits(const std::array<double, kNumJoints>& joint_positions) -> std::array<double, kNumJoints>` | Returns the lower joint-velocity limits for the 7 joints, in rad/s. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `joint_positions` | Input, `std::array<double,7>` | Joint positions used to compute the velocity limits, in rad. |

This `Robot` member function computes the lower joint-velocity limits for the given joint positions. The example passes `robot_state.q` in the first cycle and `robot_state.q_d` afterwards, and hands the result to `limitRate()` to constrain velocity/acceleration before writing the command.

```{rubric} Call example
```

```cpp
auto lower_velocity_limits = robot.getLowerJointVelocityLimits(reference_joint_position);
```


````

(fci-en-cpp-14_generate_joint_position_motion_external_control_loop-api-176)=
### `getUpperJointVelocityLimits()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Robot::getUpperJointVelocityLimits` | `auto getUpperJointVelocityLimits(const std::array<double, kNumJoints>& joint_positions) -> std::array<double, kNumJoints>` | Returns the upper joint-velocity limits for the 7 joints, in rad/s. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `joint_positions` | Input, `std::array<double,7>` | Joint positions used to compute the velocity limits, in rad. |

This `Robot` member function computes the upper joint-velocity limits for the given joint positions. The example passes the upper and lower limits together to `limitRate()`.

```{rubric} Call example
```

```cpp
auto upper_velocity_limits = robot.getUpperJointVelocityLimits(reference_joint_position);
```


````

(fci-en-cpp-14_generate_joint_position_motion_external_control_loop-api-175)=
### `limitRate()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `franka::limitRate` | `std::array<double, 7> limitRate(const std::array<double, 7>& upper_limits_velocity, const std::array<double, 7>& lower_limits_velocity, const std::array<double, 7>& max_acceleration, const std::array<double, 7>& max_jerk, const std::array<double, 7>& commanded_positions, const std::array<double, 7>& last_commanded_positions, const std::array<double, 7>& last_commanded_velocities, const std::array<double, 7>& last_commanded_accelerations)` | Returns the rate-limited target positions for the 7 joints; throws `std::invalid_argument` if `commanded_positions` contains infinite or NaN values. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `upper_limits_velocity` / `lower_limits_velocity` | Input, `std::array<double,7>` | Upper / lower joint-velocity limits. |
| `max_acceleration` / `max_jerk` | Input, `std::array<double,7>` | Maximum joint acceleration / jerk; the example uses `franka::kMaxJointAcceleration` and `franka::kMaxJointJerk`. |
| `commanded_positions` | Input, `std::array<double,7>` | Desired joint positions for the current cycle. |
| `last_commanded_positions` / `last_commanded_velocities` / `last_commanded_accelerations` | Input, `std::array<double,7>` | Commanded joint positions, velocities, and accelerations of the previous cycle; the example uses the reference joint position, `robot_state.dq_d`, and `robot_state.ddq_d`. |

`limitRate()` constrains the rate of change of the target command according to the model-specific limits; the header also provides overloads for joint velocities, Cartesian velocities, Cartesian poses, and torques. The example rate-limits the target joint positions in the external control loop before calling `writeOnce()`.

```{rubric} Call example
```

```cpp
auto rate_limited_positions_array =
    franka::limitRate(upper_velocity_limits, lower_velocity_limits,
                      franka::kMaxJointAcceleration, franka::kMaxJointJerk, target_positions,
                      reference_joint_position, robot_state.dq_d, robot_state.ddq_d);
```


````

```{note}
The code excerpts on this page are adapted from the libfranka examples (Copyright (c) 2023 Franka Robotics GmbH, Apache License 2.0) and modified for Diana robots; the adapted parts are Copyright (c) 2026 Agile Robots SE. See "License and Third-Party Notices" in the [Manual Overview](/about/overview.md).
```

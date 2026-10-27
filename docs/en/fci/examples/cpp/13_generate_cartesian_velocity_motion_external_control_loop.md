# 13 generate_cartesian_velocity_motion_external_control_loop

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

Source: `libfranka/examples/<model>/generate_cartesian_velocity_motion_external_control_loop.cpp`.

Runs Cartesian-velocity control through an explicit active-control loop.

`<model>` is the selected patched robot directory: `diana3`, `diana7`, or `diana7G2`.

```bash
./build/libfranka/examples/<model>/generate_cartesian_velocity_motion_external_control_loop <robot-ip>
```

| Used API | Purpose in this example |
|---|---|
| `setJointImpedance()` | Sets the internal joint-impedance stiffness. |
| `startCartesianVelocityControl()` | Starts the Cartesian-velocity external-control session. |
## Example flow

Move to the initial pose and set joint impedance → startCartesianVelocityControl() → readOnce() / writeOnce() loop.

### Key source excerpt

```cpp
auto active_control = robot.startCartesianVelocityControl(
    research_interface::robot::Move::ControllerMode::kJointImpedance);
auto [robot_state, duration] = active_control->readOnce();
active_control->writeOnce(callback_control(robot_state, duration));
```

(fci-en-cpp-13_generate_cartesian_velocity_motion_external_control_loop-api)=
## API usage and call examples

(fci-en-cpp-13_generate_cartesian_velocity_motion_external_control_loop-api-169)=
### `setJointImpedance()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Robot::setJointImpedance` | `void setJointImpedance(const std::array<double, 7>& K_theta)` | No return value; throws an exception if the network connection is lost or the controller rejects the configuration. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `K_theta` | Input, `std::array<double,7>` | Stiffness values for the seven joints. |

`setJointImpedance()` sets the per-joint stiffness of the internal joint-impedance controller. Cartesian-velocity and impedance examples set it before control to tune the internal controller behavior; it does not change the torque commands sent by the user.

In the patched examples, the `diana3` directory changes the stiffness in this call to `{{600, 600, 400, 100, 100, 100, 100}}`, while the `diana7` and `diana7G2` directories remove this call from this example.

```{rubric} Call example
```

```cpp
robot.setJointImpedance({{3000, 3000, 3000, 2500, 2500, 2000, 2000}});
```


````

(fci-en-cpp-13_generate_cartesian_velocity_motion_external_control_loop-api-170)=
### `startCartesianVelocityControl()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Robot::startCartesianVelocityControl()` | `std::unique_ptr<ActiveControlBase> startCartesianVelocityControl(const research_interface::robot::Move::ControllerMode& control_type)` | Returns an active-control object; throws `ControlException` on a control conflict, network interruption, or robot error. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `control_type` | Input, `research_interface::robot::Move::ControllerMode` | Internal controller mode, typically `kJointImpedance` or `kCartesianImpedance`. |

`startCartesianVelocityControl()` starts external-control mode. After it starts, the example calls `readOnce()` every cycle to read the state and cycle duration, then writes the target command with `writeOnce(CartesianVelocities)`.

```{rubric} Call example
```

```cpp
auto active_control = robot.startCartesianVelocityControl(
    research_interface::robot::Move::ControllerMode::kJointImpedance);
```


````

```{note}
The code excerpts on this page are adapted from the libfranka examples (Copyright (c) 2023 Franka Robotics GmbH, Apache License 2.0) and modified for Diana robots; the adapted parts are Copyright (c) 2026 Agile Robots SE. See "License and Third-Party Notices" in the [Manual Overview](/about/overview.md).
```

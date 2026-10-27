# 18 cartesian_impedance_control

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

Source: `libfranka/examples/<model>/cartesian_impedance_control.cpp`.

Computes impedance torques in Cartesian space from the model Jacobian and Coriolis terms.

`<model>` is the selected patched robot directory: `diana3`, `diana7`, or `diana7G2`.

```bash
./build/libfranka/examples/<model>/cartesian_impedance_control <robot-ip>
```

| Used API | Purpose in this example |
|---|---|
| `Model::zeroJacobian()` | Computes the end-effector zero Jacobian. |
## Example flow

readOnce() gets the initial state → load the model → zeroJacobian() computes the Jacobian → compute position/orientation error and torques → robot.control().

### Key source excerpt

```cpp
franka::RobotState initial_state = robot.readOnce();
franka::Model model(robot.loadModel());
auto jacobian = model.zeroJacobian(franka::Frame::kEndEffector, state);
return franka::Torques(tau_task + model.coriolis(state));
```

(fci-en-cpp-18_cartesian_impedance_control-api)=
## API usage and call examples

(fci-en-cpp-18_cartesian_impedance_control-api-191)=
### `Model::zeroJacobian()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Model::zeroJacobian` | `std::array<double, 42> zeroJacobian(Frame frame, const RobotState& robot_state) const` | Returns the 6x7 zero (base-frame) Jacobian, flattened in column-major order. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `frame` | Input, `Frame` | Target frame, commonly `Frame::kEndEffector`. |
| `robot_state` | Input, `const RobotState&` | Current state snapshot. |

`zeroJacobian()` computes the Jacobian of the given frame expressed in the base frame. The impedance and force-control examples use it to map Cartesian quantities into joint space.

```{rubric} Call example
```

```cpp
std::array<double, 42> jacobian_array =
    model.zeroJacobian(franka::Frame::kEndEffector, state);
```


````

```{note}
The code excerpts on this page are adapted from the libfranka examples (Copyright (c) 2023 Franka Robotics GmbH, Apache License 2.0) and modified for Diana robots; the adapted parts are Copyright (c) 2026 Agile Robots SE. See "License and Third-Party Notices" in the [Manual Overview](/about/overview.md).
```

# 19 force_control

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

Source: `libfranka/examples/<model>/force_control.cpp`.

Controls the desired end-effector force using the Jacobian and gravity terms.

`<model>` is the selected patched robot directory: `diana3`, `diana7`, or `diana7G2`.

```bash
./build/libfranka/examples/<model>/force_control <robot-ip>
```

| Used API | Purpose in this example |
|---|---|
| `Model::gravity()` | Computes the gravity term in the initial state, used to remove the torque-sensor bias and estimate the external torque. |
## Example flow

loadModel() → readOnce() for the initial state → gravity() to calibrate the external-torque bias → zeroJacobian() in the torque callback maps the desired end-effector force to joint torques → feed-forward + PI control outputs Torques.

### Key source excerpt

```cpp
std::array<double, 7> gravity_array = model.gravity(initial_state);
initial_tau_ext = initial_tau_measured - initial_gravity;
// in the torque-control callback:
std::array<double, 42> jacobian_array =
    model.zeroJacobian(franka::Frame::kEndEffector, robot_state);
tau_ext << tau_measured - gravity - initial_tau_ext;
tau_d << jacobian.transpose() * desired_force_torque;
tau_error_integral += period.toSec() * (tau_d - tau_ext);
tau_cmd << tau_d + k_p * (tau_d - tau_ext) + k_i * tau_error_integral;
```

(fci-en-cpp-19_force_control-api)=
## API usage and call examples

(fci-en-cpp-19_force_control-api-196)=
### `Model::gravity()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Model::gravity` | `std::array<double, 7> gravity(const franka::RobotState& robot_state) const noexcept` | Returns the 7-element gravity torque array, in Nm. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `robot_state` | Input, `const franka::RobotState&` | Robot state used for the computation. |

`gravity()` computes the gravity term for the current configuration. This example computes it only once from the initial state before starting, subtracting it from the measured torque `tau_J` to obtain the initial external-torque bias; the control callback keeps using this gravity term to estimate the external torque `tau_ext`.

```{rubric} Call example
```

```cpp
franka::RobotState initial_state = robot.readOnce();
std::array<double, 7> gravity_array = model.gravity(initial_state);
```


````

```{note}
The code excerpts on this page are adapted from the libfranka examples (Copyright (c) 2023 Franka Robotics GmbH, Apache License 2.0) and modified for Diana robots; the adapted parts are Copyright (c) 2026 Agile Robots SE. See "License and Third-Party Notices" in the [Manual Overview](/about/overview.md).
```

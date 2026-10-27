# 17 joint_impedance_control

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

Source: `libfranka/examples/<model>/joint_impedance_control.cpp`.

Uses a joint impedance law with coriolis compensation while following a Cartesian trajectory.

`<model>` is the selected patched robot directory: `diana3`, `diana7`, or `diana7G2`.

```bash
./build/libfranka/examples/<model>/joint_impedance_control <robot-ip>
```

| Used API | Purpose in this example |
|---|---|
| `Model::coriolis()` | Computes the Coriolis and centrifugal compensation term. |
| `Model::gravity()` | Computes the gravity term used to print the actual torque. |
| `Robot::control()` | Starts the torque-control callback together with the Cartesian-pose motion-generator callback. |
## Example flow

Load the model → pose callback generates a circular trajectory → torque callback computes stiffness, damping, and Coriolis compensation → rate limiting, then combined control.

### Key source excerpt

```cpp
auto coriolis = model.coriolis(state);
tau_d_calculated[i] = k_gains[i] * (state.q_d[i] - state.q[i])
                    - d_gains[i] * state.dq[i] + coriolis[i];
return franka::limitRate(franka::kMaxTorqueRate,
                         tau_d_calculated, state.tau_J_d);
```

(fci-en-cpp-17_joint_impedance_control-api)=
## API usage and call examples

(fci-en-cpp-17_joint_impedance_control-api-186)=
### `Model::coriolis()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Model::coriolis` | `std::array<double, 7> coriolis(const franka::RobotState& robot_state) const noexcept` | Returns the 7-element Coriolis/centrifugal torque array, in Nm. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `robot_state` | Input, `const franka::RobotState&` | Robot state used for the computation. |

`coriolis()` computes the compensation term from the current state. This example adds it to the output of the joint-impedance control law to form the joint torques sent to the robot control interface.

```{rubric} Call example
```

```cpp
std::array<double, 7> coriolis = model.coriolis(state);
```


````

(fci-en-cpp-17_joint_impedance_control-api-187)=
### `Model::gravity()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Model::gravity` | `std::array<double, 7> gravity(const franka::RobotState& robot_state) const noexcept` | Returns the 7-element gravity torque array, in Nm. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `robot_state` | Input, `const franka::RobotState&` | Robot state used for the computation. |

`gravity()` computes the gravity term for the current configuration. This example does not add it to the torque command; it only adds it to the rate-limited torque when printing, to show the actual joint torque.

```{rubric} Call example
```

```cpp
print_data.gravity = model.gravity(state);
```


````

(fci-en-cpp-17_joint_impedance_control-api-188)=
### `Robot::control()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Robot::control` | `void control(std::function<Torques(const RobotState&, franka::Duration)> control_callback, std::function<CartesianPose(const RobotState&, franka::Duration)> motion_generator_callback, bool limit_rate = false, double cutoff_frequency = kDefaultCutoffFrequency)` | No return value; the callback ends control by returning `MotionFinished(...)`; throws an exception on a control conflict, real-time configuration failure, network interruption, or invalid command. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `control_callback` | Input, `std::function` | Returns a `Torques` command every control cycle. |
| `motion_generator_callback` | Input, `std::function` | Returns a `CartesianPose` motion-generator command every control cycle. |
| `limit_rate` | Input, `bool`, default `false` | Whether to enable rate limiting; this can change the trajectory. |
| `cutoff_frequency` | Input, `double` | Low-pass filter cutoff frequency. |

`control()` starts the 1 kHz FCI control loop. This example uses the "torque control + Cartesian-pose motion generation" overload: the pose callback provides the target pose, and the `q_d` obtained from the internal inverse kinematics is tracked by the torque callback. Only one control/motion-generation loop can be active at a time.

```{rubric} Call example
```

```cpp
robot.control(impedance_control_callback, cartesian_pose_callback);
```


````

```{warning}
Risk: Torque. This example sends robot commands. Confirm workspace, emergency stop, and collision thresholds before execution.
```

```{note}
The code excerpts on this page are adapted from the libfranka examples (Copyright (c) 2023 Franka Robotics GmbH, Apache License 2.0) and modified for Diana robots; the adapted parts are Copyright (c) 2026 Agile Robots SE. See "License and Third-Party Notices" in the [Manual Overview](/about/overview.md).
```

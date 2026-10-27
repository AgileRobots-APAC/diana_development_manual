# 05 cartesian_velocity_example

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

Source: `libfranka/pylibfranka/examples/<model>/cartesian_velocity_example.py`.

Sets the joint impedance, starts Cartesian-velocity control and sends CartesianVelocities in an external loop.

`<model>` is `diana3`, `diana7`, or `diana7G2` after applying the selected overlay patch.

```bash
python3 libfranka/pylibfranka/examples/<model>/cartesian_velocity_example.py --ip <robot-ip>
```

| Used API | Purpose in this example |
|---|---|
| `set_joint_impedance()` | Sets the internal joint-impedance stiffness. |
| `start_cartesian_velocity_control()` | Starts the Cartesian-velocity external-control session. |
| `CartesianVelocities` | Wraps the end-effector velocity command. |
## Example flow

Parse --ip → set collision behavior and joint impedance → start_cartesian_velocity_control() → readOnce() / writeOnce() → automatic_error_recovery() on exception.

### Key source excerpt

```python
active_control = robot.start_cartesian_velocity_control(
    ControllerMode.JointImpedance)
robot_state, duration = active_control.readOnce()
active_control.writeOnce(CartesianVelocities(velocities))
```

(fci-en-python-05_cartesian_velocity_example-api)=
## API usage and call examples

(fci-en-python-05_cartesian_velocity_example-api-219)=
### `set_joint_impedance()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Robot.set_joint_impedance` | `set_joint_impedance(K_theta: list[float])` | No return value; network interruptions or configuration failures raise exceptions. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `K_theta` | Input, `list[float]` | Seven joint stiffness values. |

Sets the seven-axis stiffness of the internal joint-impedance controller. The Cartesian-velocity example calls it before control to tune the internal controller behavior.

```{rubric} Call example
```

```python
robot.set_joint_impedance([3000, 3000, 3000, 2500, 2500, 2000, 2000])
```


````

(fci-en-python-05_cartesian_velocity_example-api-220)=
### `start_cartesian_velocity_control()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Robot.start_cartesian_velocity_control()` | `start_cartesian_velocity_control(controller_mode: ControllerMode) -> ActiveControl` | Returns an active-control object; control conflicts, network interruptions or robot errors raise exceptions. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `controller_mode` | Input, `ControllerMode` | Internal controller mode. |

Starts active-control mode. The returned object reads the state and period via `readOnce()` and writes `CartesianVelocities` commands via `writeOnce()`.

```{rubric} Call example
```

```python
active_control = robot.start_cartesian_velocity_control(ControllerMode.CartesianImpedance)
```


````

(fci-en-python-05_cartesian_velocity_example-api-223)=
### `CartesianVelocities`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `CartesianVelocities` | `CartesianVelocities(cartesian_velocities: list[float], elbow: list[float] \| None = None)` | Returns a Cartesian-velocity command object. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `cartesian_velocities` | Input, `list[float]` | `x/y/z/wx/wy/wz` velocities. |
| `elbow` | Input, optional `list[float]` | 2-element elbow configuration. |

Wraps the 6-D end-effector velocity: the first three entries are linear velocities in m/s, the last three are angular velocities in rad/s.

```{rubric} Call example
```

```python
command = pylibfranka.CartesianVelocities([0.0, 0.0, 0.05, 0.0, 0.0, 0.0])
```


````


```{warning}
Risk: Motion. This example sends control commands. Confirm workspace, emergency stop, and collision thresholds before running it.
```

```{note}
The code excerpts on this page are adapted from the libfranka examples (Copyright (c) 2023 Franka Robotics GmbH, Apache License 2.0) and modified for Diana robots; the adapted parts are Copyright (c) 2026 Agile Robots SE. See "License and Third-Party Notices" in the [Manual Overview](/about/overview.md).
```

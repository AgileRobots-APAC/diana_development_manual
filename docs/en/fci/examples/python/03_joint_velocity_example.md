# 03 joint_velocity_example

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

Source: `libfranka/pylibfranka/examples/<model>/joint_velocity_example.py`.

Starts a joint-velocity external-control session and computes and sends JointVelocities every cycle.

`<model>` is `diana3`, `diana7`, or `diana7G2` after applying the selected overlay patch.

```bash
python3 libfranka/pylibfranka/examples/<model>/joint_velocity_example.py --ip <robot-ip>
```

| Used API | Purpose in this example |
|---|---|
| `start_joint_velocity_control()` | Starts the joint-velocity external-control session. |
| `JointVelocities` | Wraps the seven-axis target joint velocities. |
## Example flow

Parse --ip → set collision behavior → start_joint_velocity_control() → readOnce() / writeOnce() loop.

### Key source excerpt

```python
active_control = robot.start_joint_velocity_control(
    ControllerMode.CartesianImpedance)
robot_state, duration = active_control.readOnce()
active_control.writeOnce(JointVelocities(velocities))
```

(fci-en-python-03_joint_velocity_example-api)=
## API usage and call examples

(fci-en-python-03_joint_velocity_example-api-211)=
### `start_joint_velocity_control()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Robot.start_joint_velocity_control()` | `start_joint_velocity_control(controller_mode: ControllerMode) -> ActiveControl` | Returns an active-control object; control conflicts, network interruptions or robot errors raise exceptions. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `controller_mode` | Input, `ControllerMode` | Internal controller mode. |

Starts active-control mode. The returned object reads the state and period via `readOnce()` and writes `JointVelocities` commands via `writeOnce()`.

```{rubric} Call example
```

```python
active_control = robot.start_joint_velocity_control(ControllerMode.CartesianImpedance)
```


````

(fci-en-python-03_joint_velocity_example-api-214)=
### `JointVelocities`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `JointVelocities` | `JointVelocities(joint_velocities: list[float])` | Returns a joint-velocity command object. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `joint_velocities` | Input, `list[float]` | Seven-axis target joint velocities, in rad/s. |

Wraps the seven-axis target joint velocities, in rad/s.

```{rubric} Call example
```

```python
command = pylibfranka.JointVelocities([0.0] * 7)
```


````


```{warning}
Risk: Motion. This example sends control commands. Confirm workspace, emergency stop, and collision thresholds before running it.
```

```{note}
The code excerpts on this page are adapted from the libfranka examples (Copyright (c) 2023 Franka Robotics GmbH, Apache License 2.0) and modified for Diana robots; the adapted parts are Copyright (c) 2026 Agile Robots SE. See "License and Third-Party Notices" in the [Manual Overview](/about/overview.md).
```

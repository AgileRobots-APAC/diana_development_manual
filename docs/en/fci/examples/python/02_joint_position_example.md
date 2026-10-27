# 02 joint_position_example

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

Source: `libfranka/pylibfranka/examples/<model>/joint_position_example.py`.

Starts a joint-position external-control session; in each control cycle it reads the state and writes seven-axis JointPositions.

`<model>` is `diana3`, `diana7`, or `diana7G2` after applying the selected overlay patch.

```bash
python3 libfranka/pylibfranka/examples/<model>/joint_position_example.py --ip <robot-ip>
```

| Used API | Purpose in this example |
|---|---|
| `start_joint_position_control()` | Starts the joint-position external-control session. |
| `ActiveControl.readOnce()` | Reads the current state and period. |
| `ActiveControl.writeOnce()` | Writes the joint-position command for this cycle. |
| `JointPositions` | Wraps the seven-axis target joint angles. |
## Example flow

Parse --ip → set collision behavior → start_joint_position_control() → readOnce() / writeOnce() loop → set motion_finished.

### Key source excerpt

```python
active_control = robot.start_joint_position_control(
    ControllerMode.CartesianImpedance)
robot_state, duration = active_control.readOnce()
joint_positions = JointPositions(new_positions)
active_control.writeOnce(joint_positions)
```

(fci-en-python-02_joint_position_example-api)=
## API usage and call examples

(fci-en-python-02_joint_position_example-api-207)=
### `start_joint_position_control()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Robot.start_joint_position_control()` | `start_joint_position_control(controller_mode: ControllerMode) -> ActiveControl` | Returns an active-control object; control conflicts, network interruptions or robot errors raise exceptions. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `controller_mode` | Input, `ControllerMode` | Internal controller mode. |

Starts active-control mode. The returned object reads the state and period via `readOnce()` and writes `JointPositions` commands via `writeOnce()`.

```{rubric} Call example
```

```python
active_control = robot.start_joint_position_control(ControllerMode.CartesianImpedance)
```


````

(fci-en-python-02_joint_position_example-api-208)=
### `ActiveControl.readOnce()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `ActiveControl.readOnce` | `readOnce() -> tuple[RobotState, Duration]` | Returns the current state and the period; network, protocol or robot errors raise exceptions. |

Read-cycle interface of active control. The example first reads the state and `Duration`, then computes the command for this cycle.

```{rubric} Call example
```

```python
state, period = active_control.readOnce()
```


````

(fci-en-python-02_joint_position_example-api-209)=
### `ActiveControl.writeOnce()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `ActiveControl.writeOnce` | `writeOnce(command, control_input: Torques \| None = None)` | No return value; raises an exception if the command type does not match the current control mode. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `command` | Input, control command object | Target command for this cycle. |
| `control_input` | Input, optional `Torques` | Used when superimposing torque control. |

Write-cycle interface of active control. The command type written must match the control mode that was started, e.g. `JointPositions` in joint-position mode and `Torques` in torque mode.

```{rubric} Call example
```

```python
active_control.writeOnce(pylibfranka.JointPositions(q_desired))
```


````

(fci-en-python-02_joint_position_example-api-210)=
### `JointPositions`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `JointPositions` | `JointPositions(joint_positions: list[float])` | Returns a joint-position command object. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `joint_positions` | Input, `list[float]` | Seven-axis target joint angles, in rad. |

Wraps the seven-axis target joint angles, in rad. The joint-position active-control example constructs and writes this object every cycle.

```{rubric} Call example
```

```python
command = pylibfranka.JointPositions(q_desired)
```


````


```{warning}
Risk: Motion. This example sends control commands. Confirm workspace, emergency stop, and collision thresholds before running it.
```

```{note}
The code excerpts on this page are adapted from the libfranka examples (Copyright (c) 2023 Franka Robotics GmbH, Apache License 2.0) and modified for Diana robots; the adapted parts are Copyright (c) 2026 Agile Robots SE. See "License and Third-Party Notices" in the [Manual Overview](/about/overview.md).
```

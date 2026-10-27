# 06 joint_impedance_example

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

Source: `libfranka/pylibfranka/examples/<model>/joint_impedance_example.py`.

Loads the model and reads the initial state, then starts torque control and writes Torques according to the joint-impedance control law in an external loop.

`<model>` is `diana3`, `diana7`, or `diana7G2` after applying the selected overlay patch.

```bash
python3 libfranka/pylibfranka/examples/<model>/joint_impedance_example.py --ip <robot-ip>
```

| Used API | Purpose in this example |
|---|---|
| `load_model()` | Loads the dynamics model used for Coriolis compensation. |
| `read_once()` | Reads the initial joint positions as the start of the first trajectory segment. |
| `start_torque_control()` | Starts the torque external-control session. |
| `Torques` | Wraps the joint-torque command. |
## Example flow

Parse --ip → set collision behavior → read_once() → start_torque_control() → load_model() → readOnce() / writeOnce(Torques).

### Key source excerpt

```python
initial_state = robot.read_once()
active_control = robot.start_torque_control()
model = robot.load_model()
robot_state, _ = active_control.readOnce()
coriolis = np.array(model.coriolis(robot_state))
torque_command = Torques(tau_d.tolist())
active_control.writeOnce(torque_command)
```

(fci-en-python-06_joint_impedance_example-api)=
## API usage and call examples

(fci-en-python-06_joint_impedance_example-api-224)=
### `load_model()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Robot.load_model` | `load_model() -> Model` | Returns a model object; throws an exception if loading the model library fails or the network connection is lost. |

`load_model()` loads the kinematics/dynamics model of the connected robot through the Python bindings. This example uses `model.coriolis(robot_state)` in the control loop to compute the Coriolis compensation term.

```{rubric} Call example
```

```python
model = robot.load_model()
```


````

(fci-en-python-06_joint_impedance_example-api-225)=
### `read_once()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Robot.read_once` | `read_once() -> RobotState` | Returns one `RobotState` snapshot; throws an exception while a control loop is running, or on a network or robot error. |

`read_once()` is the one-shot state-reading interface of the Python bindings. Use it when only the current state is needed; continuous control examples use `readOnce()` on the active-control object. This example calls it before starting torque control to obtain the initial joint positions.

```{rubric} Call example
```

```python
initial_state = robot.read_once()
current_position = np.array(initial_state.q)
```


````

(fci-en-python-06_joint_impedance_example-api-226)=
### `start_torque_control()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Robot.start_torque_control()` | `start_torque_control() -> ActiveControlBase` | Returns an active-control object; throws an exception on a control conflict, network interruption, or robot error. |

Starts active-control mode. The returned object reads the state and cycle duration through `readOnce()` and writes `Torques` commands through `writeOnce()`.

```{rubric} Call example
```

```python
active_control = robot.start_torque_control()
```


````

(fci-en-python-06_joint_impedance_example-api-229)=
### `Torques`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Torques` | `Torques(tau_J: list[float])` | Returns a joint-torque command object. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `tau_J` | Input, `list[float]` | Torques for the 7 joints, in Nm. |

Wraps a 7-joint torque command, in Nm; setting the `motion_finished` attribute to `True` ends the motion. Torque-control examples write the control-law output to the active-control object.

```{rubric} Call example
```

```python
torque_command = Torques(tau_d.tolist())
torque_command.motion_finished = False
active_control.writeOnce(torque_command)
```


````

```{warning}
Risk: Torque. This example sends robot commands. Confirm workspace, emergency stop, and collision thresholds before execution.
```

```{note}
The code excerpts on this page are adapted from the libfranka examples (Copyright (c) 2023 Franka Robotics GmbH, Apache License 2.0) and modified for Diana robots; the adapted parts are Copyright (c) 2026 Agile Robots SE. See "License and Third-Party Notices" in the [Manual Overview](/about/overview.md).
```

# 01 print_robot_state

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

Source: `libfranka/pylibfranka/examples/<model>/print_robot_state.py`.

Creates a Robot, sets the collision thresholds, then calls read_once() to get and print the RobotState.

`<model>` is `diana3`, `diana7`, or `diana7G2` after applying the selected overlay patch.

```bash
python3 libfranka/pylibfranka/examples/<model>/print_robot_state.py --ip <robot-ip>
```

| Used API | Purpose in this example |
|---|---|
| `Robot` | Creates the robot connection object. |
| `set_collision_behavior()` | Sets the collision and contact thresholds. |
| `read_once()` | Reads the robot state once. |
| `RobotState` | Holds and prints the state snapshot. |
## Example flow

Parse --ip → create Robot → set_collision_behavior() → read_once() → print the state fields.

### Key source excerpt

```python
robot = Robot(args.ip)
robot.set_collision_behavior(lower_torque, upper_torque,
                             lower_force, upper_force)
robot_state = robot.read_once()
print(robot_state)
```

(fci-en-python-01_print_robot_state-api)=
## API usage and call examples

(fci-en-python-01_print_robot_state-api-203)=
### `pylibfranka.Robot`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `pylibfranka.Robot` | `Robot(robot_ip_address: str, realtime_config: RealtimeConfig = RealtimeConfig.kEnforce)` | Returns the Python robot object; connection failures, version incompatibility or realtime configuration failures raise binding-layer exceptions. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `robot_ip_address` | Input, `str` | IP address or hostname of the robot. |
| `realtime_config` | Input, `RealtimeConfig`, default `kEnforce` | Whether realtime priority is enforced. |

The Python `Robot` is the binding entry point of `pylibfranka.PyRobot` and holds a `franka::Robot` underneath. It provides state reading, model loading, collision/impedance configuration and functions for starting active control.

```{rubric} Call example
```

```python
robot = pylibfranka.Robot(robot_ip)
```


````

(fci-en-python-01_print_robot_state-api-204)=
### `Robot.set_collision_behavior()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Robot.set_collision_behavior` | `set_collision_behavior(lower_torque_thresholds, upper_torque_thresholds, lower_force_thresholds, upper_force_thresholds)` | No return value; invalid arguments, network interruptions or a rejected configuration raise exceptions. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `lower_torque_thresholds` | Input, `list[float]` | 7-D joint contact thresholds. |
| `upper_torque_thresholds` | Input, `list[float]` | 7-D joint collision thresholds. |
| `lower_force_thresholds` | Input, `list[float]` | 6-D Cartesian contact thresholds. |
| `upper_force_thresholds` | Input, `list[float]` | 6-D Cartesian collision thresholds. |

Configures the collision/contact thresholds. The four arrays are the lower/upper joint-torque thresholds and the lower/upper Cartesian force/torque thresholds. The examples set them before motion or control.

```{rubric} Call example
```

```python
robot.set_collision_behavior(
    [20.0] * 7, [20.0] * 7,
    [20.0] * 6, [20.0] * 6,
)
```


````

(fci-en-python-01_print_robot_state-api-205)=
### `Robot.read_once()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Robot.read_once` | `read_once() -> RobotState` | Returns one `RobotState` snapshot; raises an exception if a control loop is running or on network or robot errors. |

`read_once()` is the one-shot state-reading interface of the Python binding. Use it when only the current state is needed; continuous-control examples use `readOnce()` of the active-control object instead.

```{rubric} Call example
```

```python
state = robot.read_once()
print(state.q)
```


````

(fci-en-python-01_print_robot_state-api-206)=
### `RobotState`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `RobotState` | `RobotState` | State object; returned by `read_once()` or by the active-control `readOnce()`. |

`RobotState` contains the joint state, end-effector pose, commanded pose, collision/contact flags and other fields. The Python examples read its fields for printing or as control-law inputs.

```{rubric} Call example
```

```python
state = robot.read_once()
q = state.q
```


````


```{warning}
Risk: Read-only. This example sends no control commands.
```

```{note}
The code excerpts on this page are adapted from the libfranka examples (Copyright (c) 2023 Franka Robotics GmbH, Apache License 2.0) and modified for Diana robots; the adapted parts are Copyright (c) 2026 Agile Robots SE. See "License and Third-Party Notices" in the [Manual Overview](/about/overview.md).
```

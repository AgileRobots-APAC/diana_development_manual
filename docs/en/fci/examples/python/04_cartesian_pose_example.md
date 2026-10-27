# 04 cartesian_pose_example

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

Source: `libfranka/pylibfranka/examples/<model>/cartesian_pose_example.py`.

Starts a Cartesian-pose external-control session and generates a circular target trajectory around the initial end-effector pose.

`<model>` is `diana3`, `diana7`, or `diana7G2` after applying the selected overlay patch.

```bash
python3 libfranka/pylibfranka/examples/<model>/cartesian_pose_example.py --ip <robot-ip>
```

| Used API | Purpose in this example |
|---|---|
| `start_cartesian_pose_control()` | Starts the Cartesian-pose external-control session. |
| `CartesianPose` | Wraps the end-effector target pose. |
## Example flow

Parse --ip → set collision behavior → start_cartesian_pose_control() → readOnce() → compute CartesianPose → writeOnce().

### Key source excerpt

```python
active_control = robot.start_cartesian_pose_control(
    ControllerMode.JointImpedance)
robot_state, duration = active_control.readOnce()
active_control.writeOnce(CartesianPose(new_pose))
```

(fci-en-python-04_cartesian_pose_example-api)=
## API usage and call examples

(fci-en-python-04_cartesian_pose_example-api-215)=
### `start_cartesian_pose_control()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Robot.start_cartesian_pose_control()` | `start_cartesian_pose_control(controller_mode: ControllerMode) -> ActiveControl` | Returns an active-control object; control conflicts, network interruptions or robot errors raise exceptions. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `controller_mode` | Input, `ControllerMode` | Internal controller mode. |

Starts active-control mode. The returned object reads the state and period via `readOnce()` and writes `CartesianPose` commands via `writeOnce()`.

```{rubric} Call example
```

```python
active_control = robot.start_cartesian_pose_control(ControllerMode.CartesianImpedance)
```


````

(fci-en-python-04_cartesian_pose_example-api-218)=
### `CartesianPose`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `CartesianPose` | `CartesianPose(cartesian_pose: list[float], elbow: list[float] \| None = None)` | Returns a Cartesian-pose command object. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `cartesian_pose` | Input, `list[float]` | 16-element pose matrix, column-major. |
| `elbow` | Input, optional `list[float]` | 2-element elbow configuration. |

Wraps the 4x4 target pose matrix of the end effector relative to the base frame, flattened in column-major order; the optional elbow specifies the elbow configuration.

```{rubric} Call example
```

```python
command = pylibfranka.CartesianPose(target_pose)
```


````


```{warning}
Risk: Motion. This example sends control commands. Confirm workspace, emergency stop, and collision thresholds before running it.
```

```{note}
The code excerpts on this page are adapted from the libfranka examples (Copyright (c) 2023 Franka Robotics GmbH, Apache License 2.0) and modified for Diana robots; the adapted parts are Copyright (c) 2026 Agile Robots SE. See "License and Third-Party Notices" in the [Manual Overview](/about/overview.md).
```

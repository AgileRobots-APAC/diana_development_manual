# Python FCI Examples

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

Python FCI examples come from `libfranka/pylibfranka/examples/<model>/` after applying the selected robot patch. They use `pylibfranka`, not the ordinary Diana Python SDK documented elsewhere on this site.

<div class="example-list-table">

| Example | Purpose | Used API | Risk |
|---|---|---|---|
| [`01_print_robot_state`](01_print_robot_state.md) | Read and print robot state | <a href="01_print_robot_state.html#fci-en-python-01-print-robot-state-api-203"><code>pylibfranka.Robot</code></a>, <a href="01_print_robot_state.html#fci-en-python-01-print-robot-state-api-204"><code>Robot.set_collision_behavior()</code></a>, <a href="01_print_robot_state.html#fci-en-python-01-print-robot-state-api-205"><code>Robot.read_once()</code></a>, <a href="01_print_robot_state.html#fci-en-python-01-print-robot-state-api-206"><code>RobotState</code></a> | Read-only |
| [`02_joint_position_example`](02_joint_position_example.md) | Joint-position external control | <a href="02_joint_position_example.html#fci-en-python-02-joint-position-example-api-207"><code>start_joint_position_control()</code></a>, <a href="02_joint_position_example.html#fci-en-python-02-joint-position-example-api-208"><code>ActiveControl.readOnce()</code></a>, <a href="02_joint_position_example.html#fci-en-python-02-joint-position-example-api-209"><code>ActiveControl.writeOnce()</code></a>, <a href="02_joint_position_example.html#fci-en-python-02-joint-position-example-api-210"><code>JointPositions</code></a> | Motion |
| [`03_joint_velocity_example`](03_joint_velocity_example.md) | Joint-velocity external control | <a href="03_joint_velocity_example.html#fci-en-python-03-joint-velocity-example-api-211"><code>start_joint_velocity_control()</code></a>, <a href="03_joint_velocity_example.html#fci-en-python-03-joint-velocity-example-api-214"><code>JointVelocities</code></a> | Motion |
| [`04_cartesian_pose_example`](04_cartesian_pose_example.md) | Cartesian-pose external control | <a href="04_cartesian_pose_example.html#fci-en-python-04-cartesian-pose-example-api-215"><code>start_cartesian_pose_control()</code></a>, <a href="04_cartesian_pose_example.html#fci-en-python-04-cartesian-pose-example-api-218"><code>CartesianPose</code></a> | Motion |
| [`05_cartesian_velocity_example`](05_cartesian_velocity_example.md) | Cartesian-velocity external control | <a href="05_cartesian_velocity_example.html#fci-en-python-05-cartesian-velocity-example-api-219"><code>set_joint_impedance()</code></a>, <a href="05_cartesian_velocity_example.html#fci-en-python-05-cartesian-velocity-example-api-220"><code>start_cartesian_velocity_control()</code></a>, <a href="05_cartesian_velocity_example.html#fci-en-python-05-cartesian-velocity-example-api-223"><code>CartesianVelocities</code></a> | Motion |
| [`06_joint_impedance_example`](06_joint_impedance_example.md) | Joint-impedance torque control | <a href="06_joint_impedance_example.html#fci-en-python-06-joint-impedance-example-api-224"><code>load_model()</code></a>, <a href="06_joint_impedance_example.html#fci-en-python-06-joint-impedance-example-api-225"><code>read_once()</code></a>, <a href="06_joint_impedance_example.html#fci-en-python-06-joint-impedance-example-api-226"><code>start_torque_control()</code></a>, <a href="06_joint_impedance_example.html#fci-en-python-06-joint-impedance-example-api-229"><code>Torques</code></a> | Torque |
</div>

`move_gripper.py` is retained from upstream but gripper support is not available in Diana FCI, so it is excluded from this guide.

```{warning}
Python examples also open an FCI session; motion and torque examples must be run only after an on-site safety check. Some examples first move to a model-specific initial pose; see {ref}`Initial Pose <fci-initial-pose>`.
```

```{toctree}
:hidden:

01_print_robot_state
02_joint_position_example
03_joint_velocity_example
04_cartesian_pose_example
05_cartesian_velocity_example
06_joint_impedance_example
```

# C++ FCI Examples

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

C++ examples are in `libfranka/examples/<model>/` after applying the robot patch. `<model>` is `diana3`, `diana7`, or `diana7G2`.

<div class="example-list-table">

| Example | Purpose | Used API | Risk |
|---|---|---|---|
| [`01_echo_robot_state`](01_echo_robot_state.md) | Continuously read and print robot state | <a href="01_echo_robot_state.html#fci-en-cpp-01-echo-robot-state-api-122"><code>franka::Robot</code></a>, <a href="01_echo_robot_state.html#fci-en-cpp-01-echo-robot-state-api-123"><code>Robot::read()</code></a>, <a href="01_echo_robot_state.html#fci-en-cpp-01-echo-robot-state-api-124"><code>franka::RobotState</code></a> | Read-only |
| [`02_communication_test`](02_communication_test.md) | Measure control communication success rate and lost cycles | <a href="02_communication_test.html#fci-en-cpp-02-communication-test-api-125"><code>Robot::startTorqueControl()</code></a>, <a href="02_communication_test.html#fci-en-cpp-02-communication-test-api-126"><code>readOnce()</code></a>, <a href="02_communication_test.html#fci-en-cpp-02-communication-test-api-127"><code>writeOnce()</code></a>, <a href="02_communication_test.html#fci-en-cpp-02-communication-test-api-128"><code>control_command_success_rate</code></a> | Torque / motion |
| [`03_print_joint_poses`](03_print_joint_poses.md) | Print joint and end-effector poses | <a href="03_print_joint_poses.html#fci-en-cpp-03-print-joint-poses-api-132"><code>franka::RobotState</code></a>, <a href="03_print_joint_poses.html#fci-en-cpp-03-print-joint-poses-api-129"><code>Robot::readOnce()</code></a>, <a href="03_print_joint_poses.html#fci-en-cpp-03-print-joint-poses-api-130"><code>Robot::loadModel()</code></a>, <a href="03_print_joint_poses.html#fci-en-cpp-03-print-joint-poses-api-131"><code>Model::pose()</code></a> | Read-only |
| [`04_async_position_control`](04_async_position_control.md) | Experimental asynchronous position control | <a href="04_async_position_control.html#fci-en-cpp-04-async-position-control-api-133"><code>AsyncPositionControlHandler::configure()</code></a>, <a href="04_async_position_control.html#fci-en-cpp-04-async-position-control-api-134"><code>getTargetFeedback()</code></a>, <a href="04_async_position_control.html#fci-en-cpp-04-async-position-control-api-135"><code>setJointPositionTarget()</code></a>, <a href="04_async_position_control.html#fci-en-cpp-04-async-position-control-api-136"><code>stopControl()</code></a> | Motion |
| [`05_joint_point_to_point_motion`](05_joint_point_to_point_motion.md) | Point-to-point joint motion | <a href="05_joint_point_to_point_motion.html#fci-en-cpp-05-joint-point-to-point-motion-api-137"><code>MotionGenerator</code></a>, <a href="05_joint_point_to_point_motion.html#fci-en-cpp-05-joint-point-to-point-motion-api-138"><code>Robot::setCollisionBehavior()</code></a>, <a href="05_joint_point_to_point_motion.html#fci-en-cpp-05-joint-point-to-point-motion-api-139"><code>Robot::control()</code></a> | Motion |
| [`06_generate_joint_position_motion`](06_generate_joint_position_motion.md) | Joint-position callback motion | <a href="06_generate_joint_position_motion.html#fci-en-cpp-06-generate-joint-position-motion-api-140"><code>Robot::control()</code></a>, <a href="06_generate_joint_position_motion.html#fci-en-cpp-06-generate-joint-position-motion-api-141"><code>RobotState::q</code></a>, <a href="06_generate_joint_position_motion.html#fci-en-cpp-06-generate-joint-position-motion-api-142"><code>Duration::toSec()</code></a>, <a href="06_generate_joint_position_motion.html#fci-en-cpp-06-generate-joint-position-motion-api-143"><code>JointPositions</code></a>, <a href="06_generate_joint_position_motion.html#fci-en-cpp-06-generate-joint-position-motion-api-144"><code>MotionFinished()</code></a> | Motion |
| [`07_generate_joint_velocity_motion`](07_generate_joint_velocity_motion.md) | Joint-velocity callback motion | <a href="07_generate_joint_velocity_motion.html#fci-en-cpp-07-generate-joint-velocity-motion-api-145"><code>Robot::control()</code></a>, <a href="07_generate_joint_velocity_motion.html#fci-en-cpp-07-generate-joint-velocity-motion-api-147"><code>JointVelocities</code></a> | Motion |
| [`08_generate_consecutive_motions`](08_generate_consecutive_motions.md) | Consecutive joint-velocity motions | <a href="08_generate_consecutive_motions.html#fci-en-cpp-08-generate-consecutive-motions-api-151"><code>ControlException</code></a>, <a href="08_generate_consecutive_motions.html#fci-en-cpp-08-generate-consecutive-motions-api-152"><code>automaticErrorRecovery()</code></a> | Motion |
| [`09_generate_elbow_motion`](09_generate_elbow_motion.md) | Cartesian motion with elbow redundancy | <a href="09_generate_elbow_motion.html#fci-en-cpp-09-generate-elbow-motion-api-155"><code>Robot::control()</code></a>, <a href="09_generate_elbow_motion.html#fci-en-cpp-09-generate-elbow-motion-api-153"><code>CartesianPose</code></a>, <a href="09_generate_elbow_motion.html#fci-en-cpp-09-generate-elbow-motion-api-154"><code>RobotState::O_T_EE</code></a> | Motion |
| [`10_generate_cartesian_pose_motion`](10_generate_cartesian_pose_motion.md) | Cartesian-pose callback motion | <a href="10_generate_cartesian_pose_motion.html#fci-en-cpp-10-generate-cartesian-pose-motion-api-157"><code>Robot::control()</code></a> | Motion |
| [`11_generate_cartesian_velocity_motion`](11_generate_cartesian_velocity_motion.md) | Cartesian-velocity callback motion | <a href="11_generate_cartesian_velocity_motion.html#fci-en-cpp-11-generate-cartesian-velocity-motion-api-162"><code>Robot::control()</code></a>, <a href="11_generate_cartesian_velocity_motion.html#fci-en-cpp-11-generate-cartesian-velocity-motion-api-163"><code>CartesianVelocities</code></a> | Motion |
| [`12_generate_cartesian_pose_motion_external_control_loop`](12_generate_cartesian_pose_motion_external_control_loop.md) | External Cartesian-pose loop | <a href="12_generate_cartesian_pose_motion_external_control_loop.html#fci-en-cpp-12-generate-cartesian-pose-motion-external-control-loop-api-165"><code>startCartesianPoseControl()</code></a>, <a href="12_generate_cartesian_pose_motion_external_control_loop.html#fci-en-cpp-12-generate-cartesian-pose-motion-external-control-loop-api-166"><code>ActiveControl::readOnce()</code></a>, <a href="12_generate_cartesian_pose_motion_external_control_loop.html#fci-en-cpp-12-generate-cartesian-pose-motion-external-control-loop-api-167"><code>ActiveControl::writeOnce()</code></a> | Motion |
| [`13_generate_cartesian_velocity_motion_external_control_loop`](13_generate_cartesian_velocity_motion_external_control_loop.md) | External Cartesian-velocity loop | <a href="13_generate_cartesian_velocity_motion_external_control_loop.html#fci-en-cpp-13-generate-cartesian-velocity-motion-external-control-loop-api-169"><code>setJointImpedance()</code></a>, <a href="13_generate_cartesian_velocity_motion_external_control_loop.html#fci-en-cpp-13-generate-cartesian-velocity-motion-external-control-loop-api-170"><code>startCartesianVelocityControl()</code></a> | Motion |
| [`14_generate_joint_position_motion_external_control_loop`](14_generate_joint_position_motion_external_control_loop.md) | External joint-position loop | <a href="14_generate_joint_position_motion_external_control_loop.html#fci-en-cpp-14-generate-joint-position-motion-external-control-loop-api-173"><code>startJointPositionControl()</code></a>, <a href="14_generate_joint_position_motion_external_control_loop.html#fci-en-cpp-14-generate-joint-position-motion-external-control-loop-api-174"><code>getLowerJointVelocityLimits()</code></a>, <a href="14_generate_joint_position_motion_external_control_loop.html#fci-en-cpp-14-generate-joint-position-motion-external-control-loop-api-176"><code>getUpperJointVelocityLimits()</code></a>, <a href="14_generate_joint_position_motion_external_control_loop.html#fci-en-cpp-14-generate-joint-position-motion-external-control-loop-api-175"><code>limitRate()</code></a> | Motion |
| [`15_generate_joint_velocity_motion_external_control_loop`](15_generate_joint_velocity_motion_external_control_loop.md) | External joint-velocity loop | <a href="15_generate_joint_velocity_motion_external_control_loop.html#fci-en-cpp-15-generate-joint-velocity-motion-external-control-loop-api-177"><code>startJointVelocityControl()</code></a> | Motion |
| [`16_motion_with_control_external_control_loop`](16_motion_with_control_external_control_loop.md) | External combined motion and torque loop | <a href="16_motion_with_control_external_control_loop.html#fci-en-cpp-16-motion-with-control-external-control-loop-api-183"><code>Torques</code></a>, <a href="16_motion_with_control_external_control_loop.html#fci-en-cpp-16-motion-with-control-external-control-loop-api-184"><code>logToCSV()</code></a> | Torque |
| [`17_joint_impedance_control`](17_joint_impedance_control.md) | Joint impedance control | <a href="17_joint_impedance_control.html#fci-en-cpp-17-joint-impedance-control-api-186"><code>Model::coriolis()</code></a>, <a href="17_joint_impedance_control.html#fci-en-cpp-17-joint-impedance-control-api-187"><code>Model::gravity()</code></a>, <a href="17_joint_impedance_control.html#fci-en-cpp-17-joint-impedance-control-api-188"><code>Robot::control()</code></a> | Torque |
| [`18_cartesian_impedance_control`](18_cartesian_impedance_control.md) | Cartesian impedance control | <a href="18_cartesian_impedance_control.html#fci-en-cpp-18-cartesian-impedance-control-api-191"><code>Model::zeroJacobian()</code></a> | Torque |
| [`19_force_control`](19_force_control.md) | Force control | <a href="19_force_control.html#fci-en-cpp-19-force-control-api-196"><code>Model::gravity()</code></a> | Torque |
| [`20_motion_with_control`](20_motion_with_control.md) | Combined motion generation and torque control | <a href="20_motion_with_control.html#fci-en-cpp-20-motion-with-control-api-198"><code>Robot::control()</code></a>, <a href="20_motion_with_control.html#fci-en-cpp-20-motion-with-control-api-199"><code>Record</code></a> | Torque |
</div>

`grasp_object` and `vacuum_object` are unsupported gripper-related upstream files and are excluded.

```{warning}
Apart from `echo_robot_state` and `print_joint_poses`, examples may send motion or torque commands; `communication_test` also moves first and then enters a zero-torque control session. Most motion examples first move to a model-specific initial pose; see {ref}`Initial Pose <fci-initial-pose>`.
```

```{toctree}
:hidden:

01_echo_robot_state
02_communication_test
03_print_joint_poses
04_async_position_control
05_joint_point_to_point_motion
06_generate_joint_position_motion
07_generate_joint_velocity_motion
08_generate_consecutive_motions
09_generate_elbow_motion
10_generate_cartesian_pose_motion
11_generate_cartesian_velocity_motion
12_generate_cartesian_pose_motion_external_control_loop
13_generate_cartesian_velocity_motion_external_control_loop
14_generate_joint_position_motion_external_control_loop
15_generate_joint_velocity_motion_external_control_loop
16_motion_with_control_external_control_loop
17_joint_impedance_control
18_cartesian_impedance_control
19_force_control
20_motion_with_control
```

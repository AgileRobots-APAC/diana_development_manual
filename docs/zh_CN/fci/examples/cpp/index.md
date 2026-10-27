# C++ FCI 示例

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

C++ 示例位于应用机型补丁后的 `libfranka/examples/<model>/`。`<model>` 为 `diana3`、`diana7` 或 `diana7G2`。

<div class="example-list-table">

| 示例 | 用途 | 使用的接口 | 风险 |
|---|---|---|---|
| [`01_echo_robot_state`](01_echo_robot_state.md) | 连续读取并打印机器人状态 | <a href="01_echo_robot_state.html#fci-zh-cpp-01-echo-robot-state-api-1"><code>franka::Robot</code></a>、<a href="01_echo_robot_state.html#fci-zh-cpp-01-echo-robot-state-api-2"><code>Robot::read()</code></a>、<a href="01_echo_robot_state.html#fci-zh-cpp-01-echo-robot-state-api-124"><code>franka::RobotState</code></a> | 只读 |
| [`02_communication_test`](02_communication_test.md) | 评估控制通信成功率和丢失周期 | <a href="02_communication_test.html#fci-zh-cpp-02-communication-test-api-1"><code>Robot::startTorqueControl()</code></a>、<a href="02_communication_test.html#fci-zh-cpp-02-communication-test-api-2"><code>readOnce()</code></a>、<a href="02_communication_test.html#fci-zh-cpp-02-communication-test-api-3"><code>writeOnce()</code></a>、<a href="02_communication_test.html#fci-zh-cpp-02-communication-test-api-128"><code>control_command_success_rate</code></a> | 力矩 / 运动 |
| [`03_print_joint_poses`](03_print_joint_poses.md) | 打印各关节及末端执行器坐标系位姿 | <a href="03_print_joint_poses.html#fci-zh-cpp-03-print-joint-poses-api-1"><code>franka::RobotState</code></a>、<a href="03_print_joint_poses.html#fci-zh-cpp-03-print-joint-poses-api-2"><code>Robot::readOnce()</code></a>、<a href="03_print_joint_poses.html#fci-zh-cpp-03-print-joint-poses-api-3"><code>Robot::loadModel()</code></a>、<a href="03_print_joint_poses.html#fci-zh-cpp-03-print-joint-poses-api-4"><code>Model::pose()</code></a> | 只读 |
| [`04_async_position_control`](04_async_position_control.md) | 实验性异步位置控制 | <a href="04_async_position_control.html#fci-zh-cpp-04-async-position-control-api-5"><code>AsyncPositionControlHandler::configure()</code></a>、<a href="04_async_position_control.html#fci-zh-cpp-04-async-position-control-api-6"><code>getTargetFeedback()</code></a>、<a href="04_async_position_control.html#fci-zh-cpp-04-async-position-control-api-7"><code>setJointPositionTarget()</code></a>、<a href="04_async_position_control.html#fci-zh-cpp-04-async-position-control-api-8"><code>stopControl()</code></a> | 运动 |
| [`05_joint_point_to_point_motion`](05_joint_point_to_point_motion.md) | 关节点到点运动 | <a href="05_joint_point_to_point_motion.html#fci-zh-cpp-05-joint-point-to-point-motion-api-9"><code>MotionGenerator</code></a>、<a href="05_joint_point_to_point_motion.html#fci-zh-cpp-05-joint-point-to-point-motion-api-10"><code>Robot::setCollisionBehavior()</code></a>、<a href="05_joint_point_to_point_motion.html#fci-zh-cpp-05-joint-point-to-point-motion-api-11"><code>Robot::control()</code></a> | 运动 |
| [`06_generate_joint_position_motion`](06_generate_joint_position_motion.md) | 关节位置回调运动 | <a href="06_generate_joint_position_motion.html#fci-zh-cpp-06-generate-joint-position-motion-api-12"><code>Robot::control()</code></a>、<a href="06_generate_joint_position_motion.html#fci-zh-cpp-06-generate-joint-position-motion-api-13"><code>RobotState::q</code></a>、<a href="06_generate_joint_position_motion.html#fci-zh-cpp-06-generate-joint-position-motion-api-14"><code>Duration::toSec()</code></a>、<a href="06_generate_joint_position_motion.html#fci-zh-cpp-06-generate-joint-position-motion-api-15"><code>JointPositions</code></a>、<a href="06_generate_joint_position_motion.html#fci-zh-cpp-06-generate-joint-position-motion-api-16"><code>MotionFinished()</code></a> | 运动 |
| [`07_generate_joint_velocity_motion`](07_generate_joint_velocity_motion.md) | 关节速度回调运动 | <a href="07_generate_joint_velocity_motion.html#fci-zh-cpp-07-generate-joint-velocity-motion-api-17"><code>Robot::control()</code></a>、<a href="07_generate_joint_velocity_motion.html#fci-zh-cpp-07-generate-joint-velocity-motion-api-19"><code>JointVelocities</code></a> | 运动 |
| [`08_generate_consecutive_motions`](08_generate_consecutive_motions.md) | 连续关节速度运动 | <a href="08_generate_consecutive_motions.html#fci-zh-cpp-08-generate-consecutive-motions-api-24"><code>ControlException</code></a>、<a href="08_generate_consecutive_motions.html#fci-zh-cpp-08-generate-consecutive-motions-api-25"><code>automaticErrorRecovery()</code></a> | 运动 |
| [`09_generate_elbow_motion`](09_generate_elbow_motion.md) | 带 elbow 冗余的笛卡尔运动 | <a href="09_generate_elbow_motion.html#fci-zh-cpp-09-generate-elbow-motion-api-26"><code>Robot::control()</code></a>、<a href="09_generate_elbow_motion.html#fci-zh-cpp-09-generate-elbow-motion-api-27"><code>CartesianPose</code></a>、<a href="09_generate_elbow_motion.html#fci-zh-cpp-09-generate-elbow-motion-api-28"><code>RobotState::O_T_EE</code></a> | 运动 |
| [`10_generate_cartesian_pose_motion`](10_generate_cartesian_pose_motion.md) | 笛卡尔位姿回调运动 | <a href="10_generate_cartesian_pose_motion.html#fci-zh-cpp-10-generate-cartesian-pose-motion-api-157"><code>Robot::control()</code></a> | 运动 |
| [`11_generate_cartesian_velocity_motion`](11_generate_cartesian_velocity_motion.md) | 笛卡尔速度回调运动 | <a href="11_generate_cartesian_velocity_motion.html#fci-zh-cpp-11-generate-cartesian-velocity-motion-api-37"><code>Robot::control()</code></a>、<a href="11_generate_cartesian_velocity_motion.html#fci-zh-cpp-11-generate-cartesian-velocity-motion-api-38"><code>CartesianVelocities</code></a> | 运动 |
| [`12_generate_cartesian_pose_motion_external_control_loop`](12_generate_cartesian_pose_motion_external_control_loop.md) | 笛卡尔位姿外部控制循环 | <a href="12_generate_cartesian_pose_motion_external_control_loop.html#fci-zh-cpp-12-generate-cartesian-pose-motion-external-control-loop-api-41"><code>startCartesianPoseControl()</code></a>、<a href="12_generate_cartesian_pose_motion_external_control_loop.html#fci-zh-cpp-12-generate-cartesian-pose-motion-external-control-loop-api-42"><code>ActiveControl::readOnce()</code></a>、<a href="12_generate_cartesian_pose_motion_external_control_loop.html#fci-zh-cpp-12-generate-cartesian-pose-motion-external-control-loop-api-43"><code>ActiveControl::writeOnce()</code></a> | 运动 |
| [`13_generate_cartesian_velocity_motion_external_control_loop`](13_generate_cartesian_velocity_motion_external_control_loop.md) | 笛卡尔速度外部控制循环 | <a href="13_generate_cartesian_velocity_motion_external_control_loop.html#fci-zh-cpp-13-generate-cartesian-velocity-motion-external-control-loop-api-45"><code>setJointImpedance()</code></a>、<a href="13_generate_cartesian_velocity_motion_external_control_loop.html#fci-zh-cpp-13-generate-cartesian-velocity-motion-external-control-loop-api-46"><code>startCartesianVelocityControl()</code></a> | 运动 |
| [`14_generate_joint_position_motion_external_control_loop`](14_generate_joint_position_motion_external_control_loop.md) | 关节位置外部控制循环 | <a href="14_generate_joint_position_motion_external_control_loop.html#fci-zh-cpp-14-generate-joint-position-motion-external-control-loop-api-50"><code>startJointPositionControl()</code></a>、<a href="14_generate_joint_position_motion_external_control_loop.html#fci-zh-cpp-14-generate-joint-position-motion-external-control-loop-api-51"><code>getLowerJointVelocityLimits()</code></a>、<a href="14_generate_joint_position_motion_external_control_loop.html#fci-zh-cpp-14-generate-joint-position-motion-external-control-loop-api-52"><code>getUpperJointVelocityLimits()</code></a>、<a href="14_generate_joint_position_motion_external_control_loop.html#fci-zh-cpp-14-generate-joint-position-motion-external-control-loop-api-53"><code>limitRate()</code></a> | 运动 |
| [`15_generate_joint_velocity_motion_external_control_loop`](15_generate_joint_velocity_motion_external_control_loop.md) | 关节速度外部控制循环 | <a href="15_generate_joint_velocity_motion_external_control_loop.html#fci-zh-cpp-15-generate-joint-velocity-motion-external-control-loop-api-55"><code>startJointVelocityControl()</code></a> | 运动 |
| [`16_motion_with_control_external_control_loop`](16_motion_with_control_external_control_loop.md) | 运动与力矩组合外部控制循环 | <a href="16_motion_with_control_external_control_loop.html#fci-zh-cpp-16-motion-with-control-external-control-loop-api-62"><code>Torques</code></a>、<a href="16_motion_with_control_external_control_loop.html#fci-zh-cpp-16-motion-with-control-external-control-loop-api-65"><code>logToCSV()</code></a> | 力矩 |
| [`17_joint_impedance_control`](17_joint_impedance_control.md) | 关节阻抗控制 | <a href="17_joint_impedance_control.html#fci-zh-cpp-17-joint-impedance-control-api-67"><code>Model::coriolis()</code></a>、<a href="17_joint_impedance_control.html#fci-zh-cpp-17-joint-impedance-control-api-68"><code>Model::gravity()</code></a>、<a href="17_joint_impedance_control.html#fci-zh-cpp-17-joint-impedance-control-api-71"><code>Robot::control()</code></a> | 力矩 |
| [`18_cartesian_impedance_control`](18_cartesian_impedance_control.md) | 笛卡尔阻抗控制 | <a href="18_cartesian_impedance_control.html#fci-zh-cpp-18-cartesian-impedance-control-api-74"><code>Model::zeroJacobian()</code></a> | 力矩 |
| [`19_force_control`](19_force_control.md) | 力控制 | <a href="19_force_control.html#fci-zh-cpp-19-force-control-api-80"><code>Model::gravity()</code></a> | 力矩 |
| [`20_motion_with_control`](20_motion_with_control.md) | 运动生成与力矩控制组合 | <a href="20_motion_with_control.html#fci-zh-cpp-20-motion-with-control-api-82"><code>Robot::control()</code></a>、<a href="20_motion_with_control.html#fci-zh-cpp-20-motion-with-control-api-86"><code>Record</code></a> | 力矩 |
</div>

`grasp_object` 和 `vacuum_object` 为夹爪相关上游文件，当前 Diana FCI 不支持，已排除。

```{warning}
除 `echo_robot_state` 与 `print_joint_poses` 外，示例可能发送运动或力矩命令；`communication_test` 也会先运动并进入零力矩控制会话。多数运动示例会先移至按机型不同的初始姿态，见 {ref}`初始姿态 <fci-initial-pose>`。
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

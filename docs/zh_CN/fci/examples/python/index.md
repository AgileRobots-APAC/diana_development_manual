# Python FCI 示例总览

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

Python FCI 示例来自选定机型补丁后的 `libfranka/pylibfranka/examples/<model>/`，使用的是 `pylibfranka`，不是本网站已有的普通 Diana Python SDK。

<div class="example-list-table">

| 示例 | 用途 | 使用的接口 | 风险 |
|---|---|---|---|
| [`01_print_robot_state`](01_print_robot_state.md) | 读取并打印机器人状态 | <a href="01_print_robot_state.html#fci-zh-python-01-print-robot-state-api-88"><code>pylibfranka.Robot</code></a>、<a href="01_print_robot_state.html#fci-zh-python-01-print-robot-state-api-89"><code>Robot.set_collision_behavior()</code></a>、<a href="01_print_robot_state.html#fci-zh-python-01-print-robot-state-api-90"><code>Robot.read_once()</code></a>、<a href="01_print_robot_state.html#fci-zh-python-01-print-robot-state-api-91"><code>RobotState</code></a> | 只读 |
| [`02_joint_position_example`](02_joint_position_example.md) | 关节位置外部控制 | <a href="02_joint_position_example.html#fci-zh-python-02-joint-position-example-api-94"><code>start_joint_position_control()</code></a>、<a href="02_joint_position_example.html#fci-zh-python-02-joint-position-example-api-95"><code>ActiveControl.readOnce()</code></a>、<a href="02_joint_position_example.html#fci-zh-python-02-joint-position-example-api-96"><code>ActiveControl.writeOnce()</code></a>、<a href="02_joint_position_example.html#fci-zh-python-02-joint-position-example-api-97"><code>JointPositions</code></a> | 运动 |
| [`03_joint_velocity_example`](03_joint_velocity_example.md) | 关节速度外部控制 | <a href="03_joint_velocity_example.html#fci-zh-python-03-joint-velocity-example-api-100"><code>start_joint_velocity_control()</code></a>、<a href="03_joint_velocity_example.html#fci-zh-python-03-joint-velocity-example-api-103"><code>JointVelocities</code></a> | 运动 |
| [`04_cartesian_pose_example`](04_cartesian_pose_example.md) | 笛卡尔位姿外部控制 | <a href="04_cartesian_pose_example.html#fci-zh-python-04-cartesian-pose-example-api-105"><code>start_cartesian_pose_control()</code></a>、<a href="04_cartesian_pose_example.html#fci-zh-python-04-cartesian-pose-example-api-108"><code>CartesianPose</code></a> | 运动 |
| [`05_cartesian_velocity_example`](05_cartesian_velocity_example.md) | 笛卡尔速度外部控制 | <a href="05_cartesian_velocity_example.html#fci-zh-python-05-cartesian-velocity-example-api-110"><code>set_joint_impedance()</code></a>、<a href="05_cartesian_velocity_example.html#fci-zh-python-05-cartesian-velocity-example-api-111"><code>start_cartesian_velocity_control()</code></a>、<a href="05_cartesian_velocity_example.html#fci-zh-python-05-cartesian-velocity-example-api-114"><code>CartesianVelocities</code></a> | 运动 |
| [`06_joint_impedance_example`](06_joint_impedance_example.md) | 关节阻抗力矩控制 | <a href="06_joint_impedance_example.html#fci-zh-python-06-joint-impedance-example-api-116"><code>load_model()</code></a>、<a href="06_joint_impedance_example.html#fci-zh-python-06-joint-impedance-example-api-117"><code>read_once()</code></a>、<a href="06_joint_impedance_example.html#fci-zh-python-06-joint-impedance-example-api-118"><code>start_torque_control()</code></a>、<a href="06_joint_impedance_example.html#fci-zh-python-06-joint-impedance-example-api-121"><code>Torques</code></a> | 力矩 |
</div>

`move_gripper.py` 虽随上游文件保留，但当前 Diana FCI 不支持夹爪，因此不属于本教程范围。

```{warning}
Python 示例同样会进入 FCI 会话；运动和力矩示例必须经过现场安全确认后运行。部分示例会先移至按机型不同的初始姿态，见 {ref}`初始姿态 <fci-initial-pose>`。
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

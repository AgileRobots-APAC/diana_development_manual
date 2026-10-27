# `diana_msgs`

## Installation

See [Development Setup](../development.md).

## Package Overview

`diana_msgs` contains the message, service and action definitions shared by the Diana ROS 2 packages. It has no nodes of its own. It depends on `std_msgs`, `geometry_msgs` and `sensor_msgs`.

| Kind | Definitions |
| --- | --- |
| Messages | `DianaRobotState`, `CollisionIndicators`, `Elbow`, `Errors`, `TargetStatus` |
| Services | `SetCartesianStiffness`, `SetForceTorqueCollisionBehavior`, `SetFullCollisionBehavior`, `SetJointStiffness`, `SetLoad`, `SetStiffnessFrame`, `SetTCPFrame` |
| Actions | `ErrorRecovery`, `PTPMotion` |

Used by: [diana_hardware](diana_hardware.md) (services and the `ErrorRecovery` action), [diana_semantic_components](diana_semantic_components.md) and [diana_robot_state_broadcaster](diana_robot_state_broadcaster.md) (`DianaRobotState`).

## Messages

### DianaRobotState

`diana_msgs/msg/DianaRobotState` carries the full robot state. It is published by [diana_robot_state_broadcaster](diana_robot_state_broadcaster.md). Field names are lower case. Wrench, pose, twist and inertia fields use the stamped geometry message types.

| Group | Field | Type | Meaning |
| --- | --- | --- | --- |
| Header | `header` | `std_msgs/Header` | time stamp of the sample |
| Collision | `collision_indicators` | `CollisionIndicators` | active contact and collision flags |
| Joint space | `measured_joint_state` | `sensor_msgs/JointState` | measured position `q`, velocity `dq`, effort `tau_J` |
| Joint space | `desired_joint_state` | `sensor_msgs/JointState` | desired position `q_d`, velocity `dq_d`, effort `tau_J_d` |
| Joint space | `measured_joint_motor_state` | `sensor_msgs/JointState` | motor position `theta` and velocity `dtheta` |
| Joint space | `ddq_d` | `float64[7]` | desired joint acceleration |
| Joint space | `dtau_j` | `float64[7]` | derivative of the measured torque signal |
| Joint space | `tau_ext_hat_filtered` | `sensor_msgs/JointState` | filtered external torque (in `effort`) |
| Elbow | `elbow` | `Elbow` | elbow state, desired and commanded values |
| External wrench | `k_f_ext_hat_k` | `geometry_msgs/WrenchStamped` | estimated external wrench in the stiffness frame |
| External wrench | `o_f_ext_hat_k` | `geometry_msgs/WrenchStamped` | estimated external wrench in the base frame |
| Inertia | `inertia_ee` | `geometry_msgs/InertiaStamped` | end-effector inertia |
| Inertia | `inertia_load` | `geometry_msgs/InertiaStamped` | load inertia |
| Inertia | `inertia_total` | `geometry_msgs/InertiaStamped` | total (end effector + load) inertia |
| Poses | `o_t_ee` | `geometry_msgs/PoseStamped` | measured end-effector pose in the base frame |
| Poses | `o_t_ee_d` | `geometry_msgs/PoseStamped` | last desired end-effector pose of the motion generation |
| Poses | `o_t_ee_c` | `geometry_msgs/PoseStamped` | last commanded end-effector pose of the motion generation |
| Poses | `f_t_ee` | `geometry_msgs/PoseStamped` | flange to end-effector frame |
| Poses | `ee_t_k` | `geometry_msgs/PoseStamped` | end-effector to stiffness frame |
| Twist / accel | `o_dp_ee_d` | `geometry_msgs/TwistStamped` | desired end-effector twist in the base frame |
| Twist / accel | `o_dp_ee_c` | `geometry_msgs/TwistStamped` | last commanded end-effector twist in the base frame |
| Twist / accel | `o_ddp_ee_c` | `geometry_msgs/AccelStamped` | last commanded end-effector acceleration in the base frame |
| Additional | `time` | `float64` | robot time in seconds |
| Additional | `control_command_success_rate` | `float64` | success rate of the control commands |
| Additional | `robot_mode` | `uint8` | one of the `ROBOT_MODE_*` constants below |
| Errors | `current_errors` | `Errors` | currently active errors |
| Errors | `last_motion_errors` | `Errors` | errors that stopped the last motion |

Constants for `robot_mode`:

| Constant | Value |
| --- | --- |
| `ROBOT_MODE_OTHER` | 0 |
| `ROBOT_MODE_IDLE` | 1 |
| `ROBOT_MODE_MOVE` | 2 |
| `ROBOT_MODE_GUIDING` | 3 |
| `ROBOT_MODE_REFLEX` | 4 |
| `ROBOT_MODE_USER_STOPPED` | 5 |
| `ROBOT_MODE_AUTOMATIC_ERROR_RECOVERY` | 6 |

### Supporting Messages

| Message | Fields | Purpose |
| --- | --- | --- |
| `CollisionIndicators` | `is_cartesian_linear_collision`, `is_cartesian_angular_collision`, `is_cartesian_linear_contact`, `is_cartesian_angular_contact` (each `geometry_msgs/Vector3`); `is_joint_collision`, `is_joint_contact` (each `float64[7]`) | which Cartesian directions and joints have an active collision or contact flag |
| `Elbow` | `position`, `desired_position`, `commanded_position`, `commanded_velocity`, `commanded_acceleration` (each `float64[2]`) | elbow configuration as `[joint_3_position, joint_4_sign]` for each quantity |
| `Errors` | 36 `bool` flags, for example `joint_position_limits_violation`, `cartesian_velocity_violation`, `joint_reflex`, `cartesian_reflex`, `communication_constraints_violation`, `power_limit_violation`, `instability_detected` | one flag per controller or motion-generator error; see `msg/Errors.msg` for the complete list |
| `TargetStatus` | `status` (`uint8`); constants `IDLE`=0, `EXECUTING`=1, `TARGET_REACHED`=2, `ABORTED`=3 | status of a motion action |

## Services

All services share the same response: `bool success` and `string error`. Arrays are fixed size. The services are served by the plugin node `service_server` of [diana_hardware](diana_hardware.md).

### Service Definitions

| Service | Request fields | Meaning |
| --- | --- | --- |
| `SetJointStiffness` | `float64[7] joint_stiffness` | impedance of each joint in the internal controller |
| `SetCartesianStiffness` | `float64[6] cartesian_stiffness` | Cartesian stiffness (x, y, z, roll, pitch, yaw) in the stiffness frame |
| `SetTCPFrame` | `float64[16] transformation` | 4x4 column-major transform NE_T_EE from NE to EE |
| `SetStiffnessFrame` | `float64[16] transformation` | 4x4 column-major transform EE_T_K from EE to the stiffness frame K |
| `SetLoad` | `float64 mass`, `float64[3] center_of_mass`, `float64[9] load_inertia` | load mass, center of mass, and 3x3 column-major inertia |
| `SetForceTorqueCollisionBehavior` | `float64[7] lower_torque_thresholds_nominal`, `float64[7] upper_torque_thresholds_nominal`, `float64[6] lower_force_thresholds_nominal`, `float64[6] upper_force_thresholds_nominal` | collision and contact thresholds |
| `SetFullCollisionBehavior` | the four fields above plus `lower_torque_thresholds_acceleration`, `upper_torque_thresholds_acceleration` (`float64[7]`), `lower_force_thresholds_acceleration`, `upper_force_thresholds_acceleration` (`float64[6]`) | collision and contact thresholds including the acceleration-dependent ones |

```{warning}
These services change impedance, tool frames, payload and collision thresholds of the robot controller. Wrong values change how the robot reacts to contact and can lead to unexpected motion or missed collision detection. Set values that match your tool and workspace, and keep the emergency stop within reach; see [Safety Boundaries](../../../reference/safety.md).
```

### Calling Services

The examples use the default namespace `NS_1` of `diana.config.yaml`; drop `/NS_1` if you launched without a namespace.

Set a load (mass in kg, center of mass in m, inertia in kg m^2):

```bash
ros2 service call /NS_1/service_server/set_load diana_msgs/srv/SetLoad \
  "{mass: 0.5, center_of_mass: [0.0, 0.0, 0.05], load_inertia: [0.001, 0.0, 0.0, 0.0, 0.001, 0.0, 0.0, 0.0, 0.001]}"
```

Set the joint stiffness:

```bash
ros2 service call /NS_1/service_server/set_joint_stiffness diana_msgs/srv/SetJointStiffness \
  "{joint_stiffness: [600.0, 600.0, 600.0, 600.0, 250.0, 150.0, 50.0]}"
```

Set the transform from NE to EE to the identity transform (column-major):

```bash
ros2 service call /NS_1/service_server/set_tcp_frame diana_msgs/srv/SetTCPFrame \
  "{transformation: [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0]}"
```

```{note}
The numeric values above only illustrate the argument format. The valid ranges depend on your robot model and tool.
```

## Actions

### Action Definitions

| Action | Goal | Result | Feedback |
| --- | --- | --- | --- |
| `ErrorRecovery` | empty | empty | empty |
| `PTPMotion` | `float64[] goal_joint_configuration` (rad), `float64[] maximum_joint_velocities` (rad/s), `float64 goal_tolerance` (rad) | `TargetStatus target_status`, `string error_message` | `TargetStatus target_status` |

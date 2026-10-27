# Coordinates, Poses, and Kinematics

This page describes SDK-independent kinematics concepts. Consult the relevant SDK page for function names and types.

## Forward and inverse kinematics

| Need | Concept | Note |
|---|---|---|
| Joint angles known, end-effector pose wanted | Forward kinematics | Compute the TCP pose from the robot model |
| End-effector pose known, joint angles wanted | Inverse kinematics | Multiple candidate solutions may exist |
| End-effector pose and reference joint angles known | Reference inverse kinematics | Use the reference joint angles to find the solution closest to them |
| Multiple candidates need inspection | Solution enumeration / filtering | Select by joint limits, path continuity, and process constraints |

The same end-effector pose can have several joint solutions on redundant robots. Read [Inverse Solutions and Configuration Continuity](inverse_uniqueness.md) before Cartesian motion on a 7-axis arm.

## Poses and coordinate transforms

| Need | Concept |
|---|---|
| Convert between orientation representations | RPY, axis-angle, quaternion, and other conversions |
| Convert between matrices and poses | Homogeneous matrix and pose conversions |
| Move a pose from one frame to another | Coordinate / pose transform |
| Describe tool or workpiece relationships | TCP, flange, base frame, workpiece frame |

## Model parameters and Jacobian

| Need | Concept |
|---|---|
| Describe link geometry | DH parameters or an equivalent kinematics model |
| Calibrate or correct the model | DH calibration / model parameter correction |
| Relate joint velocity to TCP velocity | Jacobian matrix |
| Detect singularity or near singularity | Jacobian degeneracy and condition-number analysis |

## Coordinate Frames and Redundancy in FCI and ROS 2

- **Redundancy parameter:** In both FCI and ROS 2, Cartesian pose and Cartesian velocity commands can carry an elbow parameter, which fixes the intended one of several joint configurations of a 7-axis arm. This is the same idea as [Inverse Solutions and Configuration Continuity](inverse_uniqueness.md). The elbow parameter is two numbers: the first is the desired position of joint 3 (rad), which the arm can change to move the elbow while the end-effector pose stays fixed; the second is the flip direction of joint 4, which tells which side the elbow points to. In ROS 2 it is written `[joint_3_position, joint_4_sign]` and maps to the `elbow_command` interfaces.
- **End-effector frames (ROS 2):** The nominal end-effector frame NE, the end-effector frame EE, and the stiffness frame K are chained in that order. The service `set_tcp_frame` sets the transform NE_T_EE from NE to EE, and `set_stiffness_frame` sets EE_T_K from EE to K; Cartesian stiffness acts along the axes of K.

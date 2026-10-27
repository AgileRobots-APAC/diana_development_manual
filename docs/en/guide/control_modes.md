# Control Models and Mode Selection

Choose the control capability before selecting an API. Function names, parameters, and limits belong to the matching programming guide or API reference.

| Need | Recommended control | Typical use |
|---|---|---|
| Reach a defined target | Target-point motion | Pick and place, homing, camera positions |
| Approach along a line | Cartesian linear motion | Insertion, approach, tool-axis movement |
| Make a short adjustment | Jog | Debugging, teaching assistance, low-speed positioning |
| Move continuously at a velocity | Velocity control | Human-robot interaction, scanning, continuous external adjustment |
| Update targets at high rate | Online servo control | Visual servoing, hybrid force/position strategies, external real-time planners |
| Control or send torque | Torque control | Dynamics experiments, low-level control research, special real-time control |
| Adapt to contact force | Force/impedance control | Grinding, assembly, contact detection, compliant control |
| Hand-guide the robot | Free drive | Teaching, path capture, pose adjustment |

## Trajectory and real-time control are different concepts

Trajectory control is controller-planned. Real-time control requires continuous host updates; choose trajectory control when update period, latency, or target continuity cannot be guaranteed.

## Selection and transition rules

- Validate a process with point-to-point or linear trajectories first. Introduce velocity, servo, torque, or force control only when an external closed loop is truly required.
- Velocity control and online servo are not trajectory commands that can be sent once and waited on. Prepare a continuous target source, packet-loss/timeout behavior, and an explicit stop condition.
- Before entering force, impedance, or free-drive modes, confirm tool payload, TCP, collision policy, and on-site safety boundaries. Restore the normal position-control flow only after leaving the mode.
- Let only one application state machine own motion commands at a time. During a mode transition, error recovery, or shutdown, stop the current motion and confirm controller state before sending another command type.

## Real-Time Control in Each Access Method

Both FCI and ROS 2 support the five real-time control inputs below. FCI returns the matching type from the real-time callback; in ROS 2 the controller claims the matching command interfaces. In both, only one control input is active at a time.

| Control input | Type returned by an FCI callback | ROS 2 command interface |
|---|---|---|
| Joint position | `franka::JointPositions` | the joints' `position` command interfaces |
| Joint velocity | `franka::JointVelocities` | the joints' `velocity` command interfaces |
| Joint torque | `franka::Torques` | the joints' `effort` command interfaces |
| Cartesian pose | `franka::CartesianPose` (optionally with an elbow parameter) | `cartesian_pose_command` command interfaces (optionally with elbow interfaces) |
| Cartesian velocity | `franka::CartesianVelocities` (optionally with an elbow parameter) | `cartesian_velocity` command interfaces (optionally with elbow interfaces) |

In ROS 2, trajectory-type control is usually planned by MoveIt and then executed by a trajectory controller.

```{warning}
The real-time call period, look-ahead time, and gain constrain one another. Parameter ranges, mode availability, and exit behavior must be verified against the current SDK headers and API Reference.
```

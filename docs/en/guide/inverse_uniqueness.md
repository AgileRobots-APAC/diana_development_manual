# Inverse Solutions and Configuration Continuity

This page mainly targets redundant robots such as Diana. They can have multiple joint configurations for one TCP pose; to keep the robot moving in the intended configuration, make the inverse-kinematics solution unique during trajectory design.

```{figure} ../../_static/diagrams/redundant_ik_en.png
:alt: Multiple redundant configurations can correspond to one TCP pose
:width: 100%

One TCP pose can correspond to several different joint configurations. In actual planning, choose the most suitable IK solution using the joint angles of the reference point, joint limits, singularity, collision risk, and path continuity.
```

## Case 1: joint angles at a waypoint are known

For example, the joint angles at point A and the pose at point B are known.

| Step | Recommended approach | Purpose |
|---|---|---|
| Return to point A | Use the known joint angles of A directly as the target | Return to a deterministic configuration |
| Move from A to B | Generate the next motion segment from the target pose | Solve near the known configuration |
| Reciprocal motion | Keep returning to A with the known joint angles of A | Return to the same joint angles every time |

## Case 2: only poses are known, no joint angles

| Step | Recommended approach | Purpose |
|---|---|---|
| Prepare a reference point | Teach a reference point near each target pose | Provide a reference for IK |
| Record the reference joint angles | Record the joint angles of each reference point | Use them as the reference when solving |
| Solve the target | Use the inverse function with reference joint angles (`inverse_ext`) to find the solution closest to them in Euclidean distance | Keep the solution near the reference point |
| Execute the motion | Move to the solved joint angles as the target (`moveJToTarget` or `moveLToTarget`) | Move with the joint angles already solved |

## Case 3: real-time Cartesian control (FCI and ROS 2)

An FCI callback or a ROS 2 controller sends a Cartesian pose or velocity every control cycle, and the controller solves the inverse kinematics internally. The application can constrain the configuration only through the continuity of the pose and the elbow parameter.

| Step | Recommended approach | Purpose |
|---|---|---|
| Read the start | Read the current pose and the current elbow value first, and use them as the target of the first cycle | The first step matches the current state, with no jump |
| Hold the configuration | Send the elbow parameter together with the pose in every cycle, and change it only when needed | Fix the configuration on the 7-axis redundancy |
| Stay continuous | Change the pose and the elbow value only by small steps between cycles | Avoid a jump relative to the current state |

The FCI example `generate_elbow_motion` and the ROS 2 `cartesian_elbow_example_controller` both work this way: they read the initial pose and elbow value, then change joint 3 of the elbow step by step while keeping the end-effector pose fixed.

## Case 4: inverse kinematics from MoveIt in ROS 2

In ROS 2, controllers that need inverse kinematics, such as `joint_impedance_with_ik_example_controller`, solve it through the MoveIt `compute_ik` service. The solver is set in `kinematics.yaml` of `diana_moveit_config` (by default `lma_kinematics_plugin/LMAKinematicsPlugin`). For a target pose the solver returns one of the possible solutions, which is not guaranteed to match the configuration used when teaching, so the design principles below still apply: store joint angles and keep the joint angles of a reference point for key waypoints.

## Design principles

| Principle | Reason |
|---|---|
| Store joint angles whenever possible | They include configuration information |
| Store the joint angles of a reference point with Cartesian targets | The inverse function uses them as the reference and returns the closest solution |
| In reciprocal motion, use joint angles as the target of at least one point | Returning to that point with joint angles instead of a pose brings the robot back to the same joint angles every time, with no inverse kinematics needed |

For how to pass reference joint angles or enumerate/filter candidate solutions in a specific SDK, see that SDK's programming guide or the separate interface reference.

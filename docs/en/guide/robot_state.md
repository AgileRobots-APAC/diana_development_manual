# State, Feedback, and Callbacks

SDKs can expose state by callbacks, polling, ROS topics, or real-time streams. The state categories that matter during development are common across them. This page explains only the data-handling boundary and does not define the callback signature of a specific SDK.

| State | Meaning | Common use |
|---|---|---|
| Joint positions | Current angle or displacement of each joint | Position recording, pre/post-motion verification, trajectory debugging |
| Joint velocities | Current velocity of each joint | Determine whether the robot is still moving |
| Joint current / torque | Drive-side load information | Load, abnormal resistance, and motor diagnostics |
| TCP pose | Position and orientation of the tool center point | Cartesian debugging, process pose recording |
| TCP external force | Measured or estimated external force at the end effector | Contact detection, force control, process monitoring |
| Collision / error state | Controller safety and exception flags | Safety protection, fault diagnosis, workflow interruption |
| I/O state | Digital, analog, or extended I/O state | Gripper, sensor, and external-device coordination |

## State handling recommendations

| Situation | Recommendation |
|---|---|
| State arrives in a callback | Only copy data, update flags, or write non-blocking logs |
| Expensive computation or file writes needed | Move the work to an application thread; never block the state path |
| Latest state snapshot needed | Update shared state where state is received; let application threads read it |
| State read only occasionally | Use the SDK's active query interface, which is simpler |

Field names, structure names, and query functions are maintained by the individual SDKs or the separate interface reference.

## Recommended state machine

Do not use “connection succeeded” as the only condition for motion. Keep communication, controller, and application state separate, for example:

```{figure} ../../_static/images/robot-state-machine-en.png
:alt: Robot application state machine for network, SDK connection, safety conditions, and exception handling
:width: 100%
```

For the C/C++ SDK, the state callback commonly carries high-rate joint position/velocity, current or torque, TCP pose, TCP external force, and collision information. Active queries are better suited to startup checks, low-rate diagnostics, and command-result confirmation. In either case, retain the newest timestamp at the receiving boundary so the application can detect stale feedback.

## State Sources in Each Access Method

| Access method | How state reaches the application | Notes |
|---|---|---|
| C++ / Python SDK | State callback or active query | See above |
| FCI | `franka::RobotState` from `read()`, `readOnce()`, or the control callback; model data from `franka::Model` | Arrives with the callback every control cycle; do not block in the callback |
| ROS 2 | `diana_robot_state_broadcaster` publishes `~/robot_state` (every control cycle, 1000 Hz) and a set of convenience topics | The convenience topics use best-effort QoS, so a subscriber must use a compatible QoS to receive them |

```{important}
A callback is not a safety function. After a collision, error, or feedback interruption, immediately stop the application from issuing further commands and handle the site according to the applicable robot safety procedure.
```

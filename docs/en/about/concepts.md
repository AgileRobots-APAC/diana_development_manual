# Core Concepts

This section contains concepts that are independent of individual function names but determine whether an application is correct and safe. It is not an API index and does not have to be read end to end on first integration: choose the topic that matches the development task.

```{toctree}
:hidden:

../guide/control_modes
../guide/robot_state
../guide/kinematics
../guide/inverse_uniqueness
```

| Development task | Read |
|---|---|
| Choose between target motion, velocity control, servo control, or force control | [Control Models and Mode Selection](../guide/control_modes.md) |
| Receive state, errors, I/O, or high-rate feedback | [State, Feedback, and Callbacks](../guide/robot_state.md) |
| Use TCP, workpiece frames, pose transforms, or Cartesian targets | [Coordinates, Poses, and Kinematics](../guide/kinematics.md) |
| Plan Cartesian or reciprocal paths on a 7-axis robot | [Inverse Solutions and Configuration Continuity](../guide/inverse_uniqueness.md) |

## Choosing an Access Method

The same control concepts can be used through different access methods. Choose the access method first, then continue with its programming guide:

| Access method | Suited to | How it runs | Main prerequisites |
|---|---|---|---|
| C++ / Python SDK | Discrete motion commands, I/O, paths, tool frames, and controller function calls | Calls the interfaces provided by the controller, which generates and executes the motion | Control PC and control cabinet are connected over the network |
| FCI | Real-time closed loops, model computation, and torque control | The application supplies targets or torques continuously in a real-time callback, every control cycle | Verified real-time link, no blocking I/O in the callback, collaborative mode |
| ROS 2 | Joining the ROS 2 ecosystem: `ros2_control` controllers, MoveIt planning, and Gazebo simulation | Controllers read and write interfaces of the `diana_hardware` hardware interface in the control cycle; only one command mode runs per cycle | A supported Ubuntu and ROS 2 distribution, `libfranka 0.18.2`, real-time permissions, and collaborative mode on a real robot |

FCI callbacks and ROS 2 controllers both run inside the real-time control cycle, so the real-time principles in Control Models and Mode Selection apply to them as well.

For function names, structure fields, and valid parameter ranges, use the programming guide of the chosen access method and the separately maintained API reference.

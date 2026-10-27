# ROS 2 Overview and Distribution Selection

When choosing a distribution, check Ubuntu, ROS 2, and the package versions in the workspace together. Humble and Jazzy use different sources and package structures: Humble is mostly `diana_*` packages, while Jazzy moves the hardware, message, and controller layers to `franka_*` packages.

Model visualization, MoveIt planning, and fake-hardware demos are not equivalent to validating control on a real robot. Before using the example controllers or MoveIt, also check the network, the controller, the safety interfaces, and the configuration of the selected robot model.

## Distribution Comparison

| Item | Humble | Jazzy |
| --- | --- | --- |
| Platform | Ubuntu 22.04 | Ubuntu 24.04 |
| Hardware access, messages, and state broadcasting | `diana_hardware`, `diana_msgs`, `diana_robot_state_broadcaster` | `franka_hardware`, `franka_msgs`, `franka_robot_state_broadcaster` |
| Robot description `diana_description` | Imported through `dependency.repos` in the source | Ships with the source |
| Default namespace in `diana.config.yaml` | `NS_1` | Empty |
| Documentation | [diana_ros2: Humble](humble/index.md) | [diana_ros2: Jazzy](jazzy/index.md) |

## Shared Prerequisites

For both distributions, real-robot control connects to the robot through libfranka (FCI) and needs the same prerequisites:

- the teach pendant is in Collaborative mode and FCI is enabled, see the [FCI chapter](../fci/overview.md);
- the control PC can reach the controller, see [Network Setup](../programming/network.md);
- any operation that moves the robot or applies torque requires the on-site checks in [Safety Notes](../reference/safety.md) first.

```{important}
Do not mix Humble and Jazzy package sources, dependency versions, or workspaces. The default address of Diana robots is `192.168.10.75`, which matches the default controller A-port address given in [Network Setup](../programming/network.md). When connecting to a real robot, confirm the address on the teach pendant and pass `robot_ip` explicitly.
```

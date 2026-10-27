# diana_ros2: Jazzy

This section describes `diana_ros2`, the ROS 2 Jazzy package set for Diana robots. It is based on the FCI implementation (libfranka) and contains the hardware interface, example controllers, the robot state broadcaster, the MoveIt 2 configuration, Gazebo simulation, and the robot description `diana_description`, which ships with the source. The package layout follows franka_ros2 Jazzy and is adapted for the Diana robot description, MoveIt configuration, and Gazebo launch files.

```{important}
`diana_ros2` Jazzy targets **Ubuntu 24.04 and ROS 2 Jazzy**. Jazzy and Humble use different sources, dependencies, and package sets; do not mix their commands or workspaces. See [Overview and Distribution Selection](../overview.md).
```

```{warning}
Before connecting to a real robot, meet the same prerequisites as in the [FCI chapter](../../fci/overview.md): the teach pendant is in Collaborative mode, FCI is enabled, and the control PC can reach the controller (see [Network Setup](../../programming/network.md)). Any operation that moves the robot or applies torque also requires the on-site checks in [Safety Notes](../../reference/safety.md).
```

```{note}
This chapter is written against the current Jazzy source. Some packages keep the upstream `franka_*` names (for example `franka_hardware` and `franka_msgs`); the pages keep them as they are in the source.
```

## Reading Order

1. Read [Development Setup](development.md) to check the version requirements and set up ROS 2, libfranka, the source and dependencies, the build, and real-time permissions.
2. Follow the [Quick Start](quick_start.md) to verify model visualization, simulation, and the first example controller.
3. Look up the interfaces, parameters, and usage of each package in [Packages](packages/index.md); the example controllers are described in [franka_example_controllers](packages/franka_example_controllers.md).

```{toctree}
:hidden:
:maxdepth: 1

development
quick_start
packages/index
```

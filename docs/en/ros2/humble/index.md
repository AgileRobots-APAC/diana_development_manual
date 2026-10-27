# diana_ros2: Humble

This section describes `diana_ros2`, the ROS 2 Humble package set for Diana robots: the `ros2_control` hardware interface, example controllers, the robot state broadcaster, the MoveIt 2 configuration, and Gazebo simulation. The packages follow the structure of franka_ros2 and adapt the robot description, MoveIt configuration, and Gazebo launch files to Diana.

```{important}
`diana_ros2` Humble targets **Ubuntu 22.04 and ROS 2 Humble**. Humble and Jazzy use different sources, dependencies, and package sets; do not mix their commands or workspaces. See [Overview and Distribution Selection](../overview.md).
```

```{warning}
`diana_hardware` connects to the robot through libfranka (FCI). Before connecting to a real robot, meet the same prerequisites as in the [FCI chapter](../../fci/overview.md): the teach pendant is in Collaborative mode, FCI is enabled, and the control PC can reach the controller (see [Network Setup](../../programming/network.md)). Any operation that moves the robot or applies torque also requires the on-site checks in [Safety Notes](../../reference/safety.md).
```

## Reading Order

1. Read [Development Setup](development.md) to check the version requirements and set up ROS 2, the source and dependencies, the build, and realtime permissions.
2. Follow [Quick Start](quick_start.md) to verify model visualization, simulation, and the first example controller.
3. The interfaces, parameters, and usage of each package are in [Packages](packages/index.md); the example controllers are in [diana_example_controllers](packages/diana_example_controllers.md).

```{toctree}
:hidden:
:maxdepth: 1

development
quick_start
packages/index
```

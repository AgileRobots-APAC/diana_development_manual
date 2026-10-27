# Packages

`diana_ros2` Jazzy consists of the packages below. Each package has its own page; look it up by package name.

## Package List

| Package | Version | Purpose |
| --- | --- | --- |
| `diana_ros2` | 3.5.3 | Metapackage that organizes the other Diana ROS 2 packages |
| [`diana_description`](diana_description.md) | 2.0.0 | Robot description, meshes, and RViz configuration, shipped with the source |
| [`diana_bringup`](diana_bringup.md) | 3.5.3 | `ros2_control` launch files and runtime configuration |
| [`franka_example_controllers`](franka_example_controllers.md) | 3.5.3 | Example controllers |
| [`diana_moveit_config`](diana_moveit_config.md) | 3.5.3 | MoveIt 2 planning configuration and launch files |
| [`diana_gazebo_bringup`](diana_gazebo_bringup.md), [`diana_gazebo_hardware`](diana_gazebo_bringup.md) | 3.4.1, 3.5.3 | Gazebo launch files, worlds, and the simulated hardware plugin |
| [`franka_hardware`](franka_hardware.md) | 3.5.3 | libfranka-based `ros2_control` hardware interface |
| [`franka_msgs`](franka_msgs.md) | 3.5.3 | Messages, services, and actions |
| [`franka_robot_state_broadcaster`](franka_robot_state_broadcaster.md) | 3.5.3 | Robot state broadcaster |
| [`franka_semantic_components`](franka_semantic_components.md) | 3.5.3 | Semantic components that give controllers access to state and command interfaces |
| [`diana_selfcollision`](diana_selfcollision.md) | 1.0.0 | Self-collision checking |

`diana_gazebo_bringup` and `diana_gazebo_hardware` are located under the `diana_gazebo/` directory of the source, not at the top level. The `franka_*` package names keep the upstream naming and are currently unchanged.

## Package Dependencies

```{figure} ../../../../_static/images/ros2-jazzy-package-deps-en.png
:alt: Dependencies between the Diana ROS 2 Jazzy packages
:width: 80%

Dependencies between the packages according to their `package.xml` files. Arrows point from the dependent package to the package it depends on. The metapackage `diana_ros2` depends on all the others and is not drawn.
```

```{toctree}
:hidden:
:maxdepth: 1

diana_bringup
diana_description
franka_example_controllers
diana_moveit_config
diana_gazebo_bringup
franka_hardware
franka_msgs
franka_robot_state_broadcaster
franka_semantic_components
diana_selfcollision
```

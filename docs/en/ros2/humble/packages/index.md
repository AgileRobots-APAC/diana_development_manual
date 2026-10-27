# Packages

`diana_ros2` Humble consists of the packages below. Each package has its own page; look it up by package name.

## Package List

| Package | Version | Purpose |
| --- | --- | --- |
| `diana_ros2` | 2.5.0 | Meta package that organizes the other Diana ROS 2 packages |
| [`diana_description`](diana_description.md) | Pinned by `dependency.repos` | Robot description, meshes, and RViz configuration (external package, not in this source tree) |
| [`diana_bringup`](diana_bringup.md) | 2.7.0 | `ros2_control` launch files and runtime configuration |
| [`diana_example_controllers`](diana_example_controllers.md) | 2.7.0 | Example controllers |
| [`diana_hardware`](diana_hardware.md) | 2.7.0 | libfranka-based `ros2_control` hardware interface |
| [`diana_moveit_config`](diana_moveit_config.md) | 2.7.0 | MoveIt 2 planning configuration and launch files |
| [`diana_gazebo_bringup`](diana_gazebo_bringup.md), [`diana_gazebo_hardware`](diana_gazebo_bringup.md) | 2.7.0 | Gazebo launch files, simulation worlds, and the simulated hardware plugin |
| [`diana_msgs`](diana_msgs.md) | 2.5.0 | Diana-specific messages, services, and actions |
| [`diana_robot_state_broadcaster`](diana_robot_state_broadcaster.md) | 2.7.0 | Robot state broadcaster |
| [`diana_semantic_components`](diana_semantic_components.md) | 2.7.0 | Semantic components that give controllers access to state and command interfaces |

`diana_gazebo_bringup` and `diana_gazebo_hardware` are located under the `diana_gazebo/` directory of the source tree, not at the top level.

## Package Dependencies

```{figure} ../../../../_static/images/ros2-humble-package-deps-en.png
:alt: Dependencies between the Diana ROS 2 Humble packages
:width: 80%

Dependencies between the packages. Arrows point from the dependent package to the package it depends on. The metapackage `diana_ros2` depends on all the others and is not drawn.
```

```{toctree}
:hidden:
:maxdepth: 1

diana_bringup
diana_description
diana_example_controllers
diana_moveit_config
diana_gazebo_bringup
diana_hardware
diana_msgs
diana_robot_state_broadcaster
diana_semantic_components
```

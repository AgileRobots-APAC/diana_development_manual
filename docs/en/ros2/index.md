# ROS 2 Development Guide

This chapter covers ROS 2 environment setup, model visualization, simulation, and example verification for Diana robots. ROS 2 is maintained as an independent development approach alongside FCI, the C++ SDK, and the Python SDK.

The chapter is organized separately for each ROS 2 distribution: the two source trees differ in package structure, dependencies, and default parameters, so do not mix their commands or workspaces.

## Choose a Distribution

| Distribution | Platform | Hardware access | Entry |
| --- | --- | --- | --- |
| Humble | Ubuntu 22.04 | `diana_hardware` (`diana_*` packages) | [diana_ros2: Humble](humble/index.md) |
| Jazzy | Ubuntu 24.04 | `franka_hardware` (`franka_*` packages) | [diana_ros2: Jazzy](jazzy/index.md) |

For the differences between the two distributions and the shared prerequisites, see [Overview and Distribution Selection](overview.md).

## Reading Order

1. Complete the shared [Network Setup](../programming/network.md) first, so the control PC and the controller can communicate.
2. Read [Overview and Distribution Selection](overview.md), check the shared prerequisites, and choose a distribution.
3. Go to the chosen distribution, complete development setup and the quick start in turn, then look up interfaces, parameters, and usage package by package.

## Chapter Contents

:::{container} toctree-wrapper
- [ROS 2 Overview and Distribution Selection](overview.md)
- [diana_ros2: Humble](humble/index.md)
  - [Development Setup](humble/development.md)
  - [Quick Start](humble/quick_start.md)
  - [Packages](humble/packages/index.md)
    - [diana_bringup](humble/packages/diana_bringup.md)
    - [diana_description](humble/packages/diana_description.md)
    - [diana_example_controllers](humble/packages/diana_example_controllers.md)
    - [diana_moveit_config](humble/packages/diana_moveit_config.md)
    - [diana_gazebo_bringup](humble/packages/diana_gazebo_bringup.md)
    - [diana_hardware](humble/packages/diana_hardware.md)
    - [diana_msgs](humble/packages/diana_msgs.md)
    - [diana_robot_state_broadcaster](humble/packages/diana_robot_state_broadcaster.md)
    - [diana_semantic_components](humble/packages/diana_semantic_components.md)
- [diana_ros2: Jazzy](jazzy/index.md)
  - [Development Setup](jazzy/development.md)
  - [Quick Start](jazzy/quick_start.md)
:::

```{toctree}
:hidden:
:maxdepth: 2

overview
humble/index
jazzy/index
```

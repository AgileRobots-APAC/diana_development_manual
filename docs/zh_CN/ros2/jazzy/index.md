# diana_ros2: Jazzy

本节介绍 Diana 机械臂的 ROS 2 Jazzy 软件包集合 `diana_ros2`：基于 FCI（libfranka）实现，包含硬件接口、示例控制器、机器人状态广播器、MoveIt 2 配置、Gazebo 仿真，以及随源码提供的机器人描述 `diana_description`。软件包的组织方式沿用 franka_ros2 Jazzy 的结构，并针对 Diana 的机器人描述、MoveIt 配置和 Gazebo 启动文件做了适配。

```{important}
`diana_ros2` Jazzy 面向 **Ubuntu 24.04 与 ROS 2 Jazzy**。Jazzy 与 Humble 的源码、依赖和软件包构成不同，命令与工作空间不要混用，参见[概述与版本选择](../overview.md)。
```

```{warning}
连接实机前必须满足与 [FCI 章节](../../fci/overview.md)相同的前提：示教器处于协作模式、FCI 已开启、控制 PC 与控制柜网络连通（参见[网络配置](../../programming/network.md)）。涉及运动或力矩的操作还必须先完成[安全说明](../../reference/safety.md)中的现场检查。
```

```{note}
本章依据当前的 Jazzy 源码编写。部分软件包沿用上游的 `franka_*` 命名（例如 `franka_hardware`、`franka_msgs`），页面中保持与源码一致。
```

## 阅读顺序

1. 阅读[开发准备](development.md)，核对版本要求，完成 ROS 2、libfranka、源码与依赖、构建和实时权限配置。
2. 按[快速开始](quick_start.md)验证模型可视化、仿真和第一个示例控制器。
3. 各软件包的接口、参数和用法见[软件包](packages/index.md)，示例控制器见 [franka_example_controllers](packages/franka_example_controllers.md)。

```{toctree}
:hidden:
:maxdepth: 1

development
quick_start
packages/index
```

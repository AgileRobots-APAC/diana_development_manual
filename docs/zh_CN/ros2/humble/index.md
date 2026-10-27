# diana_ros2: Humble

本节介绍 Diana 机械臂的 ROS 2 Humble 软件包集合 `diana_ros2`：基于 `ros2_control` 的硬件接口、示例控制器、机器人状态广播器、MoveIt 2 配置以及 Gazebo 仿真。软件包的组织方式沿用 franka_ros2 的结构，并针对 Diana 的机器人描述、MoveIt 配置和 Gazebo 启动文件做了适配。

```{important}
`diana_ros2` Humble 面向 **Ubuntu 22.04 与 ROS 2 Humble**。Humble 与 Jazzy 的源码、依赖和软件包构成不同，命令与工作空间不要混用，参见[概述与版本选择](../overview.md)。
```

```{warning}
`diana_hardware` 通过 libfranka（FCI）连接机械臂。连接实机前必须满足与 [FCI 章节](../../fci/overview.md)相同的前提：示教器处于协作模式、FCI 已开启、控制 PC 与控制柜网络连通（参见[网络配置](../../programming/network.md)）。涉及运动或力矩的操作还必须先完成[安全说明](../../reference/safety.md)中的现场检查。
```

## 阅读顺序

1. 阅读[开发准备](development.md)，核对版本要求，完成 ROS 2、源码与依赖、构建和实时权限配置。
2. 按[快速开始](quick_start.md)验证模型可视化、仿真和第一个示例控制器。
3. 各软件包的接口、参数和用法见[软件包](packages/index.md)，示例控制器见 [diana_example_controllers](packages/diana_example_controllers.md)。

```{toctree}
:hidden:
:maxdepth: 1

development
quick_start
packages/index
```

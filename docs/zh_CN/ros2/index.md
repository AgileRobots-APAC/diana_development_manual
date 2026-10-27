# ROS 2 开发指南

本章介绍 Diana 机械臂的 ROS 2 环境准备、模型可视化、仿真与示例验证。ROS 2 与 FCI、C++ SDK 和 Python SDK 并列，作为独立的开发方式维护。

本章按 ROS 2 发行版分开组织：两套源码的包结构、依赖和默认参数不同，命令与工作空间不要混用。

## 选择发行版

| 发行版 | 平台 | 硬件接入 | 入口 |
| --- | --- | --- | --- |
| Humble | Ubuntu 22.04 | `diana_hardware`（`diana_*` 软件包） | [diana_ros2: Humble](humble/index.md) |
| Jazzy | Ubuntu 24.04 | `franka_hardware`（`franka_*` 软件包） | [diana_ros2: Jazzy](jazzy/index.md) |

两个发行版的差异与共用前提参见[概述与版本选择](overview.md)。

## 阅读顺序

1. 先完成公共[网络配置](../programming/network.md)，确保控制 PC 与控制柜通信正常。
2. 阅读[概述与版本选择](overview.md)，核对共用前提并选定发行版。
3. 进入所选发行版，依次完成开发准备和快速开始，再按软件包查阅接口、参数和用法。

## 章节目录

:::{container} toctree-wrapper
- [ROS 2 概述与版本选择](overview.md)
- [diana_ros2: Humble](humble/index.md)
  - [开发准备](humble/development.md)
  - [快速开始](humble/quick_start.md)
  - [软件包](humble/packages/index.md)
    - [启动与运行配置](humble/packages/diana_bringup.md)
    - [机器人描述](humble/packages/diana_description.md)
    - [示例控制器](humble/packages/diana_example_controllers.md)
    - [MoveIt 配置](humble/packages/diana_moveit_config.md)
    - [Gazebo 仿真](humble/packages/diana_gazebo_bringup.md)
    - [硬件接口](humble/packages/diana_hardware.md)
    - [消息、服务与动作](humble/packages/diana_msgs.md)
    - [机器人状态广播器](humble/packages/diana_robot_state_broadcaster.md)
    - [语义组件](humble/packages/diana_semantic_components.md)
- [diana_ros2: Jazzy](jazzy/index.md)
  - [开发准备](jazzy/development.md)
  - [快速开始](jazzy/quick_start.md)
:::

```{toctree}
:hidden:
:maxdepth: 2

overview
humble/index
jazzy/index
```

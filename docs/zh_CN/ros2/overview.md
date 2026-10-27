# ROS 2 概述与版本选择

选择发行版时，应同时核对 Ubuntu、ROS 2 和工作空间中的软件包版本。Humble 与 Jazzy 使用不同的源码和包结构：Humble 以 `diana_*` 软件包为主，Jazzy 的硬件、消息和控制器层改为 `franka_*` 软件包。

模型可视化、MoveIt 规划和假硬件演示都不能等同于实机控制验证。使用示例控制器或 MoveIt 前，应同时核对网络、控制器、安全接口和所选机型的配置。

## 发行版对比

| 项目 | Humble | Jazzy |
| --- | --- | --- |
| 平台 | Ubuntu 22.04 | Ubuntu 24.04 |
| 硬件接入、消息与状态广播 | `diana_hardware`、`diana_msgs`、`diana_robot_state_broadcaster` | `franka_hardware`、`franka_msgs`、`franka_robot_state_broadcaster` |
| 机器人描述 `diana_description` | 通过源码中的 `dependency.repos` 导入 | 随源码一起提供 |
| `diana.config.yaml` 默认命名空间 | `NS_1` | 空 |
| 文档入口 | [diana_ros2: Humble](humble/index.md) | [diana_ros2: Jazzy](jazzy/index.md) |

## 共用前提

两个发行版的实机控制都通过 libfranka（FCI）连接机械臂，需要满足相同的前提：

- 示教器处于协作模式，FCI 已开启，参见 [FCI 章节](../fci/overview.md)；
- 控制 PC 与控制柜网络连通，参见[网络配置](../programming/network.md)；
- 涉及运动或力矩的操作先完成[安全说明](../reference/safety.md)中的现场检查。

```{important}
Humble 与 Jazzy 的安装源、依赖版本和工作空间不要交叉使用。Diana 机器人的默认地址是 `192.168.10.75`，与[网络配置](../programming/network.md)所述控制柜 A 网口的默认地址一致。接入实机时，应在示教器上确认地址并显式传入 `robot_ip`。
```

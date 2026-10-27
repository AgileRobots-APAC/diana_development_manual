# 手册概述

本文档面向负责集成、调试或维护 Diana / Thor 机械臂应用的开发人员，说明控制 PC 侧的接入准备、通用控制概念、C++ 与 Python SDK 的工程集成、FCI 开发、ROS 2 集成以及共用参考资料。它帮助开发人员正确使用已发布的接口，不替代机械臂用户手册、安全资料或 SDK 自带的发布说明。

## 文档基线

| 项目 | 内容 |
|---|---|
| C++ SDK | 《工业版 API 手册（C/C++ 版）》V3.4.0，原手册函数序号 1-234 |
| Python SDK | 《思灵机器人工业版 API 手册（Python 版）》V3.4.0（2026-05-28）及 Python SDK 3.4.0 wrapper |
| FCI | Diana FCI Example 源码及 `libfranka 0.18.2` API Reference |
| ROS 2 | `diana_ros2` Humble 源码（元包 2.5.0）、Jazzy 源码（元包 3.5.3）及 `libfranka 0.18.2` |
| Example | C++ Example 1.0.0、Python Example 1.0.0，兼容 SDK 3.3.0 与 3.4.0 |
| 本手册版本 | 1.0.1（开发中） |
| 正式发布方式 | 不可变 Git tag |

## 内容来源说明

### C++ SDK 主内容源

《工业版 API 手册（C/C++ 版）》：

- 软件版本：V3.4.0
- 文档版本：V3.4.0
- 文件日期：2026-05-28
- 原手册函数序号：1-234
- 附件 A：DianaApi 接口错误码
- 附录 B：如何确保运动学逆解唯一
- 附录 C：对于实时指令的进一步说明

### Python SDK 主内容源

- 《思灵机器人工业版 API 手册（Python 版）》V3.4.0，文件日期 2026-05-28
- Python SDK 子模块中的 `lib/DianaApi.py` 和 `version` 文件
- `diana_examples_python` 示例源码及其配套文档

Python 接口原型以当前 SDK wrapper 为准，参数语义和取值范围同时参考匹配版本的 Python API 手册。Example 的调用流程和参数以示例仓库当前源码为准。

### FCI 主内容源

- Diana FCI Example 源码
- `libfranka 0.18.2` 官方 API Reference、类型定义和控制接口说明

FCI 章节只按 0.18.2 版本核对接口原型、重载、返回类型和异常，不跨版本套用其他 `libfranka` 文档。

### ROS 2 主内容源

- `diana_ros2` Humble 源码：各软件包的 `package.xml`、启动文件、配置文件、控制器与消息定义，以及 `diana_description` 软件包的 README
- `libfranka 0.18.2`，`diana_hardware` 依赖该版本

ROS 2 章节分别按 Humble 源码和当前的 Jazzy 源码核对启动参数、接口名称、服务与动作。

### 网页化重组

函数级 API Reference 由独立站点维护。本仓库保留生成错误码表所需的结构化数据，并围绕开发准备、快速开始、可运行 Example、接口调用流程和共用参考资料重新组织内容。

## 内容边界

- **接口概述**：手册适用范围、资料入口、网络准备、核心概念与版本更新。
- **编程指南**：按语言和平台（C++、Python、FCI、ROS 2）说明环境准备、SDK 或软件包接入、连接初始化与 Example。
- **参考**：单位、机器人规格、安全、错误码、故障排查和 I/O 等共用资料。
- **API Reference**：函数签名和逐函数参数语义由独立站点维护，当前手册不提供目录入口。

## 适用范围与资料入口

当前内容基于上述匹配版本资料整理，适用于 Diana 与 Thor 系列机械臂的控制器软件接入。具体型号、轴数、负载、工作半径和可选硬件能力以设备铭牌、控制器版本和对应产品资料为准。

| 需要解决的问题 | 优先查阅的资料 |
|---|---|
| 机械臂安装、接线、安全与现场操作 | 对应型号的用户手册和安全资料 |
| 控制 PC 与控制柜通信 | 编程指南的公共[网络配置](../programming/network.md) |
| SDK 的版本、头文件、wrapper、库文件与工程链接 | C++、Python、FCI 或 ROS 2 对应的概述、开发准备和快速开始 |
| 函数语义、参数、返回值和错误码 | 编程指南、参考资料及独立 API 索引站点 |
| 可运行工程 | C++、Python 或 FCI 对应的 Example 总览；ROS 2 的快速开始与示例控制器 |

```{important}
在连接真机、使能或下发运动指令前，现场必须完成风险评估、人员隔离、急停检查和负载/工具确认。本手册不替代机械臂用户手册或安全操作规程。
```

## 阅读建议

首次接入先阅读[核心概念](concepts.md)，再进入编程指南完成公共[网络配置](../programming/network.md)和 SDK 接入。

涉及单位、关节数量和姿态表达时，以[单位与通用约定](../reference/units.md)为准；涉及安全操作时，先阅读机械臂使用手册和本网站的[安全说明](../reference/safety.md)。

## 许可证与第三方声明

本仓库采用 Apache License 2.0，见仓库根目录的 `LICENSE` 与 `NOTICE`。

本手册的 FCI 与 ROS 2 章节引用并改编了下列第三方项目的内容，它们均采用 Apache License 2.0：

| 项目 | 版权声明 | 在本手册中的使用 |
|---|---|---|
| [libfranka](https://github.com/frankaemika/libfranka) | Copyright (c) 2023 Franka Robotics GmbH | FCI 章节中的示例说明和代码片段，改编自 libfranka 的示例，已针对 Diana 机械臂做了修改 |
| [franka_ros2](https://github.com/frankarobotics/franka_ros2) | Copyright (c) 2023 Franka Robotics GmbH | ROS 2 章节中的软件包说明和代码片段；`diana_ros2` 的源码沿用了 franka_ros2 的结构，源文件带有 Franka Robotics GmbH 的版权声明 |

改编部分的版权声明：Copyright (c) 2026 Agile Robots SE（修改：适配 Diana 机械臂）。上游项目的完整许可证与声明以其各自仓库为准。
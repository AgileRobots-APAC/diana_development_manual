# C++ SDK 概述

本章面向在控制 PC 上使用 Diana C/C++ SDK 开发应用的工程师。SDK 提供连接管理、运动控制、状态反馈、I/O、运动学、TCP/负载、路径与实时控制等接口；函数的完整参数语义以对应发布版本的 API Reference 和 SDK 头文件为准。

## 发布基线

当前手册内容基于工业版 API 手册 **V3.4.0**。排查问题或发布应用时，应同时记录以下版本，避免用一份文档去解释另一版二进制库的行为：

::::{div} release-baseline-chain
:::{div} release-baseline-step
<span class="release-baseline-index">01</span>
<div><strong>控制器软件版本</strong><small>机器人控制器实际运行的软件版本</small></div>
:::
:::{div} release-baseline-step
<span class="release-baseline-index">02</span>
<div><strong>C/C++ SDK 的 <code>version</code> 文件与头文件</strong><small>编译期接口与 SDK 包版本</small></div>
:::
:::{div} release-baseline-step
<span class="release-baseline-index">03</span>
<div><strong>Example 版本及其固定的 SDK 版本</strong><small>可复现的示例源码基线</small></div>
:::
:::{div} release-baseline-step
<span class="release-baseline-index">04</span>
<div><strong>本手册的发布 tag</strong><small>与上述组件对应的文档版本</small></div>
:::
::::

同名函数的参数、限制或可用性可能随 SDK 版本调整。实际集成始终以当前发布 SDK 的 `include/`、`lib/`、`version` 文件和发布说明为准。

当前 SDK 的 `version` 文件记录发布版本；运行时可使用 `getLibraryVersion()` 读取库版本。发布或排障时，建议保存这两项信息。

本手册核对时的 SDK `version` 文件内容为 `industry-v3.4.0.260605`，用于标识基线；实际集成仍以客户现场安装的 SDK、API 手册和发布说明为准。

仓库内附带的动态库为 Linux x86_64 版本。Linux aarch64 或 Windows 用户应使用随设备交付、且与控制 PC 系统和架构匹配的完整 SDK 包。

## 接口修订摘要

### SDK V3.4

- 新增 `addTcpPose`、`setTcpPoseByTcpName`、`deleteTcpPoseByTcpName`、`switchTcpPoseByTcpName`，按工具名称管理工具坐标系。

### SDK V3.3

- 新增 `moveLToPose_ex`。
- 新增 `powerOn`、`powerOnConfirmation`、`powerOff`。

## 平台状态

| 平台 | 当前状态 | 入口 |
|---|---|---|
| Linux x64 | 已提供环境、工程接入和 Example 指引 | [开发准备](development.md) |

## 多机械臂接入

可在同一应用中接入多台机械臂。每台机械臂都应有独立的 IP、连接生命周期、最新状态、错误上下文和业务状态机。调用支持目标 IP 的接口时，始终明确指定目标；不要依赖“当前机械臂”这类隐式全局状态。

多臂应用还应在应用层和现场层面完成工作空间隔离、互锁和统一急停策略。SDK 能否连接多台机械臂不等同于现场允许它们在同一空间并行运动。

## 本章内容

- **开发准备**：系统、编译器、CMake 和网络前提。
- **快速开始**：SDK 放置、CMake 链接、动态库路径与最小初始化程序。
- **Example 仓库**：可运行示例的用途、安全边界和后续逐例说明。
- **实时控制**：`servoJ`、`servoL`、`speedJ` 和 `speedL` 的实时调用约束。

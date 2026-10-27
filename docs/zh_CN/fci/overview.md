# 概述与版本要求

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

FCI（Franka Control Interface 风格的实时控制接口）面向需要高频、低延迟控制能力的应用。Diana FCI 以 `diana_libfranka_overlay` 为工程入口：它固定上游 `libfranka 0.18.2` 子模块，并通过机型补丁提供直连的 C++ 与 Python 示例，不依赖 ROS2。

## 适用范围

- 固定周期外部控制器。
- 关节位置、关节速度、笛卡尔位姿、笛卡尔速度控制。
- 基于模型项、雅可比和外力估计的力矩控制。
- 需要读取实时状态、动力学模型和控制反馈的高级应用。

## 发布基线

排查实时控制问题或发布应用时，应将以下组件作为一组记录。FCI 的 overlay 按机型分支应用补丁，因此应记录 overlay 的版本和实际使用的机型分支 tag（例如 `v1.0.0-libfranka0.18.2-diana3`），而不是套用其他机型的基线：

::::{div} release-baseline-chain
:::{div} release-baseline-step
<span class="release-baseline-index">01</span>
<div><strong>控制器软件版本与机型</strong><small>控制器能力及实际使用的 Diana 机型</small></div>
:::
:::{div} release-baseline-step
<span class="release-baseline-index">02</span>
<div><strong>Overlay 版本与机型分支 tag</strong><small>例如 <code>v1.0.0-libfranka0.18.2-diana3</code>、<code>v1.0.0-libfranka0.18.2-diana7</code> 或 <code>v1.0.0-libfranka0.18.2-diana7g2</code></small></div>
:::
:::{div} release-baseline-step
<span class="release-baseline-index">03</span>
<div><strong>固定的 <code>libfranka 0.18.2</code> 子模块、头文件与动态库</strong><small>不要混用其他 libfranka 版本</small></div>
:::
:::{div} release-baseline-step
<span class="release-baseline-index">04</span>
<div><strong>本手册的发布 tag</strong><small>与上述组件对应的文档版本</small></div>
:::
::::

## 版本与工程

| 项目 | 内容 |
|---|---|
| Overlay 仓库 | [diana_libfranka_overlay](https://github.com/AgileRobots-APAC/diana_libfranka_overlay.git) |
| Overlay 版本 | 1.0.0（对应软件版本 3.3.0），机型分支 tag：`v1.0.0-libfranka0.18.2-diana3`、`v1.0.0-libfranka0.18.2-diana7`、`v1.0.0-libfranka0.18.2-diana7g2` |
| FCI 接口及子模块 | `libfranka 0.18.2`（由 overlay 固定提交） |
| 支持机型 | Diana3、Diana7、Diana7G2；每个分支只包含一个机型补丁 |
| 上游源码 | [`libfranka 0.18.2`](https://github.com/frankarobotics/libfranka/tree/0.18.2) |
| API 文档 | [`libfranka 0.18.2` C++ API Reference](https://frankarobotics.github.io/libfranka/0.18.2/index.html) |
| 示例语言 | C++17 |
| 构建系统 | CMake |

## 参考依据

FCI 章节的接口原型按应用机型补丁后的 overlay 工作树、[`libfranka 0.18.2` 源码](https://github.com/frankarobotics/libfranka/tree/0.18.2)和官方 [`0.18.2` C++ API Reference](https://frankarobotics.github.io/libfranka/0.18.2/index.html) 核对，重点覆盖 `franka::Robot`、`franka::RobotState`、`franka::Model` 和 `control_types.h` 中的运动/力矩命令类型。
```{important}
不要混用其他 `libfranka` 版本的函数签名或行为说明。
```
## 与普通 C++ SDK 的关系

普通 C++ SDK 示例更适合离散运动指令、I/O、路径、工具坐标系和控制器功能调用。FCI 示例面向实时回调和更底层的控制输入，应用需要在控制周期内连续提供目标或力矩。

```{attention}
FCI 不应直接替代普通 SDK 的所有功能。只有在确实需要实时闭环、模型计算或力矩控制时，才建议使用 FCI。
```
## 使用前提

1. 控制 PC 与控制柜网络稳定，且实时控制链路已验证。
2. 机器人、工具、负载、碰撞阈值和工作空间已完成安全评估。
3. 应用回调计算可在控制周期内完成，不做阻塞 I/O。
4. 具备异常停止、错误恢复和现场急停策略。

```{note}
当前文档按 overlay 中选定机型的补丁结果和 `libfranka 0.18.2` API Reference 整理。最终接口签名、行为和可用性仍以随 Diana FCI 发布的 `libfranka` 头文件和控制器软件版本为准。
```

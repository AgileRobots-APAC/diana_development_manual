# Python SDK 概述

本章面向在控制 PC 上使用 `diana_sdk_python` 开发应用的工程师。SDK 通过 `DianaApi.py` 封装原生 Diana API 动态库，提供连接管理、状态反馈、运动控制、I/O、运动学、TCP/负载、路径与实时控制等接口；函数的完整参数语义以对应发布版本的 Python API 手册、`DianaApi.py` 和原生库为准。

## 发布基线

当前 Python SDK 子模块内容为 **3.3.0**，随示例仓库放在：

```text
diana_examples_python/
└── third_party/diana_sdk_python/
    ├── lib/
    │   └── DianaApi.py
    ├── doc/
    │   └── 思灵机器人工业版API手册(Python版)_V3.3.0_20260205.pdf
    └── version
```

排查问题或发布应用时，应同时记录以下版本，避免用一份文档去解释另一版 SDK 的行为：

::::{div} release-baseline-chain
:::{div} release-baseline-step
<span class="release-baseline-index">01</span>
<div><strong>控制器软件版本</strong><small>机器人控制器实际运行的软件版本</small></div>
:::
:::{div} release-baseline-step
<span class="release-baseline-index">02</span>
<div><strong>Python SDK 的 <code>version</code> 文件、<code>DianaApi.py</code> 与原生动态库</strong><small>Python 包装层与运行时库必须来自同一 SDK 包</small></div>
:::
:::{div} release-baseline-step
<span class="release-baseline-index">03</span>
<div><strong>Example 版本及其固定的 SDK 版本</strong><small>可复现的示例源码与依赖基线</small></div>
:::
:::{div} release-baseline-step
<span class="release-baseline-index">04</span>
<div><strong>本手册的发布 tag</strong><small>与上述组件对应的文档版本</small></div>
:::
::::

实际集成始终以客户现场安装的 SDK、API 手册和发布说明为准。

同名函数的参数、限制或可用性可能随 SDK 版本调整。实际集成始终以当前发布 SDK 的 `lib/DianaApi.py`、原生动态库、`version` 文件和发布说明为准。

当前 SDK 的 `version` 文件记录发布版本；运行时可使用 `getLibraryVersion()` 读取库版本。发布或排障时，建议保存这两项信息。

## 接口修订摘要

### SDK V3.3

- Python SDK 子模块随示例仓库提供 3.3.0 版本。
- `DianaApi.py` 中可见 `moveLToPose_ex`。
- `DianaApi.py` 中可见 `powerOn`、`powerOnConfirmation`、`powerOff`。

## 接口形态

Python 示例通过 `import DianaApi` 调用官方封装。封装内部使用 `ctypes` 加载同目录下的原生运行时库：

```text
libDianaApi.so    # Linux
DianaApi.dll      # Windows
```

示例仓库当前随 SDK 子模块提供 Linux x86_64 原生库。其他操作系统或 CPU 架构必须换用厂商提供的匹配 SDK 包；不要混用不同版本或不同平台架构的 `DianaApi.py` 与原生库。

## 平台状态

| 平台 | 当前状态 | 入口 |
|---|---|---|
| Linux x64 | 示例仓库提供 Python 脚本和 SDK 子模块；全部 Example 已完成真机验证，逐例页面附实际运行输出 | [开发准备](development.md) |

## 多机械臂接入

Python SDK 的多数接口都提供 `ipAddress` 参数。多机械臂应用中，每台机械臂都应有独立的 IP、连接生命周期、状态缓存、错误上下文和业务状态机。调用支持目标 IP 的接口时，始终明确传入目标 IP；不要依赖空 IP 或“当前机械臂”这类隐式全局状态。

多臂应用还应在应用层完成工作空间隔离、互锁和统一急停策略。SDK 能否连接多台机械臂不等同于现场允许它们在同一空间并行运动。

## 本章内容

- **开发准备**：系统、Python、SDK 路径、动态库和网络前提。
- **快速开始**：SDK 放置、环境变量、最小初始化程序与连接生命周期。
- **Example 仓库**：可运行示例的用途、安全边界和逐例说明。
- **执行效果**：每个 Example 页面附真机实际运行输出，便于对照。

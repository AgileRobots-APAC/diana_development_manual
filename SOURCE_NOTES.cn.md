# 内容来源说明

[English](SOURCE_NOTES.md) | [中文](SOURCE_NOTES.cn.md)

本文记录 Diana 开发者文档采用的资料基线和证据边界。

## C++ SDK 主内容源

《工业版 API 手册（C/C++ 版）》：

- 软件版本：V3.3.0
- 文档版本：V3.3.0
- 文件日期：2026-02-05
- 原手册函数序号：1-230
- 附件 A：DianaApi 接口错误码
- 附录 B：如何确保运动学逆解唯一
- 附录 C：对于实时指令的进一步说明

C++ Example 指南还会对照匹配版本的 SDK 头文件、发布信息和当前 `diana-api-examples-cpp` 源码。

## Python SDK 主内容源

- 《思灵机器人工业版 API 手册（Python 版）》V3.3.0，文件日期 2026-02-05
- Python SDK 版本 `industry-v3.3.0.260211`
- Python SDK 子模块中的 `lib/DianaApi.py` 和 `version` 文件
- 当前 `diana-api-examples-python` 源码及其配套文档

Python 函数原型以匹配版本的 SDK wrapper 为准。参数含义、单位、范围和返回值同时对照 Python API 手册；Example 的调用流程、常量和源码片段以当前示例仓库为准。

## FCI 主内容源

- 当前 Diana FCI Example 源码
- `libfranka 0.18.2` 官方 API Reference
- `libfranka 0.18.2` 类型定义和控制接口说明

FCI 接口原型、重载、控制类型、返回值和异常只按 0.18.2 版本核对，不默认套用其他 `libfranka` 版本的资料。

## 网页化重组

函数级 API Reference 由独立站点维护。本仓库保留生成错误码表所需的结构化数据，并将来源资料重组为：

- 共用概念、单位、安全边界、I/O 和故障排查
- C++、Python 和 FCI 的开发准备与快速开始
- 可运行 Example 总览和逐例说明
- 每个 Example 实际使用接口的原型、返回值和调用案例
- 错误码表及部分手册附录的网页版本

`data/api_v3_3_0.json` 是从 C/C++ V3.3.0 手册结构化得到的初始数据，目前只用于生成中英文错误码表。

## 不自行推断的内容

当匹配版本的手册、SDK 发布包、发布说明和 Example 仓库没有完整描述时，本仓库不自行推断：

- 机器人机械尺寸、额定负载和工作半径
- 控制箱端子、网络口和完整电气接线
- 未发布 SDK 版本的接口行为或兼容性
- 未经测试的操作系统或 Python 版本兼容性
- 未经部署现场验证的实时性能或安全性能
- 尚未实际采集的真机运行输出

这些内容应以对应产品用户手册、安全资料、SDK 发布说明、设备配置和现场验证结果为准。

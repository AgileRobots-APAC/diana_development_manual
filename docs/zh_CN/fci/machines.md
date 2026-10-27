# 选择机械臂型号

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

本指南以 `diana_libfranka_overlay` 为 FCI 示例和机型适配的唯一工程来源。该仓库固定包含上游 `libfranka 0.18.2` 子模块；选择机械臂型号不是运行时参数，而是选择 overlay 分支并将该分支的补丁应用到子模块。

请只选择与现场机械臂一致的一个型号。不要在同一个 `libfranka` 工作树中混用多个补丁。

| 机械臂 | Overlay 分支 | 补丁 | 应用后的 C++ 示例目录 |
|---|---|---|---|
| [Diana3](machines/diana3.md) | `diana3` | `patches/diana3.patch` | `libfranka/examples/diana3/` |
| [Diana7](machines/diana7.md) | `diana7` | `patches/diana7.patch` | `libfranka/examples/diana7/` |
| [Diana7G2](machines/diana7g2.md) | `diana7g2` | `patches/diana7g2.patch` | `libfranka/examples/diana7G2/` |

三个补丁还分别生成 `libfranka/pylibfranka/examples/<型号>/` 、`libfranka/examples/<型号>/`和对应的 `rate_limiting_<型号>.h`。本章 C++ 示例页以 `libfranka/examples/<型号>/` 为准，Python 示例页以 `libfranka/pylibfranka/examples/<型号>/` 为准。

```{warning}
补丁只能应用到干净且位于 overlay 固定提交的 `libfranka` 子模块。已经应用某型号补丁后，要切换型号必须先恢复该子模块；不要在已打补丁的树上继续应用另一个补丁。
```

```{toctree}
:hidden:

machines/diana3
machines/diana7
machines/diana7g2
```

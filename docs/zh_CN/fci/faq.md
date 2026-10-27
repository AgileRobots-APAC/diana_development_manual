# FAQ：常见问题与解决方案

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

本页用于沉淀 FCI 使用过程中的常见问题。FAQ 按主题分组，每条问题默认折叠，便于快速浏览。

## 仓库与补丁

::::{dropdown} Q：拉取 overlay 仓库后，为什么找不到对应机型的 examples？
:class-container: api-example-block

**现象**

- `libfranka/examples/<model>/` 或 `libfranka/pylibfranka/examples/<model>/` 不存在。
- CMake 或运行命令提示找不到对应示例。

**可能原因**

- 只拉取了仓库，但还没有初始化子模块。
- 还没有应用当前机械臂机型对应的补丁。

**处理步骤**

1. 确认已完整拉取 overlay 仓库和子模块。
2. 按当前机械臂型号应用对应 patch。
3. 重新查看 `libfranka/examples/` 与 `libfranka/pylibfranka/examples/` 下是否出现 `diana3`、`diana7` 或 `diana7G2` 目录。

**安全提醒**

- 补丁和机型必须对应。不要用非当前机型的示例目录直接连接真机。

::::

::::{dropdown} Q：补丁已经应用，但文档中的 example 路径和本地路径对不上怎么办？
:class-container: api-example-block

**现象**

- 文档写的是 `libfranka/examples/<model>/xxx.cpp`，本地目录名或文件名不一致。
- 示例总览里有的条目，本地没有对应源文件。

**可能原因**

- overlay 仓库版本与文档版本不一致。
- 使用了错误机型补丁。
- 夹爪相关示例未纳入当前 FCI 支持范围。

**处理步骤**

1. 确认当前文档对应的 overlay 仓库版本。
2. 确认 `<model>` 只使用当前支持的 `diana3`、`diana7` 或 `diana7G2`。
3. 以当前补丁后的 example 目录为准，更新文档示例清单。

**安全提醒**

- 示例清单只代表文档支持范围，不代表所有 libfranka 官方示例都适用于当前机器人。

::::

## 编译与依赖

::::{dropdown} Q：创建 Python 虚拟环境时报 `ensurepip is not available` 怎么办？
:class-container: api-example-block

**现象**

```text
The virtual environment was not created successfully because ensurepip is not available.
```

**可能原因**

- Debian/Ubuntu 系统缺少 `python3-venv` 包。

**处理步骤**

1. 安装当前 Python 版本对应的 `python3-venv`。
2. 删除未创建完整的 `.venv` 目录。
3. 重新创建虚拟环境并安装依赖。

**安全提醒**

- 只删除当前文档仓库下未创建完整的 `.venv`，不要清理系统 Python 目录。

::::

## 实时网络与系统

::::{dropdown} Q：通信测试成功率不稳定，应该先看哪里？
:class-container: api-example-block

**现象**

- `communication_test` 输出控制通信成功率偏低。
- 丢失周期数量上升。
- 控制过程中偶发网络或实时性相关异常。

**可能原因**

- 应用机没有完成实时系统配置。
- 网卡、中断亲和性、CPU 调度或省电策略影响控制周期。
- 网络链路存在交换机、非直连、网线或 IP 配置问题。

**处理步骤**

1. 先确认实时内核、用户权限和调度策略配置。
2. 确认应用机与控制器网络链路稳定，优先使用直连或确定性网络环境。
3. 运行只读示例确认状态读取稳定。
4. 在完成安全确认后，再运行 `communication_test`。

**安全提醒**

- `communication_test` 不是只读示例，会先运动到初始姿态并进入零力矩控制会话。

::::

::::{dropdown} Q：能不能用 `echo_robot_state` 代替 `communication_test` 判断实时控制质量？
:class-container: api-example-block

**现象**

- `echo_robot_state` 能正常打印状态，但控制示例仍然报通信或实时相关错误。

**可能原因**

- `echo_robot_state` 只读状态，不发送运动或力矩命令。
- 只读链路正常不等于 1 kHz 控制读写链路满足要求。

**处理步骤**

1. 用 `echo_robot_state` 确认基础连接和状态读取。
2. 用实时网络配置检查系统实时性。
3. 在安全条件满足后，用 `communication_test` 评估控制读写通信质量。

**安全提醒**

- 不要因为只读示例正常，就直接运行运动或力矩控制示例。

::::

## 示例运行与安全

::::{dropdown} Q：哪些 FCI examples 是只读的？
:class-container: api-example-block

**现象**

- 需要先找不发送运动或力矩命令的示例验证连接。

**可能原因**

- FCI 示例既包含状态读取，也包含运动生成、外部控制循环和力矩控制。

**处理步骤**

1. 优先使用 `echo_robot_state` 做连续状态读取。
2. 使用 `print_joint_poses` 做一次状态读取和模型位姿计算。
3. 其他 C++ / Python FCI 示例默认按运动或力矩示例处理。

**安全提醒**

- 除只读示例外，运行前必须完成急停、净空、负载、碰撞阈值和退出路径确认。

::::

::::{dropdown} Q：Python FCI 示例和普通 Diana Python SDK 示例有什么区别？
:class-container: api-example-block

**现象**

- 文档里同时有普通 Python SDK 示例和 Python FCI 示例，接口名不一致。

**可能原因**

- Python FCI 示例使用 `pylibfranka`，路径位于 `libfranka/pylibfranka/examples/<model>/`。
- 普通 Diana Python SDK 示例使用的是 Diana SDK Python 封装，属于另一套接口。

**处理步骤**

1. 看当前章节标题：FCI 章节中的 Python 示例使用 `pylibfranka`。
2. 按 FCI Python 示例总览中的路径和接口运行。
3. 不要把普通 Python SDK 的接口名直接套到 FCI 示例中。

**安全提醒**

- 无论 C++ FCI 还是 Python FCI，只要进入运动或力矩控制，都需要按真机控制示例处理。

::::

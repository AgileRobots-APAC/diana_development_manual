# 快速开始（Linux）

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

目标是在 Linux 上为指定机型准备 overlay、应用补丁、构建 `libfranka` 示例，并先执行一次只读状态读取。

## 1. 选择机械臂并应用补丁

先在[机型选择](machines.md)中选择现场机械臂。下面以 Diana3 为例；Diana7 和 Diana7G2 必须替换为各自的分支名、补丁名和输出目录。

```bash
git clone --recurse-submodules https://github.com/AgileRobots-APAC/diana_libfranka_overlay.git
cd diana_libfranka_overlay
git switch diana3
git submodule update --init --recursive
git -C libfranka apply --check ../patches/diana3.patch
git -C libfranka apply ../patches/diana3.patch
```

补丁把上游示例置于 `libfranka/examples/diana3/`，并选择 Diana3 对应的限速实现。不要对同一工作树重复应用补丁。

## 2. 配置 CMake 并构建示例

先按[开发准备](development.md)完成依赖、控制器 FCI 状态和网络配置。主机侧在 overlay 根目录构建：

```bash
cmake -S libfranka -B build/libfranka -DBUILD_EXAMPLES=ON
cmake --build build/libfranka
```

上面的 Diana3 可执行文件在 `build/libfranka/examples/diana3/`。如果在容器中从 `libfranka/` 目录构建，输出目录为 `build/examples/diana3/`。那相应的编译指令就需要改为：
```bash
cmake -S . -B build -DBUILD_EXAMPLES=ON
cmake --build build/
```

## 3. 最小只读验证

先运行不发送运动目标的状态读取。将机器人 IP 替换为现场实际值：

```bash
./build/libfranka/examples/diana3/echo_robot_state 192.168.10.75
```

`communication_test` 不是只读检查：它会先移动到初始姿态，再开启力矩控制会话并发送零力矩。因此只能在现场安全条件已满足后运行。不同机型请使用其自身输出目录。

## 4. 连接生命周期

```text
确认机器人进入 FCI 运行条件 → 创建 Robot 连接
    → 读取状态或进入控制回调 → 正常结束控制循环 → 释放连接资源
```
控制回调失败通常与超时、目标不连续、限位、网络抖动或控制模式不匹配有关。进入实时控制前，应完成网络和系统实时性配置。

```{warning}
编译成功或只读示例成功不代表现场可以运动。运行任何会发送位置、速度或力矩命令的上游示例前，必须确认人员净空、夹具、工件、线缆、速度、力矩、急停和退出路径。
```

## 5. Python 接口编译（可选）

进入 `libfranka` 根目录：

```bash
cd libfranka
```

安装：

```bash
pip3 install .
```

```{attention}
Python 编译默认不编译 C++ 示例；编译成功后可以通过 `python3` 运行程序。
```

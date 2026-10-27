# Diana3 FCI 环境

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

选择 `diana3` 分支，并将 Diana3 补丁应用到上游子模块：

```bash
git clone --recurse-submodules https://github.com/AgileRobots-APAC/diana_libfranka_overlay.git
cd diana_libfranka_overlay
git switch diana3
git submodule update --init --recursive
git -C libfranka apply --check ../patches/diana3.patch
git -C libfranka apply ../patches/diana3.patch
```

然后按[开发准备](../development.md)配置环境，并构建：

```bash
cmake -S libfranka -B build/libfranka -DBUILD_EXAMPLES=ON
cmake --build build/libfranka
```

主机侧构建后的 C++ 示例位于 `build/libfranka/examples/diana3/`；容器内从 `libfranka/` 执行 `cmake -S . -B build -DBUILD_EXAMPLES=ON` 时，对应目录为 `build/examples/diana3/`。

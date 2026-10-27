# 开发准备

开始 C++ 开发前，请确认控制 PC 已按[网络配置](../programming/network.md)与控制柜连通，并已经完成现场安全准备。

```{important}
使用 C++ API 编程时，需要确保机器人的 <span class="power-on">FCI</span> 模式已经关闭（字变为**红色**）。机器人处于 <span class="power-on">FCI</span> 模式时，无法通过 API 连接和控制机械臂。
```

```{important}
运行代码前，需要将示教器左上角的档位切换至 <span class="power-on">自动</span> 模式或 <span class="power-on">协作</span> 模式。
```

```{important}
运行代码前，请在启动界面点击 <span class="power-on">上电</span> 按钮，确认机械臂处于上电状态。
```

## 开发环境

本章节介绍 Diana 机器人应用程序在 Ubuntu x86_64 系统下的基础开发环境配置。下面讲解 Ubuntu x86_64 系统下的开发流程。

```{tip}
推荐使用 <span class="power-on">Ubuntu x86_64</span> 系统做机器人控制的开发。
```

## 已验证的 Linux 环境

| 系统 | 状态 | 已验证编译器 | 已验证 CMake |
|---|---|---|---|
| Ubuntu 18.04 x64 | 支持 | GCC 7.5 | 3.10 |
| Ubuntu 20.04 x64 | 支持 | GCC 7.5、GCC 9.4 | 3.16 |
| Ubuntu 22.04 x64 | 支持 | GCC 11.4 | 3.22 |

## 系统推荐

推荐使用以下操作系统：

| 项目      | 推荐配置             |
| ------- | ---------------- |
| 操作系统    | Ubuntu 20.04 LTS |
| 系统架构    | x86_64           |
| C++ 编译器 | GCC / G++        |
| 构建系统    | CMake            |
| 构建工具    | GNU Make         |

```{attention}
在进行实时控制时，应优先保证控制 PC 的系统实时性。如有必要，请根据控制 PC 所使用的 Ubuntu 系统版本安装对应的实时内核。
```
## 安装基础开发工具

打开终端并更新软件包索引：

```bash
sudo apt update
```

安装 Diana 开发所需的基础工具：

```bash
sudo apt install -y \
    ca-certificates \
    git \
    cmake \
    g++ \
    make
```

安装完成后，可以通过以下命令检查开发环境：

```bash
g++ --version
cmake --version
make --version
```

如果以上命令均能够正常输出版本信息，则基础开发环境安装完成。

## 编译环境说明

Diana 示例程序使用 C++ 进行开发，并通过 CMake 管理工程构建过程。

典型的工程编译流程如下：

```bash
mkdir -p build
cd build

cmake ..
make -j$(nproc)
```

编译完成后，可在工程对应的构建目录中找到生成的可执行程序。

```{note}
如果 Ubuntu 官方软件源访问速度较慢，可以根据所在网络环境配置合适的软件镜像源。例如，在中国大陆环境中可以使用阿里云、清华大学等 Ubuntu 镜像源。软件源配置仅用于提高软件包下载速度，不影响 Diana 开发接口本身的使用。
```

## 实时控制环境

普通运动控制和状态读取通常可以直接在标准 Ubuntu 系统中运行。

对于周期性实时控制、高频状态交互或对控制周期抖动较为敏感的应用，建议对控制 PC 的实时性能进行优化。

根据实际应用需求，可以考虑：

* 安装与当前 Ubuntu 版本对应的实时内核；
* 为实时控制线程配置合适的调度优先级；
* 避免在实时控制过程中运行占用大量 CPU 或 I/O 资源的程序；
* 使用稳定的有线网络连接机器人控制器；
* 对控制周期和通信延迟进行实际测试。

```{hint}
实时控制程序运行前，应确认控制 PC、网络以及机器人控制系统均满足相应的实时控制要求。
```

## 所需工具

- Git，用于获取 Example 仓库及其 SDK 子模块。
- CMake，用于配置 C++ 工程。
- 与所选 Ubuntu 版本匹配的 C++ 编译器和构建工具。
- 为控制柜 A 网口配置了静态 IP 的有线网卡。

## 其他系统版本

随机械臂交付的 U 盘除 Linux x86_64 版 SDK 外，还包含 Linux aarch64 版和 Windows 版 C++ SDK。请始终使用与控制 PC 操作系统和 CPU 架构一致的 SDK；不要将 x86_64、aarch64 和 Windows 的头文件、库文件或运行时文件混用。

### Linux aarch64

Linux aarch64 版的工程组织、CMake 配置、SDK 初始化和 API 用法与上文的 Linux x86_64 路径一致。将工程中的 SDK 目录替换为 U 盘提供的 aarch64 版本，并在 aarch64 Linux 主机上使用本机编译器构建即可。

- 确认控制 PC 是 aarch64 架构，而不是 x86_64 系统上的交叉编译环境。
- `include/`、`lib/` 和 `version` 必须来自同一个 aarch64 SDK 包。
- 运行前按[快速开始](quick_start.md)配置动态库搜索路径，确保加载的是 aarch64 的 `.so` 文件。
- 未在本页“已验证的 Linux 环境”中列出的系统、编译器或内核组合，需要在目标设备上自行完成构建和真机验证。

### Windows

Windows 版 SDK 同样随 U 盘提供，但需要在 Windows 工程中手动完成头文件、链接库和运行时 DLL 的配置。建议先创建一个最小控制台程序，确认 SDK 能加载、网络能连接，再接入业务逻辑或运动控制。

1. 从 U 盘选择与 Windows 主机架构一致的 SDK 包，并保持 `include`、`lib` 和 DLL 来自同一发布版本。
2. 将 SDK 的头文件目录加入工程的包含目录；将 `lib` 目录加入链接器库目录，并链接 SDK 提供的导入库。
3. 将 SDK 的 DLL 及其依赖 DLL 复制到生成的 `.exe` 同目录，或将 DLL 所在目录加入运行时 `PATH`。仅能在编译期找到 `.lib` 不能保证程序能够启动。
4. 确认工程的目标架构、编译器运行库和 Debug/Release 配置与 SDK 包兼容；出现“找不到 DLL”或架构不匹配时，先检查实际加载的 DLL 路径和文件架构。
5. 完成编译后，先执行不触发运动的连接或状态读取程序，并按公共[网络配置](../programming/network.md)确认控制 PC 与控制柜连通。

```{warning}
Windows SDK 的具体库名、依赖 DLL 和工程模板以随该机械臂交付的 SDK 内容和发布说明为准。不要将 Linux 的 `.so` 文件用于 Windows 工程，也不要将 Windows DLL 复制到 Linux 环境。
```

# 开发准备

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

FCI 开发需要准备：

- C++ 开发环境；
- Diana 修改版 `libfranka 0.18.2`；
- Pinocchio 3.9.0；
- 控制 PC 与机器人之间的网络环境。

建议先完成机器人连接测试，再运行运动、力矩或阻抗控制程序。

```{important}
运行任何 FCI 程序前，请在示教器上确认：

- **FCI 模式已开启**（状态显示为绿色）；FCI 未开启时，无法通过 FCI 接口连接和控制机械臂。
- 示教器保持在**协作模式**，运行运动程序期间不要切换。
- 已在启动界面点击 **上电** 按钮，机械臂处于上电状态。
```

## 开发环境

| 项目     | 要求                                 |
| ------ | ---------------------------------- |
| 操作系统   | Ubuntu 20.04 / Ubuntu 22.04 x86_64 |
| C++ 标准 | C++17                              |
| 编译工具   | CMake、Ninja、GCC                    |
| FCI 库  | Diana 修改版 `libfranka 0.18.2`       |
| 运动学库   | Pinocchio 3.9.0                    |
| 依赖库    | Eigen3、Boost、Poco、Threads          |
| 网络     | 控制 PC 与机器人同网段，建议使用有线连接             |

```{attention}
注意：不要混用其他版本的 `libfranka` 头文件和动态库。本文档所有接口均基于 `libfranka 0.18.2`。
```

## 环境准备

### 1. 获取源码

下载工程：

```bash
git clone --recurse-submodules https://github.com/AgileRobots-APAC/diana_libfranka_overlay.git

cd diana_libfranka_overlay
```

工程结构：

```text
diana_libfranka_overlay/

├── libfranka/
│   ├── include/
│   ├── src/
│   ├── examples/
│   └── pylibfranka/
│
├── patches/
├── LICENSE
├── NOTICE
├── README.md
├── README.cn.md
└── VERSION
```

### 2. 应用 Diana 修改补丁

选择对应机械臂版本：

```bash
git switch <arm-version>

git submodule update --init --recursive
```

检查补丁：

```bash
git -C libfranka apply --check ../patches/<arm-version>.patch
```

应用补丁：

```bash
git -C libfranka apply ../patches/<arm-version>.patch
```

每个 overlay 分支只包含对应机型的一个补丁。需要复现某个发布基线时，请检出 tag 而不是分支，例如 `git switch --detach v1.0.0-libfranka0.18.2-diana3`；上游 `libfranka` 的版本记录在仓库根目录的 `VERSION` 文件中（`0.18.2`）。

切换机型时，先丢弃子模块中已应用的改动，再切换到另一个 overlay 分支，更新子模块并应用该分支的补丁：

```bash
git -C libfranka reset --hard "$(cat VERSION)"
git -C libfranka clean -fd
git switch <arm-version>
git submodule update --init --recursive
git -C libfranka apply --check ../patches/<arm-version>.patch
git -C libfranka apply ../patches/<arm-version>.patch
```

```{warning}
`reset` 和 `clean` 会删除子模块中的本地修改和未跟踪文件，只能在可丢弃或确认干净的子模块中执行。
```

## 3. 开发环境配置

FCI 开发环境有两种方式：

* VS Code Dev Container；
* Ubuntu 原生环境。

### 3.1 使用 VS Code Dev Container

适用于安装 Docker 的开发主机。

Dev Container 会自动完成：

* 安装编译依赖；
* 编译 Pinocchio 3.9.0；
* 编译 Diana 修改版 `libfranka 0.18.2`；
* 配置 FCI 示例运行环境。

#### 3.1.1 打开开发容器

进入工程：

```bash
cd diana_libfranka_overlay
```

打开 libfranka：

```bash
code libfranka
```

在 VS Code 中执行：

```text
Dev Containers: Reopen in Container
```

```{note}
首次启动需要构建开发镜像。由于需要编译 Pinocchio 和 libfranka，首次启动时间可能较长。
```

#### 3.1.2 容器环境说明

Dev Container 默认配置用于保证 FCI 通信和硬件调试。

```{attention}
机器人网络配置仍需要在宿主机完成
```
```text
控制 PC 网卡：
192.168.10.xxx(与机器人同一网段)
机器人控制器：
192.168.10.75(需确定)
```

#### 3.1.3 编译示例程序

进入源码：

```bash
cd /workspaces
```

生成工程：

```bash
cmake -S . \
      -B build \
      -DBUILD_EXAMPLES=ON
```

编译：

```bash
cmake --build build
```

编译完成：

```text
build/examples/diana3/
```

目录中包含 Diana FCI 示例程序。

#### 3.1.4 运行测试

例如：

```bash
./build/examples/diana3/echo_robot_state <robot-ip>
```

其中：

```text
<robot-ip>
```

为机器人控制器 IP 地址。

#### 3.1.5 修改源码后重新编译

修改 libfranka 或示例代码后：

```bash
cd /workspaces

cmake --build build
```

无需重新创建容器。

如果修改 CMake 配置：

重新生成：

```bash
cmake -S . \
      -B build \
      -DBUILD_EXAMPLES=ON

cmake --build build
```
### 3.2 使用 Ubuntu 原生环境

适用于：

- 无法使用 Docker 的控制 PC；
- 机器人现场控制电脑；
- 需要直接运行 FCI 程序的环境。

该方式需要手动安装：

- 编译依赖；
- Pinocchio 3.9.0；
- Diana 修改版 `libfranka 0.18.2`。

#### 3.2.1 检查系统环境

查看 Ubuntu 版本：

```bash
lsb_release -a
```

查看系统架构：

```bash
uname -m
```

推荐环境：

```text
Ubuntu 20.04 / Ubuntu 22.04

x86_64
```

#### 3.2.2 安装系统依赖

执行：

```bash
sudo apt update

sudo apt install -y \
build-essential \
cmake \
git \
ninja-build \
pkg-config \
python3-dev \
python3-pip \
python3-numpy \
libboost-filesystem-dev \
libboost-system-dev \
libboost-serialization-dev \
libconsole-bridge-dev \
libeigen3-dev \
libfmt-dev \
libpoco-dev \
libtinyxml2-dev \
liburdfdom-dev
```

检查工具：

```bash
cmake --version

g++ --version

ninja --version
```

#### 3.2.3 编译并安装 Pinocchio 3.9.0

进入临时目录：

```bash
cd /tmp
```

下载源码：

```bash
git clone --recursive \
--branch v3.9.0 \
https://github.com/stack-of-tasks/pinocchio.git
```

进入源码：

```bash
cd /tmp/pinocchio
```

初始化子模块：

```bash
git submodule update --init --recursive
```

配置：

```bash
cmake -S /tmp/pinocchio \
      -B /tmp/pinocchio/build \
      -GNinja \
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_INSTALL_PREFIX=/opt/openrobots \
      -DCMAKE_INSTALL_LIBDIR=lib \
      -DBUILD_TESTING=OFF \
      -DBUILD_PYTHON_INTERFACE=OFF \
      -DBUILD_WITH_COLLISION_SUPPORT=OFF \
      -DBUILD_WITH_CASADI_SUPPORT=OFF \
      -DINSTALL_DOCUMENTATION=OFF
```

编译：

```bash
cmake --build /tmp/pinocchio/build \
      -- -j$(getconf _NPROCESSORS_ONLN)
```

安装：

```bash
sudo cmake --install /tmp/pinocchio/build
```

配置动态库：

```bash
sudo sh -c 'echo "/opt/openrobots/lib" > /etc/ld.so.conf.d/openrobots.conf'

sudo ldconfig
```

检查：

```bash
ldconfig -p | grep pinocchio
```

#### 3.2.4 编译 Diana 修改版 libfranka 0.18.2

进入源码目录：

```bash
cd /path/to/diana_libfranka_overlay/libfranka
```

确认目录结构：

```text
libfranka/

├── CMakeLists.txt
├── include/
├── src/
├── examples/
└── pylibfranka/
```

##### 配置编译

```bash
cmake -S . \
      -B build \
      -GNinja \
      -DCMAKE_BUILD_TYPE=Release \
      -DBUILD_TESTS=OFF \
      -DBUILD_EXAMPLES=ON \
      -DGENERATE_PYLIBFRANKA=ON \
      -DCMAKE_INSTALL_PREFIX=/usr/local \
      -DCMAKE_PREFIX_PATH=/opt/openrobots
```

参数说明：

| 参数                     | 说明                |
| ---------------------- | ----------------- |
| `BUILD_TESTS`          | 关闭 libfranka 内部测试 |
| `BUILD_EXAMPLES`       | 编译 Diana FCI 示例程序 |
| `GENERATE_PYLIBFRANKA` | 生成 Python 接口      |
| `CMAKE_PREFIX_PATH`    | 指定 Pinocchio 安装位置 |

##### 编译

```bash
cmake --build build \
      -- -j$(getconf _NPROCESSORS_ONLN)
```

##### 安装

```bash
sudo cmake --install build

sudo ldconfig
```

#### 3.2.5 编译 Diana FCI 示例程序

进入：

```bash
cd /path/to/diana_libfranka_overlay/libfranka
```

编译：

```bash
cmake --build build
```

查看生成程序：

```bash
ls build/examples/diana3
```

#### 3.2.6 运行 FCI 连接测试

运行：
```bash
./build/examples/diana3/echo_robot_state \
<robot-ip>
```

程序会连续输出机器人状态，然后正常退出；不发送运动或力矩命令。

不同机型请替换为对应的示例目录。

#### 3.2.7 Python 接口安装（可选）

进入：

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

## 连接前检查

运行程序前确认：

1. 控制柜已开启 FCI；
2. 控制 PC 与机器人同网段；
3. 网络连接正常；
4. 机器人已上电；
5. 示教器处于协作模式。

## 安全提示

```{warning}

编译成功或连接测试通过，并不代表可以直接执行运动控制。

所有运动、力矩、阻抗控制程序运行前，需要确认现场安全环境，并准备急停。

```

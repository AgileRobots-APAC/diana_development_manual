# 开发准备

开始 Python 开发前，请确认控制 PC 已按[网络配置](../programming/network.md)与控制柜连通，并已经完成现场安全准备。

```{important}
在使用 Python 版本的 API 编程时，需要确保机器人的 <span class="power-on">FCI</span> 模式已经关闭（字变为**红色**）。机器人工作在 <span class="power-on">FCI</span> 模式下时，无法通过常规 API 连接控制机械臂。
```

```{important}
运行代码时需要将示教器左上角的档位切换至 <span class="power-on">自动</span> 模式或 <span class="power-on">协作</span> 模式。
```

```{important}
运行代码前请在启动界面点击 <span class="power-on">上电</span> 按钮，保证机械臂处于上电状态。
```

## 开发环境

推荐使用 Ubuntu x86_64 系统做机器人控制开发。Python 示例不需要 CMake 编译，但需要 Python 解释器能够导入 `DianaApi.py`，并且系统动态链接器能够加载匹配版本的原生 SDK 库。

```{tip}
推荐使用 <span class="power-on">Ubuntu x86_64</span> 系统做机器人控制的开发。
```

## 已验证的 Linux 环境

| 系统 | 状态 | 已验证 Python |
|---|---|---|
| Ubuntu 20.04 x64 | 已验证 | Python 3 |
| Ubuntu 22.04 x64 | 已验证 | Python 3 |

以上验证覆盖 SDK 导入、连接与真机测试。未列出的发行版、Python 版本或 SDK 原生库组合，应由项目自行完成验证。

| 项目 | 推荐配置 |
|---|---|
| 操作系统 | Ubuntu 20.04 LTS / Ubuntu 22.04 LTS |
| 系统架构 | x86_64 |
| Python | Python 3 |
| SDK wrapper | `third_party/diana_sdk_python/lib/DianaApi.py` |
| 原生库目录 | `third_party/diana_sdk_python/lib/` |

## 安装基础工具

打开终端并更新软件包索引：

```bash
sudo apt update
```

安装基础工具：

```bash
sudo apt install -y \
    ca-certificates \
    git \
    python3
```

检查 Python：

```bash
python3 --version
```

## SDK 路径

Python 示例仓库默认将 SDK 作为子模块放在：

```text
third_party/diana_sdk_python/
```

运行前设置 Python wrapper 和原生动态库搜索路径：

```bash
export PYTHONPATH="$PWD/third_party/diana_sdk_python/lib:$PYTHONPATH"
export LD_LIBRARY_PATH="$PWD/third_party/diana_sdk_python/lib:$LD_LIBRARY_PATH"
```

示例仓库的公共 helper 会在运行时把 `third_party/diana_sdk_python/lib` 加入 `sys.path`，但建议仍显式设置环境变量，便于独立脚本、排障和动态库加载保持一致。

## 导入问题排查

分别检查 Python wrapper 和原生库依赖：

```bash
python3 -c "import DianaApi; print(DianaApi.__file__)"
ldd third_party/diana_sdk_python/lib/libDianaApi.so
```

出现 `ModuleNotFoundError: No module named 'DianaApi'` 时，优先检查 `PYTHONPATH`。错误信息包含 `libDianaApi.so` 或其依赖库名称时，优先检查 `LD_LIBRARY_PATH`、`uname -m` 输出以及 SDK 原生库的系统和架构是否匹配。

## Python 运行环境说明

Diana Python 示例以普通 Python 脚本方式运行，不需要 CMake 构建。典型流程如下：

```bash
cd diana_examples_python
git submodule update --init --recursive
export PYTHONPATH="$PWD/third_party/diana_sdk_python/lib:$PYTHONPATH"
export LD_LIBRARY_PATH="$PWD/third_party/diana_sdk_python/lib:$LD_LIBRARY_PATH"
python3 examples/01_connection/main.py --list-models
```

`--list-models` 会在加载原生 SDK 前退出，可用于没有连接机器人、甚至暂未准备原生动态库的环境。需要连接真机的示例必须确认 PC 与机器人处于同一网段。

## 冒烟测试

所有 Python 示例均已在真机上完成验证，各示例页的“执行效果”区域给出了真实运行输出。完成本地部署后，可先执行以下冒烟测试，再对照各示例页核对运行结果。

不连接机器人的基础检查命令如下：

```bash
python3 scripts/check_repository.py
```

该脚本检查 Python 语法、示例引用的 SDK 名称、本地 Markdown 链接、中英文档配对，以及 12 个示例的 `--list-models` 路径。也可以分开执行最基础的语法和 CLI 检查：

```bash
python3 -m py_compile common/*.py robots/*.py examples/*/main.py
for f in examples/*/main.py; do python3 "$f" --list-models >/dev/null; done
```

这些检查只覆盖 Python 语法和不加载原生 SDK 的 `--list-models` 路径，不代表机器人通信或运动控制已经验证。

## 实时控制环境

普通状态读取和非实时运动控制通常可以直接在标准 Ubuntu 系统中运行。

对于 `servoJ`、`servoL`、`speedJ`、`speedL` 等周期性接口，普通 Linux 不保证硬实时。生产应用应根据控制 PC、网络和机器人控制系统的实际条件评估实时性，并避免在实时循环中执行阻塞操作、复杂日志或大规模内存分配。

## 其他系统版本

Python SDK wrapper 通过 `ctypes` 加载原生库，因此平台兼容性由 Python 解释器、`DianaApi.py` 和原生动态库共同决定。随附的运行库为 Linux x86_64 版本。请始终使用与控制 PC 操作系统和 CPU 架构一致的 SDK 内容；不要将 Linux x86_64、Linux aarch64 和 Windows 的动态库混用。

### Linux aarch64

Linux aarch64 的 Python 调用方式与 x86_64 一致，但 `libDianaApi.so` 及其全部依赖库必须来自 aarch64 SDK 包。未在“已验证的 Linux 环境”中确认的组合，部署前需要在目标设备上自行完成导入、通信和真机验证。

### Windows

Windows 版 Python SDK 需要 `DianaApi.py` 能在同一 `lib/` 目录或运行时 `PATH` 中找到匹配的 `DianaApi.dll`，且 Python 解释器的位数/架构必须与 SDK 原生库一致。具体 DLL 名称、依赖项和 Python 版本兼容性以随机械臂交付的 SDK 和发布说明为准。

```{warning}
不要将 Linux 的 `.so` 用于 Windows，也不要将 Windows DLL 复制到 Linux 环境。Python 脚本能被解释器解析，不代表原生库一定能被加载。
```

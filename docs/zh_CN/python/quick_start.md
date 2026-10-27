# 快速开始（Linux）

目标是在 Linux 上完成一个最小 Python 程序：找到 SDK、导入 `DianaApi`、初始化服务、读取一次机器人状态并释放资源。

## 1. 获取并放置 SDK

Example 仓库默认将 SDK 作为子模块放在以下目录：

```text
diana_examples_python/
└── third_party/diana_sdk_python/
    ├── lib/
    │   └── DianaApi.py
    ├── doc/
    └── version
```

获取示例及 SDK：

```bash
git clone --recurse-submodules https://github.com/AgileRobots-APAC/diana_examples_python.git
cd diana_examples_python
```

已有主仓库时执行：

```bash
git submodule update --init --recursive
```

## 2. 配置运行环境

运行前设置 Python wrapper 和原生动态库搜索路径：

```bash
export PYTHONPATH="$PWD/third_party/diana_sdk_python/lib:$PYTHONPATH"
export LD_LIBRARY_PATH="$PWD/third_party/diana_sdk_python/lib:$LD_LIBRARY_PATH"
```

当前 SDK 子模块已经包含 Linux x86_64 原生运行库。其他系统或 CPU 架构需要换用厂商提供的完整匹配库集合，不能只替换单个 `libDianaApi.so`。

在自有 Python 程序中，至少需要保证 `DianaApi.py` 可导入，并且原生运行时库可被动态链接器找到：

```python
import DianaApi as api
```

如果不想依赖外部 `PYTHONPATH`，也可以在程序启动早期将 SDK wrapper 目录加入 `sys.path`：

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "third_party" / "diana_sdk_python" / "lib"))
import DianaApi as api
```

## 3. 最小初始化与读取

```python
import time
import DianaApi as api

robot_ip = "192.168.10.75"

error_cb = api.FNCERRORCALLBACK(lambda code, ip: print(f"error: {code}"))
state_cb = api.FNCSTATECALLBACK(lambda state, ip: None)

if not api.initSrv([robot_ip, 0, 0, 0, 0, 0], error_cb, state_cb):
    raise SystemExit("initSrv failed")

try:
    time.sleep(0.2)
    print("library version:", api.getLibraryVersion())
    print("robot state:", api.getRobotState(robot_ip))
finally:
    api.destroySrv(robot_ip)
```

错误和状态回调可能在 SDK 线程中触发，不要在回调中执行 `sleep`、长耗时 I/O 或会阻塞实时控制的业务逻辑。

## 4. 连接生命周期

每台机械臂按以下顺序管理资源：

```text
准备 SDK 路径 → 构造 FNCERRORCALLBACK / FNCSTATECALLBACK
    → initSrv([robot_ip, 0, 0, 0, 0, 0], error_cb, state_cb)
    → 使用其他 API → destroySrv(robot_ip)
```

回调对象需要在连接生命周期内保持引用；多机械臂应用应为每个目标 IP 明确管理状态和错误上下文。

## 5. 运行示例

先查看支持型号，不连接机器人：

```bash
python3 examples/01_connection/main.py --list-models
```

连接 Diana7：

```bash
python3 examples/01_connection/main.py --model diana7 --ip 192.168.10.75
```

连接 Thor12：

```bash
python3 examples/01_connection/main.py --model thor12 --ip 192.168.10.75
```

下一步运行不会触发运动的 [Example](examples/index.md)，确认型号、网络和 SDK 加载均正常。

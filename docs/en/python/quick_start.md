# Quick Start (Linux)

The goal is to run a minimal Python program on Linux: find the SDK, import `DianaApi`, initialize the service, read one robot state, and release resources.

## 1. Get the SDK

The examples repository keeps the SDK as a submodule:

```text
diana_examples_python/
└── third_party/diana_sdk_python/
    ├── lib/
    │   └── DianaApi.py
    ├── doc/
    └── version
```

Clone with submodules:

```bash
git clone --recurse-submodules https://github.com/AgileRobots-APAC/diana_examples_python.git
cd diana_examples_python
```

For an existing checkout:

```bash
git submodule update --init --recursive
```

## 2. Configure Runtime Paths

```bash
export PYTHONPATH="$PWD/third_party/diana_sdk_python/lib:$PYTHONPATH"
export LD_LIBRARY_PATH="$PWD/third_party/diana_sdk_python/lib:$LD_LIBRARY_PATH"
```

The current SDK submodule already includes the Linux x86_64 native runtime. For another operating system or CPU architecture, use the complete matching vendor library set rather than replacing only `libDianaApi.so`.

In your own Python program, at minimum make sure `DianaApi.py` is importable and the native runtime libraries can be found by the dynamic linker:

```python
import DianaApi as api
```

For an application that does not use an external `PYTHONPATH`, insert the wrapper directory before importing the SDK:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "third_party" / "diana_sdk_python" / "lib"))
import DianaApi as api
```

## 3. Minimal Program

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

Callbacks may run on SDK threads. Do not perform `sleep`, long-running I/O, or blocking business logic inside callbacks.

## 4. Connection Lifecycle

Manage resources for each robot in this order:

```text
prepare SDK paths → construct FNCERRORCALLBACK / FNCSTATECALLBACK
    → initSrv([robot_ip, 0, 0, 0, 0, 0], error_cb, state_cb)
    → use other APIs → destroySrv(robot_ip)
```

Keep callback objects alive for the connection lifetime. Multi-arm applications should manage state and error context per target IP.

## 5. Run Examples

List models without connecting to a robot:

```bash
python3 examples/01_connection/main.py --list-models
```

Connect to a Diana7:

```bash
python3 examples/01_connection/main.py --model diana7 --ip 192.168.10.75
```

Connect to a Thor12:

```bash
python3 examples/01_connection/main.py --model thor12 --ip 192.168.10.75
```

Next, run the non-motion [Examples](examples/index.md) to confirm model selection, networking, and SDK loading.

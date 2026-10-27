# Development Setup

Before Python development, confirm that the control PC can reach the controller through the shared [Network Setup](../programming/network.md), and complete site safety preparation.

```{important}
When using the Python API, make sure the robot's <span class="power-on">FCI</span> mode is disabled (the text turns **red**). A robot running in <span class="power-on">FCI</span> mode cannot be controlled through the regular API connection.
```

```{important}
Set the teach pendant mode selector to <span class="power-on">Auto</span> mode or <span class="power-on">Collaborative</span> mode before running code.
```

```{important}
Power on the robot from the startup screen before running API examples.
```

## Environment

Ubuntu x86_64 is recommended for robot-control development. Python examples do not require CMake, but Python must be able to import `DianaApi.py`, and the system dynamic linker must be able to load the matching native SDK library.

```{tip}
Use <span class="power-on">Ubuntu x86_64</span> for robot-control development.
```

## Verified Linux Environments

| System | Status | Verified Python |
|---|---|---|
| Ubuntu 20.04 x64 | Verified | Python 3 |
| Ubuntu 22.04 x64 | Verified | Python 3 |

Verification covers SDK import, connection, and robot testing. Validate any unlisted distribution, Python version, or native-SDK-library combination in the target project.

| Item | Recommended |
|---|---|
| Operating system | Ubuntu 20.04 LTS / Ubuntu 22.04 LTS |
| Architecture | x86_64 |
| Python | Python 3 |
| SDK wrapper | `third_party/diana_sdk_python/lib/DianaApi.py` |
| Native library path | `third_party/diana_sdk_python/lib/` |

## Basic Tools

Open a terminal and update the package index:

```bash
sudo apt update
```

Install the basic tools:

```bash
sudo apt install -y \
    ca-certificates \
    git \
    python3
```

Check Python:

```bash
python3 --version
```

## SDK Paths

The examples repository keeps the SDK as a submodule:

```text
third_party/diana_sdk_python/
```

Set the wrapper path and native library path before running:

```bash
export PYTHONPATH="$PWD/third_party/diana_sdk_python/lib:$PYTHONPATH"
export LD_LIBRARY_PATH="$PWD/third_party/diana_sdk_python/lib:$LD_LIBRARY_PATH"
```

The examples helper also inserts `third_party/diana_sdk_python/lib` into `sys.path`, but setting the environment explicitly keeps standalone scripts and dynamic-library loading easier to diagnose.

## Import Troubleshooting

Check the wrapper and native dependencies separately:

```bash
python3 -c "import DianaApi; print(DianaApi.__file__)"
ldd third_party/diana_sdk_python/lib/libDianaApi.so
```

`ModuleNotFoundError: No module named 'DianaApi'` indicates a Python search-path problem. An error mentioning `libDianaApi.so` or one of its dependencies indicates a dynamic-library search-path or architecture mismatch. Confirm `PYTHONPATH`, `LD_LIBRARY_PATH`, and the output of `uname -m`.

## Python Runtime

The Diana Python examples are ordinary Python scripts and do not require a CMake build. A typical setup is:

```bash
cd diana_examples_python
git submodule update --init --recursive
export PYTHONPATH="$PWD/third_party/diana_sdk_python/lib:$PYTHONPATH"
export LD_LIBRARY_PATH="$PWD/third_party/diana_sdk_python/lib:$LD_LIBRARY_PATH"
python3 examples/01_connection/main.py --list-models
```

`--list-models` exits before the native SDK is loaded. It can therefore be used without a robot connection and even before the native library is ready. Examples that connect to a robot require the control PC and the robot to be on the same subnet.

## Smoke Tests

All Python examples have been verified on real robots, and each example page includes real run output in its “Execution Results” section. After deploying locally, first run the smoke tests below and compare your results with those pages.

The basic checks below do not require a robot connection:

```bash
python3 scripts/check_repository.py
```

This script checks Python syntax, SDK names referenced by examples, local Markdown links, bilingual document pairs, and all 12 `--list-models` paths. To run only the basic syntax and CLI checks separately:

```bash
python3 -m py_compile common/*.py robots/*.py examples/*/main.py
for f in examples/*/main.py; do python3 "$f" --list-models >/dev/null; done
```

These checks cover Python syntax and `--list-models` paths only. They do not validate robot communication or motion.

## Realtime Environment

Standard Ubuntu is usually enough for state reading and non-realtime motion commands.

For periodic interfaces such as `servoJ`, `servoL`, `speedJ`, and `speedL`, standard Linux does not guarantee hard realtime behavior. Production applications should evaluate the actual control PC, network, and controller timing, and avoid blocking calls, heavy logging, or large allocations inside realtime loops.

## Other Platforms

The Python wrapper loads native libraries through `ctypes`, so compatibility depends on the Python interpreter, `DianaApi.py`, and the native runtime as one matching set. The bundled runtime is for Linux x86_64. Always use SDK contents that match the control PC's operating system and CPU architecture; never mix Linux x86_64, Linux aarch64, and Windows native libraries.

### Linux aarch64

The Python call pattern is the same, but `libDianaApi.so` and all dependent libraries must come from an aarch64 SDK package. For any combination not confirmed in “Verified Linux Environments”, validate import, communication, and robot behavior on the target device before deployment.

### Windows

The Windows Python SDK requires `DianaApi.py` to find a matching `DianaApi.dll` in the same `lib/` directory or on the runtime `PATH`, and the Python interpreter's bitness/architecture must match the SDK native libraries. The exact DLL names, dependencies, and Python version compatibility are defined by the SDK and release notes delivered with the robot.

```{warning}
Do not use Linux `.so` files on Windows or Windows DLLs on Linux. Successful Python syntax checking does not prove that the native runtime can be loaded.
```

# Development Preparation

Before C++ development, verify that the control PC can reach the controller as described in the shared [Network Setup](../programming/network.md), and complete all on-site safety preparation.

```{important}
When programming with the C++ API, ensure that the robot's <span class="power-on">FCI</span> mode is disabled (the text turns **red**). The robot cannot be connected to or controlled through the API while it is operating in <span class="power-on">FCI</span> mode.
```

```{important}
Before running code, set the mode selector in the upper-left corner of the teach pendant to <span class="power-on">Automatic</span> mode or <span class="power-on">Collaborative</span> mode.
```

```{important}
Before running code, select Power On on the startup screen and confirm that the robot is powered on.
```

## Development Environment

This section describes the baseline development environment for Diana robot applications on Ubuntu x86_64 and the corresponding development flow.

```{tip}
Ubuntu x86_64 is the recommended platform for robot-control development.
```

## Verified Linux environments

| System | Status | Verified compiler | Verified CMake |
|---|---|---|---|
| Ubuntu 18.04 x64 | Supported | GCC 7.5 | 3.10 |
| Ubuntu 20.04 x64 | Supported | GCC 7.5, GCC 9.4 | 3.16 |
| Ubuntu 22.04 x64 | Supported | GCC 11.4 | 3.22 |

## Recommended system

The recommended configuration is:

| Item | Recommended configuration |
|---|---|
| Operating system | Ubuntu 20.04 LTS |
| System architecture | x86_64 |
| C++ compiler | GCC / G++ |
| Build system | CMake |
| Build tool | GNU Make |

```{attention}
For real-time control, prioritize control-PC real-time performance. If necessary, install a real-time kernel matching the Ubuntu release used by the control PC.
```

## Install baseline development tools

Update the package index:

```bash
sudo apt update
```

Install the baseline tools required for Diana development:

```bash
sudo apt install -y \
    ca-certificates \
    git \
    cmake \
    g++ \
    make
```

Verify the installed environment:

```bash
g++ --version
cmake --version
make --version
```

If each command prints version information successfully, the baseline environment is ready.

## Build environment

Diana examples are written in C++ and use CMake to manage project configuration and builds. A typical build sequence is:

```bash
mkdir -p build
cd build

cmake ..
make -j$(nproc)
```

The generated executable is placed in the project's build output directory.

```{note}
If Ubuntu's default package sources are slow on the current network, configure an appropriate mirror. For example, users in mainland China can select a mirror provided by Alibaba Cloud or Tsinghua University. This affects only package download speed, not the Diana API itself.
```

## Real-time control environment

Normal motion control and state reads can usually run on a standard Ubuntu installation. For periodic real-time control, high-frequency state exchange, or applications sensitive to control-period jitter, optimize the control PC for real-time performance.

Depending on application requirements, consider:

- Installing a real-time kernel matching the Ubuntu release.
- Assigning appropriate scheduling priority to real-time control threads.
- Avoiding CPU- or I/O-intensive processes during real-time control.
- Using a stable wired network connection to the robot controller.
- Measuring control period and communication latency on the target system.

```{hint}
Before running a real-time control application, confirm that the control PC, network, and robot control system meet the applicable real-time requirements.
```

## Required tools

- Git, to obtain the example repository and its SDK submodule.
- CMake, to configure the C++ project.
- A C++ compiler and build tools appropriate for the selected Ubuntu release.
- A wired NIC configured with a static IP address for controller port A.

## Other system versions

The USB drive delivered with the robot contains the Linux x86_64 SDK as well as Linux aarch64 and Windows C++ SDK packages. Always use an SDK matching the control PC operating system and CPU architecture. Do not mix x86_64, aarch64, and Windows headers, libraries, or runtime files.

### Linux aarch64

The Linux aarch64 package uses the same project layout, CMake configuration, SDK initialization, and API usage as the Linux x86_64 guide. Replace the SDK directory in the project with the aarch64 package from the USB drive and build on an aarch64 Linux host.

- Confirm that the control PC is aarch64, rather than an x86_64 host using cross compilation.
- Keep `include/`, `lib/`, and `version` from the same aarch64 SDK package.
- Configure the dynamic-library search path as described in [Quick Start](quick_start.md), and ensure the loaded `.so` is aarch64.
- Validate unlisted OS, compiler, and kernel combinations on the target device and physical robot.

### Windows

The USB drive also contains the Windows SDK. Configure headers, link libraries, and runtime DLLs manually in a Windows project. First build a minimal console application, verify SDK loading and network connectivity, and only then integrate application logic or motion control.

1. Select an SDK package matching the Windows host architecture; keep its `include`, `lib`, and DLL files from one release.
2. Add the header directory to include paths, add `lib` to linker search paths, and link the SDK import library.
3. Copy the SDK DLLs and dependency DLLs beside the generated `.exe`, or add their directory to the runtime `PATH`. Finding a `.lib` at link time does not guarantee that the program can start.
4. Match target architecture, compiler runtime, and Debug/Release configuration to the SDK package. For a missing-DLL or architecture error, first inspect the DLL path actually loaded by the process and its file architecture.
5. After building, first run a non-motion connection or state-read program and verify reachability using the shared [Network Setup](../programming/network.md).

```{warning}
The exact library names, dependency DLLs, and project template are defined by the SDK package and release notes delivered with the robot. Do not use Linux `.so` files in a Windows project or Windows DLLs on Linux.
```

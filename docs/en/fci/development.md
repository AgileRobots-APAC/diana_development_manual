# Development Preparation

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

FCI development requires:

- a C++ development environment;
- the Diana-patched `libfranka 0.18.2`;
- Pinocchio 3.9.0;
- the network environment between the control PC and the robot.

Complete the robot connection test before running motion, torque, or impedance control programs.

```{important}
Before running any FCI program, confirm on the teach pendant that:

- **FCI mode is enabled** (its status is shown in green); without FCI enabled, the robot cannot be connected to or controlled through the FCI interface.
- The teach pendant stays in **Collaborative mode**; do not switch modes while a motion program runs.
- **Power On** has been clicked on the startup screen and the robot is powered on.
```

## Development Environment

| Item | Requirement |
| --- | --- |
| Operating system | Ubuntu 20.04 / Ubuntu 22.04 x86_64 |
| C++ standard | C++17 |
| Build tools | CMake, Ninja, GCC |
| FCI library | Diana-patched `libfranka 0.18.2` |
| Kinematics library | Pinocchio 3.9.0 |
| Dependencies | Eigen3, Boost, Poco, Threads |
| Network | Control PC and robot on the same subnet; wired connection recommended |

```{attention}
Note: Do not mix headers and shared libraries from other `libfranka` versions. All interfaces in this documentation are based on `libfranka 0.18.2`.
```

## Environment Preparation

### 1. Obtain the Source Code

Download the project:

```bash
git clone --recurse-submodules https://github.com/AgileRobots-APAC/diana_libfranka_overlay.git

cd diana_libfranka_overlay
```

Project structure:

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

### 2. Apply the Diana Patch

Select the corresponding robot version:

```bash
git switch <arm-version>

git submodule update --init --recursive
```

Check the patch:

```bash
git -C libfranka apply --check ../patches/<arm-version>.patch
```

Apply the patch:

```bash
git -C libfranka apply ../patches/<arm-version>.patch
```

Each overlay branch contains exactly one patch for its robot model. To reproduce a release baseline, check out a tag instead of a branch, for example `git switch --detach v1.0.0-libfranka0.18.2-diana3`; the upstream `libfranka` version is recorded in the `VERSION` file at the repository root (`0.18.2`).

To change the robot model, discard the changes applied to the submodule, switch to the other overlay branch, update the submodule, and apply that branch's patch:

```bash
git -C libfranka reset --hard "$(cat VERSION)"
git -C libfranka clean -fd
git switch <arm-version>
git submodule update --init --recursive
git -C libfranka apply --check ../patches/<arm-version>.patch
git -C libfranka apply ../patches/<arm-version>.patch
```

```{warning}
`reset` and `clean` delete local changes and untracked files in the submodule. Run them only in a disposable or known-clean submodule.
```

## 3. Development Environment Configuration

There are two ways to prepare the FCI development environment:

- VS Code Dev Container;
- native Ubuntu environment.

### 3.1 Using VS Code Dev Container

This option is suitable for development hosts with Docker installed.

The Dev Container automatically:

- installs build dependencies;
- builds Pinocchio 3.9.0;
- builds the Diana-patched `libfranka 0.18.2`;
- configures the FCI example runtime environment.

#### 3.1.1 Open the Dev Container

Enter the project:

```bash
cd diana_libfranka_overlay
```

Open `libfranka`:

```bash
code libfranka
```

Run the following command in VS Code:

```text
Dev Containers: Reopen in Container
```

```{note}
The first startup needs to build the development image. Because Pinocchio and libfranka are compiled during this process, the first startup may take a while.
```

#### 3.1.2 Container Environment Notes

The Dev Container is configured to support FCI communication and hardware debugging.

```{attention}
Robot network configuration still needs to be completed on the host machine.
```

```text
Control PC network card:
192.168.10.xxx (same subnet as the robot)
Robot controller:
192.168.10.75 (confirm the actual address)
```

#### 3.1.3 Build Example Programs

Enter the source tree:

```bash
cd /workspaces
```

Generate the build files:

```bash
cmake -S . \
      -B build \
      -DBUILD_EXAMPLES=ON
```

Build:

```bash
cmake --build build
```

After compilation, the Diana FCI example programs are available under:

```text
build/examples/diana3/
```

#### 3.1.4 Run a Test

For example:

```bash
./build/examples/diana3/echo_robot_state <robot-ip>
```

where:

```text
<robot-ip>
```

is the robot controller IP address.

#### 3.1.5 Rebuild After Modifying Source Code

After modifying libfranka or example code:

```bash
cd /workspaces

cmake --build build
```

The container does not need to be recreated.

If the CMake configuration is modified, regenerate the build files:

```bash
cmake -S . \
      -B build \
      -DBUILD_EXAMPLES=ON

cmake --build build
```

### 3.2 Using Native Ubuntu Environment

This option is suitable for:

- control PCs where Docker cannot be used;
- robot on-site control computers;
- environments that need to run FCI programs directly.

This method requires manual installation of:

- build dependencies;
- Pinocchio 3.9.0;
- Diana-patched `libfranka 0.18.2`.

#### 3.2.1 Check the System Environment

View the Ubuntu version:

```bash
lsb_release -a
```

View the system architecture:

```bash
uname -m
```

Recommended environment:

```text
Ubuntu 20.04 / Ubuntu 22.04

x86_64
```

#### 3.2.2 Install System Dependencies

Run:

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

Check the tools:

```bash
cmake --version

g++ --version

ninja --version
```

#### 3.2.3 Build and Install Pinocchio 3.9.0

Enter a temporary directory:

```bash
cd /tmp
```

Download the source code:

```bash
git clone --recursive \
--branch v3.9.0 \
https://github.com/stack-of-tasks/pinocchio.git
```

Enter the source tree:

```bash
cd /tmp/pinocchio
```

Initialize submodules:

```bash
git submodule update --init --recursive
```

Configure:

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

Build:

```bash
cmake --build /tmp/pinocchio/build \
      -- -j$(getconf _NPROCESSORS_ONLN)
```

Install:

```bash
sudo cmake --install /tmp/pinocchio/build
```

Configure shared libraries:

```bash
sudo sh -c 'echo "/opt/openrobots/lib" > /etc/ld.so.conf.d/openrobots.conf'

sudo ldconfig
```

Check:

```bash
ldconfig -p | grep pinocchio
```

#### 3.2.4 Build Diana-Patched libfranka 0.18.2

Enter the source directory:

```bash
cd /path/to/diana_libfranka_overlay/libfranka
```

Confirm the directory structure:

```text
libfranka/

├── CMakeLists.txt
├── include/
├── src/
├── examples/
└── pylibfranka/
```

##### Configure the Build

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

Parameter description:

| Parameter | Description |
| --- | --- |
| `BUILD_TESTS` | Disables internal libfranka tests |
| `BUILD_EXAMPLES` | Builds Diana FCI example programs |
| `GENERATE_PYLIBFRANKA` | Generates the Python interface |
| `CMAKE_PREFIX_PATH` | Specifies the Pinocchio installation path |

##### Build

```bash
cmake --build build \
      -- -j$(getconf _NPROCESSORS_ONLN)
```

##### Install

```bash
sudo cmake --install build

sudo ldconfig
```

#### 3.2.5 Build Diana FCI Example Programs

Enter:

```bash
cd /path/to/diana_libfranka_overlay/libfranka
```

Build:

```bash
cmake --build build
```

View generated programs:

```bash
ls build/examples/diana3
```

#### 3.2.6 Run the FCI Connection Test

Run:

```bash
./build/examples/diana3/echo_robot_state \
<robot-ip>
```

The program continuously prints robot state, then exits normally. It does not send motion or torque commands.

Use the matching example directory for another robot model.

#### 3.2.7 Install Python Interface (Optional)

Enter:

```bash
cd libfranka
```

Install:

```bash
pip3 install .
```

```{attention}
Python compilation does not build the C++ examples by default. After the build succeeds, the programs can be run with `python3`.
```

## Pre-Connection Checks

Before running a program, confirm that:

1. FCI is enabled on the controller;
2. the control PC and robot are on the same subnet;
3. the network connection is normal;
4. the robot is powered on;
5. the teach pendant is in Collaborative mode.

## Safety Notes

```{warning}

A successful build or connection test does not mean that motion control can be executed directly.

Before running any motion, torque, or impedance control program, confirm the on-site safety environment and prepare the emergency stop.

```

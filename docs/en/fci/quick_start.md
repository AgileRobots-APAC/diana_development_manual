# Quick Start (Linux)

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

This workflow prepares the overlay for one robot, applies its patch, builds the `libfranka` examples, and performs an initial read-only state check.

## 1. Select the Robot and Apply Its Patch

First select the physical robot in [Select a Robot Model](machines.md). The following commands use Diana3; substitute the branch, patch, and output directory for Diana7 or Diana7G2.

```bash
git clone --recurse-submodules https://github.com/AgileRobots-APAC/diana_libfranka_overlay.git
cd diana_libfranka_overlay
git switch diana3
git submodule update --init --recursive
git -C libfranka apply --check ../patches/diana3.patch
git -C libfranka apply ../patches/diana3.patch
```

The patch places the upstream examples in `libfranka/examples/diana3/` and selects the Diana3 rate-limiting implementation. Do not apply a second patch to the same work tree.

## 2. Configure CMake and Build the Examples

Complete dependency, controller-FCI, and network preparation in [Development Preparation](development.md). For a host build, run from the overlay root:

```bash
cmake -S libfranka -B build/libfranka -DBUILD_EXAMPLES=ON
cmake --build build/libfranka
```

The Diana3 executables are written to `build/libfranka/examples/diana3/`. When building in a container from `libfranka/`, the corresponding location is `build/examples/diana3/`. Then the corresponding compilation command needs to be changed to:
```bash
cmake -S . -B build -DBUILD_EXAMPLES=ON
cmake --build build/
```

## 3. Minimal Read-Only Validation

Start with state reading, which does not send a motion target. Replace the robot IP with the site value:

```bash
./build/libfranka/examples/diana3/echo_robot_state 192.168.10.75
```

`communication_test` is not a read-only check: it first moves to an initial pose, then opens a torque-control session and sends zero torque. Run it only after site safety conditions are satisfied. Use the output directory for the selected robot.

## 4. Connection Lifecycle

```text
confirm the robot is ready for FCI → create the Robot connection
    → read state or enter a control callback → exit the control loop normally
    → release connection resources
```

Callback failures commonly result from timeout, discontinuous targets, limits, network jitter, or a control-mode mismatch. Complete realtime network and system preparation before entering realtime control.

```{warning}
A successful build or read-only example does not authorize motion. Before running any upstream example that sends position, velocity, or torque commands, confirm personnel clearance, fixtures, workpieces, cables, velocity, torque, emergency-stop access, and the exit path.
```

## 5. Python Interface Compilation (Optional)

Enter the `libfranka` root directory:

```bash
cd libfranka
```

Install:

```bash
pip3 install .
```

```{attention}
The Python build does not compile the C++ examples by default. After a successful build you can run the programs with `python3`.
```

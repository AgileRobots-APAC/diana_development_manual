# Example Overview

The example repository contains runnable C++ reference projects. It calls the Diana API directly; common code only handles argument parsing, callbacks, waiting, logging, and model validation, and does not wrap the SDK.

```{note}
Each example page summarizes the relevant guidance from the Industrial Diana API Manual for C/C++ V3.4.0. Function signatures, availability, and behavior are ultimately defined by the current SDK headers, release notes, and example source.
```

| Item | Value |
|---|---|
| Git repository | [diana_examples_cpp](https://github.com/AgileRobots-APAC/diana_examples_cpp.git) |
| SDK repository | [diana_sdk_cpp](https://github.com/AgileRobots-APAC/diana_sdk_cpp.git) |
| Example license | MIT License |
| Examples version | 1.0.0 (compatible with SDK 3.3.0 and 3.4.0; bundles SDK 3.3.0) |
| SDK location | `third_party/diana_sdk_cpp/` |
| Build system | CMake 3.10+, C++11 |
| Output directory | `build/bin/` |

## Obtain, build, and validate

```bash
git clone --recurse-submodules https://github.com/AgileRobots-APAC/diana_examples_cpp.git
cd diana_examples_cpp
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -- -j"$(getconf _NPROCESSORS_ONLN)"
export LD_LIBRARY_PATH="$PWD/third_party/diana_sdk_cpp/lib:$LD_LIBRARY_PATH"
./build/bin/01_connection --list-models
```

Use `git submodule update --init --recursive` for an existing clone. For an SDK outside the repository, add `-DDIANA_SDK_DIR=/path/to/diana_sdk_cpp` when configuring CMake. See [Development Preparation](../development.md) for system and toolchain requirements.

Common arguments are:

| Argument | Meaning |
|---|---|
| `--ip <address>` | Controller IP. The examples default to `192.168.10.75`; a positional IP is also accepted for compatibility. |
| `--model <name>` | Robot profile. Motion examples require an explicit model when `--run` is used. |
| `--run` | Allows a motion example to send commands; without it, the example remains in dry-run mode. |
| `--list-models` | Run `01_connection --list-models` to print the currently registered profiles without connecting. |

## Repository layout

```text
diana_examples_cpp/
├── common/                  # Argument, callback, wait, and logging helpers
├── robots/                  # Diana and Thor model profiles
├── examples/                # Runnable examples
├── docs/                    # Tutorials in the example repository
└── third_party/diana_sdk_cpp/    # diana_sdk_cpp submodule
```

```{toctree}
:hidden:
:maxdepth: 1

01_connection
02_robot_state
03_joint_motion
04_cartesian_motion
05_kinematics
06_io
07_tcp_and_frames
08_motion_limits
09_path_and_waypoints
10_jog_motion
11_force_guarded_motion
12_servoL_realtime
```

## Example list

<div class="example-list-table">

| Example | Purpose | APIs used | Moves by default |
|---|---|---|---|
| [01 Connection and Model Identification](01_connection.md) | Connection, version, model/joint-count detection, and state | <a href="01_connection.html#initsrvnetinfo-initsrv-destroysrv"><code>initSrvNetInfo</code></a>, <a href="01_connection.html#initsrvnetinfo-initsrv-destroysrv"><code>initSrv</code></a>, <a href="01_connection.html#initsrvnetinfo-initsrv-destroysrv"><code>destroySrv</code></a><br><a href="01_connection.html#getlibraryversion-getrobotstate-getjointcount"><code>getLibraryVersion</code></a>, <a href="01_connection.html#getlibraryversion-getrobotstate-getjointcount"><code>getRobotState</code></a>, <a href="01_connection.html#getlibraryversion-getrobotstate-getjointcount"><code>getJointCount</code></a><br><a href="01_connection.html#releasebrake-holdbrake"><code>releaseBrake</code></a>, <a href="01_connection.html#releasebrake-holdbrake"><code>holdBrake</code></a> | No |
| [02 Robot State and Diagnostics](02_robot_state.md) | State, external force, link, error/warning, and collision diagnostics | <a href="02_robot_state.html#getjointpos-getjointangularvel-getjointcurrent-getjointtorque"><code>getJointPos</code></a>, <a href="02_robot_state.html#getjointpos-getjointangularvel-getjointcurrent-getjointtorque"><code>getJointAngularVel</code></a>, <a href="02_robot_state.html#getjointpos-getjointangularvel-getjointcurrent-getjointtorque"><code>getJointCurrent</code></a>, <a href="02_robot_state.html#getjointpos-getjointangularvel-getjointcurrent-getjointtorque"><code>getJointTorque</code></a><br><a href="02_robot_state.html#gettcppos-gettcpexternalforce-gettcpforce-getjointforce"><code>getTcpPos</code></a>, <a href="02_robot_state.html#gettcppos-gettcpexternalforce-gettcpforce-getjointforce"><code>getTcpExternalForce</code></a>, <a href="02_robot_state.html#gettcppos-gettcpexternalforce-gettcpforce-getjointforce"><code>getTcpForce</code></a>, <a href="02_robot_state.html#gettcppos-gettcpexternalforce-gettcpforce-getjointforce"><code>getJointForce</code></a><br><a href="02_robot_state.html#getrobotstate-getlinkstate-getlasterror-getlastwarning-formaterror-iscollision"><code>getRobotState</code></a>, <a href="02_robot_state.html#getrobotstate-getlinkstate-getlasterror-getlastwarning-formaterror-iscollision"><code>getLinkState</code></a>, <a href="02_robot_state.html#getrobotstate-getlinkstate-getlasterror-getlastwarning-formaterror-iscollision"><code>getLastError</code></a>, <a href="02_robot_state.html#getrobotstate-getlinkstate-getlasterror-getlastwarning-formaterror-iscollision"><code>getLastWarning</code></a>, <a href="02_robot_state.html#getrobotstate-getlinkstate-getlasterror-getlastwarning-formaterror-iscollision"><code>formatError</code></a>, <a href="02_robot_state.html#getrobotstate-getlinkstate-getlasterror-getlastwarning-formaterror-iscollision"><code>isCollision</code></a> | No, read-only |
| [03 Joint Motion](03_joint_motion.md) | Joint target motion | <a href="03_joint_motion.html#getjointpos"><code>getJointPos</code></a>, <a href="03_joint_motion.html#movejtotarget"><code>moveJToTarget</code></a> | No; requires `--run` |
| [04 Cartesian Motion](04_cartesian_motion.md) | Cartesian linear motion | <a href="04_cartesian_motion.html#gettcppos"><code>getTcpPos</code></a>, <a href="04_cartesian_motion.html#moveltopose"><code>moveLToPose</code></a> | No; requires `--run` |
| [05 Kinematics](05_kinematics.md) | FK, IK, reference IK, RPY/axis-angle conversion | <a href="05_kinematics.html#getjointpos-forward-inverse-inverse-ext"><code>getJointPos</code></a>, <a href="05_kinematics.html#getjointpos-forward-inverse-inverse-ext"><code>forward</code></a>, <a href="05_kinematics.html#getjointpos-forward-inverse-inverse-ext"><code>inverse</code></a>, <a href="05_kinematics.html#getjointpos-forward-inverse-inverse-ext"><code>inverse_ext</code></a><br><a href="05_kinematics.html#rpy2axis-axis2rpy"><code>rpy2Axis</code></a>, <a href="05_kinematics.html#rpy2axis-axis2rpy"><code>axis2RPY</code></a> | No |
| [06 I/O](06_io.md) | DI/DO/AI/AO and bus electrical data | <a href="06_io.html#readdi-readdo-writedo"><code>readDI</code></a>, <a href="06_io.html#readdi-readdo-writedo"><code>readDO</code></a>, <a href="06_io.html#readdi-readdo-writedo"><code>writeDO</code></a><br><a href="06_io.html#readai-readao-writeao"><code>readAI</code></a>, <a href="06_io.html#readai-readao-writeao"><code>readAO</code></a>, <a href="06_io.html#readai-readao-writeao"><code>writeAO</code></a><br><a href="06_io.html#readbuscurrent-readbusvoltage"><code>readBusCurrent</code></a>, <a href="06_io.html#readbuscurrent-readbusvoltage"><code>readBusVoltage</code></a> | No; writing needs explicit arguments |
| [07 TCP, Frames, and Payload](07_tcp_and_frames.md) | TCP, frames, payload, and tool-relative transforms | <a href="07_tcp_and_frames.html#gettcppos-getdefaultactivetcppose-getdefaultactivetcp-getdefaulttcpcoordinate-getdefaultworkpiececoordinate-getactivetcppayload"><code>getTcpPos</code></a>, <a href="07_tcp_and_frames.html#gettcppos-getdefaultactivetcppose-getdefaultactivetcp-getdefaulttcpcoordinate-getdefaultworkpiececoordinate-getactivetcppayload"><code>getDefaultActiveTcpPose</code></a>, <a href="07_tcp_and_frames.html#gettcppos-getdefaultactivetcppose-getdefaultactivetcp-getdefaulttcpcoordinate-getdefaultworkpiececoordinate-getactivetcppayload"><code>getDefaultActiveTcp</code></a>, <a href="07_tcp_and_frames.html#gettcppos-getdefaultactivetcppose-getdefaultactivetcp-getdefaulttcpcoordinate-getdefaultworkpiececoordinate-getactivetcppayload"><code>getDefaultTcpCoordinate</code></a>, <a href="07_tcp_and_frames.html#gettcppos-getdefaultactivetcppose-getdefaultactivetcp-getdefaulttcpcoordinate-getdefaultworkpiececoordinate-getactivetcppayload"><code>getDefaultWorkPieceCoordinate</code></a>, <a href="07_tcp_and_frames.html#gettcppos-getdefaultactivetcppose-getdefaultactivetcp-getdefaulttcpcoordinate-getdefaultworkpiececoordinate-getactivetcppayload"><code>getActiveTcpPayload</code></a><br><a href="07_tcp_and_frames.html#rpy2axis-pose2homogeneous-homogeneous2pose"><code>rpy2Axis</code></a>, <a href="07_tcp_and_frames.html#rpy2axis-pose2homogeneous-homogeneous2pose"><code>pose2Homogeneous</code></a>, <a href="07_tcp_and_frames.html#rpy2axis-pose2homogeneous-homogeneous2pose"><code>homogeneous2Pose</code></a> | No, read-only |
| [08 Motion Limits](08_motion_limits.md) | Controller motion-limit queries | <a href="08_motion_limits.html#getjointspositionrange-getmaxjointsvel-getmaxjointsacc"><code>getJointsPositionRange</code></a>, <a href="08_motion_limits.html#getjointspositionrange-getmaxjointsvel-getmaxjointsacc"><code>getMaxJointsVel</code></a>, <a href="08_motion_limits.html#getjointspositionrange-getmaxjointsvel-getmaxjointsacc"><code>getMaxJointsAcc</code></a><br><a href="08_motion_limits.html#getmaxcarttranslationvel-getmaxcarttranslationacc-getmaxcartrotationvel-getmaxcartrotationacc"><code>getMaxCartTranslationVel</code></a>, <a href="08_motion_limits.html#getmaxcarttranslationvel-getmaxcarttranslationacc-getmaxcartrotationvel-getmaxcartrotationacc"><code>getMaxCartTranslationAcc</code></a>, <a href="08_motion_limits.html#getmaxcarttranslationvel-getmaxcarttranslationacc-getmaxcartrotationvel-getmaxcartrotationacc"><code>getMaxCartRotationVel</code></a>, <a href="08_motion_limits.html#getmaxcarttranslationvel-getmaxcarttranslationacc-getmaxcartrotationvel-getmaxcartrotationacc"><code>getMaxCartRotationAcc</code></a> | No, read-only |
| [09 Paths and Waypoints](09_path_and_waypoints.md) | Basic and complex waypoint paths | <a href="09_path_and_waypoints.html#createpath-addmovej-runpath-destroypath"><code>createPath</code></a>, <a href="09_path_and_waypoints.html#createpath-addmovej-runpath-destroypath"><code>addMoveJ</code></a>, <a href="09_path_and_waypoints.html#createpath-addmovej-runpath-destroypath"><code>runPath</code></a>, <a href="09_path_and_waypoints.html#createpath-addmovej-runpath-destroypath"><code>destroyPath</code></a><br><a href="09_path_and_waypoints.html#createcomplexpath-addmovejbytarget-runcomplexpath-destroycomplexpath"><code>createComplexPath</code></a>, <a href="09_path_and_waypoints.html#createcomplexpath-addmovejbytarget-runcomplexpath-destroycomplexpath"><code>addMoveJByTarget</code></a>, <a href="09_path_and_waypoints.html#createcomplexpath-addmovejbytarget-runcomplexpath-destroycomplexpath"><code>runComplexPath</code></a>, <a href="09_path_and_waypoints.html#createcomplexpath-addmovejbytarget-runcomplexpath-destroycomplexpath"><code>destroyComplexPath</code></a> | No; requires `--run` |
| [10 Jog Motion](10_jog_motion.md) | Low-speed, short-duration J1, TCP translation, and TCP rotation jogging | <a href="10_jog_motion.html#movejoint-movetcp-ex-rotationtcp-ex-stop"><code>moveJoint</code></a>, <a href="10_jog_motion.html#movejoint-movetcp-ex-rotationtcp-ex-stop"><code>moveTcp_ex</code></a>, <a href="10_jog_motion.html#movejoint-movetcp-ex-rotationtcp-ex-stop"><code>rotationTCP_ex</code></a>, <a href="10_jog_motion.html#movejoint-movetcp-ex-rotationtcp-ex-stop"><code>stop</code></a> | No; requires `--run` |
| [11 Force-Guarded Stop](11_force_guarded_motion.md) | Force-threshold stop during up to 10 s of low-speed Cartesian motion | <a href="11_force_guarded_motion.html#speedl"><code>speedL</code></a>, <a href="11_force_guarded_motion.html#gettcpforce-stop"><code>getTcpForce</code></a>, <a href="11_force_guarded_motion.html#gettcpforce-stop"><code>stop</code></a> | No; requires `--run` |
| [12 ServoL Realtime Streaming](12_servoL_realtime.md) | 10 ms `servoL_ex` sine trajectory at ±5 cm in Z | <a href="12_servoL_realtime.html#gettcppos"><code>getTcpPos</code></a>, <a href="12_servoL_realtime.html#servol-ex"><code>servoL_ex</code></a> | No; requires `--run` |

</div>

## Usage principles

1. Run the non-motion connection, version, or state-reading examples first to verify SDK loading and networking.
2. Explicitly select the robot model and IP address.
3. Use `--run` for motion examples only after the on-site safety conditions are met.

The current examples cover connection, state, joint/Cartesian motion, kinematics, I/O, TCP and frames, motion limits, paths, jogging, force-threshold stop, and realtime `servoL`.

## Models and safe execution

The registered profiles are `diana3`, `diana7`, and `diana7-g2` for the Diana series, plus `thor7`, `thor12`, and `thor20` for the Thor series. A `thor7-pro` profile source file remains in the repository but is not currently enabled in the registry and cannot be passed to `--model`.

The program compares the selected profile with the joint count reported by the controller: seven axes identify the Diana series and six axes identify the Thor series. This detects a family/joint-count mismatch, but it cannot distinguish models with the same joint count. Select the exact profile from the robot nameplate and delivery records.

Pass the model and IP explicitly when connecting a physical robot, for example:

```bash
./build/bin/01_connection --model diana7 --ip 192.168.10.75
./build/bin/02_robot_state --model diana7 --ip 192.168.10.75
```

```{warning}
Any example that moves the robot requires confirmation of personnel, speed, payload, clearance, and emergency stop. Do not treat “the project compiles successfully” as authorization to move the robot.
```

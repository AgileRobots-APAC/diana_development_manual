# Examples Overview

The examples repository provides runnable Python scripts. They call the Diana API directly where possible; shared code only handles argument parsing, callbacks, waiting, logging, SDK loading, and model validation, and does not add another wrapper layer over the SDK.

```{note}
All examples have been verified on real robots; the "Execution Results" section of each example page contains the actual run output. Function prototypes, availability, and behavior are still defined by the current SDK `DianaApi.py`, its release notes, and the example source.
```

| Item | Value |
|---|---|
| Git repository | [diana_examples_python](https://github.com/AgileRobots-APAC/diana_examples_python.git) |
| SDK repository | [diana_sdk_python](https://github.com/AgileRobots-APAC/diana_sdk_python.git) |
| Example license | MIT License |
| Examples version | 1.0.0 (compatible with SDK 3.3.0) |
| SDK location | `third_party/diana_sdk_python/` |
| SDK wrapper | `third_party/diana_sdk_python/lib/DianaApi.py` |
| Run command | `python3 examples/<name>/main.py` |
| Output | Terminal logs; each example page includes real-robot output |

## Obtain and Validate

```bash
git clone --recurse-submodules https://github.com/AgileRobots-APAC/diana_examples_python.git
cd diana_examples_python
export PYTHONPATH="$PWD/third_party/diana_sdk_python/lib:$PYTHONPATH"
export LD_LIBRARY_PATH="$PWD/third_party/diana_sdk_python/lib:$LD_LIBRARY_PATH"
python3 examples/01_connection/main.py --list-models
```

For an existing checkout, run `git submodule update --init --recursive` to fetch the SDK.

## Repository Layout

```text
diana_examples_python/
├── common/                 # Shared helpers
├── robots/                 # Diana / Thor model profiles
├── examples/               # Runnable examples
├── docs/                   # Tutorials in the examples repository
└── third_party/diana_sdk_python/    # diana_sdk_python submodule
```

## Example List

<div class="example-list-table">

| Example | Purpose | Used API | Motion by default |
|---|---|---|---|
| [`01_connection`](01_connection.md) | Connection, version, model/joint-count validation, state, optional brake release/hold | <a href="01_connection.html#initsrv-destroysrv"><code>initSrv</code></a>, <a href="01_connection.html#initsrv-destroysrv"><code>destroySrv</code></a><br><a href="01_connection.html#getlibraryversion-getrobotstate-getjointcount"><code>getLibraryVersion</code></a>, <a href="01_connection.html#getlibraryversion-getrobotstate-getjointcount"><code>getRobotState</code></a>, <a href="01_connection.html#getlibraryversion-getrobotstate-getjointcount"><code>getJointCount</code></a><br><a href="01_connection.html#releasebrake-holdbrake"><code>releaseBrake</code></a>, <a href="01_connection.html#releasebrake-holdbrake"><code>holdBrake</code></a> | No |
| [`02_robot_state`](02_robot_state.md) | State, force, link, error/warning, and collision diagnostics | <a href="02_robot_state.html#getjointpos-getjointangularvel-getjointcurrent-getjointtorque"><code>getJointPos</code></a>, <a href="02_robot_state.html#getjointpos-getjointangularvel-getjointcurrent-getjointtorque"><code>getJointAngularVel</code></a>, <a href="02_robot_state.html#getjointpos-getjointangularvel-getjointcurrent-getjointtorque"><code>getJointCurrent</code></a>, <a href="02_robot_state.html#getjointpos-getjointangularvel-getjointcurrent-getjointtorque"><code>getJointTorque</code></a><br><a href="02_robot_state.html#gettcppos-gettcpexternalforce-gettcpforce-getjointforce"><code>getTcpPos</code></a>, <a href="02_robot_state.html#gettcppos-gettcpexternalforce-gettcpforce-getjointforce"><code>getTcpExternalForce</code></a>, <a href="02_robot_state.html#gettcppos-gettcpexternalforce-gettcpforce-getjointforce"><code>getTcpForce</code></a>, <a href="02_robot_state.html#gettcppos-gettcpexternalforce-gettcpforce-getjointforce"><code>getJointForce</code></a><br><a href="02_robot_state.html#getrobotstate-getlinkstate-getlasterror-getlastwarning-iscollision"><code>getRobotState</code></a>, <a href="02_robot_state.html#getrobotstate-getlinkstate-getlasterror-getlastwarning-iscollision"><code>getLinkState</code></a>, <a href="02_robot_state.html#getrobotstate-getlinkstate-getlasterror-getlastwarning-iscollision"><code>getLastError</code></a>, <a href="02_robot_state.html#getrobotstate-getlinkstate-getlasterror-getlastwarning-iscollision"><code>getLastWarning</code></a>, <a href="02_robot_state.html#getrobotstate-getlinkstate-getlasterror-getlastwarning-iscollision"><code>isCollision</code></a> | No, read-only |
| [`03_joint_motion`](03_joint_motion.md) | Joint motion | <a href="03_joint_motion.html#getjointpos"><code>getJointPos</code></a>, <a href="03_joint_motion.html#movejtotarget"><code>moveJToTarget</code></a> | No, requires `--run` |
| [`04_cartesian_motion`](04_cartesian_motion.md) | Cartesian linear motion | <a href="04_cartesian_motion.html#gettcppos"><code>getTcpPos</code></a>, <a href="04_cartesian_motion.html#moveltopose"><code>moveLToPose</code></a> | No, requires `--run` |
| [`05_kinematics`](05_kinematics.md) | Forward kinematics, inverse kinematics, reference-based inverse kinematics, and RPY/axis-angle conversion | <a href="05_kinematics.html#forward-inverse-inverse-ext"><code>forward</code></a>, <a href="05_kinematics.html#forward-inverse-inverse-ext"><code>inverse</code></a>, <a href="05_kinematics.html#forward-inverse-inverse-ext"><code>inverse_ext</code></a><br><a href="05_kinematics.html#rpy2axis-axis2rpy"><code>rpy2Axis</code></a>, <a href="05_kinematics.html#rpy2axis-axis2rpy"><code>axis2RPY</code></a> | No |
| [`06_io`](06_io.md) | DI / DO / AI / AO and bus electrical values | <a href="06_io.html#readdi-readdo-writedo"><code>readDI</code></a>, <a href="06_io.html#readdi-readdo-writedo"><code>readDO</code></a>, <a href="06_io.html#readdi-readdo-writedo"><code>writeDO</code></a><br><a href="06_io.html#readai-readao-writeao"><code>readAI</code></a>, <a href="06_io.html#readai-readao-writeao"><code>readAO</code></a>, <a href="06_io.html#readai-readao-writeao"><code>writeAO</code></a><br><a href="06_io.html#readbuscurrent-readbusvoltage"><code>readBusCurrent</code></a>, <a href="06_io.html#readbuscurrent-readbusvoltage"><code>readBusVoltage</code></a> | No; writes require explicit arguments |
| [`07_tcp_and_frames`](07_tcp_and_frames.md) | TCP, frames, payload, and tool-relative offset calculation | <a href="07_tcp_and_frames.html#gettcppos-getdefaultactivetcppose-getdefaultactivetcp-getdefaulttcpcoordinate-getdefaultworkpiececoordinate-getactivetcppayload"><code>getTcpPos</code></a>, <a href="07_tcp_and_frames.html#gettcppos-getdefaultactivetcppose-getdefaultactivetcp-getdefaulttcpcoordinate-getdefaultworkpiececoordinate-getactivetcppayload"><code>getDefaultActiveTcpPose</code></a>, <a href="07_tcp_and_frames.html#gettcppos-getdefaultactivetcppose-getdefaultactivetcp-getdefaulttcpcoordinate-getdefaultworkpiececoordinate-getactivetcppayload"><code>getDefaultActiveTcp</code></a>, <a href="07_tcp_and_frames.html#gettcppos-getdefaultactivetcppose-getdefaultactivetcp-getdefaulttcpcoordinate-getdefaultworkpiececoordinate-getactivetcppayload"><code>getDefaultTcpCoordinate</code></a>, <a href="07_tcp_and_frames.html#gettcppos-getdefaultactivetcppose-getdefaultactivetcp-getdefaulttcpcoordinate-getdefaultworkpiececoordinate-getactivetcppayload"><code>getDefaultWorkPieceCoordinate</code></a>, <a href="07_tcp_and_frames.html#gettcppos-getdefaultactivetcppose-getdefaultactivetcp-getdefaulttcpcoordinate-getdefaultworkpiececoordinate-getactivetcppayload"><code>getActiveTcpPayload</code></a><br><a href="07_tcp_and_frames.html#rpy2axis-pose2homogeneous-homogeneous2pose"><code>rpy2Axis</code></a>, <a href="07_tcp_and_frames.html#rpy2axis-pose2homogeneous-homogeneous2pose"><code>pose2Homogeneous</code></a>, <a href="07_tcp_and_frames.html#rpy2axis-pose2homogeneous-homogeneous2pose"><code>homogeneous2Pose</code></a> | No, read-only |
| [`08_motion_limits`](08_motion_limits.md) | Read controller motion limits | <a href="08_motion_limits.html#getjointspositionrange-getmaxjointsvel-getmaxjointsacc"><code>getJointsPositionRange</code></a>, <a href="08_motion_limits.html#getjointspositionrange-getmaxjointsvel-getmaxjointsacc"><code>getMaxJointsVel</code></a>, <a href="08_motion_limits.html#getjointspositionrange-getmaxjointsvel-getmaxjointsacc"><code>getMaxJointsAcc</code></a><br><a href="08_motion_limits.html#getmaxcarttranslationvel-getmaxcarttranslationacc-getmaxcartrotationvel-getmaxcartrotationacc"><code>getMaxCartTranslationVel</code></a>, <a href="08_motion_limits.html#getmaxcarttranslationvel-getmaxcarttranslationacc-getmaxcartrotationvel-getmaxcartrotationacc"><code>getMaxCartTranslationAcc</code></a>, <a href="08_motion_limits.html#getmaxcarttranslationvel-getmaxcarttranslationacc-getmaxcartrotationvel-getmaxcartrotationacc"><code>getMaxCartRotationVel</code></a>, <a href="08_motion_limits.html#getmaxcarttranslationvel-getmaxcarttranslationacc-getmaxcartrotationvel-getmaxcartrotationacc"><code>getMaxCartRotationAcc</code></a> | No, read-only |
| [`09_path_and_waypoints`](09_path_and_waypoints.md) | Basic and complex joint paths | <a href="09_path_and_waypoints.html#createpath-addmovej-runpath-destroypath"><code>createPath</code></a>, <a href="09_path_and_waypoints.html#createpath-addmovej-runpath-destroypath"><code>addMoveJ</code></a>, <a href="09_path_and_waypoints.html#createpath-addmovej-runpath-destroypath"><code>runPath</code></a>, <a href="09_path_and_waypoints.html#createpath-addmovej-runpath-destroypath"><code>destroyPath</code></a><br><a href="09_path_and_waypoints.html#createcomplexpath-addmovejsegmentbytarget-runcomplexpath-destroycomplexpath"><code>createComplexPath</code></a>, <a href="09_path_and_waypoints.html#createcomplexpath-addmovejsegmentbytarget-runcomplexpath-destroycomplexpath"><code>addMoveJSegmentByTarget</code></a>, <a href="09_path_and_waypoints.html#createcomplexpath-addmovejsegmentbytarget-runcomplexpath-destroycomplexpath"><code>runComplexPath</code></a>, <a href="09_path_and_waypoints.html#createcomplexpath-addmovejsegmentbytarget-runcomplexpath-destroycomplexpath"><code>destroyComplexPath</code></a> | No, requires `--run` |
| [`10_jog_motion`](10_jog_motion.md) | Short, low-speed jogs of J1, TCP translation, and TCP rotation | <a href="10_jog_motion.html#movejoint-movetcp-ex-rotationtcp-stop"><code>moveJoint</code></a>, <a href="10_jog_motion.html#movejoint-movetcp-ex-rotationtcp-stop"><code>moveTcp_ex</code></a>, <a href="10_jog_motion.html#movejoint-movetcp-ex-rotationtcp-stop"><code>rotationTCP</code></a>, <a href="10_jog_motion.html#movejoint-movetcp-ex-rotationtcp-stop"><code>stop</code></a> | No, requires `--run` |
| [`11_force_guarded_motion`](11_force_guarded_motion.md) | Low-speed Cartesian motion of up to 10 s with force-threshold stop | <a href="11_force_guarded_motion.html#speedl"><code>speedL</code></a>, <a href="11_force_guarded_motion.html#gettcpforce-stop"><code>getTcpForce</code></a>, <a href="11_force_guarded_motion.html#gettcpforce-stop"><code>stop</code></a> | No, requires `--run` |
| [`12_servoL_realtime`](12_servoL_realtime.md) | 10 ms-cycle `servoL_ex` sine trajectory of ±5 cm along Z | <a href="12_servoL_realtime.html#gettcppos"><code>getTcpPos</code></a>, <a href="12_servoL_realtime.html#servol-ex"><code>servoL_ex</code></a> | No, requires `--run` |

</div>

## Usage Principles

1. Start with connection, version, or state-reading examples that do not move the robot.
2. Explicitly select the robot model and IP address.
3. Use `--run` only after site safety conditions are satisfied.

The current examples cover, by function, connection, state, joint/Cartesian motion, kinematics, I/O, TCP and frames, motion limits, paths, jogging, force-threshold stop, and realtime `servoL`.

## Common Command-Line Options

| Option | Meaning |
|---|---|
| `--ip <address>` | Controller IP; defaults to `192.168.10.75` |
| `--model <name>` | Select a robot model explicitly; required for every real motion |
| `--list-models` | Print supported models and exit without loading the native SDK or connecting |
| `--run` | Available on motion examples; without it the example remains a dry run |

Example-specific options are `--enable` for `01_connection`, `--set-do` / `--set-ao` for `06_io`, `--offset` for `07_tcp_and_frames`, `--complex` for `09_path_and_waypoints`, and `--mode` / `--duration` for `10_jog_motion`. Their accepted formats are documented on the corresponding example pages.

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

## Models and Safety

Current model profiles include Diana `diana3`, `diana7`, `diana7-g2`, and Thor `thor7`, `thor12`, `thor20`. The scripts use `getJointCount()` to validate 7-axis Diana and 6-axis Thor families.

Pass the model and IP explicitly when connecting to a real robot, for example:

```bash
python3 examples/01_connection/main.py --model diana7 --ip 192.168.10.75
python3 examples/02_robot_state/main.py --model diana7 --ip 192.168.10.75
```

```{warning}
Any motion example requires personnel, speed, payload, clearance, and emergency-stop checks. A runnable script is not permission to move the robot.
```

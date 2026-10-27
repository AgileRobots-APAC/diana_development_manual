# Example 总览

Example 仓库提供可运行的 C++ 参考工程。它尽量直接调用 Diana API；公共代码只负责参数解析、回调、等待、日志和型号校验，不对 SDK 进行二次封装。

```{note}
各逐例页面还整理了《思灵机器人工业版 API 手册（C/C++ 版）V3.3.0》中与该示例相关的接口使用要点。函数签名、可用性和行为仍以当前 SDK 的头文件、发布说明和本 Example 源码为准。
```

| 项目 | 内容 |
|---|---|
| Git 仓库 | [diana_examples_cpp](https://github.com/AgileRobots-APAC/diana_examples_cpp.git) |
| SDK 仓库 | [diana_sdk_cpp](https://github.com/AgileRobots-APAC/diana_sdk_cpp.git) |
| Example 许可证 | MIT License |
| Example 版本 | 1.0.0（适配 SDK 3.3.0） |
| SDK 位置 | `third_party/diana_sdk_cpp/` |
| 构建系统 | CMake 3.10 及以上，C++11 |
| 输出目录 | `build/bin/` |

## 获取、构建与验证

```bash
git clone --recurse-submodules https://github.com/AgileRobots-APAC/diana_examples_cpp.git
cd diana_examples_cpp
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -- -j"$(getconf _NPROCESSORS_ONLN)"
export LD_LIBRARY_PATH="$PWD/third_party/diana_sdk_cpp/lib:$LD_LIBRARY_PATH"
./build/bin/01_connection --list-models
```

已克隆主仓库时，使用 `git submodule update --init --recursive` 获取 SDK。SDK 位于外部目录时，可在 CMake 配置中传入 `-DDIANA_SDK_DIR=/path/to/diana_sdk_cpp`。系统与工具链要求见[开发准备](../development.md)。

常用参数如下：

| 参数 | 说明 |
|---|---|
| `--ip <address>` | 指定控制器 IP；未指定时示例默认使用 `192.168.10.75`。也兼容将 IP 作为位置参数传入。 |
| `--model <name>` | 选择机器人 profile；运动示例使用 `--run` 时必须显式指定。 |
| `--run` | 允许运动示例实际下发命令；不带该参数时保持 dry-run。 |
| `--list-models` | 使用 `01_connection --list-models` 查看当前注册型号，不连接机器人。 |

## 仓库结构

```text
diana_examples_cpp/
├── common/                 # 参数解析、回调、等待与日志等辅助代码
├── robots/                 # Diana / Thor 型号 profile
├── examples/               # 可运行示例
├── docs/                   # examples 仓库自己的教程
└── third_party/diana_sdk_cpp/    # diana_sdk_cpp 子模块
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

## 示例清单

<div class="example-list-table">

| 示例 | 说明 | 使用的 API | 默认是否运动 |
|---|---|---|---|
| [`01_connection`](01_connection.md) | 连接、版本、型号/轴数识别、状态 | <a href="01_connection.html#initsrvnetinfo-initsrv-destroysrv"><code>initSrvNetInfo</code></a>、<a href="01_connection.html#initsrvnetinfo-initsrv-destroysrv"><code>initSrv</code></a>、<a href="01_connection.html#initsrvnetinfo-initsrv-destroysrv"><code>destroySrv</code></a><br><a href="01_connection.html#getlibraryversion-getrobotstate-getjointcount"><code>getLibraryVersion</code></a>、<a href="01_connection.html#getlibraryversion-getrobotstate-getjointcount"><code>getRobotState</code></a>、<a href="01_connection.html#getlibraryversion-getrobotstate-getjointcount"><code>getJointCount</code></a><br><a href="01_connection.html#releasebrake-holdbrake"><code>releaseBrake</code></a>、<a href="01_connection.html#releasebrake-holdbrake"><code>holdBrake</code></a> | 否 |
| [`02_robot_state`](02_robot_state.md) | 状态、外力、链路、错误/警告与碰撞诊断 | <a href="02_robot_state.html#getjointpos-getjointangularvel-getjointcurrent-getjointtorque"><code>getJointPos</code></a>、<a href="02_robot_state.html#getjointpos-getjointangularvel-getjointcurrent-getjointtorque"><code>getJointAngularVel</code></a>、<a href="02_robot_state.html#getjointpos-getjointangularvel-getjointcurrent-getjointtorque"><code>getJointCurrent</code></a>、<a href="02_robot_state.html#getjointpos-getjointangularvel-getjointcurrent-getjointtorque"><code>getJointTorque</code></a><br><a href="02_robot_state.html#gettcppos-gettcpexternalforce-gettcpforce-getjointforce"><code>getTcpPos</code></a>、<a href="02_robot_state.html#gettcppos-gettcpexternalforce-gettcpforce-getjointforce"><code>getTcpExternalForce</code></a>、<a href="02_robot_state.html#gettcppos-gettcpexternalforce-gettcpforce-getjointforce"><code>getTcpForce</code></a>、<a href="02_robot_state.html#gettcppos-gettcpexternalforce-gettcpforce-getjointforce"><code>getJointForce</code></a><br><a href="02_robot_state.html#getrobotstate-getlinkstate-getlasterror-getlastwarning-formaterror-iscollision"><code>getRobotState</code></a>、<a href="02_robot_state.html#getrobotstate-getlinkstate-getlasterror-getlastwarning-formaterror-iscollision"><code>getLinkState</code></a>、<a href="02_robot_state.html#getrobotstate-getlinkstate-getlasterror-getlastwarning-formaterror-iscollision"><code>getLastError</code></a>、<a href="02_robot_state.html#getrobotstate-getlinkstate-getlasterror-getlastwarning-formaterror-iscollision"><code>getLastWarning</code></a>、<a href="02_robot_state.html#getrobotstate-getlinkstate-getlasterror-getlastwarning-formaterror-iscollision"><code>formatError</code></a>、<a href="02_robot_state.html#getrobotstate-getlinkstate-getlasterror-getlastwarning-formaterror-iscollision"><code>isCollision</code></a> | 否，只读 |
| [`03_joint_motion`](03_joint_motion.md) | 关节运动 | <a href="03_joint_motion.html#getjointpos"><code>getJointPos</code></a>、<a href="03_joint_motion.html#movejtotarget"><code>moveJToTarget</code></a> | 否，需 `--run` |
| [`04_cartesian_motion`](04_cartesian_motion.md) | 笛卡尔直线运动 | <a href="04_cartesian_motion.html#gettcppos"><code>getTcpPos</code></a>、<a href="04_cartesian_motion.html#moveltopose"><code>moveLToPose</code></a> | 否，需 `--run` |
| [`05_kinematics`](05_kinematics.md) | 正解、逆解、参考逆解、RPY / 轴角转换 | <a href="05_kinematics.html#getjointpos-forward-inverse-inverse-ext"><code>getJointPos</code></a>、<a href="05_kinematics.html#getjointpos-forward-inverse-inverse-ext"><code>forward</code></a>、<a href="05_kinematics.html#getjointpos-forward-inverse-inverse-ext"><code>inverse</code></a>、<a href="05_kinematics.html#getjointpos-forward-inverse-inverse-ext"><code>inverse_ext</code></a><br><a href="05_kinematics.html#rpy2axis-axis2rpy"><code>rpy2Axis</code></a>、<a href="05_kinematics.html#rpy2axis-axis2rpy"><code>axis2RPY</code></a> | 否 |
| [`06_io`](06_io.md) | DI / DO / AI / AO、总线电参读取 | <a href="06_io.html#readdi-readdo-writedo"><code>readDI</code></a>、<a href="06_io.html#readdi-readdo-writedo"><code>readDO</code></a>、<a href="06_io.html#readdi-readdo-writedo"><code>writeDO</code></a><br><a href="06_io.html#readai-readao-writeao"><code>readAI</code></a>、<a href="06_io.html#readai-readao-writeao"><code>readAO</code></a>、<a href="06_io.html#readai-readao-writeao"><code>writeAO</code></a><br><a href="06_io.html#readbuscurrent-readbusvoltage"><code>readBusCurrent</code></a>、<a href="06_io.html#readbuscurrent-readbusvoltage"><code>readBusVoltage</code></a> | 否；写入需显式参数 |
| [`07_tcp_and_frames`](07_tcp_and_frames.md) | TCP、坐标系、负载与工具相对偏移计算 | <a href="07_tcp_and_frames.html#gettcppos-getdefaultactivetcppose-getdefaultactivetcp-getdefaulttcpcoordinate-getdefaultworkpiececoordinate-getactivetcppayload"><code>getTcpPos</code></a>、<a href="07_tcp_and_frames.html#gettcppos-getdefaultactivetcppose-getdefaultactivetcp-getdefaulttcpcoordinate-getdefaultworkpiececoordinate-getactivetcppayload"><code>getDefaultActiveTcpPose</code></a>、<a href="07_tcp_and_frames.html#gettcppos-getdefaultactivetcppose-getdefaultactivetcp-getdefaulttcpcoordinate-getdefaultworkpiececoordinate-getactivetcppayload"><code>getDefaultActiveTcp</code></a>、<a href="07_tcp_and_frames.html#gettcppos-getdefaultactivetcppose-getdefaultactivetcp-getdefaulttcpcoordinate-getdefaultworkpiececoordinate-getactivetcppayload"><code>getDefaultTcpCoordinate</code></a>、<a href="07_tcp_and_frames.html#gettcppos-getdefaultactivetcppose-getdefaultactivetcp-getdefaulttcpcoordinate-getdefaultworkpiececoordinate-getactivetcppayload"><code>getDefaultWorkPieceCoordinate</code></a>、<a href="07_tcp_and_frames.html#gettcppos-getdefaultactivetcppose-getdefaultactivetcp-getdefaulttcpcoordinate-getdefaultworkpiececoordinate-getactivetcppayload"><code>getActiveTcpPayload</code></a><br><a href="07_tcp_and_frames.html#rpy2axis-pose2homogeneous-homogeneous2pose"><code>rpy2Axis</code></a>、<a href="07_tcp_and_frames.html#rpy2axis-pose2homogeneous-homogeneous2pose"><code>pose2Homogeneous</code></a>、<a href="07_tcp_and_frames.html#rpy2axis-pose2homogeneous-homogeneous2pose"><code>homogeneous2Pose</code></a> | 否，只读 |
| [`08_motion_limits`](08_motion_limits.md) | 控制器实际运动限制读取 | <a href="08_motion_limits.html#getjointspositionrange-getmaxjointsvel-getmaxjointsacc"><code>getJointsPositionRange</code></a>、<a href="08_motion_limits.html#getjointspositionrange-getmaxjointsvel-getmaxjointsacc"><code>getMaxJointsVel</code></a>、<a href="08_motion_limits.html#getjointspositionrange-getmaxjointsvel-getmaxjointsacc"><code>getMaxJointsAcc</code></a><br><a href="08_motion_limits.html#getmaxcarttranslationvel-getmaxcarttranslationacc-getmaxcartrotationvel-getmaxcartrotationacc"><code>getMaxCartTranslationVel</code></a>、<a href="08_motion_limits.html#getmaxcarttranslationvel-getmaxcarttranslationacc-getmaxcartrotationvel-getmaxcartrotationacc"><code>getMaxCartTranslationAcc</code></a>、<a href="08_motion_limits.html#getmaxcarttranslationvel-getmaxcarttranslationacc-getmaxcartrotationvel-getmaxcartrotationacc"><code>getMaxCartRotationVel</code></a>、<a href="08_motion_limits.html#getmaxcarttranslationvel-getmaxcarttranslationacc-getmaxcartrotationvel-getmaxcartrotationacc"><code>getMaxCartRotationAcc</code></a> | 否，只读 |
| [`09_path_and_waypoints`](09_path_and_waypoints.md) | 基础或复杂多路点关节路径 | <a href="09_path_and_waypoints.html#createpath-addmovej-runpath-destroypath"><code>createPath</code></a>、<a href="09_path_and_waypoints.html#createpath-addmovej-runpath-destroypath"><code>addMoveJ</code></a>、<a href="09_path_and_waypoints.html#createpath-addmovej-runpath-destroypath"><code>runPath</code></a>、<a href="09_path_and_waypoints.html#createpath-addmovej-runpath-destroypath"><code>destroyPath</code></a><br><a href="09_path_and_waypoints.html#createcomplexpath-addmovejbytarget-runcomplexpath-destroycomplexpath"><code>createComplexPath</code></a>、<a href="09_path_and_waypoints.html#createcomplexpath-addmovejbytarget-runcomplexpath-destroycomplexpath"><code>addMoveJByTarget</code></a>、<a href="09_path_and_waypoints.html#createcomplexpath-addmovejbytarget-runcomplexpath-destroycomplexpath"><code>runComplexPath</code></a>、<a href="09_path_and_waypoints.html#createcomplexpath-addmovejbytarget-runcomplexpath-destroycomplexpath"><code>destroyComplexPath</code></a> | 否，需 `--run` |
| [`10_jog_motion`](10_jog_motion.md) | J1、TCP 平移与 TCP 旋转的低速短时长点动 | <a href="10_jog_motion.html#movejoint-movetcp-ex-rotationtcp-ex-stop"><code>moveJoint</code></a>、<a href="10_jog_motion.html#movejoint-movetcp-ex-rotationtcp-ex-stop"><code>moveTcp_ex</code></a>、<a href="10_jog_motion.html#movejoint-movetcp-ex-rotationtcp-ex-stop"><code>rotationTCP_ex</code></a>、<a href="10_jog_motion.html#movejoint-movetcp-ex-rotationtcp-ex-stop"><code>stop</code></a> | 否，需 `--run` |
| [`11_force_guarded_motion`](11_force_guarded_motion.md) | 最长 10 秒的低速笛卡尔力阈值停止 | <a href="11_force_guarded_motion.html#speedl"><code>speedL</code></a>、<a href="11_force_guarded_motion.html#gettcpforce-stop"><code>getTcpForce</code></a>、<a href="11_force_guarded_motion.html#gettcpforce-stop"><code>stop</code></a> | 否，需 `--run` |
| [`12_servoL_realtime`](12_servoL_realtime.md) | 10 ms 周期、Z 方向 ±5 cm 的 `servoL_ex` 正弦轨迹 | <a href="12_servoL_realtime.html#gettcppos"><code>getTcpPos</code></a>、<a href="12_servoL_realtime.html#servol-ex"><code>servoL_ex</code></a> | 否，需 `--run` |

</div>

## 使用原则

1. 先执行连接、版本或状态读取等不运动示例，验证 SDK 加载和网络。
2. 明确选择机器人型号与 IP 地址。
3. 只有在现场安全条件满足后，才使用 `--run` 执行运动示例。

当前示例按功能覆盖连接、状态、关节/笛卡尔运动、运动学、I/O、TCP 与坐标系、运动限制、路径、点动、力阈值停止和实时 `servoL`。

## 型号与安全运行

目前注册的型号 profile 包括 Diana 系列的 `diana3`、`diana7`、`diana7-g2`，以及 Thor 系列的 `thor7`、`thor12`、`thor20`。仓库中虽保留 `thor7-pro` 的 profile 源文件，但当前未在型号注册表中启用，因此不能传给 `--model`。

程序通过控制器报告的关节数检查所选 profile：7 轴对应 Diana 系列，6 轴对应 Thor 系列。该检查只能发现系列/轴数不匹配，不能区分同一系列内轴数相同的具体型号；用户仍需根据机械臂铭牌和交付资料选择正确 profile。

连接真机时显式传入型号和 IP，例如：

```bash
./build/bin/01_connection --model diana7 --ip 192.168.10.75
./build/bin/02_robot_state --model diana7 --ip 192.168.10.75
```

```{warning}
任何会使机械臂运动的 Example 都必须经过人员、速度、负载、净空与急停确认。不要把“工程编译成功”视为可以直接运动的授权。
```

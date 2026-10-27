# Example 总览

Example 仓库提供可运行的 Python 参考脚本。它尽量直接调用 Diana API；公共代码只负责参数解析、回调、等待、日志、SDK 加载和型号校验，不对 SDK 进行二次封装。

```{note}
全部 Example 已完成真机验证，逐例页面的“执行效果”区域附实际运行输出。函数原型、可用性和行为仍以当前 SDK 的 `DianaApi.py`、发布说明和本 Example 源码为准。
```

| 项目 | 内容 |
|---|---|
| Git 仓库 | [diana_examples_python](https://github.com/AgileRobots-APAC/diana_examples_python.git) |
| SDK 仓库 | [diana_sdk_python](https://github.com/AgileRobots-APAC/diana_sdk_python.git) |
| Example 许可证 | MIT License |
| Example 版本 | 1.0.0（适配 SDK 3.3.0） |
| SDK 位置 | `third_party/diana_sdk_python/` |
| SDK wrapper | `third_party/diana_sdk_python/lib/DianaApi.py` |
| 运行方式 | `python3 examples/<name>/main.py` |
| 输出形式 | 终端日志；逐例页面附真机运行输出 |

## 获取与验证

```bash
git clone --recurse-submodules https://github.com/AgileRobots-APAC/diana_examples_python.git
cd diana_examples_python
export PYTHONPATH="$PWD/third_party/diana_sdk_python/lib:$PYTHONPATH"
export LD_LIBRARY_PATH="$PWD/third_party/diana_sdk_python/lib:$LD_LIBRARY_PATH"
python3 examples/01_connection/main.py --list-models
```

已克隆主仓库时，使用 `git submodule update --init --recursive` 获取 SDK。

## 仓库结构

```text
diana_examples_python/
├── common/                 # 公共辅助代码
├── robots/                 # Diana / Thor 型号 profile
├── examples/               # 可运行示例
├── docs/                   # examples 仓库自己的教程
└── third_party/diana_sdk_python/    # diana_sdk_python 子模块
```

## 示例清单

<div class="example-list-table">

| 示例 | 说明 | 使用的 API | 默认是否运动 |
|---|---|---|---|
| [`01_connection`](01_connection.md) | 连接、版本、型号/轴数识别、状态、可选抱闸释放/保持 | <a href="01_connection.html#initsrv-destroysrv"><code>initSrv</code></a>、<a href="01_connection.html#initsrv-destroysrv"><code>destroySrv</code></a><br><a href="01_connection.html#getlibraryversion-getrobotstate-getjointcount"><code>getLibraryVersion</code></a>、<a href="01_connection.html#getlibraryversion-getrobotstate-getjointcount"><code>getRobotState</code></a>、<a href="01_connection.html#getlibraryversion-getrobotstate-getjointcount"><code>getJointCount</code></a><br><a href="01_connection.html#releasebrake-holdbrake"><code>releaseBrake</code></a>、<a href="01_connection.html#releasebrake-holdbrake"><code>holdBrake</code></a> | 否 |
| [`02_robot_state`](02_robot_state.md) | 状态、外力、链路、错误/警告与碰撞诊断 | <a href="02_robot_state.html#getjointpos-getjointangularvel-getjointcurrent-getjointtorque"><code>getJointPos</code></a>、<a href="02_robot_state.html#getjointpos-getjointangularvel-getjointcurrent-getjointtorque"><code>getJointAngularVel</code></a>、<a href="02_robot_state.html#getjointpos-getjointangularvel-getjointcurrent-getjointtorque"><code>getJointCurrent</code></a>、<a href="02_robot_state.html#getjointpos-getjointangularvel-getjointcurrent-getjointtorque"><code>getJointTorque</code></a><br><a href="02_robot_state.html#gettcppos-gettcpexternalforce-gettcpforce-getjointforce"><code>getTcpPos</code></a>、<a href="02_robot_state.html#gettcppos-gettcpexternalforce-gettcpforce-getjointforce"><code>getTcpExternalForce</code></a>、<a href="02_robot_state.html#gettcppos-gettcpexternalforce-gettcpforce-getjointforce"><code>getTcpForce</code></a>、<a href="02_robot_state.html#gettcppos-gettcpexternalforce-gettcpforce-getjointforce"><code>getJointForce</code></a><br><a href="02_robot_state.html#getrobotstate-getlinkstate-getlasterror-getlastwarning-iscollision"><code>getRobotState</code></a>、<a href="02_robot_state.html#getrobotstate-getlinkstate-getlasterror-getlastwarning-iscollision"><code>getLinkState</code></a>、<a href="02_robot_state.html#getrobotstate-getlinkstate-getlasterror-getlastwarning-iscollision"><code>getLastError</code></a>、<a href="02_robot_state.html#getrobotstate-getlinkstate-getlasterror-getlastwarning-iscollision"><code>getLastWarning</code></a>、<a href="02_robot_state.html#getrobotstate-getlinkstate-getlasterror-getlastwarning-iscollision"><code>isCollision</code></a> | 否，只读 |
| [`03_joint_motion`](03_joint_motion.md) | 关节运动 | <a href="03_joint_motion.html#getjointpos"><code>getJointPos</code></a>、<a href="03_joint_motion.html#movejtotarget"><code>moveJToTarget</code></a> | 否，需 `--run` |
| [`04_cartesian_motion`](04_cartesian_motion.md) | 笛卡尔直线运动 | <a href="04_cartesian_motion.html#gettcppos"><code>getTcpPos</code></a>、<a href="04_cartesian_motion.html#moveltopose"><code>moveLToPose</code></a> | 否，需 `--run` |
| [`05_kinematics`](05_kinematics.md) | 正解、逆解、参考逆解、RPY / 轴角转换 | <a href="05_kinematics.html#forward-inverse-inverse-ext"><code>forward</code></a>、<a href="05_kinematics.html#forward-inverse-inverse-ext"><code>inverse</code></a>、<a href="05_kinematics.html#forward-inverse-inverse-ext"><code>inverse_ext</code></a><br><a href="05_kinematics.html#rpy2axis-axis2rpy"><code>rpy2Axis</code></a>、<a href="05_kinematics.html#rpy2axis-axis2rpy"><code>axis2RPY</code></a> | 否 |
| [`06_io`](06_io.md) | DI / DO / AI / AO、总线电参读取 | <a href="06_io.html#readdi-readdo-writedo"><code>readDI</code></a>、<a href="06_io.html#readdi-readdo-writedo"><code>readDO</code></a>、<a href="06_io.html#readdi-readdo-writedo"><code>writeDO</code></a><br><a href="06_io.html#readai-readao-writeao"><code>readAI</code></a>、<a href="06_io.html#readai-readao-writeao"><code>readAO</code></a>、<a href="06_io.html#readai-readao-writeao"><code>writeAO</code></a><br><a href="06_io.html#readbuscurrent-readbusvoltage"><code>readBusCurrent</code></a>、<a href="06_io.html#readbuscurrent-readbusvoltage"><code>readBusVoltage</code></a> | 否；写入需显式参数 |
| [`07_tcp_and_frames`](07_tcp_and_frames.md) | TCP、坐标系、负载与工具相对偏移计算 | <a href="07_tcp_and_frames.html#gettcppos-getdefaultactivetcppose-getdefaultactivetcp-getdefaulttcpcoordinate-getdefaultworkpiececoordinate-getactivetcppayload"><code>getTcpPos</code></a>、<a href="07_tcp_and_frames.html#gettcppos-getdefaultactivetcppose-getdefaultactivetcp-getdefaulttcpcoordinate-getdefaultworkpiececoordinate-getactivetcppayload"><code>getDefaultActiveTcpPose</code></a>、<a href="07_tcp_and_frames.html#gettcppos-getdefaultactivetcppose-getdefaultactivetcp-getdefaulttcpcoordinate-getdefaultworkpiececoordinate-getactivetcppayload"><code>getDefaultActiveTcp</code></a>、<a href="07_tcp_and_frames.html#gettcppos-getdefaultactivetcppose-getdefaultactivetcp-getdefaulttcpcoordinate-getdefaultworkpiececoordinate-getactivetcppayload"><code>getDefaultTcpCoordinate</code></a>、<a href="07_tcp_and_frames.html#gettcppos-getdefaultactivetcppose-getdefaultactivetcp-getdefaulttcpcoordinate-getdefaultworkpiececoordinate-getactivetcppayload"><code>getDefaultWorkPieceCoordinate</code></a>、<a href="07_tcp_and_frames.html#gettcppos-getdefaultactivetcppose-getdefaultactivetcp-getdefaulttcpcoordinate-getdefaultworkpiececoordinate-getactivetcppayload"><code>getActiveTcpPayload</code></a><br><a href="07_tcp_and_frames.html#rpy2axis-pose2homogeneous-homogeneous2pose"><code>rpy2Axis</code></a>、<a href="07_tcp_and_frames.html#rpy2axis-pose2homogeneous-homogeneous2pose"><code>pose2Homogeneous</code></a>、<a href="07_tcp_and_frames.html#rpy2axis-pose2homogeneous-homogeneous2pose"><code>homogeneous2Pose</code></a> | 否，只读 |
| [`08_motion_limits`](08_motion_limits.md) | 控制器实际运动限制读取 | <a href="08_motion_limits.html#getjointspositionrange-getmaxjointsvel-getmaxjointsacc"><code>getJointsPositionRange</code></a>、<a href="08_motion_limits.html#getjointspositionrange-getmaxjointsvel-getmaxjointsacc"><code>getMaxJointsVel</code></a>、<a href="08_motion_limits.html#getjointspositionrange-getmaxjointsvel-getmaxjointsacc"><code>getMaxJointsAcc</code></a><br><a href="08_motion_limits.html#getmaxcarttranslationvel-getmaxcarttranslationacc-getmaxcartrotationvel-getmaxcartrotationacc"><code>getMaxCartTranslationVel</code></a>、<a href="08_motion_limits.html#getmaxcarttranslationvel-getmaxcarttranslationacc-getmaxcartrotationvel-getmaxcartrotationacc"><code>getMaxCartTranslationAcc</code></a>、<a href="08_motion_limits.html#getmaxcarttranslationvel-getmaxcarttranslationacc-getmaxcartrotationvel-getmaxcartrotationacc"><code>getMaxCartRotationVel</code></a>、<a href="08_motion_limits.html#getmaxcarttranslationvel-getmaxcarttranslationacc-getmaxcartrotationvel-getmaxcartrotationacc"><code>getMaxCartRotationAcc</code></a> | 否，只读 |
| [`09_path_and_waypoints`](09_path_and_waypoints.md) | 基础或复杂多路点关节路径 | <a href="09_path_and_waypoints.html#createpath-addmovej-runpath-destroypath"><code>createPath</code></a>、<a href="09_path_and_waypoints.html#createpath-addmovej-runpath-destroypath"><code>addMoveJ</code></a>、<a href="09_path_and_waypoints.html#createpath-addmovej-runpath-destroypath"><code>runPath</code></a>、<a href="09_path_and_waypoints.html#createpath-addmovej-runpath-destroypath"><code>destroyPath</code></a><br><a href="09_path_and_waypoints.html#createcomplexpath-addmovejsegmentbytarget-runcomplexpath-destroycomplexpath"><code>createComplexPath</code></a>、<a href="09_path_and_waypoints.html#createcomplexpath-addmovejsegmentbytarget-runcomplexpath-destroycomplexpath"><code>addMoveJSegmentByTarget</code></a>、<a href="09_path_and_waypoints.html#createcomplexpath-addmovejsegmentbytarget-runcomplexpath-destroycomplexpath"><code>runComplexPath</code></a>、<a href="09_path_and_waypoints.html#createcomplexpath-addmovejsegmentbytarget-runcomplexpath-destroycomplexpath"><code>destroyComplexPath</code></a> | 否，需 `--run` |
| [`10_jog_motion`](10_jog_motion.md) | J1、TCP 平移与 TCP 旋转的低速短时长点动 | <a href="10_jog_motion.html#movejoint-movetcp-ex-rotationtcp-stop"><code>moveJoint</code></a>、<a href="10_jog_motion.html#movejoint-movetcp-ex-rotationtcp-stop"><code>moveTcp_ex</code></a>、<a href="10_jog_motion.html#movejoint-movetcp-ex-rotationtcp-stop"><code>rotationTCP</code></a>、<a href="10_jog_motion.html#movejoint-movetcp-ex-rotationtcp-stop"><code>stop</code></a> | 否，需 `--run` |
| [`11_force_guarded_motion`](11_force_guarded_motion.md) | 最长 10 秒的低速笛卡尔力阈值停止 | <a href="11_force_guarded_motion.html#speedl"><code>speedL</code></a>、<a href="11_force_guarded_motion.html#gettcpforce-stop"><code>getTcpForce</code></a>、<a href="11_force_guarded_motion.html#gettcpforce-stop"><code>stop</code></a> | 否，需 `--run` |
| [`12_servoL_realtime`](12_servoL_realtime.md) | 10 ms 周期、Z 方向 ±5 cm 的 `servoL_ex` 正弦轨迹 | <a href="12_servoL_realtime.html#gettcppos"><code>getTcpPos</code></a>、<a href="12_servoL_realtime.html#servol-ex"><code>servoL_ex</code></a> | 否，需 `--run` |

</div>

## 使用原则

1. 先执行连接、版本或状态读取等不运动示例，验证 SDK 加载和网络。
2. 明确选择机器人型号与 IP 地址。
3. 只有在现场安全条件满足后，才使用 `--run` 执行运动示例。

当前示例按功能覆盖连接、状态、关节/笛卡尔运动、运动学、I/O、TCP 与坐标系、运动限制、路径、点动、力阈值停止和实时 `servoL`。

## 通用命令行参数

| 参数 | 说明 |
|---|---|
| `--ip <address>` | 机器人控制器 IP；未指定时默认 `192.168.10.75` |
| `--model <name>` | 显式选择机器人型号；所有真实运动都必须指定 |
| `--list-models` | 打印支持的型号后退出，不加载原生 SDK、不连接机器人 |
| `--run` | 仅运动示例提供；未指定时保持 dry-run |

各示例的专用参数包括：`01_connection` 的 `--enable`、`06_io` 的 `--set-do` / `--set-ao`、`07_tcp_and_frames` 的 `--offset`、`09_path_and_waypoints` 的 `--complex`，以及 `10_jog_motion` 的 `--mode` / `--duration`。具体格式见对应示例页。

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

## 型号与安全运行

目前的型号 profile 包括 Diana 系列的 `diana3`、`diana7`、`diana7-g2`，以及 Thor 系列的 `thor7`、`thor12`、`thor20`。程序会通过关节数查询校验 7 轴 Diana 与 6 轴 Thor 是否匹配。

连接真机时显式传入型号和 IP，例如：

```bash
python3 examples/01_connection/main.py --model diana7 --ip 192.168.10.75
python3 examples/02_robot_state/main.py --model diana7 --ip 192.168.10.75
```

```{warning}
任何会使机械臂运动的 Example 都必须经过人员、速度、负载、净空与急停确认。不要把“脚本能运行”视为可以直接运动的授权。
```

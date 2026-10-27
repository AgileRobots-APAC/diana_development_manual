# 07 TCP、坐标系与负载

该示例只读显示 TCP、默认坐标系和活动负载；指定 `--offset` 时仅在本地计算工具坐标系偏移后的目标位姿，不会修改控制器配置。

```bash
./build/bin/07_tcp_and_frames --model diana7 --ip 192.168.10.75
./build/bin/07_tcp_and_frames --model diana7 --ip 192.168.10.75 --offset=0,0,0.01,0,0,0
```

| API | 用途 |
|---|---|
| `getTcpPos` / `getDefaultActiveTcpPose` | 读取当前 TCP 和活动 TCP 相对法兰的位姿 |
| `getDefaultActiveTcp` / `getDefaultTcpCoordinate` / `getDefaultWorkPieceCoordinate` | 读取默认活动 TCP 相对法兰的 4x4 齐次矩阵，以及默认 TCP 坐标系和工件坐标系名称 |
| `getActiveTcpPayload` | 读取活动 TCP 负载 |
| `rpy2Axis` / `pose2Homogeneous` / `homogeneous2Pose` | 将偏移转为轴角和齐次矩阵，再得到目标位姿 |

## Example 调用流程

解析 `x,y,z,roll,pitch,yaw` 偏移（米、度）→ 读取控制器配置 → 将当前 TCP 矩阵与工具偏移矩阵相乘 → 输出计算结果 → 释放服务。

### 关键源码片段

```cpp
double tcp_pose[6] = {0.0};
double active_tcp_pose[6] = {0.0};
double payload[10] = {0.0};

getTcpPos(tcp_pose, ip);
getDefaultActiveTcpPose(active_tcp_pose, ip);
getActiveTcpPayload(payload, ip);

double offset_axis[6] = {offset[0], offset[1], offset[2],
                         offset[3] * kPi / 180.0,
                         offset[4] * kPi / 180.0,
                         offset[5] * kPi / 180.0};
rpy2Axis(offset_axis + 3);
pose2Homogeneous(tcp_pose, current_matrix);
pose2Homogeneous(offset_axis, offset_matrix);
multiply4x4(current_matrix, offset_matrix, target_matrix);
homogeneous2Pose(target_matrix, target_pose);
```
## 执行效果
::::{dropdown} 运行输出（无参数）
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/07_tcp_and_frames --model thor20 --ip 192.168.10.75
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-58344,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-43722,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-46522,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-54770,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-33062,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  6
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 6 (Thor series)
Selected model: Thor20 (expected 6 axes)
Current TCP pose:
  x : 0.764008 m
  y : 0.247045 m
  z : 0.653840 m
  rx: -0.593473 rad
  ry: 2.538024 rad
  rz: 0.050282 rad
Default active TCP pose relative to flange:
  x : 0.000000 m
  y : 0.000000 m
  z : 0.000000 m
  rx: 0.000000 rad
  ry: 0.000000 rad
  rz: 0.000000 rad
Default active TCP homogeneous matrix:
  1.000000 0.000000 0.000000 0.000000
  -0.000000 1.000000 0.000000 0.000000
  0.000000 -0.000000 1.000000 0.000000
  0.000000 0.000000 0.000000 1.000000
Default TCP coordinate: TestTCP
Default workpiece coordinate: Base
Active TCP payload:
  mass: 0.000000 kg
  center of mass: 0.000000, 0.000000, 0.000000 m
  inertia: 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000
Tool-relative offset: 0.000000, 0.000000, 0.010000, 0.000000, 0.000000, 0.000000 (m, deg)
Equivalent base-frame target (axis-angle):
  x : 0.764000 m
  y : 0.247044 m
  z : 0.663856 m
  rx: -0.593528 rad
  ry: 2.538010 rad
  rz: 0.050253 rad
Read-only example: no TCP, payload, or coordinate configuration is modified.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} 运行输出（--offset=0,0,0.01,0,0,0）
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/07_tcp_and_frames --model thor20 --ip 192.168.10.75 --offset=0,0,0.01,0,0,0
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-48060,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-46654,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-58932,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-59057,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-39286,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  6
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 6 (Thor series)
Selected model: Thor20 (expected 6 axes)
Current TCP pose:
  x : 0.764016 m
  y : 0.247031 m
  z : 0.653857 m
  rx: -0.593416 rad
  ry: 2.538024 rad
  rz: 0.050259 rad
Default active TCP pose relative to flange:
  x : 0.000000 m
  y : 0.000000 m
  z : 0.000000 m
  rx: 0.000000 rad
  ry: 0.000000 rad
  rz: 0.000000 rad
Default active TCP homogeneous matrix:
  1.000000 0.000000 0.000000 0.000000
  -0.000000 1.000000 0.000000 0.000000
  0.000000 -0.000000 1.000000 0.000000
  0.000000 0.000000 0.000000 1.000000
Default TCP coordinate: TestTCP
Default workpiece coordinate: Base
Active TCP payload:
  mass: 0.000000 kg
  center of mass: 0.000000, 0.000000, 0.000000 m
  inertia: 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000
Tool-relative offset: 0.000000, 0.000000, 0.010000, 0.000000, 0.000000, 0.000000 (m, deg)
Equivalent base-frame target (axis-angle):
  x : 0.764001 m
  y : 0.247043 m
  z : 0.663857 m
  rx: -0.593332 rad
  ry: 2.538046 rad
  rz: 0.050318 rad
Read-only example: no TCP, payload, or coordinate configuration is modified.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::

## 逐项 API 用法与调用案例

### `getTcpPos` / `getDefaultActiveTcpPose` / `getDefaultActiveTcp` / `getDefaultTcpCoordinate` / `getDefaultWorkPieceCoordinate` / `getActiveTcpPayload`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `getTcpPos` | `int getTcpPos(double *pose, const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败；完整参数说明见 <a href="02_robot_state.html#gettcppos-gettcpexternalforce-gettcpforce-getjointforce">02 机器人状态读取</a>。 |
| `getDefaultActiveTcpPose` | `int getDefaultActiveTcpPose(double *arrPose, const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败。 |
| `getDefaultActiveTcp` | `int getDefaultActiveTcp(double *default_tcp, const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败。 |
| `getDefaultTcpCoordinate` | `int getDefaultTcpCoordinate(char *tcpName, const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败。 |
| `getDefaultWorkPieceCoordinate` | `int getDefaultWorkPieceCoordinate(char *workpieceName, const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败。 |
| `getActiveTcpPayload` | `int getActiveTcpPayload(double *payload, const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `pose` / `arrPose` | 输出，`double[6]` | 六维位姿 `[x, y, z, rx, ry, rz]`；位置单位 m，姿态为轴角 rad。 |
| `default_tcp` | 输出，`double[16]` | 默认 TCP 相对法兰的 4x4 齐次变换矩阵。 |
| `tcpName` / `workpieceName` | 输出，`char*` | 默认 TCP 坐标系名称、默认工件坐标系名称；调用方负责提供足够大的字符缓冲区。 |
| `payload` | 输出，`double[10]` | 当前活动 TCP 负载参数数组；本例只展示质量等读数，不修改配置。 |
| `strIpAddress` | 输入，`const char*`，默认 `""` | 机械臂 IP；为空时仅适合单臂连接场景。 |

`getTcpPos` 读取当前默认 TCP 的 `[x,y,z,rx,ry,rz]`；`getDefaultActiveTcpPose` 读取活动 TCP 相对法兰的位姿。两者的平移单位为 m、旋转为轴角 rad，含义不能互换。

`getDefaultActiveTcp` 输出默认活动 TCP 相对法兰的 4x4 齐次变换矩阵（`double[16]`）；`getDefaultTcpCoordinate`、`getDefaultWorkPieceCoordinate` 返回控制器当前默认坐标系名称，本例为名称分配 256 字节缓冲区；`getActiveTcpPayload` 读取活动 TCP 负载。它们都是只读查询，本例不修改任何 TCP、工件坐标系或负载配置。

```{rubric} 调用案例
```

```cpp
double tcp_pose[6] = {0.0};
double active_tcp_pose[6] = {0.0};
getTcpPos(tcp_pose, "192.168.10.75");
getDefaultActiveTcpPose(active_tcp_pose, "192.168.10.75");

double payload[10] = {0.0};
if (getActiveTcpPayload(payload, "192.168.10.75") == 0) {
    printf("mass: %f kg\n", payload[0]);
}
```


````

### `rpy2Axis` / `pose2Homogeneous` / `homogeneous2Pose`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `rpy2Axis` | `int rpy2Axis(double *arr)` | `0` 表示成功，`-1` 表示失败；完整参数说明见 <a href="05_kinematics.html#rpy2axis-axis2rpy">05 运动学与姿态转换</a>。 |
| `pose2Homogeneous` | `int pose2Homogeneous(double *pose, double *matrix)` | `0` 表示成功，`-1` 表示失败。 |
| `homogeneous2Pose` | `int homogeneous2Pose(double *matrix, double *pose)` | `0` 表示成功，`-1` 表示失败。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `pose` | 输入或输出，`double[6]` | 六维位姿 `[x, y, z, rx, ry, rz]`；位置单位 m，姿态为轴角 rad。 |
| `matrix` | 输入或输出，`double[16]` | 4x4 齐次变换矩阵，按 API 约定的一维数组传入。 |
| `arr` | 输入输出，`double[3]` | 旋转数组，`rpy2Axis` 会原地把 RPY 转为轴角，单位 rad。 |

`rpy2Axis` 原地把 `--offset` 输入的 RPY（本例命令行以度输入后已转换为 rad）改为轴角；`pose2Homogeneous` 与 `homogeneous2Pose` 在六维位姿和 4×4 齐次矩阵间转换。

示例用 `T_base_tcp × T_tcp_offset` 在本地组合变换，所得结果仅供显示。若要执行该目标，仍须根据实际 TCP、工件坐标系、逆解和路径安全进行单独校验。

```{rubric} 调用案例
```

```cpp
double tcp_pose[6] = {0.0};
double matrix[16] = {0.0};
double pose_again[6] = {0.0};

getTcpPos(tcp_pose, "192.168.10.75");
pose2Homogeneous(tcp_pose, matrix);
homogeneous2Pose(matrix, pose_again);
```

````

### SDK V3.4 新增的工具坐标系接口

本示例没有使用下面四个接口，它们自 SDK V3.4 起提供，用于按工具名称管理工具坐标系。`arrPose` 是 TCP 相对于末端法兰的位姿，长度为 6：前三个为位置 XYZ（单位 m），后三个为轴角 RxRyRz（单位 rad）；工具名称需为 UTF-8 编码，长度不超过 255 个字符。

| 接口 | 作用 |
|---|---|
| `addTcpPose(strToolName, arrPose, strIpAddress)` | 新增工具坐标系 |
| `setTcpPoseByTcpName(strToolName, arrPose, strIpAddress)` | 修改指定名称的工具坐标系 |
| `deleteTcpPoseByTcpName(strToolName, strIpAddress)` | 删除指定名称的工具坐标系 |
| `switchTcpPoseByTcpName(strToolName, strIpAddress)` | 切换到指定名称的工具坐标系，使其成为默认生效的工具坐标系 |

返回值：`0` 表示成功，`-1` 表示失败。使用时请注意：

- 系统默认的 `Flange` 坐标系在任何情况下都不支持修改，也不支持删除。
- 修改或删除工具坐标系后，在该坐标系下设置的路点都会受到影响，请酌情使用。
- 修改的是当前生效的坐标系时，客户端修改值的生效有一个推送周期的延迟，需要等待一个推送周期，再使用 `forward`、`inverse` 等依赖最新工具坐标系的函数。
- 在阻抗模式下，如果修改的工具坐标系为默认工具坐标系，将返回失败。

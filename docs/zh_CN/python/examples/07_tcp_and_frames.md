# 07 TCP、坐标系与负载

本示例读取当前 TCP、默认 TCP、默认工具/工件坐标系和当前负载，并演示位姿矩阵转换。默认只读。

```bash
python3 examples/07_tcp_and_frames/main.py --model diana7 --ip 192.168.10.75
python3 examples/07_tcp_and_frames/main.py --model diana7 --ip 192.168.10.75 --offset=0,0,0.01,0,0,0
```

| API | 用途 |
|---|---|
| `getTcpPos` / `getDefaultActiveTcpPose` / `getDefaultActiveTcp` | 读取 TCP 位姿与默认 TCP |
| `getDefaultTcpCoordinate` / `getDefaultWorkPieceCoordinate` | 读取默认工具和工件坐标系 |
| `getActiveTcpPayload` | 读取当前活动 TCP 负载 |
| `rpy2Axis` / `pose2Homogeneous` / `homogeneous2Pose` | 位姿与齐次矩阵转换 |

## Example 调用流程

初始化连接 → 校验型号 → 读取当前 TCP 位姿 → 读取默认活动 TCP 位姿和齐次矩阵 → 读取默认工具/工件坐标系名 → 读取当前活动 TCP 负载 → 将用户输入的 `--offset` 从 RPY 转为轴角 → 计算工具相对目标位姿 → 释放资源。

### 关键源码片段

```python
tcp_pose = [0.0] * 6
active_tcp_pose = [0.0] * 6
active_tcp = [0.0] * 16
payload = [0.0] * 10

api.getTcpPos(tcp_pose, args.ip)
api.getDefaultActiveTcpPose(active_tcp_pose, args.ip)
api.getDefaultActiveTcp(active_tcp, args.ip)
api.getActiveTcpPayload(payload, args.ip)

rotation = [v * math.pi / 180.0 for v in args.offset[3:]]
api.rpy2Axis(rotation)
offset_axis = args.offset[:3] + rotation
api.pose2Homogeneous(tcp_pose, current_matrix)
api.pose2Homogeneous(offset_axis, offset_matrix)
api.homogeneous2Pose(target_matrix, target_pose)
```

## 执行效果
::::{dropdown} 运行输出（无参数）
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/07_tcp_and_frames/main.py --model thor20 --ip 192.168.10.75
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-45655,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-57565,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-48512,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-47295,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-38953,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  6
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 6 (Thor series)
Selected model: Thor20 (expected 6 axes)
Current TCP pose:
  x : 0.709417 m
  y : 0.375856 m
  z : 0.663535 m
  rx: -0.813284 rad
  ry: 2.480481 rad
  rz: 0.112364 rad
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
  mass=0.000000 kg
  center=(0.000000, 0.000000, 0.000000) m
  inertia=(0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000)
Tool-relative target pose:
  x : 0.709417 m
  y : 0.375856 m
  z : 0.663535 m
  rx: -0.813284 rad
  ry: 2.480481 rad
  rz: 0.112364 rad
Read-only example: no TCP, payload, or coordinate configuration is modified.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} 运行输出（--offset=0,0,0.01,0,0,0）
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/07_tcp_and_frames/main.py --model thor20 --ip 192.168.10.75 --offset=0,0,0.01,0,0,0
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-48817,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-47790,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-50978,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-39225,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-39894,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  6
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 6 (Thor series)
Selected model: Thor20 (expected 6 axes)
Current TCP pose:
  x : 0.709430 m
  y : 0.375828 m
  z : 0.663507 m
  rx: -0.813197 rad
  ry: 2.480548 rad
  rz: 0.112374 rad
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
  mass=0.000000 kg
  center=(0.000000, 0.000000, 0.000000) m
  inertia=(0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000)
Tool-relative target pose:
  x : 0.709430 m
  y : 0.375828 m
  z : 0.673507 m
  rx: -0.813197 rad
  ry: 2.480548 rad
  rz: 0.112374 rad
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
|---|---|---|
| `getTcpPos` | `getTcpPos(tcpPose, ipAddress='')` | 成功返回 True，失败返回 False |
| `getDefaultActiveTcpPose` | `getDefaultActiveTcpPose(arrPose, ipAddress='')` | 成功返回 True，失败返回 False |
| `getDefaultActiveTcp` | `getDefaultActiveTcp(default_tcp, ipAddress='')` | 成功返回 True，失败返回 False |
| `getDefaultTcpCoordinate` | `getDefaultTcpCoordinate(ipAddress='')` | 返回 `(success, name)` |
| `getDefaultWorkPieceCoordinate` | `getDefaultWorkPieceCoordinate(ipAddress='')` | 返回 `(success, name)` |
| `getActiveTcpPayload` | `getActiveTcpPayload(payload, ipAddress='')` | 成功返回 True，失败返回 False |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `tcpPose` | 输出，`list[float]`（长度 6） | `getTcpPos` 输出的当前 TCP 位姿 `[x, y, z, rx, ry, rz]`；位置单位 m，姿态为轴角 rad，原地写入。 |
| `arrPose` | 输出，`list[float]`（长度 6） | `getDefaultActiveTcpPose` 输出的默认活动 TCP 位姿；位置单位 m，姿态为轴角 rad，原地写入。 |
| `default_tcp` | 输出，`list[float]`（长度 16） | `getDefaultActiveTcp` 输出的默认工具坐标系 4x4 齐次矩阵，按 16 元素一维列表原地写入。 |
| `payload` | 输出，`list[float]`（长度 10） | `getActiveTcpPayload` 输出的负载信息：第 1 位为质量，第 2~4 位为质心，第 5~10 位为惯性张量；原地写入。 |
| `ipAddress` | 输入，`str`，默认 `''` | 机械臂 IP；为空时仅适合单臂连接场景。六个函数共用。`getDefaultTcpCoordinate` / `getDefaultWorkPieceCoordinate` 只有该参数，坐标系名称以返回元组中的 `str` 给出。 |

`getDefaultActiveTcpPose` 输出默认活动 TCP 相对法兰的位姿；`getDefaultActiveTcp` 输出 4x4 齐次矩阵；两个默认坐标系查询返回 `(success, name)`；`getActiveTcpPayload` 输出负载质量和质心等信息。示例只读取，不修改控制器配置。

```python
pose = [0.0] * 6
matrix = [0.0] * 16
payload = [0.0] * 10
api.getDefaultActiveTcpPose(pose, ip)
api.getDefaultActiveTcp(matrix, ip)
api.getActiveTcpPayload(payload, ip)
```

````

### `rpy2Axis` / `pose2Homogeneous` / `homogeneous2Pose`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
|---|---|---|
| `rpy2Axis` | `rpy2Axis(arr)` | 成功返回 True，失败返回 False |
| `pose2Homogeneous` | `pose2Homogeneous(pose, matrix)` | 成功返回 True，失败返回 False |
| `homogeneous2Pose` | `homogeneous2Pose(matrix, pose)` | 成功返回 True，失败返回 False |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `arr` | 输入输出，`list[float]`（长度 3） | `rpy2Axis` 的旋转数组，单位 rad；调用前为 RPY，成功后原地改为轴角。 |
| `pose` | 输入或输出，`list[float]`（长度 6） | 位姿向量 `[x, y, z, rx, ry, rz]`；位置单位 m，姿态为轴角 rad。在 `pose2Homogeneous` 中为输入（可为元组），在 `homogeneous2Pose` 中为输出（原地写入）。 |
| `matrix` | 输入或输出，`list[float]`（长度 16） | 4x4 齐次变换矩阵的 16 元素一维列表。在 `pose2Homogeneous` 中为输出（原地写入），在 `homogeneous2Pose` 中为输入（可为元组）。 |

`--offset=x,y,z,roll,pitch,yaw` 的平移单位为 m，RPY 角单位为度。示例把角度部分从 degree 转成 rad，再用 `rpy2Axis` 转为 SDK 位姿接口使用的轴角表示。随后把当前 TCP 位姿和偏移位姿分别转为齐次矩阵，在 Python 侧相乘后转回位姿。示例不会写入 TCP、坐标系或负载配置。

```python
rotation = [roll, pitch, yaw]
api.rpy2Axis(rotation)
offset_pose = [x, y, z] + rotation
api.pose2Homogeneous(offset_pose, offset_matrix)
```

````

### SDK V3.4 新增的工具坐标系接口

本示例没有使用下面四个接口，它们自 SDK V3.4 起提供，用于按工具名称管理工具坐标系。`arrPose` 是 TCP 相对于末端法兰的位姿，长度为 6：前三个为位置 XYZ（单位 m），后三个为轴角 RxRyRz（单位 rad）；工具名称需为 UTF-8 编码，长度不超过 255 个字符。

| 接口 | 作用 |
|---|---|
| `DianaApi.addTcpPose(strToolName, arrPose, ipAddress='')` | 新增工具坐标系 |
| `DianaApi.setTcpPoseByTcpName(strToolName, arrPose, ipAddress='')` | 修改指定名称的工具坐标系 |
| `DianaApi.deleteTcpPoseByTcpName(strToolName, ipAddress='')` | 删除指定名称的工具坐标系 |
| `DianaApi.switchTcpPoseByTcpName(strToolName, ipAddress='')` | 切换到指定名称的工具坐标系，使其成为默认生效的工具坐标系 |

返回值：`True` 表示成功，`False` 表示失败。使用时请注意：

- 系统默认的 `Flange` 坐标系在任何情况下都不支持修改，也不支持删除。
- 修改或删除工具坐标系后，在该坐标系下设置的路点都会受到影响，请酌情使用。
- 修改的是当前生效的坐标系时，客户端修改值的生效有一个推送周期的延迟，需要等待一个推送周期，再使用 `forward`、`inverse` 等依赖最新工具坐标系的函数。
- 在阻抗模式下，如果修改的工具坐标系为默认工具坐标系，将返回失败。

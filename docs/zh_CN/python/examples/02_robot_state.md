# 02 机器人状态与诊断

本示例读取关节、TCP、外力、链路查询结果、错误/警告和碰撞状态。默认只读，不触发运动。

```bash
python3 examples/02_robot_state/main.py --model diana7 --ip 192.168.10.75
```

| API | 用途 |
|---|---|
| `getJointPos` / `getJointAngularVel` / `getJointCurrent` / `getJointTorque` | 读取关节位置、速度、电流和力矩 |
| `getTcpPos` / `getTcpExternalForce` / `getTcpForce` / `getJointForce` | 读取 TCP 位姿和外力/力信息 |
| `getRobotState` / `getLinkState` | 读取机器人状态，并检查链路查询是否成功 |
| `getLastError` / `getLastWarning` / `formatError` / `isCollision` | 读取错误、警告和碰撞诊断 |

## Example 调用流程

初始化连接 → 校验 `--model` 与实际轴数 → 分配关节和 TCP 输出缓冲 → 读取关节位置、速度、电流和力矩 → 读取 TCP 位姿与外力 → 读取状态、链路、错误、警告和碰撞信息 → 释放资源。

### 关键源码片段

```python
joints = [0.0] * MAX_SUPPORTED_JOINT_COUNT
speeds = [0.0] * MAX_SUPPORTED_JOINT_COUNT
currents = [0.0] * MAX_SUPPORTED_JOINT_COUNT
torques = [0.0] * MAX_SUPPORTED_JOINT_COUNT
pose = [0.0] * 6

api.getJointPos(joints, args.ip)
api.getJointAngularVel(speeds, args.ip)
api.getJointCurrent(currents, args.ip)
api.getJointTorque(torques, args.ip)
api.getTcpPos(pose, args.ip)

print(f"TCP external resultant force: {api.getTcpExternalForce(args.ip)} N")
print(f"Robot state: {api.getRobotState(args.ip)}")
print(f"Link state: {api.getLinkState(args.ip)}")
print(f"Last error: {api.getLastError(args.ip)}")
print(f"Last warning: {api.getLastWarning(args.ip)}")
print(f"Collision detected: {'yes' if api.isCollision(args.ip) else 'no'}")
```

## 执行效果
::::{dropdown} 运行输出（Thor20示例）
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/02_robot_state/main.py --model thor20 --ip 192.168.10.75
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-42492,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-43551,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-55245,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-34016,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-42811,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  6
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 6 (Thor series)
Selected model: Thor20 (expected 6 axes)
Joint position:
  J1: 0.312738 rad
  J2: 0.076608 rad
  J3: 2.261263 rad
  J4: -0.020944 rad
  J5: 0.272060 rad
  J6: -0.131611 rad
Joint angular velocity (rad/s):
  J1: 0.000000
  J2: 0.000000
  J3: -0.000052
  J4: -0.000000
  J5: -0.000129
  J6: 0.000270
Joint current (A):
  J1: -0.030000
  J2: -0.090000
  J3: -0.020000
  J4: -0.070000
  J5: 0.010000
  J6: 0.010000
Joint torque (Nm):
  J1: 0.431070
  J2: -1.212400
  J3: -0.649380
  J4: -0.891480
  J5: -0.205460
  J6: 0.243340
TCP pose:
  x : 0.763940 m
  y : 0.246959 m
  z : 0.653544 m
  rx: -0.593250 rad
  ry: 2.538431 rad
  rz: 0.050236 rad
TCP external resultant force: 81.9007575821741 N
Robot state: 5 (hold-brake)
Diagnostics:
Link state: True
Last error: 0
Last warning: 0
Collision detected: no
TCP external wrench:
  Fx: -9.007881 N
  Fy: -8.589646 N
  Fz: 80.949430 N
  Tx: 2.472332 Nm
  Ty: 9.221275 Nm
  Tz: 3.166177 Nm
Joint external force/torque:
  J1: -1.162589
  J2: -59.554468
  J3: -44.517283
  J4: 1.909759
  J5: -2.672212
  J6: -0.135624
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} 运行输出（Diana7示例）
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/02_robot_state/main.py --model diana7 --ip 192.168.10.75
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-56183,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-42942,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-55733,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-54869,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-38425,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Joint position:
  J1: -0.143918 rad
  J2: -0.497597 rad
  J3: -0.016622 rad
  J4: 2.424481 rad
  J5: 0.041777 rad
  J6: -1.157364 rad
  J7: 0.025059 rad
Joint angular velocity (rad/s):
  J1: 0.000000
  J2: 0.000000
  J3: 0.000000
  J4: 0.000000
  J5: 0.000000
  J6: -0.000000
  J7: -0.000000
Joint current (A):
  J1: -0.010000
  J2: -0.080000
  J3: -0.010000
  J4: 0.000000
  J5: 0.000000
  J6: 0.000000
  J7: 0.000000
Joint torque (Nm):
  J1: -0.210170
  J2: -5.311310
  J3: -0.214400
  J4: -25.770260
  J5: 0.610545
  J6: 1.673125
  J7: 0.192860
TCP pose:
  x : 0.376633 m
  y : 0.059481 m
  z : 0.510095 m
  rx: -0.042810 rad
  ry: -0.060300 rad
  rz: 0.199412 rad
TCP external resultant force: 2.327428372392532 N
Robot state: 5 (hold-brake)
Diagnostics:
Link state: True
Last error: 0
Last warning: 0
Collision detected: no
TCP external wrench:
  Fx: -0.065114 N
  Fy: 0.515723 N
  Fz: -2.268637 N
  Tx: -0.099276 Nm
  Ty: -0.437782 Nm
  Tz: -0.241334 Nm
Joint external force/torque:
  J1: 0.169748
  J2: 0.446997
  J3: -0.201170
  J4: 0.811536
  J5: -0.021598
  J6: 0.198123
  J7: -0.194292
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop

```
::::

## 逐项 API 用法与调用案例

### `getJointPos` / `getJointAngularVel` / `getJointCurrent` / `getJointTorque`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
|---|---|---|
| `getJointPos` | `getJointPos(jointsPosition, ipAddress='')` | 成功返回 True，失败返回 False |
| `getJointAngularVel` | `getJointAngularVel(jointAngularVel, ipAddress='')` | 成功返回 True，失败返回 False |
| `getJointCurrent` | `getJointCurrent(jointCurrent, ipAddress='')` | 成功返回 True，失败返回 False |
| `getJointTorque` | `getJointTorque(jointTorque, ipAddress='')` | 成功返回 True，失败返回 False |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `jointsPosition` | 输出（原地写入），`list[float]`（长度 `JOINT_NUM`，不超过 7） | 各关节角度，单位 rad。调用方预先分配列表（如 `[0.0] * MAX_SUPPORTED_JOINT_COUNT`），wrapper 按列表长度从 7 元素 ctypes 数组逐项写回。 |
| `jointAngularVel` | 输出（原地写入），`list[float]`（长度 `JOINT_NUM`，不超过 7） | 各关节角速度，单位 rad/s。调用方预先分配列表（如 `[0.0] * MAX_SUPPORTED_JOINT_COUNT`），wrapper 按列表长度从 7 元素 ctypes 数组逐项写回。 |
| `jointCurrent` | 输出（原地写入），`list[float]`（长度 `JOINT_NUM`，不超过 7） | 各关节电流，单位 A。调用方预先分配列表（如 `[0.0] * MAX_SUPPORTED_JOINT_COUNT`），wrapper 按列表长度从 7 元素 ctypes 数组逐项写回。 |
| `jointTorque` | 输出（原地写入），`list[float]`（长度 `JOINT_NUM`，不超过 7） | 各关节真实扭矩（已减去零偏），单位 Nm。调用方预先分配列表（如 `[0.0] * MAX_SUPPORTED_JOINT_COUNT`），wrapper 按列表长度从 7 元素 ctypes 数组逐项写回。 |
| `ipAddress` | 输入，`str`，默认 `''` | 机械臂 IP 字符串，wrapper 编码为 UTF-8 `bytes` 后传给底层库；不填仅当只连接一台机械臂时生效。适用于全部四个函数。 |

| 函数 | 输出 | 单位 |
|---|---|---|
| `getJointPos` | 关节位置数组 | rad |
| `getJointAngularVel` | 关节角速度数组 | rad/s |
| `getJointCurrent` | 关节电流数组 | A |
| `getJointTorque` | 关节力矩数组 | Nm |

Python wrapper 会把传入的 list 当作输出缓冲写入。缓冲按最大支持轴数分配，展示时只使用 `getJointCount` 返回的实际轴数。

```python
joints = [0.0] * MAX_SUPPORTED_JOINT_COUNT
if api.getJointPos(joints, ip):
    for index in range(joint_count):
        print(f"J{index + 1}: {joints[index]:.6f} rad")
```

````

### `getTcpPos` / `getTcpExternalForce` / `getTcpForce` / `getJointForce`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
|---|---|---|
| `getTcpPos` | `getTcpPos(tcpPose, ipAddress='')` | 成功返回 True，失败返回 False |
| `getTcpExternalForce` | `getTcpExternalForce(ipAddress='')` | 返回 TCP 合外力标量 |
| `getTcpForce` | `getTcpForce(tcpForce, ipAddress='')` | 成功返回 True，失败返回 False |
| `getJointForce` | `getJointForce(jointForce, ipAddress='')` | 成功返回 True，失败返回 False |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `tcpPose` | 输出（原地写入），`list[float]`（长度至少 6） | TCP 位姿 `[x, y, z, rx, ry, rz]`；位置单位 m，姿态为轴角，单位 rad。wrapper 从 6 元素 ctypes 数组写回前 6 项；结果受 `setDefaultActiveTcp` 设置的默认 TCP 影响。 |
| `tcpForce` | 输出（原地写入），`list[float]`（长度至少 6） | TCP 所受外部六维力 `[Fx, Fy, Fz, Mx, My, Mz]`；力单位 N，力矩单位 Nm。wrapper 从 6 元素 ctypes 数组写回前 6 项；结果受默认 TCP 影响。 |
| `jointForce` | 输出（原地写入），`list[float]`（长度 `JOINT_NUM`，不超过 7） | 轴空间各关节所受外力（关节轴力矩），单位 Nm。调用方预先分配列表（如 `[0.0] * MAX_SUPPORTED_JOINT_COUNT`），wrapper 按列表长度从 7 元素 ctypes 数组逐项写回。 |
| `ipAddress` | 输入，`str`，默认 `''` | 机械臂 IP 字符串，wrapper 编码为 UTF-8 `bytes` 后传给底层库；不填仅当只连接一台机械臂时生效。适用于全部四个函数；`getTcpExternalForce` 仅此一个参数，返回 TCP 坐标系下合外力大小（`float`）。 |

TCP 位姿使用 `[x, y, z, rx, ry, rz]`，前三项单位为 m，后三项单位为 rad。`getTcpExternalForce` 返回合外力标量；`getTcpForce` 返回 `[Fx, Fy, Fz, Mx, My, Mz]`，前三项单位为 N，后三项单位为 Nm。

```python
tcp_pose = [0.0] * 6
tcp_force = [0.0] * 6
api.getTcpPos(tcp_pose, ip)
api.getTcpForce(tcp_force, ip)
```

````

### `getRobotState` / `getLinkState` / `getLastError` / `getLastWarning` / `isCollision`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
|---|---|---|
| `getRobotState` | `getRobotState(ipAddress='')` | 返回机器人状态码 |
| `getLinkState` | `getLinkState(ipAddress='')` | 当前 wrapper 仅返回调用成功/失败的布尔值，不暴露原始链路状态码 |
| `getLastError` | `getLastError(ipAddress='')` | 返回值以 SDK 当前实现和 API 手册为准 |
| `getLastWarning` | `getLastWarning(ipAddress='')` | 返回值以 SDK 当前实现和 API 手册为准 |
| `isCollision` | `isCollision(ipAddress='')` | 返回值以 SDK 当前实现和 API 手册为准 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `ipAddress` | 输入，`str`，默认 `''` | 机械臂 IP 字符串，wrapper 编码为 UTF-8 `bytes` 后传给底层库；不填仅当只连接一台机械臂时生效。适用于 `getRobotState`、`getLinkState`、`getLastError`、`getLastWarning` 和 `isCollision`。 |

这些接口用于读取控制器当前诊断上下文。当前 `DianaApi.py` 的 `getLinkState` 把原生返回值交给 `message()`，因此示例打印的 `Link state` 实际是布尔调用结果，不能作为链路状态枚举解释。发生错误、警告或碰撞时，应先按控制器状态和 API 手册完成处理，不要在未知状态下继续发送运动命令。

```python
state = api.getRobotState(ip)
link_state = api.getLinkState(ip)
last_error = api.getLastError(ip)
last_warning = api.getLastWarning(ip)
collision = api.isCollision(ip)
```

````

# 04 笛卡尔运动

本示例读取当前 TCP 位姿，计算一个小幅度笛卡尔直线目标。默认 dry-run，只打印目标；传入 `--run` 后才调用运动接口。

```bash
python3 examples/04_cartesian_motion/main.py --model diana7 --ip 192.168.10.75
python3 examples/04_cartesian_motion/main.py --model diana7 --ip 192.168.10.75 --run
```

| API | 用途 |
|---|---|
| `getTcpPos` | 读取当前 TCP 位姿 |
| `moveLToPose` | 按笛卡尔位姿执行直线运动 |

```{warning}
`--run` 会使机械臂运动。请检查整条直线运动路径，而不只是终点。
```

## Example 调用流程

校验 `--model` 与轴数 → 读取当前 TCP 位姿 → 复制起点并让基坐标系 Z 增加 10 mm → dry-run 时只打印目标 → `releaseBrake` 后等待 2 秒 → 调用 `moveLToPose` → 等待完成 → 抱闸并释放资源。

### 关键源码片段

```python
start = [0.0] * 6
api.getTcpPos(start, args.ip)

target = start[:]
target[2] += 0.01

if not args.run:
    print("DRY RUN: no motion command sent.")
    return 0

api.releaseBrake(args.ip)
time.sleep(2)
if not api.moveLToPose(target, 0.02, 0.05, 0, 0.0, 0.0, False, args.ip):
    api.stop(args.ip)
    api.holdBrake(args.ip)
    return 7
wait_move(api, args.ip)
api.holdBrake(args.ip)
```

## 执行效果
::::{dropdown} 运行输出（Thor20示例）
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/04_cartesian_motion/main.py --model thor20 --ip 192.168.10.75 --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-57542,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-57879,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-41498,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-48223,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-56610,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  6
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 6 (Thor series)
Selected model: Thor20 (expected 6 axes)
Current TCP pose:
  x : 0.709443 m
  y : 0.375895 m
  z : 0.653536 m
  rx: -0.813375 rad
  ry: 2.480432 rad
  rz: 0.112399 rad
Example target (Base Z + 10 mm):
  x : 0.709443 m
  y : 0.375895 m
  z : 0.663536 m
  rx: -0.813375 rad
  ry: 2.480432 rad
  rz: 0.112399 rad
Motion finished.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} 运行输出（Diana7示例）
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/04_cartesian_motion/main.py --model diana7 --ip 192.168.10.75 --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-49497,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-45958,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-51537,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-52034,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-39529,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Current TCP pose:
  x : 0.376643 m
  y : 0.059490 m
  z : 0.500145 m
  rx: -0.042813 rad
  ry: -0.060409 rad
  rz: 0.199425 rad
Example target (Base Z + 10 mm):
  x : 0.376643 m
  y : 0.059490 m
  z : 0.510145 m
  rx: -0.042813 rad
  ry: -0.060409 rad
  rz: 0.199425 rad
Motion finished.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop

```
::::

## 逐项 API 用法与调用案例

### `getTcpPos`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
|---|---|---|
| `getTcpPos` | `getTcpPos(tcpPose, ipAddress='')` | 成功返回 True，失败返回 False |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `tcpPose` | 输出（原地写入），`list[float]`（长度至少 6） | TCP 位姿 `[x, y, z, rx, ry, rz]`；位置单位 m，姿态为轴角，单位 rad。wrapper 从 6 元素 ctypes 数组写回前 6 项；结果受 `setDefaultActiveTcp` 设置的默认 TCP 影响。 |
| `ipAddress` | 输入，`str`，默认 `''` | 机械臂 IP 字符串，wrapper 编码为 UTF-8 `bytes` 后传给底层库；不填仅当只连接一台机械臂时生效。 |

`getTcpPos` 输出 `[x, y, z, rx, ry, rz]`。位置单位为 m，姿态单位为 rad（姿态为轴角旋转向量，不是 RPY 角）。本例只对当前 Z 方向增加 `0.01`，即 10 mm。

```python
pose = [0.0] * 6
if api.getTcpPos(pose, ip):
    pose[2] += 0.01
```

````

### `moveLToPose`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
|---|---|---|
| `moveLToPose` | `moveLToPose(pose, v, a, zv_shaper_order=0, zv_shaper_frequency=0, zv_shaper_damping_ratio=0, avoid_singular = False, ipAddress='')` | 成功返回 True，失败返回 False |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `pose` | 输入，`list[float]` / `tuple`（长度 6） | 终点 TCP 位姿 `[x, y, z, rx, ry, rz]`；位置单位 m，姿态为轴角，单位 rad。wrapper 读取前 6 项，并向底层固定传入空 `active_tcp`，因此使用默认 TCP（可由 `setDefaultActiveTcp` 设置）。 |
| `v` | 输入，`float` | 直线运动速度，单位 m/s。本例为 `0.02`。 |
| `a` | 输入，`float` | 直线运动加速度，单位 m/s²。本例为 `0.05`。 |
| `zv_shaper_order` | 输入，`int`，默认 `0` | 振动整形阶次，范围 [-1, 2]；`-1` 关闭整形。三个整形参数全为 `0` 时使用机械臂默认配置；任一不为 `0` 时使用传入的阶次值。本例为 `0`。 |
| `zv_shaper_frequency` | 输入，`float`，默认 `0` | 整形频率，单位 Hz，范围 [0, 1000]；为 `0` 时使用机械臂默认配置。本例为 `0.0`。 |
| `zv_shaper_damping_ratio` | 输入，`float`，默认 `0` | 整形阻尼比，范围 [0, 1]；为 `0` 时使用机械臂默认配置。本例为 `0.0`。 |
| `avoid_singular` | 输入，`bool`，默认 `False` | 是否开启奇异点避让。本例为 `False`。 |
| `ipAddress` | 输入，`str`，默认 `''` | 机械臂 IP 字符串，wrapper 编码为 UTF-8 `bytes` 后传给底层库；不填仅当只连接一台机械臂时生效。本例传入目标机械臂 IP。 |

`moveLToPose(target, v, a, ..., avoid_singular, ip)` 按笛卡尔目标位姿执行直线运动。本例速度为 `0.02 m/s`，加速度为 `0.05 m/s²`，并将 `avoid_singular` 设为 `False`。

```python
ok = api.moveLToPose(target, 0.02, 0.05, 0, 0.0, 0.0, False, ip)
if not ok:
    api.stop(ip)
```

````

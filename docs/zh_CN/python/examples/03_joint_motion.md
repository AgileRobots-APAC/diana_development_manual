# 03 关节运动

本示例读取当前关节位置，计算一个小幅度关节目标。默认 dry-run，只打印目标；传入 `--run` 后才调用运动接口。

```bash
python3 examples/03_joint_motion/main.py --model diana7 --ip 192.168.10.75
python3 examples/03_joint_motion/main.py --model diana7 --ip 192.168.10.75 --run
```

| API | 用途 |
|---|---|
| `getJointPos` | 读取当前关节位置 |
| `moveJToTarget` | 按关节目标执行运动 |

```{warning}
`--run` 会使机械臂运动。运行前必须确认型号、负载、速度、净空和急停条件。
```

## Example 调用流程

校验 `--model` 与轴数 → 读取当前关节角 → 复制起点并让 J1 增加 10° → 未指定 `--run` 时只打印目标并退出 → `releaseBrake` 后等待 2 秒 → 调用 `moveJToTarget` → 轮询等待运动完成 → `holdBrake` 并释放资源。

### 关键源码片段

```python
start = [0.0] * MAX_SUPPORTED_JOINT_COUNT
api.getJointPos(start, args.ip)

target = start[:]
target[0] += 10.0 * math.pi / 180.0

if not args.run:
    print("DRY RUN: no motion command sent.")
    return 0

api.releaseBrake(args.ip)
time.sleep(2)
if not api.moveJToTarget(target, 0.10, 0.20, 0, 0.0, 0.0, args.ip):
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
~/work/diana_examples_python$ python3 examples/03_joint_motion/main.py --model thor20 --ip 192.168.10.75 --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-34582,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-34151,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-51266,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-55633,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-41347,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  6
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 6 (Thor series)
Selected model: Thor20 (expected 6 axes)
Current joints:
  J1: 0.312762 rad
  J2: 0.076608 rad
  J3: 2.261251 rad
  J4: -0.020944 rad
  J5: 0.272108 rad
  J6: -0.131587 rad
Example target (J1 + 10 deg):
  J1: 0.487295 rad
  J2: 0.076608 rad
  J3: 2.261251 rad
  J4: -0.020944 rad
  J5: 0.272108 rad
  J6: -0.131587 rad
Motion finished.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} 运行输出（Diana7示例）
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/03_joint_motion/main.py --model diana7 --ip 192.168.10.75 --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-51985,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-44160,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-34124,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-46612,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-46894,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Current joints:
  J1: -0.457054 rad
  J2: -0.270963 rad
  J3: -0.044689 rad
  J4: 2.461908 rad
  J5: 0.012955 rad
  J6: -1.220401 rad
  J7: 0.126050 rad
Example target (J1 + 10 deg):
  J1: -0.282521 rad
  J2: -0.270963 rad
  J3: -0.044689 rad
  J4: 2.461908 rad
  J5: 0.012955 rad
  J6: -1.220401 rad
  J7: 0.126050 rad
Motion finished.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
## 逐项 API 用法与调用案例

### `getJointPos`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
|---|---|---|
| `getJointPos` | `getJointPos(jointsPosition, ipAddress='')` | 成功返回 True，失败返回 False |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `jointsPosition` | 输出（原地写入），`list[float]`（长度 `JOINT_NUM`，不超过 7） | 各关节角度，单位 rad。调用方预先分配列表（如 `[0.0] * MAX_SUPPORTED_JOINT_COUNT`），wrapper 按列表长度从 7 元素 ctypes 数组逐项写回。 |
| `ipAddress` | 输入，`str`，默认 `''` | 机械臂 IP 字符串，wrapper 编码为 UTF-8 `bytes` 后传给底层库；不填仅当只连接一台机械臂时生效。 |

运动示例不要凭空构造完整关节数组，而是先读取当前整组关节值，再在起点基础上生成小偏移目标。这样可以避免把未知关节写成 `0` 后造成大幅运动。

```python
joints = [0.0] * MAX_SUPPORTED_JOINT_COUNT
if api.getJointPos(joints, ip):
    joints[0] += 2.0 * math.pi / 180.0
```

````

### `moveJToTarget`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
|---|---|---|
| `moveJToTarget` | `moveJToTarget(joints, v, a, zv_shaper_order=0, zv_shaper_frequency=0, zv_shaper_damping_ratio=0, ipAddress='')` | 成功返回 True，失败返回 False |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `joints` | 输入，`list[float]`（长度 `JOINT_NUM`，不超过 7） | 终点关节角，单位 rad；wrapper 按列表长度复制到 7 元素 ctypes 数组。本例传入在当前关节位置上偏移后的 `target`。 |
| `v` | 输入，`float` | 关节速度，单位 rad/s。本例为 `0.10`。 |
| `a` | 输入，`float` | 关节加速度，单位 rad/s²。本例为 `0.20`。 |
| `zv_shaper_order` | 输入，`int`，默认 `0` | 振动整形阶次，范围 [-1, 2]；`-1` 关闭整形。三个整形参数全为 `0` 时使用机械臂默认配置；任一不为 `0` 时使用传入的阶次值。本例为 `0`。 |
| `zv_shaper_frequency` | 输入，`float`，默认 `0` | 整形频率，单位 Hz，范围 [0, 1000]；为 `0` 时使用机械臂默认配置。本例为 `0.0`。 |
| `zv_shaper_damping_ratio` | 输入，`float`，默认 `0` | 整形阻尼比，范围 [0, 1]；为 `0` 时使用机械臂默认配置。本例为 `0.0`。 |
| `ipAddress` | 输入，`str`，默认 `''` | 机械臂 IP 字符串，wrapper 编码为 UTF-8 `bytes` 后传给底层库；不填仅当只连接一台机械臂时生效。本例传入目标机械臂 IP。 |

成功下发运动命令不代表机器人已经到达目标。本例使用公共 `wait_move` 轮询 `getRobotState`，等待控制器从运行态退出。

```python
ok = api.moveJToTarget(target, 0.10, 0.20, 0, 0.0, 0.0, ip)
if not ok:
    api.stop(ip)
```

````

# 09 路径与路点

本示例演示基础路径和复杂路径的创建、添加路点、运行与销毁。默认 dry-run；传入 `--run` 后才执行路径运动。

```bash
python3 examples/09_path_and_waypoints/main.py --model diana7 --ip 192.168.10.75
python3 examples/09_path_and_waypoints/main.py --model diana7 --ip 192.168.10.75 --run
python3 examples/09_path_and_waypoints/main.py --model diana7 --ip 192.168.10.75 --complex --run
```

| API | 用途 |
|---|---|
| `createPath` / `addMoveJ` / `runPath` / `destroyPath` | 基础路径生命周期 |
| `createComplexPath` / `addMoveJSegmentByTarget` / `runComplexPath` / `destroyComplexPath` | 复杂路径生命周期 |

## Example 调用流程

校验 `--model` 与轴数 → 读取当前关节角 → 生成两个路点：J1 正向偏移和返回起点 → dry-run 时只打印路点 → `releaseBrake` 后等待 2 秒 → 按 `--complex` 选择基础路径或复杂路径 API → 添加两段关节运动 → 运行路径 → 销毁路径对象 → 抱闸并释放资源。

### 关键源码片段

```python
start = [0.0] * MAX_SUPPORTED_JOINT_COUNT
api.getJointPos(start, args.ip)
target = start[:]
target[0] += (15.0 if args.complex else 10.0) * math.pi / 180.0

if args.complex:
    ret_code, path_id = api.createComplexPath(api.complex_path_type.NORMAL_JOINT_PATH, args.ip)
    api.addMoveJSegmentByTarget(path_id, target, 0.10, 0.20, 0.0, 0, 0.0, 0.0, args.ip)
    api.addMoveJSegmentByTarget(path_id, start, 0.10, 0.20, 0.0, 0, 0.0, 0.0, args.ip)
    api.runComplexPath(path_id, args.ip)
    api.destroyComplexPath(path_id, args.ip)
else:
    ret_code, path_id = api.createPath(1, args.ip)
    api.addMoveJ(path_id, target, 0.10, 0.20, 0.0, args.ip)
    api.addMoveJ(path_id, start, 0.10, 0.20, 0.0, args.ip)
    api.runPath(path_id, args.ip)
    api.destroyPath(path_id, args.ip)
```

## 执行效果
::::{dropdown} 运行输出（无参数）
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/09_path_and_waypoints/main.py --model diana7 --ip 192.168.10.75
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-48838,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-46366,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-53739,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-54196,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-38264,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Path waypoint 1:
  J1: 0.030603 rad
  J2: -0.491868 rad
  J3: -0.016598 rad
  J4: 2.442949 rad
  J5: 0.042400 rad
  J6: -1.132989 rad
  J7: 0.023897 rad
Path waypoint 2 (return to current joints):
  J1: -0.143930 rad
  J2: -0.491868 rad
  J3: -0.016598 rad
  J4: 2.442949 rad
  J5: 0.042400 rad
  J6: -1.132989 rad
  J7: 0.023897 rad
DRY RUN: no path command sent.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} 运行输出（--run）
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/09_path_and_waypoints/main.py --model diana7 --ip 192.168.10.75 --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-56503,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-41369,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-53463,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-51508,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-34190,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Path waypoint 1:
  J1: 0.030603 rad
  J2: -0.491856 rad
  J3: -0.016586 rad
  J4: 2.442949 rad
  J5: 0.042388 rad
  J6: -1.133012 rad
  J7: 0.023897 rad
Path waypoint 2 (return to current joints):
  J1: -0.143930 rad
  J2: -0.491856 rad
  J3: -0.016586 rad
  J4: 2.442949 rad
  J5: 0.042388 rad
  J6: -1.133012 rad
  J7: 0.023897 rad
 [Debug] [runPath] new custom command is created, id = 1

 [Debug] [runPath] custom command is filled, id = 1

 [Debug] [runPath] custom command is running, id = 1

 [Debug] 192.168.10.75 [destroyCustomCommand] custom command is destroyed, id = 1

Path finished.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} 运行输出（--complex --run）
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/09_path_and_waypoints/main.py --model diana7 --ip 192.168.10.75 --complex --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-48935,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-43666,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-58337,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-36622,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-43701,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Complex-path waypoint 1:
  J1: 0.117881 rad
  J2: -0.491832 rad
  J3: -0.016598 rad
  J4: 2.442961 rad
  J5: 0.042364 rad
  J6: -1.133000 rad
  J7: 0.023885 rad
Path waypoint 2 (return to current joints):
  J1: -0.143918 rad
  J2: -0.491832 rad
  J3: -0.016598 rad
  J4: 2.442961 rad
  J5: 0.042364 rad
  J6: -1.133000 rad
  J7: 0.023885 rad
Path finished.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::

## 逐项 API 用法与调用案例

### `createPath` / `addMoveJ` / `runPath` / `destroyPath`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
|---|---|---|
| `createPath` | `createPath(id_type, ipAddress='')` | 返回 (ret_code, path_id)，ret_code == 0 表示成功 |
| `addMoveJ` | `addMoveJ(id_path, joints, vel, acc, blendradius, ipAddress='')` | 成功返回 True，失败返回 False |
| `runPath` | `runPath(id_path, ipAddress='')` | 成功返回 True，失败返回 False |
| `destroyPath` | `destroyPath(id_path, ipAddress='')` | 成功返回 True，失败返回 False |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `id_type` | 输入，`int` | 基础路径类型，封装直接按整数传入；`1` 表示 `moveJ`，`2` 表示 `moveL`；本例使用 `1`（moveJ 路径）。 |
| `id_path` | 输入，`ctypes.c_uint` 或 `int` | `createPath` 返回元组中的路径 ID（`ctypes.c_uint` 对象，可直接传回）；`addMoveJ`、`runPath`、`destroyPath` 必须使用同一个 ID。 |
| `joints` | 输入，`list[float]`（长度为实际轴数，最多 7） | 路点目标关节角，单位 rad；封装按列表长度逐项复制到 7 元素数组。 |
| `vel` | 输入，`float` | 移动到该路点的速度百分比（手册记为 `vel_percent`）；本例传 `0.10`。 |
| `acc` | 输入，`float` | 移动到该路点的加速度百分比（手册记为 `acc_percent`）；本例传 `0.20`。 |
| `blendradius` | 输入，`float` | 交融半径百分比（手册记为 `blendradius_percent`）；本例传 `0.0`。 |
| `ipAddress` | 输入，`str`，默认 `''` | 机械臂 IP，四个函数均使用；为空时仅适合单臂连接场景。 |

基础路径 API 适合组织简单的连续路点。路径对象创建后必须在结束时销毁；下发失败时应停止当前任务并清理路径资源。

```python
ret_code, path_id = api.createPath(1, ip)  # 1 = moveJ 路径
if ret_code == 0:
    api.addMoveJ(path_id, waypoint1, 0.10, 0.20, 0.0, ip)
    api.addMoveJ(path_id, waypoint2, 0.10, 0.20, 0.0, ip)
    api.runPath(path_id, ip)
    api.destroyPath(path_id, ip)
```

````

### `createComplexPath` / `addMoveJSegmentByTarget` / `runComplexPath` / `destroyComplexPath`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
|---|---|---|
| `createComplexPath` | `createComplexPath(path_type, ipAddress='')` | 返回 (ret_code, path_id)，ret_code == 0 表示成功 |
| `addMoveJSegmentByTarget` | `addMoveJSegmentByTarget(complex_path_id, joints, vel_percent, acc_percent, blendradius_percent, zv_shaper_order=0, zv_shaper_frequency=0, zv_shaper_damping_ratio=0, ipAddress='')` | 成功返回 True，失败返回 False |
| `runComplexPath` | `runComplexPath(complex_path_id, ipAddress='')` | 成功返回 True，失败返回 False |
| `destroyComplexPath` | `destroyComplexPath(complex_path_id, ipAddress='')` | 成功返回 True，失败返回 False |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `path_type` | 输入，`complex_path_type` 枚举 | 复杂路径类型，封装取 `.value` 传入：`NORMAL_JOINT_PATH`（MoveJ/MoveL/MoveC，传入关节角）、`MOVEP_JOINT_PATH`（MoveP，传入关节角）、`NORMAL_POSE_PATH`（MoveJ/MoveL/MoveC，传入 TCP 位姿）、`MOVEP_POSE_PATH`（MoveP，传入 TCP 位姿）；本例使用 `NORMAL_JOINT_PATH`。 |
| `complex_path_id` | 输入，`ctypes.c_uint` 或 `int` | `createComplexPath` 返回元组中的复杂路径 ID（`ctypes.c_uint` 对象，可直接传回）；`addMoveJSegmentByTarget`、`runComplexPath`、`destroyComplexPath` 必须使用同一个 ID。 |
| `joints` | 输入，`list[float]`（长度为实际轴数，最多 7） | 目标关节角，单位 rad；封装按列表长度逐项复制到 7 元素数组。 |
| `vel_percent` / `acc_percent` / `blendradius_percent` | 输入，`float` | 移动到目标路点的速度、加速度和交融半径百分比；本例传 `0.10` / `0.20` / `0.0`。 |
| `zv_shaper_order` | 输入，`int`，默认 `0` | 整形阶次，范围 `[-1, 2]`，`-1` 关闭整形；三个整形参数均为 `0` 时使用机械臂默认配置，任一不为 `0` 时使用传入的阶次。本例传 `0`。 |
| `zv_shaper_frequency` | 输入，`float`，默认 `0` | 整形频率，单位 Hz，范围 `[0, 1000]`；`0` 表示使用机械臂默认配置。 |
| `zv_shaper_damping_ratio` | 输入，`float`，默认 `0` | 整形阻尼比，范围 `[0, 1]`；`0` 表示使用机械臂默认配置。 |
| `ipAddress` | 输入，`str`，默认 `''` | 机械臂 IP，四个函数均使用；为空时仅适合单臂连接场景。 |

复杂路径 API 使用 `complex_path_type` 指定路径类型。本例选择 `NORMAL_JOINT_PATH`，通过 `addMoveJSegmentByTarget` 添加关节目标段。

```python
ret_code, path_id = api.createComplexPath(api.complex_path_type.NORMAL_JOINT_PATH, ip)
if ret_code == 0:
    api.addMoveJSegmentByTarget(path_id, waypoint, 0.10, 0.20, 0.0, 0, 0.0, 0.0, ip)
    api.runComplexPath(path_id, ip)
    api.destroyComplexPath(path_id, ip)
```

````

不带 `--complex` 时，示例将 J1 偏移 10 度并使用基础路径接口；带 `--complex` 时，将 J1 偏移 15 度并创建 `NORMAL_JOINT_PATH`。两种方式都会加入回到起点的路点。请检查每个返回值，在路径设置或执行失败时调用 `stop`，并在使用后销毁路径对象。

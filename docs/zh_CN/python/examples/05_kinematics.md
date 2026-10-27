# 05 运动学

本示例演示正解、逆解、参考逆解，以及 RPY 与轴角表示之间的转换。默认不运动机器人。

```bash
python3 examples/05_kinematics/main.py --model diana7 --ip 192.168.10.75
```

| API | 用途 |
|---|---|
| `getJointPos` | 获取当前关节作为计算输入 |
| `forward` | 由关节位置计算 TCP 位姿 |
| `inverse` / `inverse_ext` | 由 TCP 位姿计算关节解 |
| `rpy2Axis` / `axis2RPY` | 姿态表示转换 |

## Example 调用流程

初始化连接 → 校验型号与轴数 → 读取当前关节角 → 调用 `forward` 计算 TCP 位姿 → 调用 `inverse` 求一组逆解 → 调用 `inverse_ext` 求靠近当前关节的参考逆解 → 演示 RPY 与轴角转换 → 释放资源。

### 关键源码片段

```python
joints = [0.0] * MAX_SUPPORTED_JOINT_COUNT
pose = [0.0] * 6
inverse_joints = [0.0] * MAX_SUPPORTED_JOINT_COUNT
reference_solution = [0.0] * MAX_SUPPORTED_JOINT_COUNT

api.getJointPos(joints, args.ip)
api.forward(joints, pose, args.ip)
api.inverse(pose, inverse_joints, args.ip)
api.inverse_ext(joints, pose, reference_solution, args.ip)

rotation = [math.pi, math.pi / 3.0, math.pi / 6.0]
api.rpy2Axis(rotation)
api.axis2RPY(rotation)
```

## 执行效果
::::{dropdown} 运行输出（Thor20示例）
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/05_kinematics/main.py --model thor20 --ip 192.168.10.75
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-60285,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-52335,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-53390,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-44814,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-39161,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  6
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 6 (Thor series)
Selected model: Thor20 (expected 6 axes)
Forward kinematics result:
  x : 0.709453 m
  y : 0.375831 m
  z : 0.663533 m
  rx: -0.813242 rad
  ry: 2.480505 rad
  rz: 0.112341 rad
Inverse kinematics result:
  J1: 0.487324 rad
  J2: 0.066365 rad
  J3: 2.255955 rad
  J4: -0.020274 rad
  J5: 0.287691 rad
  J6: -0.132209 rad
Inverse solution near current joints (inverse_ext):
  J1: 0.487324 rad
  J2: 0.066365 rad
  J3: 2.255955 rad
  J4: -0.020274 rad
  J5: 0.287691 rad
  J6: -0.132209 rad
Original RPY: 3.141593, 1.047198, 0.523599
Axis-angle vector: 2.431323, 0.651471, -1.403725
Converted back to RPY: -3.141593, 1.047198, 0.523599
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} 运行输出（Diana7示例）
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/05_kinematics/main.py --model diana7 --ip 192.168.10.75
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-34890,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-42965,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-39521,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-57192,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-34704,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Forward kinematics result:
  x : 0.376637 m
  y : 0.059488 m
  z : 0.500142 m
  rx: -0.042819 rad
  ry: -0.060398 rad
  rz: 0.199418 rad
Inverse kinematics result:
  J1: -0.143903 rad
  J2: -0.491833 rad
  J3: -0.016611 rad
  J4: 2.442997 rad
  J5: 0.042358 rad
  J6: -1.133012 rad
  J7: 0.023880 rad
Inverse solution near current joints (inverse_ext):
  J1: -0.143918 rad
  J2: -0.491832 rad
  J3: -0.016598 rad
  J4: 2.442997 rad
  J5: 0.042364 rad
  J6: -1.133012 rad
  J7: 0.023873 rad
Original RPY: 3.141593, 1.047198, 0.523599
Axis-angle vector: 2.431323, 0.651471, -1.403725
Converted back to RPY: -3.141593, 1.047198, 0.523599
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::

## 逐项 API 用法与调用案例

### `forward` / `inverse` / `inverse_ext`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
|---|---|---|
| `forward` | `forward(joints, pose, ipAddress='')` | 成功返回 True，失败返回 False |
| `inverse` | `inverse(pose, joints, ipAddress='')` | 成功返回 True，失败返回 False |
| `inverse_ext` | `inverse_ext(ref_joints, pose, joints, ipAddress='')` | 成功返回 True，失败返回 False |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `joints` | 输入或输出，`list[float]`（长度 `JOINT_NUM`） | 关节角，单位 rad；在 `forward` 中为输入，在 `inverse` / `inverse_ext` 中为输出，wrapper 按列表长度原地写入逆解，因此必须传入可变列表。 |
| `ref_joints` | 输入，`list[float]`（长度 `JOINT_NUM`） | 参考关节角，单位 rad；`inverse_ext` 用它选择欧氏距离最近的逆解。 |
| `pose` | 输入或输出，`list[float]`（长度 6） | TCP 位姿 `[x, y, z, rx, ry, rz]`；位置单位 m，姿态为轴角 rad。在 `forward` 中为输出（原地写入 6 个元素），在 `inverse` / `inverse_ext` 中为输入。Python wrapper 不提供 `active_tcp` 参数，固定传空指针，即按控制器当前默认 TCP 计算。 |
| `ipAddress` | 输入，`str`，默认 `''` | 机械臂 IP；为空时仅适合单臂连接场景。`forward`、`inverse`、`inverse_ext` 共用。 |

`forward(joints, pose, ip)` 使用关节角计算 TCP 位姿，并写入 6 元素位姿。`inverse(pose, joints, ip)` 根据目标位姿求关节解；`inverse_ext(ref_joints, pose, joints, ip)` 使用参考关节角筛选更接近当前构型的解，适合希望保持构型连续的场景。运动前仍需校验关节限位和生成路径。

```python
current = [0.0] * MAX_SUPPORTED_JOINT_COUNT
pose = [0.0] * 6
solution = [0.0] * MAX_SUPPORTED_JOINT_COUNT

api.getJointPos(current, ip)
if api.forward(current, pose, ip):
    api.inverse_ext(current, pose, solution, ip)
```

````

### `rpy2Axis` / `axis2RPY`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
|---|---|---|
| `rpy2Axis` | `rpy2Axis(arr)` | 成功返回 True，失败返回 False |
| `axis2RPY` | `axis2RPY(arr)` | 成功返回 True，失败返回 False |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `arr` | 输入输出，`list[float]`（长度 3） | 旋转数组，单位 rad；`rpy2Axis` 输入 RPY、输出轴角，`axis2RPY` 输入轴角、输出 RPY。wrapper 把结果原地写回该列表，因此不能传元组。 |

Python 版转换接口会就地修改传入数组。调用 `rpy2Axis` 前数组表示 RPY；调用成功后同一数组变为轴角向量。反向调用 `axis2RPY` 时同理。若需同时保留原始值和转换结果，请先复制数组。

```python
rotation = [math.pi, math.pi / 3.0, math.pi / 6.0]
if api.rpy2Axis(rotation):
    print("axis-angle:", rotation)
if api.axis2RPY(rotation):
    print("rpy:", rotation)
```

````

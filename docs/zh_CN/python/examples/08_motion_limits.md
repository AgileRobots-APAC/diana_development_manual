# 08 运动限制

本示例读取控制器中的实际运动限制，包括关节范围、最大关节速度/加速度和最大笛卡尔速度/加速度。默认只读。

```bash
python3 examples/08_motion_limits/main.py --model diana7 --ip 192.168.10.75
```

| API | 用途 |
|---|---|
| `getJointsPositionRange` | 读取关节位置范围 |
| `getMaxJointsVel` / `getMaxJointsAcc` | 读取最大关节速度和加速度 |
| `getMaxCartTranslationVel` / `getMaxCartTranslationAcc` | 读取最大笛卡尔平移速度和加速度 |
| `getMaxCartRotationVel` / `getMaxCartRotationAcc` | 读取最大笛卡尔旋转速度和加速度 |

## Example 调用流程

初始化连接 → 校验型号与轴数 → 读取关节位置范围、最大关节速度和最大关节加速度 → 按实际轴数打印 → 读取笛卡尔平移/旋转速度和加速度限制 → 释放资源。

### 关键源码片段

```python
min_pos = [0.0] * MAX_SUPPORTED_JOINT_COUNT
max_pos = [0.0] * MAX_SUPPORTED_JOINT_COUNT
max_vel = [0.0] * MAX_SUPPORTED_JOINT_COUNT
max_acc = [0.0] * MAX_SUPPORTED_JOINT_COUNT

api.getJointsPositionRange(min_pos, max_pos, args.ip)
api.getMaxJointsVel(max_vel, args.ip)
api.getMaxJointsAcc(max_acc, args.ip)

translation_vel = api.getMaxCartTranslationVel(args.ip)
translation_acc = api.getMaxCartTranslationAcc(args.ip)
rotation_vel = api.getMaxCartRotationVel(args.ip)
rotation_acc = api.getMaxCartRotationAcc(args.ip)
```

## 执行效果
::::{dropdown} 运行输出（Thor20示例）
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/08_motion_limits/main.py --model thor20 --ip 192.168.10.75
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-50119,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-44513,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-42530,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-47834,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-40641,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  6
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 6 (Thor series)
Selected model: Thor20 (expected 6 axes)
Joint limits (rad, rad/s, rad/s^2):
  J1: [-6.283185, 6.283185], vel=2.094395, acc=6.108652
  J2: [-3.141593, 3.141593], vel=2.094395, acc=1.221730
  J3: [-2.967060, 2.967060], vel=2.617994, acc=4.363323
  J4: [-6.283185, 6.283185], vel=3.665191, acc=34.906585
  J5: [-6.283185, 6.283185], vel=3.665191, acc=34.906585
  J6: [-6.283185, 6.283185], vel=3.665191, acc=34.906585
Cartesian limits: translation vel=(True, 2.8) m/s, acc=(True, 8.7) m/s^2, rotation vel=(True, 3.6651914289999996) rad/s, acc=(True, 34.906585) rad/s^2
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop

```
::::
::::{dropdown} 运行输出（Diana7示例）
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/08_motion_limits/main.py --model diana7 --ip 192.168.10.75
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-60396,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-42599,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-58478,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-36851,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-43014,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Joint limits (rad, rad/s, rad/s^2):
  J1: [-3.124139, 3.124139], vel=2.967060, acc=11.868239
  J2: [-1.570796, 1.570796], vel=2.617994, acc=9.424778
  J3: [-3.124139, 3.124139], vel=2.617994, acc=9.424778
  J4: [0.000000, 3.054326], vel=2.617994, acc=9.424778
  J5: [-3.124139, 3.124139], vel=3.141593, acc=15.707963
  J6: [-3.124139, 3.124139], vel=3.141593, acc=15.707963
  J7: [-3.124139, 3.124139], vel=3.141593, acc=15.707963
Cartesian limits: translation vel=(True, 1.5) m/s, acc=(True, 5.0) m/s^2, rotation vel=(True, 3.1415926535900005) rad/s, acc=(True, 12.566370614400002) rad/s^2
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::

## 逐项 API 用法与调用案例

### `getJointsPositionRange` / `getMaxJointsVel` / `getMaxJointsAcc`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
|---|---|---|
| `getJointsPositionRange` | `getJointsPositionRange(arrMin, arrMax, ipAddress = '')` | 成功返回 True，失败返回 False |
| `getMaxJointsVel` | `getMaxJointsVel(arrVel, ipAddress = '')` | 成功返回 True，失败返回 False |
| `getMaxJointsAcc` | `getMaxJointsAcc(arrAcc, ipAddress = '')` | 成功返回 True，失败返回 False |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `arrMin` | 输出，`list[float]`（长度 `JOINT_NUM`） | 各关节最小极限位，单位 rad；wrapper 按列表长度原地写入。 |
| `arrMax` | 输出，`list[float]`（长度 `JOINT_NUM`） | 各关节最大极限位，单位 rad；wrapper 按列表长度原地写入。 |
| `arrVel` | 输出，`list[float]`（长度 `JOINT_NUM`） | 各关节最大软速度，单位 rad/s；原地写入。 |
| `arrAcc` | 输出，`list[float]`（长度 `JOINT_NUM`） | 各关节最大软加速度，单位 rad/s²；原地写入。 |
| `ipAddress` | 输入，`str`，默认 `''` | 机械臂 IP；为空时仅适合单臂连接场景。三个函数共用。 |

关节位置范围单位为 rad，关节速度为 rad/s，关节加速度为 rad/s²。示例读取的是控制器当前配置，不是文档中的理论值。

```python
min_pos = [0.0] * MAX_SUPPORTED_JOINT_COUNT
max_pos = [0.0] * MAX_SUPPORTED_JOINT_COUNT
api.getJointsPositionRange(min_pos, max_pos, ip)
```

````

### `getMaxCartTranslationVel` / `getMaxCartTranslationAcc` / `getMaxCartRotationVel` / `getMaxCartRotationAcc`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
|---|---|---|
| `getMaxCartTranslationVel` | `getMaxCartTranslationVel(ipAddress = '')` | 返回 `(success, value)` |
| `getMaxCartTranslationAcc` | `getMaxCartTranslationAcc(ipAddress = '')` | 返回 `(success, value)` |
| `getMaxCartRotationVel` | `getMaxCartRotationVel(ipAddress = '')` | 返回 `(success, value)` |
| `getMaxCartRotationAcc` | `getMaxCartRotationAcc(ipAddress = '')` | 返回 `(success, value)` |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `ipAddress` | 输入，`str`，默认 `''` | 机械臂 IP；为空时仅适合单臂连接场景。四个函数唯一的参数；限制值以返回元组第二项 `float` 给出：平移速度 m/s、平移加速度 m/s²、旋转速度 rad/s、旋转加速度 rad/s²。 |

以上四个 Python wrapper 接口返回 `(success, value)` 二元组，使用时应先检查布尔值再读取数值。平移限制以 m/s 和 m/s² 表示，旋转限制以 rad/s 和 rad/s² 表示。实际可用速度还会受到安全配置、负载、轨迹规划和现场风险评估约束。

```python
ok, translation_vel = api.getMaxCartTranslationVel(ip)
ok, translation_acc = api.getMaxCartTranslationAcc(ip)
ok, rotation_vel = api.getMaxCartRotationVel(ip)
ok, rotation_acc = api.getMaxCartRotationAcc(ip)
```

````

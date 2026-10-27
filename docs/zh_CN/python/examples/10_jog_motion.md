# 10 点动运动

本示例演示 J1 点动、TCP 平移和 TCP 旋转。默认 dry-run；传入 `--run` 后执行低速短时长点动，并在结束时调用停止。

```bash
python3 examples/10_jog_motion/main.py --model diana7 --ip 192.168.10.75
python3 examples/10_jog_motion/main.py --model diana7 --ip 192.168.10.75 --mode joint --duration=0.5 --run
python3 examples/10_jog_motion/main.py --model diana7 --ip 192.168.10.75 --mode tcp --duration=0.5 --run
python3 examples/10_jog_motion/main.py --model diana7 --ip 192.168.10.75 --mode rotate --duration=0.5 --run
```

| API | 用途 |
|---|---|
| `moveJoint` | 关节点动 |
| `moveTcp_ex` | TCP 平移点动 |
| `rotationTCP` | TCP 旋转点动 |
| `stop` | 停止当前任务 |

## Example 调用流程

校验 `--model` 与轴数 → 校验 `--duration` 在 0.1 到 2.0 秒之间 → 打印将执行的点动模式 → dry-run 时退出 → `releaseBrake` 后等待 2 秒 → 根据 `--mode` 调用关节点动、TCP 平移或 TCP 旋转 → 等待指定时长 → `stop` → `holdBrake` → 释放资源。

### 关键源码片段

```python
if args.mode == "joint":
    ok = api.moveJoint(api.joint_direction_e.T_MOVE_UP, 0, 0.05, 0.10, args.ip)
elif args.mode == "tcp":
    ok = api.moveTcp_ex(
        api.coordinate_e.E_BASE_COORDINATE,
        api.tcp_direction_e.T_MOVE_X_UP,
        0.01,
        0.02,
        args.ip,
    )
else:
    ok = api.rotationTCP(api.tcp_direction_e.T_MOVE_Z_UP, 0.05, 0.10, args.ip)

time.sleep(args.duration)
api.stop(args.ip)
api.holdBrake(args.ip)
```

## 执行效果
::::{dropdown} 运行输出（无参数）
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/10_jog_motion/main.py --model diana7 --ip 192.168.10.75
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-40543,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-51013,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-49815,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-41867,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-46164,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Jog J1 positive for 0.5 s at low speed.
DRY RUN
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} 运行输出（--mode joint --duration=0.5 --run）
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/10_jog_motion/main.py --model diana7 --ip 192.168.10.75 --mode joint --duration=0.5 --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-40179,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-39395,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-49354,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-56934,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-48961,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Jog J1 positive for 0.5 s at low speed.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} 运行输出（--mode tcp --duration=0.5 --run）
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/10_jog_motion/main.py --model diana7 --ip 192.168.10.75 --mode tcp --duration=0.5 --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-33626,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-36893,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-43167,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-35744,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-57025,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Jog TCP along base +X for 0.5 s at low speed.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} 运行输出（--mode rotate --duration=0.5 --run）
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/10_jog_motion/main.py --model diana7 --ip 192.168.10.75 --mode rotate --duration=0.5 --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-52131,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-49313,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-35287,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-49985,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-51242,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Rotate TCP about base +Z for 0.5 s at low speed.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::

## 逐项 API 用法与调用案例

### `moveJoint` / `moveTcp_ex` / `rotationTCP` / `stop`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
|---|---|---|
| `moveJoint` | `moveJoint(d, i, v, a, ipAddress='')` | 成功返回 True，失败返回 False |
| `moveTcp_ex` | `moveTcp_ex(coordinate, direction, velocity, accleartion, ipAddress='')` | 成功返回 True，失败返回 False |
| `rotationTCP` | `rotationTCP(d, v, a, ipAddress='')` | 成功返回 True，失败返回 False |
| `stop` | `stop(ipAddress='')` | 成功返回 True，失败返回 False |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `d` | 输入，`joint_direction_e` 或 `tcp_direction_e` 枚举 | 封装取 `.value` 传入。`moveJoint` 使用 `joint_direction_e`：`T_MOVE_UP` 正向、`T_MOVE_DOWN` 负向；`rotationTCP` 使用 `tcp_direction_e`（`T_MOVE_X_UP` … `T_MOVE_Z_DOWN`）表示旋转方向。 |
| `i` | 输入，`int` | `moveJoint` 的关节索引，从 `0` 开始；`0` 对应 J1。 |
| `coordinate` | 输入，`coordinate_e` 枚举 | `moveTcp_ex` 的坐标系：`E_BASE_COORDINATE` 基坐标系、`E_TOOL_COORDINATE` 工具坐标系、`E_WORK_PIECE_COORDINATE` 工件坐标系、`E_VIEW_COORDINATE` 视角坐标系；非该枚举实例时封装抛出 `TypeError`。 |
| `direction` | 输入，`tcp_direction_e` 枚举 | `moveTcp_ex` 的移动方向：`T_MOVE_X_UP` / `T_MOVE_X_DOWN`、`T_MOVE_Y_UP` / `T_MOVE_Y_DOWN`、`T_MOVE_Z_UP` / `T_MOVE_Z_DOWN` 分别表示沿 x、y、z 轴正向 / 负向；非该枚举实例时封装抛出 `TypeError`。 |
| `v` | 输入，`float` | `moveJoint` / `rotationTCP` 的速度，单位 rad/s。 |
| `a` | 输入，`float` | `moveJoint` / `rotationTCP` 的加速度，单位 rad/s²。 |
| `velocity` | 输入，`float` | `moveTcp_ex` 的速度，单位 m/s。 |
| `accleartion` | 输入，`float` | `moveTcp_ex` 的加速度，单位 m/s²；参数名按封装原样拼写。 |
| `ipAddress` | 输入，`str`，默认 `''` | 机械臂 IP，四个函数均使用；为空时仅适合单臂连接场景。 |

| 模式 | API | 示例动作 |
|---|---|---|
| `joint` | `moveJoint` | J1 正向低速点动（`0.05 rad/s`） |
| `tcp` | `moveTcp_ex` | 基坐标系 +X 方向 TCP 平移（`0.01 m/s`） |
| `rotate` | `rotationTCP` | 绕基坐标系 +Z 旋转（`0.05 rad/s`） |

点动类接口会持续运动，直到持续时间结束、调用 `stop` 或控制器因其他条件停止。本示例限制 `--duration` 为 0.1 到 2.0 秒，并在每次执行后主动调用 `stop`。

```python
ok = api.moveJoint(api.joint_direction_e.T_MOVE_UP, 0, 0.05, 0.10, ip)
time.sleep(0.5)
api.stop(ip)
```

```{warning}
点动示例虽然速度低、时间短，但仍会真实运动。执行 `--run` 前必须确认运动方向和工作空间。
```

````

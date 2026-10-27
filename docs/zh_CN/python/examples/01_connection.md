# 01 连接与型号识别

该示例演示 Python SDK 的最小连接生命周期：初始化 API 服务、校验机器人型号与轴数、读取 SDK 版本和机器人状态，并可选演示释放/保持抱闸。默认不释放抱闸，也不会使机器人运动。

```bash
python3 examples/01_connection/main.py --list-models
python3 examples/01_connection/main.py --model diana7 --ip 192.168.10.75
python3 examples/01_connection/main.py --model diana7 --ip 192.168.10.75 --enable
```

| API | 用途 |
|---|---|
| `initSrv` | 设置控制器 IP、注册错误/状态回调并启动 API 服务 |
| `getJointCount` | 读取实际轴数并校验 `--model` |
| `getLibraryVersion` / `getRobotState` | 读取 SDK 运行时版本和机器人状态 |
| `releaseBrake` / `holdBrake` | 仅在 `--enable` 时演示释放抱闸与保持抱闸 |
| `destroySrv` | 释放该 IP 对应的 API 服务资源 |

## Example 调用流程

解析型号和 IP → 构造 Python 回调对象 → 调用 `initSrv` → 等待状态线程更新 → 查询轴数并校验型号 → 打印 SDK 版本和机器人状态 → 可选释放/保持抱闸 → `destroySrv` 释放资源。

### 关键源码片段

```python
error_cb = api.FNCERRORCALLBACK(lambda code, ip: print(f"[Diana API error] code={code}"))
state_cb = api.FNCSTATECALLBACK(lambda state, ip: None)

if not api.initSrv([args.ip, 0, 0, 0, 0, 0], error_cb, state_cb):
    print("initSrv failed", file=sys.stderr)
    return 2

try:
    time.sleep(0.2)
    detect_and_validate_robot(api, args.ip, profile)
    print(f"Diana API library version(raw): {api.getLibraryVersion()}")
    state = api.getRobotState(args.ip)
    print(f"Robot state: {state} ({robot_state_name(state)})")
finally:
    api.destroySrv(args.ip)
```

```{important}
Python 的回调对象必须在连接生命周期内保持引用。示例把回调对象保存在局部变量中，并在 `try/finally` 中保证最终调用 `destroySrv`。
```

## 执行效果
### 型号轴数匹配并指定 `--enable`：释放后重新抱闸
::::{dropdown} 运行输出（Thor20示例）
:class-container: api-example-block
```bash
~/work/diana_examples_python$ export PYTHONPATH="$PWD/third_party/diana_sdk_python/lib:$PYTHONPATH"
~/work/diana_examples_python$ export LD_LIBRARY_PATH="$PWD/third_party/diana_sdk_python/lib:$LD_LIBRARY_PATH"
~/work/diana_examples_python$ python3 examples/01_connection/main.py --model thor20 --ip 192.168.10.75 --enable
Robot IP: 192.168.10.75
Requested model: Thor20
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-42800,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-60147,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-32808,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-51933,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-43539,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  6
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 6 (Thor series)
Selected model: Thor20 (expected 6 axes)
Diana API library version(raw): 769
Robot state: 5 (hold-brake)
Calling releaseBrake()...
Calling holdBrake()...
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} 运行输出（Diana7示例）
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/01_connection/main.py --model diana7 --ip 192.168.10.75 --enable
Robot IP: 192.168.10.75
Requested model: Diana7
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-53945,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-40247,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-35381,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-43896,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-52496,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Diana API library version(raw): 769
Robot state: 5 (hold-brake)
Calling releaseBrake()...
Calling holdBrake()...
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop

```
::::
### 型号轴数不匹配：在抱闸操作前退出
::::{dropdown} 运行输出
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/01_connection/main.py --model diana7 --ip 192.168.10.75 --enable
Robot IP: 192.168.10.75
Requested model: Diana7
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-39024,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-40912,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-48074,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-32835,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-35004,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  6
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 6 (Thor series)
Selected model: Diana7 (expected 7 axes)
Robot model mismatch: selected Diana7 expects 7 axes, but the connected robot reports 6.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::

## 逐项 API 用法与调用案例

### `initSrv` / `destroySrv`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
|---|---|---|
| `initSrv` | `initSrv(srv_net_st, fnError=None, fnState=None)` | 成功返回 True，失败返回 False |
| `destroySrv` | `destroySrv(ipAddress='')` | 成功返回 True，失败返回 False |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `srv_net_st` | 输入，`list` / `tuple`（6 个元素） | 服务网络信息 `[ip, 心跳端口, 状态推送端口, 服务端口, 实时服务端口, 透传服务端口]`：第 1 项为机械臂 IP 字符串，其余为本地端口号，传 `0` 时由系统自动分配。wrapper 据此填充 `SRV_NET_ST` 结构体。 |
| `fnError` | 输入，`FNCERRORCALLBACK`（ctypes 回调），默认 `None` | 错误回调，形参为 `int` 错误码和 `bytes` 机械臂 IP；可调用 `formatError` 获取提示信息。为 `None` 时 wrapper 传入空回调。回调在后台线程中实时触发，避免 sleep 等阻塞操作；回调对象需在连接期间保持引用。 |
| `fnState` | 输入，`FNCSTATECALLBACK`（ctypes 回调），默认 `None` | 状态回调，形参为 `POINTER(StrRobotStateInfo)` 和 `bytes` 机械臂 IP；结构体包含关节角度/角速度/电流/扭矩、TCP 位姿、TCP 外力、碰撞标志、TCP 六维力、轴空间外力、运行状态以及错误和告警信息。为 `None` 时 wrapper 传入空回调。 |
| `ipAddress` | 输入，`str`，默认 `''` | `destroySrv` 要释放服务资源的机械臂 IP；为空时释放全部已成功 `initSrv` 的机械臂资源。 |

| 函数 | Python 调用 | 返回值 |
|---|---|---|
| `initSrv` | `initSrv([ip, 0, 0, 0, 0, 0], error_cb, state_cb)` | 成功返回真值，失败返回假值 |
| `destroySrv` | `destroySrv(ip)` | 释放指定 IP 的服务资源；成功返回真值 |

Python 版 `initSrv` 的第一个参数是服务网络信息列表。本示例只设置第一个元素为机器人 IP，其余端口/配置项使用 `0`，由 SDK 使用默认配置。`initSrv`、`releaseBrake`、`holdBrake` 和 `destroySrv` 都会通过 wrapper 的 `message()` 辅助函数处理原生返回码，并返回布尔结果。回调对象需要在整个连接生命周期内保持引用，并在 `finally` 块中调用 `destroySrv`。

```python
robot_ip = "192.168.10.75"
error_cb = api.FNCERRORCALLBACK(lambda code, ip: print(code))
state_cb = api.FNCSTATECALLBACK(lambda state, ip: None)

if api.initSrv([robot_ip, 0, 0, 0, 0, 0], error_cb, state_cb):
    api.destroySrv(robot_ip)
```

````

### `getLibraryVersion` / `getRobotState` / `getJointCount`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
|---|---|---|
| `getLibraryVersion` | `getLibraryVersion()` | 返回 SDK 运行时版本原始值 |
| `getRobotState` | `getRobotState(ipAddress='')` | 返回机器人状态码 |
| `getJointCount` | `getJointCount(ipAddress='')` | 返回机器人轴数；失败时返回值以 SDK 为准 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `ipAddress` | 输入，`str`，默认 `''` | 机械臂 IP 字符串，wrapper 编码为 UTF-8 `bytes` 后传给底层库；不填仅当只连接一台机械臂时生效。适用于 `getRobotState` 和 `getJointCount`；`getLibraryVersion` 无参数。 |

| 函数 | Python 调用 | 说明 |
|---|---|---|
| `getLibraryVersion` | `getLibraryVersion()` | 返回 SDK 运行时版本原始值 |
| `getRobotState` | `getRobotState(ip)` | 返回控制器当前状态码 |
| `getJointCount` | `getJointCount(ip)` | 返回当前连接机械臂轴数 |

`getJointCount` 用于把用户选择的 `--model` 与实际连接的机械臂做一次轴数校验。Diana 系列通常为 7 轴，Thor 系列通常为 6 轴；示例只把轴数作为族类校验，具体型号仍以现场配置和发布资料为准。

```python
joint_count = api.getJointCount("192.168.10.75")
state = api.getRobotState("192.168.10.75")
version = api.getLibraryVersion()
```

````

### `releaseBrake` / `holdBrake`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
|---|---|---|
| `releaseBrake` | `releaseBrake(ipAddress='')` | 成功返回 True，失败返回 False |
| `holdBrake` | `holdBrake(ipAddress='')` | 成功返回 True，失败返回 False |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `ipAddress` | 输入，`str`，默认 `''` | 机械臂 IP 字符串，wrapper 编码为 UTF-8 `bytes` 后传给底层库；不填仅当只连接一台机械臂时生效。适用于 `releaseBrake` 和 `holdBrake`。 |

| 函数 | Python 调用 | 说明 |
|---|---|---|
| `releaseBrake` | `releaseBrake(ip)` | 释放抱闸/上使能；成功返回真值 |
| `holdBrake` | `holdBrake(ip)` | 保持抱闸 |

示例默认不改变抱闸状态。只有显式传入 `--enable` 时才调用 `releaseBrake`，等待约 2 秒后调用 `holdBrake`。

```python
if args.enable:
    if api.releaseBrake(args.ip):
        time.sleep(2)
        api.holdBrake(args.ip)
```

```{warning}
释放抱闸不等于允许运动。任何后续运动仍需要现场人员、负载、速度、净空与急停确认。
```

````

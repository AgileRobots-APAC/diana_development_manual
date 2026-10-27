# 11 力阈值停止

本示例在低速笛卡尔运动中轮询 TCP 外力，达到阈值或超时后停止。默认 dry-run；传入 `--run` 后才执行。

```bash
python3 examples/11_force_guarded_motion/main.py --model diana7 --ip 192.168.10.75
python3 examples/11_force_guarded_motion/main.py --model diana7 --ip 192.168.10.75 --run
```

| API | 用途 |
|---|---|
| `speedL` | 低速笛卡尔速度控制 |
| `getTcpForce` | 轮询 TCP 力 |
| `stop` | 达到阈值或超时后停止 |

```{warning}
力阈值停止不是急停功能的替代品。运行前必须完成现场力控与碰撞风险评审。
```

## Example 调用流程

校验 `--model` 与轴数 → 打印力阈值停止参数 → dry-run 时退出 → `releaseBrake` 后等待 2 秒 → 调用 `speedL` 沿基坐标系 X 方向低速运动 → 10 ms 周期轮询 `getTcpForce` → `|Fx| >= 5 N` 或 10 秒超时后调用 `stop` → 抱闸并释放资源。

### 关键源码片段

```python
ret = api.speedL([0.01, 0.0, 0.0, 0.0, 0.0, 0.0], [0.02, 0.05], 10.0, args.ip)
force = [0.0] * 6
deadline = time.monotonic() + 10.0

while ret and time.monotonic() < deadline:
    if api.getTcpForce(force, args.ip):
        if abs(force[0]) >= 5.0:
            break
    time.sleep(0.01)

api.stop(args.ip)
api.holdBrake(args.ip)
```
## 执行效果
::::{dropdown} 运行输出
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/11_force_guarded_motion/main.py --model diana7 --ip 192.168.10.75 --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-35237,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-53529,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-44042,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-56733,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-39260,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Guarded move: base X at 0.01 m/s, stop at |Fx| >= 5.0 N.
Stopped by force threshold: Fx=-5.085770490242117 N (threshold=+/-5.0 N).
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::

## 逐项 API 用法与调用案例

### `speedL`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
|---|---|---|
| `speedL` | `speedL(speed, acc, t=0.0, ipAddress='')` | 成功返回 True，失败返回 False |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `speed` | 输入，`list[float]`（长度 6） | TCP 速度 `[vx, vy, vz, wx, wy, wz]`；前三项单位 m/s，后三项单位 rad/s。封装固定 `active_tcp` 为空，使用默认 TCP。 |
| `acc` | 输入，`list[float]`（长度 2） | `acc[0]` 为平移加速度，单位 m/s²；`acc[1]` 为旋转加速度，单位 rad/s²。 |
| `t` | 输入，`float`，默认 `0.0` | 时间，单位 s；非零时函数在 `t` 后返回，不论是否达到目标速度；为 `0` 时在达到目标速度后返回。停止运动需调用 `stop`。本例传 `10.0`。 |
| `ipAddress` | 输入，`str`，默认 `''` | 机械臂 IP；为空时仅适合单臂连接场景。 |

`speedL(speed, acc, t, ip)` 下发笛卡尔速度控制。本例速度向量为 `[0.01, 0, 0, 0, 0, 0]`，即沿基坐标系 X 方向以 `0.01 m/s` 运动；加速度参数为 `[0.02, 0.05]`，最长持续 `10 s`。

```python
api.speedL([0.01, 0.0, 0.0, 0.0, 0.0, 0.0], [0.02, 0.05], 10.0, ip)
```

````

### `getTcpForce` / `stop`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
|---|---|---|
| `getTcpForce` | `getTcpForce(tcpForce, ipAddress='')` | 成功返回 True，失败返回 False |
| `stop` | `stop(ipAddress='')` | 成功返回 True，失败返回 False |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `tcpForce` | 输入输出，`list[float]`（长度 ≥ 6） | 预先分配的列表；封装把 TCP 处外部六维力/力矩 `[Fx, Fy, Fz, Mx, My, Mz]` 写入前 6 个元素。本例只使用 `tcpForce[0]`（Fx）。 |
| `ipAddress` | 输入，`str`，默认 `''` | 机械臂 IP，`getTcpForce` 与 `stop` 均使用；为空时仅适合单臂连接场景。 |

示例轮询 TCP 六维力数组，并只使用 X 向力 `force[0]` 做阈值判断。达到阈值、超时或命令失败后，都应调用 `stop`。

```python
force = [0.0] * 6
if api.getTcpForce(force, ip) and abs(force[0]) >= 5.0:
    api.stop(ip)
```

```{warning}
力阈值停止依赖应用层轮询，其响应不具确定性，不能替代控制器安全功能或硬件急停。
```

````

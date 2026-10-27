# 12 ServoL 实时下发

本示例以 10 ms 周期生成围绕当前 TCP 的 `servoL_ex` 轨迹。默认 dry-run；传入 `--run` 后才进入周期性下发。

```bash
python3 examples/12_servoL_realtime/main.py --model diana7 --ip 192.168.10.75
python3 examples/12_servoL_realtime/main.py --model diana7 --ip 192.168.10.75 --run
```

| API | 用途 |
|---|---|
| `getTcpPos` | 读取当前 TCP 位姿作为轨迹起点 |
| `servoL_ex` | 周期性下发笛卡尔位姿 |

```{attention}
普通 Linux 不保证硬实时。本示例用于理解接口模式，不能直接作为生产级实时控制方案。
```

## 实时控制前提

本例用于理解 `servoL_ex` 的周期调用方式。普通 Python 解释器、`time.sleep`、标准 Linux 调度和非实时网络都不能保证 10 ms 截止期。投入生产前，需要在目标 PC 和控制器上测量控制周期抖动、调度延迟、网络延迟、漏周期行为和停止行为，并完成失败处理验证。请将阻塞 I/O、大块内存分配和详细日志移出指令循环。

## Example 调用流程

校验 `--model` 与轴数 → 读取当前 TCP 位姿作为中心点 → 生成基坐标系 Z 方向 ±5 cm 的正弦轨迹 → dry-run 时退出 → `releaseBrake` 后等待 2 秒 → 以 10 ms 周期调用 `servoL_ex`，持续 20 秒 → `stop` → `holdBrake` → 释放资源。

### 关键源码片段

```python
start_pose = [0.0] * 6
api.getTcpPos(start_pose, args.ip)

for i in range(SERVO_CYCLE_COUNT):
    phase = 2.0 * math.pi * i / (SERVO_CYCLE_COUNT - 1)
    target_pose = start_pose[:]
    target_pose[2] = start_pose[2] + Z_AMPLITUDE_METERS * math.sin(phase)
    ret = api.servoL_ex(target_pose, 0.01, 0.01, 2000, 1.0, False, args.ip)
    if not ret:
        break
    time.sleep(0.01)

api.stop(args.ip)
api.holdBrake(args.ip)
```

## 执行效果
::::{dropdown} 运行输出
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/12_servoL_realtime/main.py --model diana7 --ip 192.168.10.75 --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-59396,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-48678,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-48966,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-58469,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-45115,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Start TCP pose:
  x : 0.343910 m
  y : 0.065446 m
  z : 0.499845 m
  rx: -0.042841 rad
  ry: -0.060938 rad
  rz: 0.197972 rad
Servo trajectory: base Z sine wave centered at current TCP, +/-0.05 m for 20 s.
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
| `tcpPose` | 输入输出，`list[float]`（长度 ≥ 6） | 预先分配的列表；封装把当前 TCP 位姿 `[x, y, z, rx, ry, rz]` 写入前 6 个元素，位置单位 m，姿态为轴角 rad。默认 TCP 会影响该值。 |
| `ipAddress` | 输入，`str`，默认 `''` | 机械臂 IP；为空时仅适合单臂连接场景。 |

实时轨迹示例先读取当前 TCP 位姿作为轨迹中心，避免使用固定绝对位姿造成未知空间运动。

```python
start_pose = [0.0] * 6
api.getTcpPos(start_pose, ip)
```

````

### `servoL_ex`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
|---|---|---|
| `servoL_ex` | `servoL_ex(tcp_pose, t=0.01, ah_t=0.01, gain=300, scale=1000, realiable=False, ipAddress='')` | 成功返回 True，失败返回 False |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `tcp_pose` | 输入，`list[float]`（长度 6） | 目标 TCP 位姿 `[x, y, z, rx, ry, rz]`；前三项单位 m，后三项为轴角，单位 rad。封装固定 `active_tcp` 为空，使用默认 TCP。 |
| `t` | 输入，`float`，默认 `0.01` | 运动时间，单位 s；不应小于控制周期，应用实际调用周期不应大于该值。本例传 `0.01`。 |
| `ah_t` | 输入，`float`，默认 `0.01` | 前瞻时间（look_ahead_time），单位 s，用于使轨迹更平滑；推荐范围 `0.03-0.2`。本例传 `0.01`，仅用于最小验证，不能直接作为生产参数。 |
| `gain` | 输入，`float`，默认 `300` | 目标位置的比例放大器，手册范围 `100-2000`。本例传 `2000`。 |
| `scale` | 输入，`float` | 平滑比例系数，范围 `0.0-1.0`。封装原型中的默认值 `1000` 不在该范围内，调用时请显式传入。本例传 `1.0`，表示不额外缩放。 |
| `realiable` | 输入，`bool`，默认 `False` | `True` 时需要 socket 反馈通信状态，行为等同 `servoJ`；`False` 时无需反馈直接返回。参数名按封装原样拼写。 |
| `ipAddress` | 输入，`str`，默认 `''` | 机械臂 IP；为空时仅适合单臂连接场景。 |

`servoL_ex(tcp_pose, t, ah_t, gain, scale, realiable, ip)` 用于周期性下发笛卡尔位姿。本例周期 `t` 和前瞻时间 `ah_t` 均为 `0.01 s`，`gain` 为 `2000`，`scale` 为 `1.0`，可靠传输参数为 `False`。

```python
target_pose = start_pose[:]
target_pose[2] += 0.01
api.servoL_ex(target_pose, 0.01, 0.01, 2000, 1.0, False, ip)
```

```{attention}
不要在实时循环中打印大量日志、执行阻塞 I/O 或做耗时计算。本例的 `time.sleep(0.01)` 只能作为示例节拍，不代表严格实时。
```

````

```{warning}
命令工作空间峰峰值约 100 mm。使用 `--run` 前必须确认整条轨迹的净空。
```

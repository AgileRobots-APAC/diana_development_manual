# 12 ServoL Realtime Streaming

This example generates a `servoL_ex` trajectory around the current TCP at a 10 ms period. It is dry-run by default; `--run` starts periodic command sending.

```bash
python3 examples/12_servoL_realtime/main.py --model diana7 --ip 192.168.10.75
python3 examples/12_servoL_realtime/main.py --model diana7 --ip 192.168.10.75 --run
```

| API | Purpose |
|---|---|
| `getTcpPos` | Read the current TCP pose as trajectory origin |
| `servoL_ex` | Periodically send Cartesian poses |

```{attention}
Standard Linux does not guarantee hard realtime behavior. This example illustrates the API pattern and is not production realtime-control code.
```

## Realtime Prerequisites

This example demonstrates how `servoL_ex` is called periodically. The ordinary Python interpreter, `time.sleep`, standard Linux scheduling, and a non-realtime network cannot guarantee a 10 ms deadline. Before production use, measure control-period jitter, scheduling latency, network delay, missed-cycle behavior, and stop behavior on the target PC and controller, and validate failure handling. Keep blocking I/O, large allocations, and verbose logging out of the command loop.

## Example Call Flow

Validate `--model` and axis count → read the current TCP pose as the trajectory centre → generate a ±5 cm sine trajectory along base-frame Z → exit in dry-run mode → `releaseBrake` and wait 2 seconds → call `servoL_ex` every 10 ms for 20 seconds → `stop` → `holdBrake` → release resources.

### Key Source Snippet

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

## Execution Results
::::{dropdown} Run Output
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

## API Usage and Call Examples

### `getTcpPos`

````{container} api-example-block

| Function | Prototype | Return Value |
|---|---|---|
| `getTcpPos` | `getTcpPos(tcpPose, ipAddress='')` | `True` on success; otherwise `False` |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `tcpPose` | In/out, `list[float]` (length ≥ 6) | Pre-allocated list; the wrapper writes the current TCP pose `[x, y, z, rx, ry, rz]` into its first 6 elements. Position is in m, orientation is axis-angle in rad. The default TCP affects this value. |
| `ipAddress` | In, `str`, default `''` | Robot IP. An empty value is only appropriate for single-arm connections. |

The realtime trajectory example first reads the current TCP pose and uses it as the trajectory centre, so that a fixed absolute pose cannot cause motion into unknown space.

```python
start_pose = [0.0] * 6
api.getTcpPos(start_pose, ip)
```

````

### `servoL_ex`

````{container} api-example-block

| Function | Prototype | Return Value |
|---|---|---|
| `servoL_ex` | `servoL_ex(tcp_pose, t=0.01, ah_t=0.01, gain=300, scale=1000, realiable=False, ipAddress='')` | `True` on success; otherwise `False` |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `tcp_pose` | In, `list[float]` (length 6) | Target TCP pose `[x, y, z, rx, ry, rz]`; the first three values are in m, the last three are axis-angle in rad. The wrapper fixes `active_tcp` to null, so the default TCP is used. |
| `t` | In, `float`, default `0.01` | Motion time, in s. It should not be smaller than the control period, and the application's actual call period should not exceed it. The example passes `0.01`. |
| `ah_t` | In, `float`, default `0.01` | Look-ahead time (look_ahead_time) in s, used to smooth the trajectory; recommended range `0.03-0.2`. The example passes `0.01`, which is only for minimal verification and must not be used directly as a production parameter. |
| `gain` | In, `float`, default `300` | Proportional gain on the target position; manual range `100-2000`. The example passes `2000`. |
| `scale` | In, `float` | Smoothing scale factor, range `0.0-1.0`. The default `1000` in the wrapper prototype is outside this range, so always pass the value explicitly. The example passes `1.0`, meaning no additional scaling. |
| `realiable` | In, `bool`, default `False` | `True` requires socket feedback on the communication status, behaving like `servoJ`; `False` returns directly without feedback. The parameter name is spelled exactly as in the wrapper. |
| `ipAddress` | In, `str`, default `''` | Robot IP. An empty value is only appropriate for single-arm connections. |

`servoL_ex(tcp_pose, t, ah_t, gain, scale, realiable, ip)` streams Cartesian pose targets periodically. In this example both the period `t` and the look-ahead time `ah_t` are `0.01 s`, `gain` is `2000`, `scale` is `1.0`, and the reliable-transport argument `realiable` is `False`.

```python
target_pose = start_pose[:]
target_pose[2] += 0.01
api.servoL_ex(target_pose, 0.01, 0.01, 2000, 1.0, False, ip)
```

```{attention}
Do not print verbose logs, perform blocking I/O, or run expensive computations inside the realtime loop. The `time.sleep(0.01)` in this example is only an illustrative cadence and does not provide strict realtime timing.
```

````

```{warning}
The commanded workspace spans about 100 mm peak to peak. Confirm clearance across the entire trajectory before using `--run`.
```

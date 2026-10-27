# 10 Jog Motion

This example demonstrates J1 jog, TCP translation jog, and TCP rotation jog. It is dry-run by default; `--run` performs short low-speed jogs and then stops.

```bash
python3 examples/10_jog_motion/main.py --model diana7 --ip 192.168.10.75
python3 examples/10_jog_motion/main.py --model diana7 --ip 192.168.10.75 --mode joint --duration=0.5 --run
python3 examples/10_jog_motion/main.py --model diana7 --ip 192.168.10.75 --mode tcp --duration=0.5 --run
python3 examples/10_jog_motion/main.py --model diana7 --ip 192.168.10.75 --mode rotate --duration=0.5 --run
```

| API | Purpose |
|---|---|
| `moveJoint` | Joint jog |
| `moveTcp_ex` | TCP translation jog |
| `rotationTCP` | TCP rotation jog |
| `stop` | Stop current task |

## Example Call Flow

Validate `--model` and the joint count → check that `--duration` is between 0.1 and 2.0 seconds → print the jog mode to be executed → exit in dry-run mode → call `releaseBrake` and wait 2 seconds → call joint jog, TCP translation, or TCP rotation according to `--mode` → wait for the specified duration → `stop` → `holdBrake` → release resources.

### Key Source Snippet

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

## Execution Results
::::{dropdown} Run Output (default options)
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
::::{dropdown} Run Output (`--mode joint --duration=0.5 --run`)
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
::::{dropdown} Run Output (`--mode tcp --duration=0.5 --run`)
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
::::{dropdown} Run Output (`--mode rotate --duration=0.5 --run`)
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

## API Usage and Call Examples

### `moveJoint` / `moveTcp_ex` / `rotationTCP` / `stop`

````{container} api-example-block

| Function | Prototype | Return Value |
|---|---|---|
| `moveJoint` | `moveJoint(d, i, v, a, ipAddress='')` | `True` on success; `False` on failure |
| `moveTcp_ex` | `moveTcp_ex(coordinate, direction, velocity, accleartion, ipAddress='')` | `True` on success; `False` on failure |
| `rotationTCP` | `rotationTCP(d, v, a, ipAddress='')` | `True` on success; `False` on failure |
| `stop` | `stop(ipAddress='')` | `True` on success; `False` on failure |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `d` | In, `joint_direction_e` or `tcp_direction_e` enum | The wrapper passes its `.value`. `moveJoint` uses `joint_direction_e`: `T_MOVE_UP` is positive, `T_MOVE_DOWN` is negative. `rotationTCP` uses `tcp_direction_e` (`T_MOVE_X_UP` ... `T_MOVE_Z_DOWN`) as the rotation direction. |
| `i` | In, `int` | Joint index for `moveJoint`, starting from `0`; `0` is J1. |
| `coordinate` | In, `coordinate_e` enum | Coordinate system for `moveTcp_ex`: `E_BASE_COORDINATE` (base), `E_TOOL_COORDINATE` (tool), `E_WORK_PIECE_COORDINATE` (work piece), `E_VIEW_COORDINATE` (view). The wrapper raises `TypeError` if it is not an instance of this enum. |
| `direction` | In, `tcp_direction_e` enum | Motion direction for `moveTcp_ex`: `T_MOVE_X_UP` / `T_MOVE_X_DOWN`, `T_MOVE_Y_UP` / `T_MOVE_Y_DOWN`, `T_MOVE_Z_UP` / `T_MOVE_Z_DOWN` move along the positive / negative x, y, z axis. The wrapper raises `TypeError` if it is not an instance of this enum. |
| `v` | In, `float` | Velocity for `moveJoint` / `rotationTCP`, in rad/s. |
| `a` | In, `float` | Acceleration for `moveJoint` / `rotationTCP`, in rad/s². |
| `velocity` | In, `float` | Velocity for `moveTcp_ex`, in m/s. |
| `accleartion` | In, `float` | Acceleration for `moveTcp_ex`, in m/s². The parameter name is spelled exactly as in the wrapper. |
| `ipAddress` | In, `str`, default `''` | Robot IP, used by all four functions. An empty value is only appropriate for single-arm connections. |

| Mode | API | Example Action |
|---|---|---|
| `joint` | `moveJoint` | Jog J1 in the positive direction at low speed (`0.05 rad/s`) |
| `tcp` | `moveTcp_ex` | Translate the TCP along base-frame +X (`0.01 m/s`) |
| `rotate` | `rotationTCP` | Rotate the TCP about base-frame +Z (`0.05 rad/s`) |

Jog commands keep moving until the duration expires, `stop` is called, or the controller stops them for another reason. This example limits `--duration` to 0.1–2.0 seconds and explicitly calls `stop` after every run.

```python
ok = api.moveJoint(api.joint_direction_e.T_MOVE_UP, 0, 0.05, 0.10, ip)
time.sleep(0.5)
api.stop(ip)
```

```{warning}
Although the jog example uses low speed and a short duration, it still produces real motion. Confirm the motion direction and the available workspace before running with `--run`.
```

````

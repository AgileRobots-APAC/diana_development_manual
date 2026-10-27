# 03 Joint Motion

This example reads the current joint position and calculates a small joint target. It is dry-run by default and only prints the target; the motion API is called only when `--run` is supplied.

```bash
python3 examples/03_joint_motion/main.py --model diana7 --ip 192.168.10.75
python3 examples/03_joint_motion/main.py --model diana7 --ip 192.168.10.75 --run
```

| API | Purpose |
|---|---|
| `getJointPos` | Read current joint positions |
| `moveJToTarget` | Execute joint-target motion |

```{warning}
`--run` moves the robot. Confirm the selected model, payload, speed, clearance, and emergency-stop conditions first.
```

## Example Call Flow

Validate `--model` against the joint count → read the current joint angles → copy the start point and increase J1 by 10° → without `--run`, only print the target and exit → call `releaseBrake` and wait 2 seconds → call `moveJToTarget` → poll until motion completes → call `holdBrake` and release resources.

### Key Source Snippet

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

## Execution Results
::::{dropdown} Run Output (Thor20 example)
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
::::{dropdown} Run Output (Diana7 example)
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
## API Usage and Call Examples

### `getJointPos`

````{container} api-example-block

| Function | Prototype | Return Value |
|---|---|---|
| `getJointPos` | `getJointPos(jointsPosition, ipAddress='')` | `True` on success; otherwise `False` |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `jointsPosition` | Out (filled in place), `list[float]` (length `JOINT_NUM`, at most 7) | Joint angles, in rad. The caller pre-allocates the list (e.g. `[0.0] * MAX_SUPPORTED_JOINT_COUNT`); the wrapper copies back as many elements as the list holds from a 7-element ctypes array. |
| `ipAddress` | In, `str`, default `''` | Robot IP string; the wrapper encodes it to UTF-8 `bytes` for the native library. Leaving it empty only works when a single robot is connected. |

Motion examples should not construct a complete joint array from scratch. Read the complete current joint array first, then generate a small-offset target from that start point. This avoids large motions caused by writing unknown joints as `0`.

```python
joints = [0.0] * MAX_SUPPORTED_JOINT_COUNT
if api.getJointPos(joints, ip):
    joints[0] += 2.0 * math.pi / 180.0
```

````

### `moveJToTarget`

````{container} api-example-block

| Function | Prototype | Return Value |
|---|---|---|
| `moveJToTarget` | `moveJToTarget(joints, v, a, zv_shaper_order=0, zv_shaper_frequency=0, zv_shaper_damping_ratio=0, ipAddress='')` | `True` on success; otherwise `False` |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `joints` | In, `list[float]` (length `JOINT_NUM`, at most 7) | Target joint angles, in rad; the wrapper copies as many elements as the list holds into a 7-element ctypes array. This example passes `target`, an offset of the current joint position. |
| `v` | In, `float` | Joint velocity, in rad/s. This example uses `0.10`. |
| `a` | In, `float` | Joint acceleration, in rad/s². This example uses `0.20`. |
| `zv_shaper_order` | In, `int`, default `0` | Vibration-shaper order, range [-1, 2]; `-1` disables shaping. When all three shaper parameters are `0`, the robot's default configuration is used; if any of them is non-zero, the given order is used. This example uses `0`. |
| `zv_shaper_frequency` | In, `float`, default `0` | Shaper frequency, in Hz, range [0, 1000]; `0` uses the robot's default configuration. This example uses `0.0`. |
| `zv_shaper_damping_ratio` | In, `float`, default `0` | Shaper damping ratio, range [0, 1]; `0` uses the robot's default configuration. This example uses `0.0`. |
| `ipAddress` | In, `str`, default `''` | Robot IP string; the wrapper encodes it to UTF-8 `bytes` for the native library. Leaving it empty only works when a single robot is connected. This example passes the target robot IP. |

Successfully sending the motion command does not mean the robot has reached the target. This example uses the shared `wait_move` helper to poll `getRobotState` and wait for the controller to leave the running state.

```python
ok = api.moveJToTarget(target, 0.10, 0.20, 0, 0.0, 0.0, ip)
if not ok:
    api.stop(ip)
```

````

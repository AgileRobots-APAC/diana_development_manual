# 04 Cartesian Motion

This example reads the current TCP pose and calculates a small Cartesian linear target. It is dry-run by default and only prints the target; the motion API is called only when `--run` is supplied.

```bash
python3 examples/04_cartesian_motion/main.py --model diana7 --ip 192.168.10.75
python3 examples/04_cartesian_motion/main.py --model diana7 --ip 192.168.10.75 --run
```

| API | Purpose |
|---|---|
| `getTcpPos` | Read current TCP pose |
| `moveLToPose` | Execute Cartesian linear motion |

```{warning}
`--run` moves the robot. Check the full linear path, not only the endpoint.
```

## Example Call Flow

Validate `--model` against the joint count → read the current TCP pose → copy the start point and increase base-frame Z by 10 mm → in dry-run mode, only print the target → call `releaseBrake` and wait 2 seconds → call `moveLToPose` → wait for completion → hold the brake and release resources.

### Key Source Snippet

```python
start = [0.0] * 6
api.getTcpPos(start, args.ip)

target = start[:]
target[2] += 0.01

if not args.run:
    print("DRY RUN: no motion command sent.")
    return 0

api.releaseBrake(args.ip)
time.sleep(2)
if not api.moveLToPose(target, 0.02, 0.05, 0, 0.0, 0.0, False, args.ip):
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
~/work/diana_examples_python$ python3 examples/04_cartesian_motion/main.py --model thor20 --ip 192.168.10.75 --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-57542,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-57879,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-41498,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-48223,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-56610,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  6
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 6 (Thor series)
Selected model: Thor20 (expected 6 axes)
Current TCP pose:
  x : 0.709443 m
  y : 0.375895 m
  z : 0.653536 m
  rx: -0.813375 rad
  ry: 2.480432 rad
  rz: 0.112399 rad
Example target (Base Z + 10 mm):
  x : 0.709443 m
  y : 0.375895 m
  z : 0.663536 m
  rx: -0.813375 rad
  ry: 2.480432 rad
  rz: 0.112399 rad
Motion finished.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} Run Output (Diana7 example)
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/04_cartesian_motion/main.py --model diana7 --ip 192.168.10.75 --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-49497,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-45958,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-51537,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-52034,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-39529,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Current TCP pose:
  x : 0.376643 m
  y : 0.059490 m
  z : 0.500145 m
  rx: -0.042813 rad
  ry: -0.060409 rad
  rz: 0.199425 rad
Example target (Base Z + 10 mm):
  x : 0.376643 m
  y : 0.059490 m
  z : 0.510145 m
  rx: -0.042813 rad
  ry: -0.060409 rad
  rz: 0.199425 rad
Motion finished.
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
| `tcpPose` | Out (filled in place), `list[float]` (length at least 6) | TCP pose `[x, y, z, rx, ry, rz]`; position in m, orientation as axis-angle in rad. The wrapper copies the first 6 elements from a 6-element ctypes array; the result depends on the default TCP set by `setDefaultActiveTcp`. |
| `ipAddress` | In, `str`, default `''` | Robot IP string; the wrapper encodes it to UTF-8 `bytes` for the native library. Leaving it empty only works when a single robot is connected. |

`getTcpPos` outputs `[x, y, z, rx, ry, rz]`. Positions are in m and orientation is in rad (an axis-angle rotation vector, not raw RPY angles). This example only adds `0.01` to the current Z, i.e. 10 mm.

```python
pose = [0.0] * 6
if api.getTcpPos(pose, ip):
    pose[2] += 0.01
```

````

### `moveLToPose`

````{container} api-example-block

| Function | Prototype | Return Value |
|---|---|---|
| `moveLToPose` | `moveLToPose(pose, v, a, zv_shaper_order=0, zv_shaper_frequency=0, zv_shaper_damping_ratio=0, avoid_singular = False, ipAddress='')` | `True` on success; otherwise `False` |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `pose` | In, `list[float]` / `tuple` (length 6) | Target TCP pose `[x, y, z, rx, ry, rz]`; position in m, orientation as axis-angle in rad. The wrapper reads the first 6 elements and always passes a null `active_tcp` to the native library, so the default TCP (set via `setDefaultActiveTcp`) is used. |
| `v` | In, `float` | Linear velocity, in m/s. This example uses `0.02`. |
| `a` | In, `float` | Linear acceleration, in m/s². This example uses `0.05`. |
| `zv_shaper_order` | In, `int`, default `0` | Vibration-shaper order, range [-1, 2]; `-1` disables shaping. When all three shaper parameters are `0`, the robot's default configuration is used; if any of them is non-zero, the given order is used. This example uses `0`. |
| `zv_shaper_frequency` | In, `float`, default `0` | Shaper frequency, in Hz, range [0, 1000]; `0` uses the robot's default configuration. This example uses `0.0`. |
| `zv_shaper_damping_ratio` | In, `float`, default `0` | Shaper damping ratio, range [0, 1]; `0` uses the robot's default configuration. This example uses `0.0`. |
| `avoid_singular` | In, `bool`, default `False` | Whether to enable singularity avoidance. This example uses `False`. |
| `ipAddress` | In, `str`, default `''` | Robot IP string; the wrapper encodes it to UTF-8 `bytes` for the native library. Leaving it empty only works when a single robot is connected. This example passes the target robot IP. |

`moveLToPose(target, v, a, ..., avoid_singular, ip)` executes linear motion to a Cartesian target pose. This example uses a velocity of `0.02 m/s` and an acceleration of `0.05 m/s²`, uses the robot's default ZV-shaper configuration (all shaper arguments `0`), and sets `avoid_singular` to `False`.

```python
ok = api.moveLToPose(target, 0.02, 0.05, 0, 0.0, 0.0, False, ip)
if not ok:
    api.stop(ip)
```

````

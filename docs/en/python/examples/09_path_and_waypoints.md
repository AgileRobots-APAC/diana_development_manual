# 09 Paths and Waypoints

This example demonstrates basic and complex path creation, waypoint insertion, execution, and destruction. It is dry-run by default; `--run` executes motion.

```bash
python3 examples/09_path_and_waypoints/main.py --model diana7 --ip 192.168.10.75
python3 examples/09_path_and_waypoints/main.py --model diana7 --ip 192.168.10.75 --run
python3 examples/09_path_and_waypoints/main.py --model diana7 --ip 192.168.10.75 --complex --run
```

| API | Purpose |
|---|---|
| `createPath` / `addMoveJ` / `runPath` / `destroyPath` | Basic path lifecycle |
| `createComplexPath` / `addMoveJSegmentByTarget` / `runComplexPath` / `destroyComplexPath` | Complex path lifecycle |

## Example Call Flow

Validate `--model` and the joint count → read the current joint angles → generate two waypoints: a positive J1 offset and a return to the start → in dry-run mode, only print the waypoints → call `releaseBrake` and wait 2 seconds → choose the basic or complex path API according to `--complex` → add two joint-motion segments → run the path → destroy the path object → hold the brake and release resources.

### Key Source Snippet

```python
start = [0.0] * MAX_SUPPORTED_JOINT_COUNT
api.getJointPos(start, args.ip)
target = start[:]
target[0] += (15.0 if args.complex else 10.0) * math.pi / 180.0

if args.complex:
    ret_code, path_id = api.createComplexPath(api.complex_path_type.NORMAL_JOINT_PATH, args.ip)
    api.addMoveJSegmentByTarget(path_id, target, 0.10, 0.20, 0.0, 0, 0.0, 0.0, args.ip)
    api.addMoveJSegmentByTarget(path_id, start, 0.10, 0.20, 0.0, 0, 0.0, 0.0, args.ip)
    api.runComplexPath(path_id, args.ip)
    api.destroyComplexPath(path_id, args.ip)
else:
    ret_code, path_id = api.createPath(1, args.ip)
    api.addMoveJ(path_id, target, 0.10, 0.20, 0.0, args.ip)
    api.addMoveJ(path_id, start, 0.10, 0.20, 0.0, args.ip)
    api.runPath(path_id, args.ip)
    api.destroyPath(path_id, args.ip)
```

## Execution Results
::::{dropdown} Run Output (default options)
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/09_path_and_waypoints/main.py --model diana7 --ip 192.168.10.75
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-48838,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-46366,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-53739,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-54196,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-38264,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Path waypoint 1:
  J1: 0.030603 rad
  J2: -0.491868 rad
  J3: -0.016598 rad
  J4: 2.442949 rad
  J5: 0.042400 rad
  J6: -1.132989 rad
  J7: 0.023897 rad
Path waypoint 2 (return to current joints):
  J1: -0.143930 rad
  J2: -0.491868 rad
  J3: -0.016598 rad
  J4: 2.442949 rad
  J5: 0.042400 rad
  J6: -1.132989 rad
  J7: 0.023897 rad
DRY RUN: no path command sent.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} Run Output (`--run`)
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/09_path_and_waypoints/main.py --model diana7 --ip 192.168.10.75 --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-56503,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-41369,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-53463,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-51508,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-34190,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Path waypoint 1:
  J1: 0.030603 rad
  J2: -0.491856 rad
  J3: -0.016586 rad
  J4: 2.442949 rad
  J5: 0.042388 rad
  J6: -1.133012 rad
  J7: 0.023897 rad
Path waypoint 2 (return to current joints):
  J1: -0.143930 rad
  J2: -0.491856 rad
  J3: -0.016586 rad
  J4: 2.442949 rad
  J5: 0.042388 rad
  J6: -1.133012 rad
  J7: 0.023897 rad
 [Debug] [runPath] new custom command is created, id = 1

 [Debug] [runPath] custom command is filled, id = 1

 [Debug] [runPath] custom command is running, id = 1

 [Debug] 192.168.10.75 [destroyCustomCommand] custom command is destroyed, id = 1

Path finished.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} Run Output (`--complex --run`)
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/09_path_and_waypoints/main.py --model diana7 --ip 192.168.10.75 --complex --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-48935,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-43666,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-58337,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-36622,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-43701,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Complex-path waypoint 1:
  J1: 0.117881 rad
  J2: -0.491832 rad
  J3: -0.016598 rad
  J4: 2.442961 rad
  J5: 0.042364 rad
  J6: -1.133000 rad
  J7: 0.023885 rad
Path waypoint 2 (return to current joints):
  J1: -0.143918 rad
  J2: -0.491832 rad
  J3: -0.016598 rad
  J4: 2.442961 rad
  J5: 0.042364 rad
  J6: -1.133000 rad
  J7: 0.023885 rad
Path finished.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::

## API Usage and Call Examples

### `createPath` / `addMoveJ` / `runPath` / `destroyPath`

````{container} api-example-block

| Function | Prototype | Return Value |
|---|---|---|
| `createPath` | `createPath(id_type, ipAddress='')` | Returns `(ret_code, path_id)`; `ret_code == 0` indicates success |
| `addMoveJ` | `addMoveJ(id_path, joints, vel, acc, blendradius, ipAddress='')` | `True` on success; `False` on failure |
| `runPath` | `runPath(id_path, ipAddress='')` | `True` on success; `False` on failure |
| `destroyPath` | `destroyPath(id_path, ipAddress='')` | `True` on success; `False` on failure |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `id_type` | In, `int` | Basic path type, passed through as an integer. `1` means `moveJ` and `2` means `moveL`; this example uses `1` (a moveJ path). |
| `id_path` | In, `ctypes.c_uint` or `int` | Path ID from the tuple returned by `createPath` (a `ctypes.c_uint` object that can be passed back directly); `addMoveJ`, `runPath`, and `destroyPath` must use the same ID. |
| `joints` | In, `list[float]` (length = actual joint count, at most 7) | Target joint positions of the waypoint, in rad. The wrapper copies as many elements as the list holds into a 7-element array. |
| `vel` | In, `float` | Velocity percentage for moving to the waypoint (named `vel_percent` in the manual). The example passes `0.10`. |
| `acc` | In, `float` | Acceleration percentage for moving to the waypoint (named `acc_percent` in the manual). The example passes `0.20`. |
| `blendradius` | In, `float` | Blend-radius percentage (named `blendradius_percent` in the manual). The example passes `0.0`. |
| `ipAddress` | In, `str`, default `''` | Robot IP, used by all four functions. An empty value is only appropriate for single-arm connections. |

The basic path API is suited to organizing simple sequences of waypoints. A path object must be destroyed when you are done with it; if sending the path fails, stop the current task and clean up the path resources.

```python
ret_code, path_id = api.createPath(1, ip)  # 1 = moveJ path
if ret_code == 0:
    api.addMoveJ(path_id, waypoint1, 0.10, 0.20, 0.0, ip)
    api.addMoveJ(path_id, waypoint2, 0.10, 0.20, 0.0, ip)
    api.runPath(path_id, ip)
    api.destroyPath(path_id, ip)
```

````

### `createComplexPath` / `addMoveJSegmentByTarget` / `runComplexPath` / `destroyComplexPath`

````{container} api-example-block

| Function | Prototype | Return Value |
|---|---|---|
| `createComplexPath` | `createComplexPath(path_type, ipAddress='')` | Returns `(ret_code, path_id)`; `ret_code == 0` indicates success |
| `addMoveJSegmentByTarget` | `addMoveJSegmentByTarget(complex_path_id, joints, vel_percent, acc_percent, blendradius_percent, zv_shaper_order=0, zv_shaper_frequency=0, zv_shaper_damping_ratio=0, ipAddress='')` | `True` on success; `False` on failure |
| `runComplexPath` | `runComplexPath(complex_path_id, ipAddress='')` | `True` on success; `False` on failure |
| `destroyComplexPath` | `destroyComplexPath(complex_path_id, ipAddress='')` | `True` on success; `False` on failure |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `path_type` | In, `complex_path_type` enum | Complex path type; the wrapper passes its `.value`. `NORMAL_JOINT_PATH` (MoveJ/MoveL/MoveC, joint targets), `MOVEP_JOINT_PATH` (MoveP, joint targets), `NORMAL_POSE_PATH` (MoveJ/MoveL/MoveC, TCP pose targets), `MOVEP_POSE_PATH` (MoveP, TCP pose targets). This example uses `NORMAL_JOINT_PATH`. |
| `complex_path_id` | In, `ctypes.c_uint` or `int` | Complex path ID from the tuple returned by `createComplexPath` (a `ctypes.c_uint` object that can be passed back directly); `addMoveJSegmentByTarget`, `runComplexPath`, and `destroyComplexPath` must use the same ID. |
| `joints` | In, `list[float]` (length = actual joint count, at most 7) | Target joint positions, in rad. The wrapper copies as many elements as the list holds into a 7-element array. |
| `vel_percent` / `acc_percent` / `blendradius_percent` | In, `float` | Velocity, acceleration, and blend-radius percentages for moving to the target waypoint. The example passes `0.10` / `0.20` / `0.0`. |
| `zv_shaper_order` | In, `int`, default `0` | Shaper order, range `[-1, 2]`; `-1` disables shaping. When all three shaper parameters are `0`, the robot's default configuration is used; if any of them is non-zero, the given order is used. The example passes `0`. |
| `zv_shaper_frequency` | In, `float`, default `0` | Shaper frequency, in Hz, range `[0, 1000]`; `0` uses the robot's default configuration. |
| `zv_shaper_damping_ratio` | In, `float`, default `0` | Shaper damping ratio, range `[0, 1]`; `0` uses the robot's default configuration. |
| `ipAddress` | In, `str`, default `''` | Robot IP, used by all four functions. An empty value is only appropriate for single-arm connections. |

The complex path API selects the path type through `complex_path_type`. This example uses `NORMAL_JOINT_PATH` and adds joint-target segments with `addMoveJSegmentByTarget`.

```python
ret_code, path_id = api.createComplexPath(api.complex_path_type.NORMAL_JOINT_PATH, ip)
if ret_code == 0:
    api.addMoveJSegmentByTarget(path_id, waypoint, 0.10, 0.20, 0.0, 0, 0.0, 0.0, ip)
    api.runComplexPath(path_id, ip)
    api.destroyComplexPath(path_id, ip)
```

````

Without `--complex`, the example offsets J1 by 10 degrees and uses the basic path API. With `--complex`, it offsets J1 by 15 degrees and creates a `NORMAL_JOINT_PATH`. Both variants add a return-to-start waypoint. Check every return value, call `stop` on setup or execution failure, and destroy the path object after use.

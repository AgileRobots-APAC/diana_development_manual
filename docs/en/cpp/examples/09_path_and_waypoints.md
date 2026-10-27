# 09 Paths and Waypoints

This example generates a two-waypoint path from the current joint position: offset target, then return to start. It prints waypoints by default. `--run` creates and runs the path, and `--complex` uses the complex path API.

```bash
./build/bin/09_path_and_waypoints --model diana7 --ip 192.168.10.75
./build/bin/09_path_and_waypoints --model diana7 --ip 192.168.10.75 --run
./build/bin/09_path_and_waypoints --model diana7 --ip 192.168.10.75 --complex --run
```

| Mode | API order |
|---|---|
| Basic path | `createPath` → two `addMoveJ` calls → `runPath` → `destroyPath` |
| Complex path | `createComplexPath` → two `addMoveJByTarget` calls → `runComplexPath` → `destroyComplexPath` |

## Example Call Flow

Connect and read current joints → generate a J1 +10° target (+15° for a complex path) → dry-run or enable → create, append waypoints, and run → `waitMove` → destroy the path → hold brake and release resources; call `stop` on failure.

### Key Source Snippet

```cpp
unsigned int path_id = 0;
int ret = createPath(1, path_id, ip);  // 1 = moveJ path
if (ret == 0) ret = addMoveJ(path_id, target, 0.10, 0.20, 0.0, ip);
if (ret == 0) ret = addMoveJ(path_id, start, 0.10, 0.20, 0.0, ip);
if (ret == 0) ret = runPath(path_id, ip);

if (ret < 0) stop(ip); else waitMove(ip);
destroyPath(path_id, ip);
```

For a complex path, use the following API group instead; do not mix it with the basic-path APIs:

```cpp
int ret = createComplexPath(0, path_id, ip);
if (ret == 0) ret = addMoveJByTarget(path_id, target,
                                      0.10, 0.20, 0.0, 0, 0.0, 0.0, ip);
if (ret == 0) ret = runComplexPath(path_id, ip);
destroyComplexPath(path_id, ip);
```

```{warning}
Waypoints are generated from the current pose. Confirm clearance, joint limits, and site safety for the full outbound and return path before running.
```

## Execution Results
::::{dropdown} Run output (No additional arguments)
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/09_path_and_waypoints --model diana7 --ip 192.168.10.75
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-43939,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-47870,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-37959,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-35350,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-34298,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Warning] -20006:_interpolaterPosition warning:SPD_UNREACHABLE.
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Path waypoint 1 (J1 + 10 deg):
  J1: -0.706849 rad
  J2: -0.420826 rad
  J3: -0.143115 rad
  J4: 2.640281 rad
  J5: -0.091499 rad
  J6: -1.187948 rad
  J7: -0.014585 rad
Path waypoint 2 (return to current joints):
  J1: -0.724302 rad
  J2: -0.420826 rad
  J3: -0.143115 rad
  J4: 2.640281 rad
  J5: -0.091499 rad
  J6: -1.187948 rad
  J7: -0.014585 rad
DRY RUN: no path is created or executed. Add --model <name> --run after checking the workspace.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} Run output (--run)
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/09_path_and_waypoints --model diana7 --ip 192.168.10.75 --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-55800,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-48597,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-56755,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-39723,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-34760,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Warning] -20006:_interpolaterPosition warning:SPD_UNREACHABLE.
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Path waypoint 1 (J1 + 10 deg):
  J1: -0.706981 rad
  J2: -0.420838 rad
  J3: -0.143115 rad
  J4: 2.640221 rad
  J5: -0.091511 rad
  J6: -1.187948 rad
  J7: -0.014621 rad
Path waypoint 2 (return to current joints):
  J1: -0.724434 rad
  J2: -0.420838 rad
  J3: -0.143115 rad
  J4: 2.640221 rad
  J5: -0.091511 rad
  J6: -1.187948 rad
  J7: -0.014621 rad
 [Debug] [runPath] new custom command is created, id = 2 
 
 [Debug] [runPath] custom command is filled, id = 2 
 
 [Debug] [runPath] custom command is running, id = 2 
 
 [Debug] 192.168.10.75 [destroyCustomCommand] custom command is destroyed, id = 2 
 
Path finished.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} Run output (--complex --run)
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/09_path_and_waypoints --model diana7 --ip 192.168.10.75 --complex --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-52107,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-52120,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-59351,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-57495,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-50791,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Warning] -20006:_interpolaterPosition warning:SPD_UNREACHABLE.
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Complex-path waypoint 1 (J1 + 15 deg):
  J1: -0.689456 rad
  J2: -0.420826 rad
  J3: -0.143103 rad
  J4: 2.640233 rad
  J5: -0.091487 rad
  J6: -1.187984 rad
  J7: -0.014597 rad
Path waypoint 2 (return to current joints):
  J1: -0.724362 rad
  J2: -0.420826 rad
  J3: -0.143103 rad
  J4: 2.640233 rad
  J5: -0.091487 rad
  J6: -1.187984 rad
  J7: -0.014597 rad
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
| --- | --- | --- |
| `createPath` | `int createPath(int type, unsigned int &id_path, const char *strIpAddress = "")` | `0` on success, `-1` on failure. On success, `id_path` receives the path ID. |
| `addMoveJ` | `int addMoveJ(unsigned int id_path, double *joints, double vel_percent, double acc_percent, double blendradius_percent, const char *strIpAddress = "")` | `0` on success, `-1` on failure. |
| `runPath` | `int runPath(unsigned int id_path, const char *strIpAddress = "")` | `0` when the command is accepted, `-1` on failure. A successful return does not mean the path has finished. |
| `destroyPath` | `int destroyPath(unsigned int id_path, const char *strIpAddress = "")` | `0` on success, `-1` on failure. |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `type` | In, `int` | Basic path type. The manual defines `1` as `moveJ` and `2` as `moveL`. |
| `id_path` | Out or in, `unsigned int` | Basic path ID returned by `createPath`; append, run, and destroy calls must use the same ID. |
| `joints` | In, `double[kMaxSupportedJointCount]` | Target joint positions for a waypoint, in rad; the actual joint count determines the valid elements. |
| `vel_percent` | In, `double` | Velocity percentage parameter. |
| `acc_percent` | In, `double` | Acceleration percentage parameter. |
| `blendradius_percent` | In, `double` | Blend-radius percentage parameter. |
| `strIpAddress` | In, `const char*`, default `""` | Robot IP. An empty value is only appropriate for single-arm connections. |

`createPath(type, path_id, ip)` creates a basic path segment. `type=1` means `moveJ`, and `type=2` means `moveL`. The API outputs `path_id`; all later append, run, and destroy calls must use the same ID.

`addMoveJ(path_id, joints, vel_percent, acc_percent, blendradius_percent, ip)` appends a joint target; the example uses a `kMaxSupportedJointCount` buffer. In V3.3 these control values are velocity percentage, acceleration percentage, and blend-radius percentage, not rad/s or rad/s². `runPath(path_id, ip)` starts execution, and `destroyPath(path_id, ip)` releases the basic path object. The execution API returns immediately, so `waitMove` is still required; whichever step fails, make sure the created object is released.

```{rubric} Call Example
```

```cpp
unsigned int path_id = 0;
double joints[kMaxSupportedJointCount] = {0.0};
createPath(1, path_id, "192.168.10.75");  // 1: moveJ
addMoveJ(path_id, joints, 0.2, 0.2, 0.3, "192.168.10.75");
runPath(path_id, "192.168.10.75");
waitMove("192.168.10.75");
destroyPath(path_id, "192.168.10.75");
```


````

### `createComplexPath` / `addMoveJByTarget` / `runComplexPath` / `destroyComplexPath`

````{container} api-example-block

| Function | Prototype | Return Value |
| --- | --- | --- |
| `createComplexPath` | `int createComplexPath(int complex_path_type, unsigned int &complex_path_id, const char *strIpAddress = "")` | `0` on success, `-1` on failure. On success, `complex_path_id` receives the complex path ID. |
| `addMoveJByTarget` | `int addMoveJByTarget(unsigned int complex_path_id, double *target_joints, double vel_percent, double acc_percent, double blendradius_percent, int zv_shaper_order = 0, double zv_shaper_frequency = 0, double zv_shaper_damping_ratio = 0, const char *strIpAddress = "")` | `0` on success, `-1` on failure. |
| `runComplexPath` | `int runComplexPath(unsigned int complex_path_id, const char *strIpAddress = "")` | `0` when the command is accepted, `-1` on failure. A successful return does not mean the path has finished. |
| `destroyComplexPath` | `int destroyComplexPath(unsigned int complex_path_id, const char *strIpAddress = "")` | `0` on success, `-1` on failure. |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `complex_path_type` | In, `int` | Complex path type. This example uses `NORMAL_JOINT_PATH`. |
| `complex_path_id` | Out or in, `unsigned int` | Complex path ID returned by `createComplexPath`; later calls must use the same ID. |
| `target_joints` | In, `double[kMaxSupportedJointCount]` | Target joint positions, in rad; the actual joint count determines the valid elements. |
| `vel_percent` / `acc_percent` / `blendradius_percent` | In, `double` | Velocity, acceleration, and blend-radius percentage parameters. |
| `zv_shaper_order` / `zv_shaper_frequency` / `zv_shaper_damping_ratio` | In, defaults `0` / `0.0` / `0.0` | Zero-vibration shaper parameters. This example disables them. |
| `strIpAddress` | In, `const char*`, default `""` | Robot IP. An empty value is only appropriate for single-arm connections. |

The complex path APIs form a separate object lifecycle and must be paired with each other. `addMoveJByTarget` target, velocity, acceleration, and shaping arguments follow the V3.3 header definition and must not be mixed with basic path objects.

When the basic-path `createPath` type is `2`, it corresponds to `moveL`; use `addMoveL` instead and pass linear velocity, acceleration, and blend radius in m/s, m/s², and m.

```{rubric} Call Example
```

```cpp
unsigned int path_id = 0;
int ret = createComplexPath(0, path_id, "192.168.10.75");
if (ret == 0) ret = addMoveJByTarget(path_id, joints,
                                     0.10, 0.20, 0.0, 0, 0.0, 0.0,
                                     "192.168.10.75");
if (ret == 0) ret = runComplexPath(path_id, "192.168.10.75");
destroyComplexPath(path_id, "192.168.10.75");
```

````

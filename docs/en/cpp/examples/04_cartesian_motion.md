# 04 Cartesian Motion

This example reads the current TCP pose, increases base-frame Z by 10 mm, and sends a linear motion with `moveLToPose`.

```bash
./build/bin/04_cartesian_motion --model diana7 --ip 192.168.10.75       # dry-run
./build/bin/04_cartesian_motion --model thor12 --ip 192.168.10.75 --run
```

| API | Purpose |
|---|---|
| `getTcpPos` | Read the current TCP pose as the target baseline |
| `releaseBrake` / `holdBrake` | Enable before motion and hold the brake afterward |
| `moveLToPose` | Send a linear motion by target TCP pose, velocity, and acceleration |
| `stop` / `waitMove` | Stop on failure or wait until motion completes |

## Example Call Flow

Initialize and validate model → read current pose → compute a target with Z + 0.01 m → print the plan → dry-run or enable → call `moveLToPose` → wait, hold brake, and release resources.

### Key Source Snippet

```cpp
double start[6] = {0.0};
getTcpPos(start, ip);

double target[6];
for (int i = 0; i < 6; ++i) target[i] = start[i];
target[2] += 0.010;  // Base Z + 10 mm

releaseBrake(ip);
std::this_thread::sleep_for(std::chrono::seconds(2));
const int ret = moveLToPose(target, 0.02, 0.05, nullptr,
                            0, 0.0, 0.0, false, ip);
if (ret < 0) stop(ip); else waitMove(ip);
holdBrake(ip);
```

```{warning}
The target is computed relative to the current TCP. The example does not check workpieces, fixtures, or singularities. Confirm path clearance before running.
```

## Execution Results
::::{dropdown} Run output (Thor20 example)
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/04_cartesian_motion --model thor20 --ip 192.168.10.75 --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-57532,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-42180,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-60821,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-40814,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-38603,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  6
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 6 (Thor series)
Selected model: Thor20 (expected 6 axes)
Current TCP pose:
  x : 0.764005 m
  y : 0.247087 m
  z : 0.643907 m
  rx: -0.593565 rad
  ry: 2.537922 rad
  rz: 0.050321 rad
Example target (Base Z + 10 mm):
  x : 0.764005 m
  y : 0.247087 m
  z : 0.653907 m
  rx: -0.593565 rad
  ry: 2.537922 rad
  rz: 0.050321 rad
Motion finished.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} Run output (Diana7 example)
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/04_cartesian_motion --model diana7 --ip 192.168.10.75 --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-45616,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-57528,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-35788,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-59074,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-60060,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Current TCP pose:
  x : 0.207016 m
  y : 0.254568 m
  z : 0.360338 m
  rx: -0.095515 rad
  ry: 0.258551 rad
  rz: 0.782288 rad
Example target (Base Z + 10 mm):
  x : 0.207016 m
  y : 0.254568 m
  z : 0.370338 m
  rx: -0.095515 rad
  ry: 0.258551 rad
  rz: 0.782288 rad
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
| --- | --- | --- |
| `getTcpPos` | `int getTcpPos(double *pose, const char *strIpAddress = "")` | `0` on success, `-1` on failure. Full parameter notes are in <a href="02_robot_state.html#gettcppos-gettcpexternalforce-gettcpforce-getjointforce">02 Robot State Reading</a>. |

`getTcpPos(pose, ip)` returns `[x, y, z, rx, ry, rz]`. Translation uses m, and orientation uses axis-angle rad. This example changes only `z` by `0.01`, which is 10 mm along the base-frame Z axis; the orientation components keep the values returned by the API.

```{rubric} Call Example
```

```cpp
double pose[6] = {0.0};
int ret = getTcpPos(pose, "192.168.10.75");
if (ret == 0) {
    pose[2] += 0.010;  // Base Z + 10 mm
}
```


````

### `moveLToPose`

````{container} api-example-block

| Function | Prototype | Return Value |
| --- | --- | --- |
| `moveLToPose` | `int moveLToPose(double *pose, double v, double a, double *active_tcp = nullptr, int zv_shaper_order = 0, double zv_shaper_frequency = 0, double zv_shaper_damping_ratio = 0, bool avoid_singular = false, const char *strIpAddress = "")` | `0` when the command is accepted, `-1` on failure. A successful return does not mean the motion has finished. |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `pose` | In, `double[6]` | Target TCP pose `[x, y, z, rx, ry, rz]`; position is in m, orientation is axis-angle in rad. |
| `v` | In, `double` | Linear translation velocity, in m/s. |
| `a` | In, `double` | Linear translation acceleration, in m/s². |
| `active_tcp` | In, `double[6]` or `nullptr` | TCP pose used for the motion calculation; `nullptr` uses the current default TCP. |
| `zv_shaper_order` / `zv_shaper_frequency` / `zv_shaper_damping_ratio` | In, defaults `0` / `0.0` / `0.0` | Zero-vibration shaper parameters. This example disables them. |
| `avoid_singular` | In, `bool`, default `false` | Whether to enable singularity avoidance. This example passes `false`. |
| `strIpAddress` | In, `const char*`, default `""` | Robot IP. An empty value is only appropriate for single-arm connections. |

`moveLToPose(pose, v, a, active_tcp, zv_shaper_order, zv_shaper_frequency, zv_shaper_damping_ratio, avoid_singular, ip)` executes linear motion to a TCP pose. `v` and `a` are translational velocity and acceleration in m/s and m/s². `active_tcp=nullptr` uses the current default TCP.

This example disables shaping and sets `avoid_singular=false`. This is not a safety guarantee: the API may still fail due to unreachable targets, singularity, joint limits, or path collision conditions, so check the return value and keep the error code. The call returns immediately; `waitMove` only confirms that execution finished. On failure, call `stop` first, then hold the brake and release the service.

```{rubric} Call Example
```

```cpp
double pose[6] = {0.4221, 0.0, 0.9403, 0.0, 0.0, 0.0};
double vel = 0.2;  // m/s
double acc = 0.2;  // m/s²
int ret = moveLToPose(pose, vel, acc, nullptr,
                      0, 0.0, 0.0, false, "192.168.10.75");
if (ret < 0) {
    printf("moveLToPose failed! Return value = %d\n", ret);
} else {
    wait_move("192.168.10.75");
}
```

````

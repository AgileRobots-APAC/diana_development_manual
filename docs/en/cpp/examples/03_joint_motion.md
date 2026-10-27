# 03 Joint Motion

This example starts from the current joint position, increases J1 by 10°, and demonstrates joint target motion with `moveJToTarget`.

```bash
./build/bin/03_joint_motion --model diana7 --ip 192.168.10.75       # dry-run
./build/bin/03_joint_motion --model diana7 --ip 192.168.10.75 --run
```

| API | Purpose |
|---|---|
| `getJointPos` | Read the current joint position and generate the target |
| `releaseBrake` | Enable the robot before motion |
| `moveJToTarget` | Send a joint target with velocity and acceleration |
| `getRobotState` in shared `waitMove` | Poll the controller until motion finishes |
| `stop` / `holdBrake` | Stop on failure and hold the brake after completion |

## Example Call Flow

Validate `--model` and joint count → read and print start/target joints → exit unless `--run` is set → enable and wait 2 s → send motion → wait for completion → hold brake and release resources.

### Key Source Snippet

```cpp
double start[kMaxSupportedJointCount] = {0.0};
getJointPos(start, ip);
double target[kMaxSupportedJointCount] = {0.0};
for (int i = 0; i < joint_count; ++i) target[i] = start[i];
target[0] += 10.0 * 3.14159265358979323846 / 180.0;

releaseBrake(ip);
std::this_thread::sleep_for(std::chrono::seconds(2));
const int ret = moveJToTarget(target, 0.10, 0.20, 0, 0.0, 0.0, ip);
if (ret < 0) stop(ip); else waitMove(ip);
holdBrake(ip);
```

```{warning}
This is a real robot motion example. Use `--run` only after personnel isolation, payload, speed, clearance, and emergency-stop checks are complete.
```

## Execution Results
::::{dropdown} Run output (Thor20 example)
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/03_joint_motion --model thor20 --ip 192.168.10.75 --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-34530,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-40279,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-43493,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-49897,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-51516,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  6
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 6 (Thor series)
Selected model: Thor20 (expected 6 axes)
Current joints:
  J1: 0.138225 rad
  J2: 0.086804 rad
  J3: 2.266153 rad
  J4: -0.021567 rad
  J5: 0.256526 rad
  J6: -0.131168 rad
Example target (J1 + 10 deg):
  J1: 0.312757 rad
  J2: 0.086804 rad
  J3: 2.266153 rad
  J4: -0.021567 rad
  J5: 0.256526 rad
  J6: -0.131168 rad
Motion finished.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} Run output (Diana7 example)
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/03_joint_motion --model diana7 --ip 192.168.10.75 --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-42154,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-50175,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-53591,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-50845,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-43160,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Current joints:
  J1: -0.898793 rad
  J2: -0.405294 rad
  J3: -0.145524 rad
  J4: 2.654542 rad
  J5: -0.092266 rad
  J6: -1.157964 rad
  J7: -0.014824 rad
Example target (J1 + 10 deg):
  J1: -0.724260 rad
  J2: -0.405294 rad
  J3: -0.145524 rad
  J4: 2.654542 rad
  J5: -0.092266 rad
  J6: -1.157964 rad
  J7: -0.014824 rad
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
| --- | --- | --- |
| `getJointPos` | `int getJointPos(double *joints, const char *strIpAddress = "")` | `0` on success, `-1` on failure. Full parameter notes are in <a href="02_robot_state.html#getjointpos-getjointangularvel-getjointcurrent-getjointtorque">02 Robot State Reading</a>. |

`getJointPos(joints, ip)` reads the current robot's joint angles in rad. The example allocates `kMaxSupportedJointCount` elements and processes the actual count returned by `getJointCount()`. It changes only J1, so it must first read the full current joint vector and then copy and adjust the target array; do not assemble a complete joint vector from an assumed pose.

```{rubric} Call Example
```

```cpp
double joints[kMaxSupportedJointCount] = {0.0};
int ret = getJointPos(joints, "192.168.10.75");
if (ret == 0) {
    joints[0] += 2.0 * PI / 180.0;
}
```


````

### `moveJToTarget`

````{container} api-example-block

| Function | Prototype | Return Value |
| --- | --- | --- |
| `moveJToTarget` | `int moveJToTarget(double *joints, double v, double a, int zv_shaper_order = 0, double zv_shaper_frequency = 0, double zv_shaper_damping_ratio = 0, const char *strIpAddress = "")` | `0` when the command is accepted, `-1` on failure. A successful return does not mean the motion has finished. |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `joints` | In, `double[kMaxSupportedJointCount]` | Target joint positions, in rad; the actual joint count determines the valid elements. |
| `v` | In, `double` | Joint motion velocity, in rad/s. |
| `a` | In, `double` | Joint motion acceleration, in rad/s². |
| `zv_shaper_order` | In, `int`, default `0` | Zero-vibration shaper order. This example passes `0`, so it is disabled. |
| `zv_shaper_frequency` | In, `double`, default `0.0` | Zero-vibration shaper frequency. Use `0.0` when shaping is disabled. |
| `zv_shaper_damping_ratio` | In, `double`, default `0.0` | Zero-vibration shaper damping ratio. Use `0.0` when shaping is disabled. |
| `strIpAddress` | In, `const char*`, default `""` | Robot IP. An empty value is only appropriate for single-arm connections. |

`moveJToTarget(joints, v, a, zv_shaper_order, zv_shaper_frequency, zv_shaper_damping_ratio, ip)` executes `moveJ` with a joint target. `joints` uses rad, `v` uses rad/s, and `a` uses rad/s². The three vibration-shaping arguments are `0` in this example, so shaping is disabled.

The call returns immediately after the command is issued. It does not mean the robot has reached the target. Use shared `waitMove` to wait for completion, and call `stop` immediately if the return value is negative; do not keep waiting or send the next motion command. See [01 Connection and Model Identification](01_connection.md) for the `releaseBrake` / `holdBrake` lifecycle usage.

```{rubric} Call Example
```

```cpp
double joints[kMaxSupportedJointCount] = {0.0};
double vel = 0.1;  // rad/s
double acc = 0.2;  // rad/s²
int ret = moveJToTarget(joints, vel, acc,
                         0, 0.0, 0.0, "192.168.10.75");
if (ret < 0) {
    printf("moveJToTarget failed! Return value = %d\n", ret);
} else {
    wait_move("192.168.10.75");
}
```

````

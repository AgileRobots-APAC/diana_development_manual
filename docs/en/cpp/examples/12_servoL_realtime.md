# 12 ServoL Realtime Streaming

This example reads the current TCP pose and generates a sine trajectory of ±5 cm in base-frame Z around it. It sends `servoL_ex` at a 10 ms period for 20 seconds (2,000 cycles), then returns to the starting pose. Dry-run is the default.

```bash
./build/bin/12_servoL_realtime --model diana7 --ip 192.168.10.75
./build/bin/12_servoL_realtime --model diana7 --ip 192.168.10.75 --run
```

| API | Purpose |
|---|---|
| `getTcpPos` | Read current TCP pose and generate the target |
| `servoL_ex` | Send Cartesian servo targets with `time=0.01`, `look_ahead_time=0.01`, and `gain=2000` |
| `stop` / `holdBrake` | Stop and hold brake when the loop exits or an error occurs |

## Real-Time Control Prerequisites

The following constraints apply to the C++ SDK `servoJ`, `servoL`, `speedJ`, `speedL`, and extension interfaces. This example uses `servoL_ex`.

For `servoJ` and `servoL`, the control-PC call period must be no greater than the configured `time`:

- If `time` is longer than the call period, a new command interrupts the previous one.
- Matching them is theoretically optimal but depends on control-PC real-time performance.
- If `time` is shorter, a late next command can cause deceleration or safety handling.

The recommended `look_ahead_time` range is 0.03–0.2 s; the recommended `gain` range is 100–2000. Aggressive parameters do not replace speed/acceleration-limit checks, network quality, or real-time guarantees. `servoJ` uses joint targets. `servoL` also involves Cartesian parameters such as `pose`, `scale`, and `active_tcp`; joint speed can still exceed a limit after inverse kinematics. `speedJ` and `speedL` plan speed changes from target velocity and allowed acceleration; at high rates, network jitter and host latency can increase position error.

```{warning}
Before high-speed or high-rate control, validate network jitter, host scheduling, and trajectory continuity at a safe speed. Unsatisfied tracking requirements can cause overshoot or motion errors.
```

```{hint}
General Linux is not hard real-time. If necessary, install a real-time kernel that matches the Ubuntu release used by the control PC.
```

## Example Call Flow

Connect and validate → read the current TCP → generate a sine trajectory of ±0.05 m in Z around it → dry-run or enable → call `servoL_ex` every 10 ms for 20 seconds (2,000 cycles) → stop, hold brake, and release resources.

### Key Source Snippet

```cpp
double start_pose[6] = {0.0};
getTcpPos(start_pose, ip);

int ret = 0;
for (int i = 0; i < kServoCycleCount && ret == 0; ++i) {
    const double phase = 2.0 * kPi * i / (kServoCycleCount - 1);
    double target_pose[6] = {
        start_pose[0], start_pose[1], start_pose[2] + kZAmplitudeMeters * std::sin(phase),
        start_pose[3], start_pose[4], start_pose[5],
    };
    ret = servoL_ex(target_pose, 0.01, 0.01, 2000, 1.0, false, nullptr, ip);
    std::this_thread::sleep_for(std::chrono::milliseconds(kServoPeriodMilliseconds));
}
stop(ip);
holdBrake(ip);
```

```{warning}
This example only validates the basic call flow and should not be used as a production real-time controller.
```

## Execution Results
::::{dropdown} Run output
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/12_servoL_realtime --model diana7 --ip 192.168.10.75 --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-57381,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-36468,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-59682,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-46332,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-45325,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Servo trajectory: base Z sine wave centered at the current TCP, +/-50 mm, 2000 cycles at 10 ms (20 s).
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

`getTcpPos(pose, ip)` reads `[x,y,z,rx,ry,rz]`, with translation in m and orientation in axis-angle rad. This example uses the current TCP as the baseline for its sinusoidal Z trajectory of ±`0.05` m, so read the current actual pose before every validation run instead of treating a previous target as the real-time starting point.

```{rubric} Call Example
```

```cpp
double start_pose[6] = {0.0};
int ret = getTcpPos(start_pose, "192.168.10.75");
```


````

### `servoL_ex`

````{container} api-example-block

| Function | Prototype | Return Value |
| --- | --- | --- |
| `servoL_ex` | `int servoL_ex(double *pose, double time, double look_ahead_time, double gain, double scale, bool realiable, double *active_tcp = nullptr, const char *strIpAddress = "")` | `0` when the command is accepted, `-1` on failure. Exit the loop and stop if any cycle fails. |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `pose` | In, `double[6]` | Target TCP pose for each control cycle `[x, y, z, rx, ry, rz]`; position is in m, orientation is axis-angle in rad. |
| `time` | In, `double` | Control-period parameter, in s. The application's real call period must not exceed it. |
| `look_ahead_time` | In, `double` | Look-ahead time for smoothing and tracking. The manual's typical range is `0.03-0.2 s`. |
| `gain` | In, `double` | Tracking gain. The manual's typical range is `100-2000`. |
| `scale` | In, `double` | Trajectory scale factor. This example uses `1.0`, meaning no additional scaling. |
| `realiable` | In, `bool` | Feedback/reliability switch of the extended interface. The current Example source passes `false`. |
| `active_tcp` | In, `double[6]` or `nullptr` | Tool coordinate pose. `nullptr` uses the controller's default TCP. |
| `strIpAddress` | In, `const char*`, default `""` | Robot IP. An empty value is only appropriate for single-arm connections. |

`servoL_ex(pose, time, look_ahead_time, gain, scale, realiable, active_tcp, ip)` is used for high-frequency Cartesian position servoing over short displacements. `pose` is `[x,y,z,rx,ry,rz]` in m and axis-angle rad, and each call should provide a continuous target.

`time=0.01` is the control-period argument; the application call period must not exceed it. This example uses a 10 ms sleep to demonstrate the call chain, but general Linux scheduling does not provide a hard real-time guarantee. `look_ahead_time` affects smoothing and tracking, and `gain` affects tracking gain; the manual gives typical ranges of 0.03–0.2 s and 100–2000. The example's `0.01` look-ahead time is only for minimal validation and must not be used directly as a production parameter.

`scale=1.0` means no additional scaling; `realiable` is the feedback switch of the extended interface, and its exact data behavior follows the current SDK header. If any cycle returns a negative value, exit the loop, call `stop`, and then hold the brake.

```{rubric} Call Example
```

```cpp
double start_pose[6] = {0.0};
getTcpPos(start_pose, "192.168.10.75");

for (int i = 0; i < 2000; ++i) {
    const double phase = 2.0 * kPi * i / 1999.0;
    double target_pose[6] = {
        start_pose[0], start_pose[1], start_pose[2] + 0.05 * std::sin(phase),
        start_pose[3], start_pose[4], start_pose[5],
    };
    int ret = servoL_ex(target_pose, 0.01, 0.01, 2000, 1.0, false, nullptr, "192.168.10.75");
    if (ret < 0) break;
    std::this_thread::sleep_for(std::chrono::milliseconds(10));
}
stop("192.168.10.75");
holdBrake("192.168.10.75");
```

````

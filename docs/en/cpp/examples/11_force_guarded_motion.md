# 11 Force-Guarded Stop

This example moves slowly along base-frame X at 0.01 m/s and stops when `|Fx| >= 5 N` or after a 10 s timeout. Dry-run is the default. On completion it reports a force-threshold stop, normal timeout, or command failure, together with the triggering or last valid `Fx` sample.

```bash
./build/bin/11_force_guarded_motion --model diana7 --ip 192.168.10.75
./build/bin/11_force_guarded_motion --model diana7 --ip 192.168.10.75 --run
```

| API | Purpose |
|---|---|
| `speedL` | Send base-frame X velocity for up to 10 s |
| `getTcpForce` | Read TCP six-axis force every 10 ms and check Fx |
| `stop` / `holdBrake` | Stop and hold brake on threshold, timeout, or completion |

## Example Call Flow

Initialize and validate model → print velocity and threshold plan → dry-run or enable → call `speedL` → read force for up to 1,000 cycles → threshold or timeout → stop, hold brake, release resources, and report the stop reason and Fx.

### Key Source Snippet

```cpp
double v[6] = {0.01, 0, 0, 0, 0, 0};
double a[2] = {0.02, 0.05};
double f[6] = {0.0};

const int ret = speedL(v, a, 10.0, nullptr, ip);
bool stopped_by_force = false;
bool has_force_sample = false;
double last_fx = 0.0;
for (int i = 0; ret == 0 && i < 1000; ++i) {
    if (getTcpForce(f, ip) == 0) {
        last_fx = f[0];
        has_force_sample = true;
        if (last_fx >= 5.0 || last_fx <= -5.0) {
            stopped_by_force = true;
            break;
        }
    }
    std::this_thread::sleep_for(std::chrono::milliseconds(10));
}
stop(ip);
holdBrake(ip);
```

```{danger}
This example does not replace collision protection or safety functions. Use it only after force sensing, payload, speed, workspace, and emergency-stop checks are complete.
```

## Execution Results
::::{dropdown} Run output
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/11_force_guarded_motion --model diana7 --ip 192.168.10.75 --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-57869,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-44051,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-51738,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-48802,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-43919,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Guarded move: base X at 0.01 m/s, stop at |Fx| >= 5 N or after 10 s.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
 
Stopped by force threshold: Fx=-5.34248 N (threshold=+/-5 N).
```
::::


## API Usage and Call Examples

### `speedL`

````{container} api-example-block

| Function | Prototype | Return Value |
| --- | --- | --- |
| `speedL` | `int speedL(double *speed, double *a, double t, double *active_tcp = nullptr, const char *strIpAddress = "")` | `0` when the command is accepted, `-1` on failure. A successful return does not mean velocity mode has ended. |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `speed` | In, `double[6]` | TCP speed `[vx, vy, vz, wx, wy, wz]`; the first three values are in m/s, and the last three are in rad/s. |
| `a` | In, `double[2]` | Acceleration array. `a[0]` is translation acceleration in m/s², and `a[1]` is rotation acceleration in rad/s². |
| `t` | In, `double` | Velocity-command duration parameter, in s. It does not replace application-level stop conditions. |
| `active_tcp` | In, `double[6]` or `nullptr` | Tool coordinate pose. `nullptr` uses the controller's default TCP. |
| `strIpAddress` | In, `const char*`, default `""` | Robot IP. An empty value is only appropriate for single-arm connections. |

`speedL(speed, a, t, active_tcp, ip)` enters Cartesian velocity mode. `speed` is `[vx,vy,vz,wx,wy,wz]`; the first three values use m/s and the last three use rad/s; this example only sets `0.01 m/s` along base-frame X. `a` is a linear/angular acceleration array, and this example passes `[0.02, 0.05]`; `t=10.0` sets the maximum duration.

The API returns immediately, and `t` is not a collision-protection or safety-stop mechanism. The application must define stop conditions and call `stop(ip)` on abnormal paths.

```{rubric} Call Example
```

```cpp
double speeds[6] = {0.1, 0.0, 0.0, 0.0, 0.0, 0.0};
double acc[2] = {0.30, 0.50};
int ret = speedL(speeds, acc, 0, nullptr, "192.168.10.75");
if (ret < 0) printf("speedL failed!\n");
```


````

### `getTcpForce` / `stop`

````{container} api-example-block

| Function | Prototype | Return Value |
| --- | --- | --- |
| `getTcpForce` | `int getTcpForce(double *forces, const char *strIpAddress = "")` | `0` when the 6D force is obtained and valid, `-1` when it cannot be obtained or is invalid. Full parameter notes are in <a href="02_robot_state.html#gettcppos-gettcpexternalforce-gettcpforce-getjointforce">02 Robot State Reading</a>. |
| `stop` | `int stop(const char *strIpAddress = "")` | `0` on success, `-1` on failure. An empty `strIpAddress` is only appropriate for single-arm connections. |

`getTcpForce(force, ip)` writes `[Fx,Fy,Fz,Mx,My,Mz]`. This example checks `|Fx| >= 5 N` every 10 ms as a business threshold. Confirm force validity, coordinate meaning, tool payload, and singularity status separately.

Regardless of threshold, timeout, or read failure, the flow calls `stop` and then `holdBrake`. Do not use this mode as a substitute for collision detection, emergency stop, or safety control systems.

```{rubric} Call Example
```

```cpp
double force[6] = {0.0};
if (getTcpForce(force, "192.168.10.75") == 0 && force[0] >= 5.0) {
    stop("192.168.10.75");
}
```

````

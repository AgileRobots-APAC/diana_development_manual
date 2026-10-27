# 10 Jog Motion

This example jogs J1 in the positive direction at low speed by default. `--mode` can instead jog the TCP along base-frame +X or rotate it about base-frame +Z. `--duration` is limited to 0.1-2.0 s, and dry-run is the default.

```bash
./build/bin/10_jog_motion --model diana7 --ip 192.168.10.75
./build/bin/10_jog_motion --model diana7 --ip 192.168.10.75 --mode joint --duration=0.5 --run
./build/bin/10_jog_motion --model diana7 --ip 192.168.10.75 --mode tcp --duration=0.5 --run
./build/bin/10_jog_motion --model diana7 --ip 192.168.10.75 --mode rotate --duration=0.5 --run
```

| API | Purpose |
|---|---|
| `releaseBrake` | Enable before jogging |
| `moveJoint` / `moveTcp_ex` / `rotationTCP_ex` | Jog J1, translate TCP along base-frame +X, or rotate TCP about base-frame +Z according to `--mode` |
| `stop` | Stop after the requested duration |
| `holdBrake` | Hold the brake after stopping |

## Example Call Flow

Check model, mode, and duration → initialize and validate → print jog plan → dry-run or enable → send the selected jog command → wait for requested duration → `stop` → hold brake and release resources.

### Key Source Snippet

```cpp
if (releaseBrake(ip) < 0) return 6;
std::this_thread::sleep_for(std::chrono::seconds(2));

int ret = 0;
if (mode == JogMode::Joint) {
    ret = moveJoint(T_MOVE_UP, 0, 0.05, 0.10, ip);
} else if (mode == JogMode::Tcp) {
    ret = moveTcp_ex(E_BASE_COORDINATE, T_MOVE_X_UP, 0.01, 0.02, ip);
} else {
    ret = rotationTCP_ex(E_BASE_COORDINATE, T_MOVE_Z_UP, 0.10, 0.20, ip);
}
std::this_thread::sleep_for(
    std::chrono::milliseconds(static_cast<int>(seconds * 1000)));

stop(ip);       // moveJoint does not stop itself
holdBrake(ip);
return ret < 0 ? 7 : 0;
```

## Execution Results
::::{dropdown} Run output (No additional arguments)
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/10_jog_motion --model diana7 --ip 192.168.10.75
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-56992,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-55761,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-33285,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-32860,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-37918,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Warning] -20006:_interpolaterPosition warning:SPD_UNREACHABLE.
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
::::{dropdown} Run output (--mode joint --duration=0.5 --run)
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/10_jog_motion --model diana7 --ip 192.168.10.75 --mode joint --duration=0.5 --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-48859,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-55242,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-43536,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-54001,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-50762,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Warning] -20006:_interpolaterPosition warning:SPD_UNREACHABLE.
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
::::{dropdown} Run output (--mode tcp --duration=0.5 --run)
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/10_jog_motion --model diana7 --ip 192.168.10.75 --mode tcp --duration=0.5 --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-57406,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-45504,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-57263,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-53911,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-48143,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Warning] -20006:_interpolaterPosition warning:SPD_UNREACHABLE.
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
::::{dropdown} Run output (--mode rotate --duration=0.5 --run)
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/10_jog_motion --model diana7 --ip 192.168.10.75 --mode rotate --duration=0.5 --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-46396,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-45755,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-57564,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-35831,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-59706,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Warning] -20006:_interpolaterPosition warning:SPD_UNREACHABLE.
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

### `moveJoint` / `moveTcp_ex` / `rotationTCP_ex` / `stop`

````{container} api-example-block

| Function | Prototype | Return Value |
| --- | --- | --- |
| `moveJoint` | `int moveJoint(joint_direction_e d, int i, double v, double a, const char *strIpAddress = "")` | `0` when the command is accepted, `-1` on failure. A successful return does not mean jogging has stopped. |
| `moveTcp_ex` | `int moveTcp_ex(coordinate_e c, tcp_direction_e d, double v, double a, const char *strIpAddress = "")` | `0` when the command is accepted, `-1` on failure. A successful return does not mean jogging has stopped. |
| `rotationTCP_ex` | `int rotationTCP_ex(coordinate_e c, tcp_direction_e d, double v, double a, const char *strIpAddress = "")` | `0` when the command is accepted, `-1` on failure. A successful return does not mean jogging has stopped. |
| `stop` | `int stop(const char *strIpAddress = "")` | `0` on success, `-1` on failure. |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `d` | In, `joint_direction_e` or `tcp_direction_e` | Joint jog direction uses `T_MOVE_UP` / `T_MOVE_DOWN`; TCP direction uses `T_MOVE_X_UP`, `T_MOVE_X_DOWN`, `T_MOVE_Y_UP`, `T_MOVE_Y_DOWN`, `T_MOVE_Z_UP`, or `T_MOVE_Z_DOWN`. |
| `i` | In, `int` | Joint index, starting from `0`; `0` is J1. |
| `c` | In, `coordinate_e` | TCP jog coordinate system. Values include `E_BASE_COORDINATE`, `E_TOOL_COORDINATE`, `E_WORK_PIECE_COORDINATE`, and `E_VIEW_COORDINATE`. |
| `v` | In, `double` | Jog velocity. Joint jog uses rad/s, TCP translation uses m/s, and TCP rotation uses rad/s. |
| `a` | In, `double` | Jog acceleration. Joint jog uses rad/s², TCP translation uses m/s², and TCP rotation uses rad/s². |
| `strIpAddress` | In, `const char*`, default `""` | Robot IP. An empty value is only appropriate for single-arm connections. |

`moveJoint(direction, index, v, a, ip)` is the manual joint jog API. `direction` selects positive or negative direction. `index` starts from `0`, so `0` is J1 in this example. `v` and `a` use rad/s and rad/s².

`moveTcp_ex(E_BASE_COORDINATE, T_MOVE_X_UP, 0.01, 0.02, ip)` jogs the TCP along base-frame +X. `rotationTCP_ex(E_BASE_COORDINATE, T_MOVE_Z_UP, 0.10, 0.20, ip)` rotates the TCP about base-frame +Z. `--mode` accepts only `joint` (default), `tcp`, or `rotate`.

The API returns immediately and does not stop automatically after the requested duration. This example measures time in the application thread and then explicitly calls `stop(ip)`, so the duration is only a business control condition, not a position-accuracy guarantee of the API. Before the call, wait about 2 s after `releaseBrake` succeeds; at the end, call `stop` first and then `holdBrake`. Error paths must follow the same stop logic and must not rely only on process exit.

```{rubric} Call Example
```

```cpp
move_direct_e direction = T_MOVE_UP;
int joint_index = 0;
double vel = 0.2;
double acc = 0.8;

int ret = moveJoint(direction, joint_index, vel, acc, "192.168.10.75");
if (ret < 0) printf("moveJoint failed!\n");
sleep(3);
stop("192.168.10.75");
```

````

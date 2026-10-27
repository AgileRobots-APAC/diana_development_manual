# 01 Connection and Model Identification

This example demonstrates the API lifecycle, SDK version query, robot state query, and selected-profile joint-count validation. It does not enable or move the robot by default.

```bash
./build/bin/01_connection --list-models
./build/bin/01_connection --model diana7 --ip 192.168.10.75
./build/bin/01_connection --model diana7 --ip 192.168.10.75 --enable
```

| API | Purpose |
|---|---|
| `initSrvNetInfo` / `initSrv` | Set the controller IP, register callbacks, and start the API service |
| `getJointCount` | Read the actual joint count and compare it with the family expected by `--model` |
| `getLibraryVersion` / `getRobotState` | Read the SDK runtime version and current robot state |
| `releaseBrake` / `holdBrake` | Demonstrate enable and brake hold only when `--enable` is set |
| `destroySrv` | Release service resources |

## Example Call Flow

Parse model and IP → initialize the network structure and service → wait for callbacks → validate joint count → print version and state → optionally enable/hold brake → release the service. A successful connection does not mean motion is allowed.

### Key Source Snippet

```cpp
srv_net_st net_info;
initSrvNetInfo(&net_info);
std::strcpy(net_info.SrvIp, ip);

const int init_ret = initSrv(errorCallback, stateCallback, &net_info);
if (init_ret < 0) return 2;

const unsigned short version = getLibraryVersion();
const char state = getRobotState(ip);

if (enable && releaseBrake(ip) == 0) {
    std::this_thread::sleep_for(std::chrono::seconds(2));
    holdBrake(ip);
}
destroySrv(ip);
```

## Execution Results
### Matching joint count with `--enable`: release and hold brake
::::{dropdown} Run output (Thor20 example)
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ export LD_LIBRARY_PATH="$PWD/third_party/diana_sdk_cpp/lib:$LD_LIBRARY_PATH"
~/work/diana_examples_cpp$ ./build/bin/01_connection --model thor20 --ip 192.168.10.75 --enable
Robot IP: 192.168.10.75
Requested model: Thor20
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-56945,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-54423,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-37044,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-44760,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-39350,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  6
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 6 (Thor series)
Selected model: Thor20 (expected 6 axes)
Diana API library version(raw): 769
Robot state: 5 (hold-brake)
Calling releaseBrake()...
Calling holdBrake()...
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} Run output (Diana7 example)
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ export LD_LIBRARY_PATH="$PWD/third_party/diana_sdk_cpp/lib:$LD_LIBRARY_PATH"
~/work/diana_examples_cpp$ ./build/bin/01_connection --model diana7 --ip 192.168.10.75 --enable
Robot IP: 192.168.10.75
Requested model: Diana7
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-37239,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-51228,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-53366,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-39892,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-33812,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Diana API library version(raw): 769
Robot state: 5 (hold-brake)
Calling releaseBrake()...
Calling holdBrake()...
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
### Joint-count mismatch: exit before brake operation
::::{dropdown} Run output
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/01_connection --model diana7 --ip 192.168.10.75 --enable
Robot IP: 192.168.10.75
Requested model: Diana7
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-49780,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-46105,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-57686,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-42316,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-40461,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  6
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 6 (Thor series)
Selected model: Diana7 (expected 7 axes)
Robot model mismatch: selected Diana7 expects 7 axes, but the connected robot reports 6.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::

## API Usage and Call Examples

The notes below follow the Industrial Diana API Manual for C/C++ V3.3.0.

### `initSrvNetInfo` / `initSrv` / `destroySrv`

````{container} api-example-block

| Function | Prototype | Return Value |
| --- | --- | --- |
| `initSrvNetInfo` | `void initSrvNetInfo(srv_net_st *pinfo)` | No return value. |
| `initSrv` | `int initSrv(FNCERRORCALLBACK fnError, FNCSTATECALLBACK fnState, srv_net_st *pinfo)` | `0` on success, `-1` on failure. |
| `destroySrv` | `int destroySrv(const char *strIpAddress = "")` | `0` on success, `-1` on failure. |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `pinfo` / `pInfo` | In/out, `srv_net_st*` | Network configuration structure. It contains `SrvIp` and local ports for heartbeat, robot-state push, service, realtime service, and pass-through service. A port value of `0` lets the system assign it automatically. Initialize it with `initSrvNetInfo`, then set `SrvIp`. |
| `fnError` | In, `FNCERRORCALLBACK` | Error callback. It receives the error code and robot IP. The callback runs from SDK threads, so avoid blocking work, motion commands, or long I/O inside it. |
| `fnState` | In, `FNCSTATECALLBACK` | State callback. It receives `StrRobotStateInfo*` and the robot IP; the structure contains joint, TCP, force, collision, error, and warning state caches. |
| `strIpAddress` | In, `const char*`, default `""` | Robot IP. An empty value is only appropriate for single-arm connections. `destroySrv("")` releases resources for all successfully initialized robots. |

`initSrvNetInfo(srv_net_st* pInfo)` initializes the network structure and randomly assigns the required ports. After that, write the controller IP to `pInfo->SrvIp`; do not partially initialize this structure yourself.

`initSrv(fnError, fnState, srv_net_st* pInfo)` is required before other API calls. It returns `0` on success and a negative value on failure. Callbacks are invoked by background threads, so keep them short and avoid motion commands or blocking I/O inside callbacks.

`destroySrv(ip)` releases service resources. Call it on every path after a successful initialization.

```{rubric} Call Example
```

```cpp
srv_net_st* pInfo = new srv_net_st();
initSrvNetInfo(pInfo);
strcpy(pInfo->SrvIp, "192.168.10.75");

int ret = initSrv(fnError, fnState, pInfo);
if (ret < 0) {
    printf("initSrv failed! Return value = %d\n", ret);
}
// ... use other APIs
destroySrv("192.168.10.75");
delete pInfo;
```


````

### `getLibraryVersion` / `getRobotState` / `getJointCount`

````{container} api-example-block

| Function | Prototype | Return Value |
| --- | --- | --- |
| `getLibraryVersion` | `unsigned short getLibraryVersion()` | Runtime library version. The high 8 bits are the major version, and the low 8 bits are the minor version. |
| `getRobotState` | `char getRobotState(const char *strIpAddress = "")` | State code: `0` running, `1` paused, `2` idle, `3` free-driving, `4` zero-space-free-driving, `5` hold-brake, `6` error, `7` handling-error, `8` rescueMode. |
| `getJointCount` | `int getJointCount(const char *strIpAddress = "")` | Joint count of the specified robot. |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `strIpAddress` | In, `const char*`, default `""` | Robot IP. An empty value is only appropriate for single-arm connections. |

`getLibraryVersion()` returns the runtime library version value for logging and troubleshooting; it cannot replace checking the SDK `version` file and headers.

`getRobotState(ip)` reads the current controller state, and `getJointCount(ip)` reads the actual joint count. After connecting, the example compares that value with the expected joint count of the selected profile, so it can detect a Diana/Thor family mismatch, but it cannot distinguish exact models with the same joint count. A successful connection itself does not mean the robot is enabled or ready to move.

```{rubric} Call Example
```

```cpp
unsigned short version = getLibraryVersion();
char state = getRobotState("192.168.10.75");
int joint_count = getJointCount("192.168.10.75");
```


````

### `releaseBrake` / `holdBrake`

````{container} api-example-block

| Function | Prototype | Return Value |
| --- | --- | --- |
| `releaseBrake` | `int releaseBrake(const char *strIpAddress = "")` | `0` on success, `-1` on failure. |
| `holdBrake` | `int holdBrake(const char *strIpAddress = "")` | `0` on success, `-1` on failure. |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `strIpAddress` | In, `const char*`, default `""` | Robot IP. An empty value is only appropriate for single-arm connections. |

`releaseBrake(ip)` releases the brake and enables the robot. The manual requires an approximately 2 s delay after success before other operations. `holdBrake(ip)` applies the brake and stops the robot. This example uses `--enable` only to verify the pair of calls and does not send motion commands.

```{rubric} Call Example
```

```cpp
int ret = releaseBrake("192.168.10.75");
if (ret < 0) printf("releaseBrake failed!\n");
sleep(2);  // The manual requires a delay after releasing the brake
holdBrake("192.168.10.75");
```

````

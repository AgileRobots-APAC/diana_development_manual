# 01 Connection and Model Identification

This example demonstrates the minimal connection lifecycle of the Python SDK: initialize the API service, validate the robot model and joint count, read the SDK version and robot state, and optionally demonstrate releasing/holding the brake. It does not release the brake or move the robot by default.

```bash
python3 examples/01_connection/main.py --list-models
python3 examples/01_connection/main.py --model diana7 --ip 192.168.10.75
python3 examples/01_connection/main.py --model diana7 --ip 192.168.10.75 --enable
```

| API | Purpose |
|---|---|
| `initSrv` | Set the controller IP, register error/state callbacks, and start the API service |
| `getJointCount` | Read the actual joint count and validate `--model` |
| `getLibraryVersion` / `getRobotState` | Read the SDK runtime version and current robot state |
| `releaseBrake` / `holdBrake` | Demonstrate brake release/hold only when `--enable` is set |
| `destroySrv` | Release the API service resources for that IP |

## Example Call Flow

Parse the model and IP → create Python callback objects → call `initSrv` → wait for the state thread to update → query the joint count and validate the model → print the SDK version and robot state → optionally release/hold the brake → call `destroySrv` to release resources.

### Key Source Snippet

```python
error_cb = api.FNCERRORCALLBACK(lambda code, ip: print(f"[Diana API error] code={code}"))
state_cb = api.FNCSTATECALLBACK(lambda state, ip: None)

if not api.initSrv([args.ip, 0, 0, 0, 0, 0], error_cb, state_cb):
    print("initSrv failed", file=sys.stderr)
    return 2

try:
    time.sleep(0.2)
    detect_and_validate_robot(api, args.ip, profile)
    print(f"Diana API library version(raw): {api.getLibraryVersion()}")
    state = api.getRobotState(args.ip)
    print(f"Robot state: {state} ({robot_state_name(state)})")
finally:
    api.destroySrv(args.ip)
```

```{important}
Keep the Python callback objects referenced for the entire connection lifetime. The example stores them in local variables and guarantees a final `destroySrv` call inside a `try/finally` block.
```

## Execution Results
### Matching model axis count with `--enable`: release, then re-engage the brakes
::::{dropdown} Run Output (Thor20 example)
:class-container: api-example-block
```bash
~/work/diana_examples_python$ export PYTHONPATH="$PWD/third_party/diana_sdk_python/lib:$PYTHONPATH"
~/work/diana_examples_python$ export LD_LIBRARY_PATH="$PWD/third_party/diana_sdk_python/lib:$LD_LIBRARY_PATH"
~/work/diana_examples_python$ python3 examples/01_connection/main.py --model thor20 --ip 192.168.10.75 --enable
Robot IP: 192.168.10.75
Requested model: Thor20
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-42800,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-60147,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-32808,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-51933,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-43539,remoteipPort:-0
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
::::{dropdown} Run Output (Diana7 example)
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/01_connection/main.py --model diana7 --ip 192.168.10.75 --enable
Robot IP: 192.168.10.75
Requested model: Diana7
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-53945,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-40247,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-35381,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-43896,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-52496,remoteipPort:-0
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
### Model axis-count mismatch: exit before brake operation
::::{dropdown} Run Output
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/01_connection/main.py --model diana7 --ip 192.168.10.75 --enable
Robot IP: 192.168.10.75
Requested model: Diana7
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-39024,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-40912,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-48074,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-32835,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-35004,remoteipPort:-0
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

### `initSrv` / `destroySrv`

````{container} api-example-block

| Function | Prototype | Return Value |
|---|---|---|
| `initSrv` | `initSrv(srv_net_st, fnError=None, fnState=None)` | `True` on success; otherwise `False` |
| `destroySrv` | `destroySrv(ipAddress='')` | `True` on success; otherwise `False` |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `srv_net_st` | In, `list` / `tuple` (6 elements) | Service network info `[ip, heartbeat port, robot-state port, service port, realtime service port, pass-through service port]`: the first element is the robot IP string, the rest are local port numbers; `0` lets the system assign the port. The wrapper fills an `SRV_NET_ST` structure from it. |
| `fnError` | In, `FNCERRORCALLBACK` (ctypes callback), default `None` | Error callback receiving an `int` error code and the robot IP as `bytes`; use `formatError` for a readable message. With `None` the wrapper passes an empty callback. It is invoked from a background thread in real time, so avoid sleep or other blocking work; keep a reference to the callback object for the whole connection. |
| `fnState` | In, `FNCSTATECALLBACK` (ctypes callback), default `None` | State callback receiving `POINTER(StrRobotStateInfo)` and the robot IP as `bytes`; the structure holds joint position/angular velocity/current/torque, TCP pose, TCP external force, collision flag, TCP six-axis force, joint-space external force, trajectory state, and error and warning info. With `None` the wrapper passes an empty callback. |
| `ipAddress` | In, `str`, default `''` | IP of the robot whose service resources `destroySrv` releases; if empty, resources of all robots successfully initialized with `initSrv` are released. |

| Function | Python Call | Return Value |
|---|---|---|
| `initSrv` | `initSrv([ip, 0, 0, 0, 0, 0], error_cb, state_cb)` | Truthy on success; falsy on failure |
| `destroySrv` | `destroySrv(ip)` | Releases the service resources for the given IP; truthy on success |

The first argument to the Python `initSrv` is the service-network information list. This example sets only the first element to the robot IP and leaves the remaining port/configuration entries as `0`, so the SDK uses its default configuration. `initSrv`, `releaseBrake`, `holdBrake`, and `destroySrv` all pass the native return code through the wrapper's `message()` helper and expose a Boolean result. Keep the callback objects referenced for the complete connection lifetime, and call `destroySrv` from a `finally` block.

```python
robot_ip = "192.168.10.75"
error_cb = api.FNCERRORCALLBACK(lambda code, ip: print(code))
state_cb = api.FNCSTATECALLBACK(lambda state, ip: None)

if api.initSrv([robot_ip, 0, 0, 0, 0, 0], error_cb, state_cb):
    api.destroySrv(robot_ip)
```

````

### `getLibraryVersion` / `getRobotState` / `getJointCount`

````{container} api-example-block

| Function | Prototype | Return Value |
|---|---|---|
| `getLibraryVersion` | `getLibraryVersion()` | Raw SDK runtime version value |
| `getRobotState` | `getRobotState(ipAddress='')` | Robot state code |
| `getJointCount` | `getJointCount(ipAddress='')` | Robot joint count; the failure return value follows the SDK |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `ipAddress` | In, `str`, default `''` | Robot IP string; the wrapper encodes it to UTF-8 `bytes` for the native library. Leaving it empty only works when a single robot is connected. Applies to `getRobotState` and `getJointCount`; `getLibraryVersion` takes no parameters. |

| Function | Python Call | Description |
|---|---|---|
| `getLibraryVersion` | `getLibraryVersion()` | Returns the raw SDK runtime version value |
| `getRobotState` | `getRobotState(ip)` | Returns the controller's current state code |
| `getJointCount` | `getJointCount(ip)` | Returns the joint count of the connected arm |

`getJointCount` validates the user-selected `--model` against the physically connected arm. Diana-series arms are typically 7-axis and Thor-series arms are typically 6-axis; the example uses the count only as a family check, and the exact model still depends on the on-site configuration and release documentation.

```python
joint_count = api.getJointCount("192.168.10.75")
state = api.getRobotState("192.168.10.75")
version = api.getLibraryVersion()
```

````

### `releaseBrake` / `holdBrake`

````{container} api-example-block

| Function | Prototype | Return Value |
|---|---|---|
| `releaseBrake` | `releaseBrake(ipAddress='')` | `True` on success; otherwise `False` |
| `holdBrake` | `holdBrake(ipAddress='')` | `True` on success; otherwise `False` |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `ipAddress` | In, `str`, default `''` | Robot IP string; the wrapper encodes it to UTF-8 `bytes` for the native library. Leaving it empty only works when a single robot is connected. Applies to `releaseBrake` and `holdBrake`. |

| Function | Python Call | Description |
|---|---|---|
| `releaseBrake` | `releaseBrake(ip)` | Release the brake / enable; truthy on success |
| `holdBrake` | `holdBrake(ip)` | Hold the brake |

The example does not change the brake state by default. Only when `--enable` is explicitly supplied does it call `releaseBrake`, wait about 2 seconds, and then call `holdBrake`.

```python
if args.enable:
    if api.releaseBrake(args.ip):
        time.sleep(2)
        api.holdBrake(args.ip)
```

```{warning}
Releasing the brake is not the same as enabling motion. Any subsequent motion still requires on-site confirmation of personnel, payload, speed, clearance, and the emergency stop.
```

````

# 02 Robot State and Diagnostics

This example reads joint state, TCP state, external force, the link-query result, errors/warnings, and collision status. It is read-only by default and does not trigger motion.

```bash
python3 examples/02_robot_state/main.py --model diana7 --ip 192.168.10.75
```

| API | Purpose |
|---|---|
| `getJointPos` / `getJointAngularVel` / `getJointCurrent` / `getJointTorque` | Read joint position, velocity, current, and torque |
| `getTcpPos` / `getTcpExternalForce` / `getTcpForce` / `getJointForce` | Read TCP pose and external-force/force values |
| `getRobotState` / `getLinkState` | Read robot state and check whether the link query succeeds |
| `getLastError` / `getLastWarning` / `formatError` / `isCollision` | Read error, warning, and collision diagnostics |

## Example Call Flow

Initialize the connection → validate `--model` against the actual joint count → allocate joint and TCP output buffers → read joint position, velocity, current, and torque → read the TCP pose and external force → read state, link, error, warning, and collision information → release resources.

### Key Source Snippet

```python
joints = [0.0] * MAX_SUPPORTED_JOINT_COUNT
speeds = [0.0] * MAX_SUPPORTED_JOINT_COUNT
currents = [0.0] * MAX_SUPPORTED_JOINT_COUNT
torques = [0.0] * MAX_SUPPORTED_JOINT_COUNT
pose = [0.0] * 6

api.getJointPos(joints, args.ip)
api.getJointAngularVel(speeds, args.ip)
api.getJointCurrent(currents, args.ip)
api.getJointTorque(torques, args.ip)
api.getTcpPos(pose, args.ip)

print(f"TCP external resultant force: {api.getTcpExternalForce(args.ip)} N")
print(f"Robot state: {api.getRobotState(args.ip)}")
print(f"Link state: {api.getLinkState(args.ip)}")
print(f"Last error: {api.getLastError(args.ip)}")
print(f"Last warning: {api.getLastWarning(args.ip)}")
print(f"Collision detected: {'yes' if api.isCollision(args.ip) else 'no'}")
```

## Execution Results
::::{dropdown} Run Output (Thor20 example)
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/02_robot_state/main.py --model thor20 --ip 192.168.10.75
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-42492,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-43551,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-55245,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-34016,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-42811,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  6
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 6 (Thor series)
Selected model: Thor20 (expected 6 axes)
Joint position:
  J1: 0.312738 rad
  J2: 0.076608 rad
  J3: 2.261263 rad
  J4: -0.020944 rad
  J5: 0.272060 rad
  J6: -0.131611 rad
Joint angular velocity (rad/s):
  J1: 0.000000
  J2: 0.000000
  J3: -0.000052
  J4: -0.000000
  J5: -0.000129
  J6: 0.000270
Joint current (A):
  J1: -0.030000
  J2: -0.090000
  J3: -0.020000
  J4: -0.070000
  J5: 0.010000
  J6: 0.010000
Joint torque (Nm):
  J1: 0.431070
  J2: -1.212400
  J3: -0.649380
  J4: -0.891480
  J5: -0.205460
  J6: 0.243340
TCP pose:
  x : 0.763940 m
  y : 0.246959 m
  z : 0.653544 m
  rx: -0.593250 rad
  ry: 2.538431 rad
  rz: 0.050236 rad
TCP external resultant force: 81.9007575821741 N
Robot state: 5 (hold-brake)
Diagnostics:
Link state: True
Last error: 0
Last warning: 0
Collision detected: no
TCP external wrench:
  Fx: -9.007881 N
  Fy: -8.589646 N
  Fz: 80.949430 N
  Tx: 2.472332 Nm
  Ty: 9.221275 Nm
  Tz: 3.166177 Nm
Joint external force/torque:
  J1: -1.162589
  J2: -59.554468
  J3: -44.517283
  J4: 1.909759
  J5: -2.672212
  J6: -0.135624
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} Run Output (Diana7 example)
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/02_robot_state/main.py --model diana7 --ip 192.168.10.75
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-56183,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-42942,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-55733,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-54869,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-38425,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Joint position:
  J1: -0.143918 rad
  J2: -0.497597 rad
  J3: -0.016622 rad
  J4: 2.424481 rad
  J5: 0.041777 rad
  J6: -1.157364 rad
  J7: 0.025059 rad
Joint angular velocity (rad/s):
  J1: 0.000000
  J2: 0.000000
  J3: 0.000000
  J4: 0.000000
  J5: 0.000000
  J6: -0.000000
  J7: -0.000000
Joint current (A):
  J1: -0.010000
  J2: -0.080000
  J3: -0.010000
  J4: 0.000000
  J5: 0.000000
  J6: 0.000000
  J7: 0.000000
Joint torque (Nm):
  J1: -0.210170
  J2: -5.311310
  J3: -0.214400
  J4: -25.770260
  J5: 0.610545
  J6: 1.673125
  J7: 0.192860
TCP pose:
  x : 0.376633 m
  y : 0.059481 m
  z : 0.510095 m
  rx: -0.042810 rad
  ry: -0.060300 rad
  rz: 0.199412 rad
TCP external resultant force: 2.327428372392532 N
Robot state: 5 (hold-brake)
Diagnostics:
Link state: True
Last error: 0
Last warning: 0
Collision detected: no
TCP external wrench:
  Fx: -0.065114 N
  Fy: 0.515723 N
  Fz: -2.268637 N
  Tx: -0.099276 Nm
  Ty: -0.437782 Nm
  Tz: -0.241334 Nm
Joint external force/torque:
  J1: 0.169748
  J2: 0.446997
  J3: -0.201170
  J4: 0.811536
  J5: -0.021598
  J6: 0.198123
  J7: -0.194292
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop

```
::::

## API Usage and Call Examples

### `getJointPos` / `getJointAngularVel` / `getJointCurrent` / `getJointTorque`

````{container} api-example-block

| Function | Prototype | Return Value |
|---|---|---|
| `getJointPos` | `getJointPos(jointsPosition, ipAddress='')` | `True` on success; otherwise `False` |
| `getJointAngularVel` | `getJointAngularVel(jointAngularVel, ipAddress='')` | `True` on success; otherwise `False` |
| `getJointCurrent` | `getJointCurrent(jointCurrent, ipAddress='')` | `True` on success; otherwise `False` |
| `getJointTorque` | `getJointTorque(jointTorque, ipAddress='')` | `True` on success; otherwise `False` |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `jointsPosition` | Out (filled in place), `list[float]` (length `JOINT_NUM`, at most 7) | Joint angles, in rad. The caller pre-allocates the list (e.g. `[0.0] * MAX_SUPPORTED_JOINT_COUNT`); the wrapper copies back as many elements as the list holds from a 7-element ctypes array. |
| `jointAngularVel` | Out (filled in place), `list[float]` (length `JOINT_NUM`, at most 7) | Joint angular velocities, in rad/s. The caller pre-allocates the list (e.g. `[0.0] * MAX_SUPPORTED_JOINT_COUNT`); the wrapper copies back as many elements as the list holds from a 7-element ctypes array. |
| `jointCurrent` | Out (filled in place), `list[float]` (length `JOINT_NUM`, at most 7) | Joint currents, in A. The caller pre-allocates the list (e.g. `[0.0] * MAX_SUPPORTED_JOINT_COUNT`); the wrapper copies back as many elements as the list holds from a 7-element ctypes array. |
| `jointTorque` | Out (filled in place), `list[float]` (length `JOINT_NUM`, at most 7) | Actual joint torques (zero offset removed), in Nm. The caller pre-allocates the list (e.g. `[0.0] * MAX_SUPPORTED_JOINT_COUNT`); the wrapper copies back as many elements as the list holds from a 7-element ctypes array. |
| `ipAddress` | In, `str`, default `''` | Robot IP string; the wrapper encodes it to UTF-8 `bytes` for the native library. Leaving it empty only works when a single robot is connected. Applies to all four functions. |

| Function | Output | Unit |
|---|---|---|
| `getJointPos` | Joint position array | rad |
| `getJointAngularVel` | Joint angular velocity array | rad/s |
| `getJointCurrent` | Joint current array | A |
| `getJointTorque` | Joint torque array | Nm |

The Python wrapper writes into the list passed in as an output buffer. Buffers are allocated for the maximum supported joint count, and only the actual joint count returned by `getJointCount` is displayed.

```python
joints = [0.0] * MAX_SUPPORTED_JOINT_COUNT
if api.getJointPos(joints, ip):
    for index in range(joint_count):
        print(f"J{index + 1}: {joints[index]:.6f} rad")
```

````

### `getTcpPos` / `getTcpExternalForce` / `getTcpForce` / `getJointForce`

````{container} api-example-block

| Function | Prototype | Return Value |
|---|---|---|
| `getTcpPos` | `getTcpPos(tcpPose, ipAddress='')` | `True` on success; otherwise `False` |
| `getTcpExternalForce` | `getTcpExternalForce(ipAddress='')` | TCP resultant external-force scalar |
| `getTcpForce` | `getTcpForce(tcpForce, ipAddress='')` | `True` on success; otherwise `False` |
| `getJointForce` | `getJointForce(jointForce, ipAddress='')` | `True` on success; otherwise `False` |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `tcpPose` | Out (filled in place), `list[float]` (length at least 6) | TCP pose `[x, y, z, rx, ry, rz]`; position in m, orientation as axis-angle in rad. The wrapper copies the first 6 elements from a 6-element ctypes array; the result depends on the default TCP set by `setDefaultActiveTcp`. |
| `tcpForce` | Out (filled in place), `list[float]` (length at least 6) | External six-axis force at the TCP `[Fx, Fy, Fz, Mx, My, Mz]`; forces in N, moments in Nm. The wrapper copies the first 6 elements from a 6-element ctypes array; the result depends on the default TCP. |
| `jointForce` | Out (filled in place), `list[float]` (length `JOINT_NUM`, at most 7) | External force on each joint in joint space (joint-axis torque), in Nm. The caller pre-allocates the list (e.g. `[0.0] * MAX_SUPPORTED_JOINT_COUNT`); the wrapper copies back as many elements as the list holds from a 7-element ctypes array. |
| `ipAddress` | In, `str`, default `''` | Robot IP string; the wrapper encodes it to UTF-8 `bytes` for the native library. Leaving it empty only works when a single robot is connected. Applies to all four functions; it is the only parameter of `getTcpExternalForce`, which returns the magnitude of the resultant external force in the TCP frame (`float`). |

TCP poses use `[x, y, z, rx, ry, rz]`, with the first three values in m and the last three in rad. `getTcpExternalForce` returns the resultant external-force scalar rather than a six-axis wrench; `getTcpForce` returns `[Fx, Fy, Fz, Mx, My, Mz]`, with the first three values in N and the last three in Nm.

```python
tcp_pose = [0.0] * 6
tcp_force = [0.0] * 6
api.getTcpPos(tcp_pose, ip)
api.getTcpForce(tcp_force, ip)
```

````

### `getRobotState` / `getLinkState` / `getLastError` / `getLastWarning` / `isCollision`

````{container} api-example-block

| Function | Prototype | Return Value |
|---|---|---|
| `getRobotState` | `getRobotState(ipAddress='')` | Robot state code |
| `getLinkState` | `getLinkState(ipAddress='')` | The current wrapper returns only a success/failure Boolean, not the raw link-state code |
| `getLastError` | `getLastError(ipAddress='')` | Refer to the current SDK implementation and the API manual |
| `getLastWarning` | `getLastWarning(ipAddress='')` | Refer to the current SDK implementation and the API manual |
| `isCollision` | `isCollision(ipAddress='')` | Refer to the current SDK implementation and the API manual |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `ipAddress` | In, `str`, default `''` | Robot IP string; the wrapper encodes it to UTF-8 `bytes` for the native library. Leaving it empty only works when a single robot is connected. Applies to `getRobotState`, `getLinkState`, `getLastError`, `getLastWarning`, and `isCollision`. |

These calls read the controller's current diagnostic context. The current `DianaApi.py` implementation passes the native `getLinkState` return value through `message()`, so the example's `Link state` line prints a Boolean call result and must not be interpreted as a link-state enum. When an error, warning, or collision is reported, first resolve it according to the controller state and the API manual. Do not continue sending motion commands from an unknown state.

```python
state = api.getRobotState(ip)
link_state = api.getLinkState(ip)
last_error = api.getLastError(ip)
last_warning = api.getLastWarning(ip)
collision = api.isCollision(ip)
```

````

# 07 TCP, Frames, and Payload

This read-only example reports the current TCP, default TCP, default tool/workpiece frames, active payload, and pose transforms.

```bash
python3 examples/07_tcp_and_frames/main.py --model diana7 --ip 192.168.10.75
python3 examples/07_tcp_and_frames/main.py --model diana7 --ip 192.168.10.75 --offset=0,0,0.01,0,0,0
```

| API | Purpose |
|---|---|
| `getTcpPos` / `getDefaultActiveTcpPose` / `getDefaultActiveTcp` | Read TCP pose and default TCP |
| `getDefaultTcpCoordinate` / `getDefaultWorkPieceCoordinate` | Read default tool and workpiece frames |
| `getActiveTcpPayload` | Read active TCP payload |
| `rpy2Axis` / `pose2Homogeneous` / `homogeneous2Pose` | Pose and homogeneous transform conversion |

## Example Call Flow

Initialize the connection → validate the model → read the current TCP pose → read the default active TCP pose and homogeneous matrix → read the default tool/workpiece frame names → read the active TCP payload → convert the user-supplied `--offset` from RPY to axis-angle → compute the tool-relative target pose → release resources.

### Key Source Snippet

```python
tcp_pose = [0.0] * 6
active_tcp_pose = [0.0] * 6
active_tcp = [0.0] * 16
payload = [0.0] * 10

api.getTcpPos(tcp_pose, args.ip)
api.getDefaultActiveTcpPose(active_tcp_pose, args.ip)
api.getDefaultActiveTcp(active_tcp, args.ip)
api.getActiveTcpPayload(payload, args.ip)

rotation = [v * math.pi / 180.0 for v in args.offset[3:]]
api.rpy2Axis(rotation)
offset_axis = args.offset[:3] + rotation
api.pose2Homogeneous(tcp_pose, current_matrix)
api.pose2Homogeneous(offset_axis, offset_matrix)
api.homogeneous2Pose(target_matrix, target_pose)
```

## Execution Results
::::{dropdown} Run Output (default options)
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/07_tcp_and_frames/main.py --model thor20 --ip 192.168.10.75
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-45655,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-57565,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-48512,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-47295,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-38953,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  6
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 6 (Thor series)
Selected model: Thor20 (expected 6 axes)
Current TCP pose:
  x : 0.709417 m
  y : 0.375856 m
  z : 0.663535 m
  rx: -0.813284 rad
  ry: 2.480481 rad
  rz: 0.112364 rad
Default active TCP pose relative to flange:
  x : 0.000000 m
  y : 0.000000 m
  z : 0.000000 m
  rx: 0.000000 rad
  ry: 0.000000 rad
  rz: 0.000000 rad
Default active TCP homogeneous matrix:
  1.000000 0.000000 0.000000 0.000000
  -0.000000 1.000000 0.000000 0.000000
  0.000000 -0.000000 1.000000 0.000000
  0.000000 0.000000 0.000000 1.000000
Default TCP coordinate: TestTCP
Default workpiece coordinate: Base
Active TCP payload:
  mass=0.000000 kg
  center=(0.000000, 0.000000, 0.000000) m
  inertia=(0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000)
Tool-relative target pose:
  x : 0.709417 m
  y : 0.375856 m
  z : 0.663535 m
  rx: -0.813284 rad
  ry: 2.480481 rad
  rz: 0.112364 rad
Read-only example: no TCP, payload, or coordinate configuration is modified.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} Run Output (`--offset=0,0,0.01,0,0,0`)
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/07_tcp_and_frames/main.py --model thor20 --ip 192.168.10.75 --offset=0,0,0.01,0,0,0
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-48817,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-47790,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-50978,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-39225,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-39894,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  6
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 6 (Thor series)
Selected model: Thor20 (expected 6 axes)
Current TCP pose:
  x : 0.709430 m
  y : 0.375828 m
  z : 0.663507 m
  rx: -0.813197 rad
  ry: 2.480548 rad
  rz: 0.112374 rad
Default active TCP pose relative to flange:
  x : 0.000000 m
  y : 0.000000 m
  z : 0.000000 m
  rx: 0.000000 rad
  ry: 0.000000 rad
  rz: 0.000000 rad
Default active TCP homogeneous matrix:
  1.000000 0.000000 0.000000 0.000000
  -0.000000 1.000000 0.000000 0.000000
  0.000000 -0.000000 1.000000 0.000000
  0.000000 0.000000 0.000000 1.000000
Default TCP coordinate: TestTCP
Default workpiece coordinate: Base
Active TCP payload:
  mass=0.000000 kg
  center=(0.000000, 0.000000, 0.000000) m
  inertia=(0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000)
Tool-relative target pose:
  x : 0.709430 m
  y : 0.375828 m
  z : 0.673507 m
  rx: -0.813197 rad
  ry: 2.480548 rad
  rz: 0.112374 rad
Read-only example: no TCP, payload, or coordinate configuration is modified.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::


## API Usage and Call Examples

### `getTcpPos` / `getDefaultActiveTcpPose` / `getDefaultActiveTcp` / `getDefaultTcpCoordinate` / `getDefaultWorkPieceCoordinate` / `getActiveTcpPayload`

````{container} api-example-block

| Function | Prototype | Return Value |
|---|---|---|
| `getTcpPos` | `getTcpPos(tcpPose, ipAddress='')` | Fills the output pose; `True` on success, otherwise `False` |
| `getDefaultActiveTcpPose` | `getDefaultActiveTcpPose(arrPose, ipAddress='')` | Fills the output pose; `True` on success, otherwise `False` |
| `getDefaultActiveTcp` | `getDefaultActiveTcp(default_tcp, ipAddress='')` | Fills a 16-element homogeneous matrix; `True` on success, otherwise `False` |
| `getDefaultTcpCoordinate` | `getDefaultTcpCoordinate(ipAddress='')` | Returns `(success, name)` |
| `getDefaultWorkPieceCoordinate` | `getDefaultWorkPieceCoordinate(ipAddress='')` | Returns `(success, name)` |
| `getActiveTcpPayload` | `getActiveTcpPayload(payload, ipAddress='')` | Fills the payload array; `True` on success, otherwise `False` |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `tcpPose` | Out, `list[float]` (length 6) | Current TCP pose `[x, y, z, rx, ry, rz]` written by `getTcpPos`; position is in m, orientation is axis-angle in rad; filled in place. |
| `arrPose` | Out, `list[float]` (length 6) | Default active TCP pose written by `getDefaultActiveTcpPose`; position is in m, orientation is axis-angle in rad; filled in place. |
| `default_tcp` | Out, `list[float]` (length 16) | Default tool frame written by `getDefaultActiveTcp` as a 4x4 homogeneous matrix in a 16-element flat list; filled in place. |
| `payload` | Out, `list[float]` (length 10) | Payload written by `getActiveTcpPayload`: element 1 is mass, elements 2-4 are the center of mass, elements 5-10 are the inertia tensor; filled in place. |
| `ipAddress` | In, `str`, default `''` | Robot IP. An empty value is only appropriate for single-arm connections. Shared by all six functions. `getDefaultTcpCoordinate` / `getDefaultWorkPieceCoordinate` take only this parameter and return the frame name as a `str` in the result tuple. |

`getDefaultActiveTcpPose` outputs the default active TCP pose relative to the flange; `getDefaultActiveTcp` outputs it as a 4x4 homogeneous matrix. The two default-frame queries return `(success, name)`, and `getActiveTcpPayload` outputs the payload mass, center of mass, and related values. The example only reads these values and never modifies controller configuration.

```python
pose = [0.0] * 6
matrix = [0.0] * 16
payload = [0.0] * 10
api.getDefaultActiveTcpPose(pose, ip)
api.getDefaultActiveTcp(matrix, ip)
api.getActiveTcpPayload(payload, ip)
```

````

### `rpy2Axis` / `pose2Homogeneous` / `homogeneous2Pose`

````{container} api-example-block

| Function | Prototype | Return Value |
|---|---|---|
| `rpy2Axis` | `rpy2Axis(arr)` | Converts the array in place; `True` on success, otherwise `False` |
| `pose2Homogeneous` | `pose2Homogeneous(pose, matrix)` | Fills the matrix; `True` on success, otherwise `False` |
| `homogeneous2Pose` | `homogeneous2Pose(matrix, pose)` | Fills the pose; `True` on success, otherwise `False` |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `arr` | In/out, `list[float]` (length 3) | Rotation array for `rpy2Axis`, in rad: RPY before the call, converted to axis-angle in place on success. |
| `pose` | In or out, `list[float]` (length 6) | Pose vector `[x, y, z, rx, ry, rz]`; position is in m, orientation is axis-angle in rad. Input for `pose2Homogeneous` (a tuple is fine); output for `homogeneous2Pose` (filled in place). |
| `matrix` | In or out, `list[float]` (length 16) | 4x4 homogeneous transform matrix as a 16-element flat list. Output for `pose2Homogeneous` (filled in place); input for `homogeneous2Pose` (a tuple is fine). |

`--offset=x,y,z,roll,pitch,yaw` specifies translation in metres and RPY angles in degrees. The example converts the angle part from degrees to radians, then uses `rpy2Axis` to convert it to the axis-angle representation used by the SDK pose APIs. It then converts the current TCP pose and the offset pose to homogeneous matrices, multiplies them on the Python side, and converts the result back to a pose. It never writes TCP, frame, or payload configuration.

```python
rotation = [roll, pitch, yaw]
api.rpy2Axis(rotation)
offset_pose = [x, y, z] + rotation
api.pose2Homogeneous(offset_pose, offset_matrix)
```

````

### Tool coordinate system functions added in SDK V3.4

This example does not use the four functions below. They are available since SDK V3.4 and manage tool coordinate systems by tool name. `arrPose` is the pose of the TCP relative to the end flange, with 6 elements: the first three are the position XYZ (m) and the last three are the axis-angle RxRyRz (rad). The tool name must be UTF-8 encoded and at most 255 characters long.

| Function | Purpose |
|---|---|
| `DianaApi.addTcpPose(strToolName, arrPose, ipAddress='')` | Add a tool coordinate system |
| `DianaApi.setTcpPoseByTcpName(strToolName, arrPose, ipAddress='')` | Modify the tool coordinate system with the given name |
| `DianaApi.deleteTcpPoseByTcpName(strToolName, ipAddress='')` | Delete the tool coordinate system with the given name |
| `DianaApi.switchTcpPoseByTcpName(strToolName, ipAddress='')` | Switch to the tool coordinate system with the given name, making it the default active one |

Return value: `True` means success and `False` means failure. Note the following:

- The default `Flange` coordinate system cannot be modified or deleted under any circumstances.
- After a tool coordinate system is modified or deleted, the waypoints set in it are affected; use these functions with care.
- When the modified coordinate system is the active one, the new value takes effect on the client after one push cycle. Wait one push cycle before calling functions that depend on the latest tool coordinate system, such as `forward` and `inverse`.
- In impedance mode, modifying the default tool coordinate system returns failure.

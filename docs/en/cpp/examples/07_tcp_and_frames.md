# 07 TCP, Frames, and Payload

This read-only example prints TCP, default frame, and active payload information. When `--offset` is supplied, it only computes a tool-frame offset target locally and does not change controller configuration.

```bash
./build/bin/07_tcp_and_frames --model diana7 --ip 192.168.10.75
./build/bin/07_tcp_and_frames --model diana7 --ip 192.168.10.75 --offset=0,0,0.01,0,0,0
```

| API | Purpose |
|---|---|
| `getTcpPos` / `getDefaultActiveTcpPose` | Read current TCP pose and active TCP pose relative to flange |
| `getDefaultActiveTcp` / `getDefaultTcpCoordinate` / `getDefaultWorkPieceCoordinate` | Read the default active TCP as a 4x4 homogeneous matrix relative to the flange, plus the default TCP frame and workpiece frame names |
| `getActiveTcpPayload` | Read active TCP payload |
| `rpy2Axis` / `pose2Homogeneous` / `homogeneous2Pose` | Convert offset to axis-angle and homogeneous matrices, then recover target pose |

## Example Call Flow

Parse `x,y,z,roll,pitch,yaw` offset in m and degrees → read controller configuration → multiply the current TCP matrix by the tool offset matrix → print the computed result → release resources.

### Key Source Snippet

```cpp
double tcp_pose[6] = {0.0};
double active_tcp_pose[6] = {0.0};
double payload[10] = {0.0};

getTcpPos(tcp_pose, ip);
getDefaultActiveTcpPose(active_tcp_pose, ip);
getActiveTcpPayload(payload, ip);

double offset_axis[6] = {offset[0], offset[1], offset[2],
                         offset[3] * kPi / 180.0,
                         offset[4] * kPi / 180.0,
                         offset[5] * kPi / 180.0};
rpy2Axis(offset_axis + 3);
pose2Homogeneous(tcp_pose, current_matrix);
pose2Homogeneous(offset_axis, offset_matrix);
multiply4x4(current_matrix, offset_matrix, target_matrix);
homogeneous2Pose(target_matrix, target_pose);
```

## Execution Results
::::{dropdown} Run output (No additional arguments)
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/07_tcp_and_frames --model thor20 --ip 192.168.10.75
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-58344,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-43722,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-46522,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-54770,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-33062,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  6
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 6 (Thor series)
Selected model: Thor20 (expected 6 axes)
Current TCP pose:
  x : 0.764008 m
  y : 0.247045 m
  z : 0.653840 m
  rx: -0.593473 rad
  ry: 2.538024 rad
  rz: 0.050282 rad
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
  mass: 0.000000 kg
  center of mass: 0.000000, 0.000000, 0.000000 m
  inertia: 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000
Tool-relative offset: 0.000000, 0.000000, 0.010000, 0.000000, 0.000000, 0.000000 (m, deg)
Equivalent base-frame target (axis-angle):
  x : 0.764000 m
  y : 0.247044 m
  z : 0.663856 m
  rx: -0.593528 rad
  ry: 2.538010 rad
  rz: 0.050253 rad
Read-only example: no TCP, payload, or coordinate configuration is modified.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} Run output (--offset=0,0,0.01,0,0,0)
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/07_tcp_and_frames --model thor20 --ip 192.168.10.75 --offset=0,0,0.01,0,0,0
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-48060,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-46654,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-58932,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-59057,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-39286,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  6
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 6 (Thor series)
Selected model: Thor20 (expected 6 axes)
Current TCP pose:
  x : 0.764016 m
  y : 0.247031 m
  z : 0.653857 m
  rx: -0.593416 rad
  ry: 2.538024 rad
  rz: 0.050259 rad
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
  mass: 0.000000 kg
  center of mass: 0.000000, 0.000000, 0.000000 m
  inertia: 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000
Tool-relative offset: 0.000000, 0.000000, 0.010000, 0.000000, 0.000000, 0.000000 (m, deg)
Equivalent base-frame target (axis-angle):
  x : 0.764001 m
  y : 0.247043 m
  z : 0.663857 m
  rx: -0.593332 rad
  ry: 2.538046 rad
  rz: 0.050318 rad
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
| --- | --- | --- |
| `getTcpPos` | `int getTcpPos(double *pose, const char *strIpAddress = "")` | `0` on success, `-1` on failure. Full parameter notes are in <a href="02_robot_state.html#gettcppos-gettcpexternalforce-gettcpforce-getjointforce">02 Robot State Reading</a>. |
| `getDefaultActiveTcpPose` | `int getDefaultActiveTcpPose(double *arrPose, const char *strIpAddress = "")` | `0` on success, `-1` on failure. |
| `getDefaultActiveTcp` | `int getDefaultActiveTcp(double *default_tcp, const char *strIpAddress = "")` | `0` on success, `-1` on failure. |
| `getDefaultTcpCoordinate` | `int getDefaultTcpCoordinate(char *tcpName, const char *strIpAddress = "")` | `0` on success, `-1` on failure. |
| `getDefaultWorkPieceCoordinate` | `int getDefaultWorkPieceCoordinate(char *workpieceName, const char *strIpAddress = "")` | `0` on success, `-1` on failure. |
| `getActiveTcpPayload` | `int getActiveTcpPayload(double *payload, const char *strIpAddress = "")` | `0` on success, `-1` on failure. |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `pose` / `arrPose` | Out, `double[6]` | Six-dimensional pose `[x, y, z, rx, ry, rz]`; position is in m, orientation is axis-angle in rad. |
| `default_tcp` | Out, `double[16]` | Default TCP transform relative to the flange as a 4x4 homogeneous matrix. |
| `tcpName` / `workpieceName` | Out, `char*` | Default TCP coordinate name and default workpiece coordinate name. The caller must provide a large enough character buffer. |
| `payload` | Out, `double[10]` | Active TCP payload parameter array. This example only reads and displays the values. |
| `strIpAddress` | In, `const char*`, default `""` | Robot IP. An empty value is only appropriate for single-arm connections. |

`getTcpPos` reads the current default TCP pose `[x,y,z,rx,ry,rz]`. `getDefaultActiveTcpPose` reads the active TCP pose relative to the flange. Translation uses m and rotation uses axis-angle rad; the two meanings are not interchangeable.

`getDefaultActiveTcp` outputs the default active TCP relative to the flange as a 4x4 homogeneous transform matrix (`double[16]`); `getDefaultTcpCoordinate` and `getDefaultWorkPieceCoordinate` return the controller's current default frame names, and this example allocates 256-byte buffers for them; `getActiveTcpPayload` reads the active TCP payload. All of them are read-only queries, and this example does not modify any TCP, workpiece frame, or payload configuration.

```{rubric} Call Example
```

```cpp
double tcp_pose[6] = {0.0};
double active_tcp_pose[6] = {0.0};
getTcpPos(tcp_pose, "192.168.10.75");
getDefaultActiveTcpPose(active_tcp_pose, "192.168.10.75");

double payload[10] = {0.0};
if (getActiveTcpPayload(payload, "192.168.10.75") == 0) {
    printf("mass: %f kg\n", payload[0]);
}
```


````

### `rpy2Axis` / `pose2Homogeneous` / `homogeneous2Pose`

````{container} api-example-block

| Function | Prototype | Return Value |
| --- | --- | --- |
| `rpy2Axis` | `int rpy2Axis(double *arr)` | `0` on success, `-1` on failure. Full parameter notes are in <a href="05_kinematics.html#rpy2axis-axis2rpy">05 Kinematics and Pose Conversion</a>. |
| `pose2Homogeneous` | `int pose2Homogeneous(double *pose, double *matrix)` | `0` on success, `-1` on failure. |
| `homogeneous2Pose` | `int homogeneous2Pose(double *matrix, double *pose)` | `0` on success, `-1` on failure. |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `pose` | In or out, `double[6]` | Six-dimensional pose `[x, y, z, rx, ry, rz]`; position is in m, orientation is axis-angle in rad. |
| `matrix` | In or out, `double[16]` | 4x4 homogeneous transform matrix passed as a one-dimensional array. |
| `arr` | In/out, `double[3]` | Rotation array. `rpy2Axis` converts RPY to axis-angle in place, in rad. |

`rpy2Axis` converts the RPY part of `--offset` in place after the example converts degrees to rad. `pose2Homogeneous` and `homogeneous2Pose` convert between a 6D pose and a 4x4 homogeneous matrix.

The example computes `T_base_tcp x T_tcp_offset` locally for display only. Executing the target still requires separate checks for TCP, workpiece frame, IK, and path safety.

```{rubric} Call Example
```

```cpp
double tcp_pose[6] = {0.0};
double matrix[16] = {0.0};
double pose_again[6] = {0.0};

getTcpPos(tcp_pose, "192.168.10.75");
pose2Homogeneous(tcp_pose, matrix);
homogeneous2Pose(matrix, pose_again);
```

````

### Tool coordinate system functions added in SDK V3.4

This example does not use the four functions below. They are available since SDK V3.4 and manage tool coordinate systems by tool name. `arrPose` is the pose of the TCP relative to the end flange, with 6 elements: the first three are the position XYZ (m) and the last three are the axis-angle RxRyRz (rad). The tool name must be UTF-8 encoded and at most 255 characters long.

| Function | Purpose |
|---|---|
| `addTcpPose(strToolName, arrPose, strIpAddress)` | Add a tool coordinate system |
| `setTcpPoseByTcpName(strToolName, arrPose, strIpAddress)` | Modify the tool coordinate system with the given name |
| `deleteTcpPoseByTcpName(strToolName, strIpAddress)` | Delete the tool coordinate system with the given name |
| `switchTcpPoseByTcpName(strToolName, strIpAddress)` | Switch to the tool coordinate system with the given name, making it the default active one |

Return value: `0` means success and `-1` means failure. Note the following:

- The default `Flange` coordinate system cannot be modified or deleted under any circumstances.
- After a tool coordinate system is modified or deleted, the waypoints set in it are affected; use these functions with care.
- When the modified coordinate system is the active one, the new value takes effect on the client after one push cycle. Wait one push cycle before calling functions that depend on the latest tool coordinate system, such as `forward` and `inverse`.
- In impedance mode, modifying the default tool coordinate system returns failure.

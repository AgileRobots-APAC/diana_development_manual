# 02 Robot State and Diagnostics

This read-only example collects state and diagnostic information without changing robot state.

```bash
./build/bin/02_robot_state --model diana7 --ip 192.168.10.75
```

| API | Purpose |
|---|---|
| `getJointPos` / `getJointAngularVel` / `getJointCurrent` / `getJointTorque` | Read joint position, velocity, current, and torque |
| `getTcpPos` / `getTcpExternalForce` / `getTcpForce` / `getJointForce` | Read TCP pose, TCP force, resultant external force, and joint force |
| `getRobotState` / `getLinkState` | Read controller and link state |
| `getLastError` / `getLastWarning` / `formatError` / `isCollision` | Print recent error/warning and collision state |

## Example Call Flow

Initialize and validate joint count → read joint, TCP, link, and diagnostic data → print arrays using the actual joint count → release the service. Analyze error codes together with [Error Codes](../../reference/error_codes.md).

### Key Source Snippet

```cpp
double joints[kMaxSupportedJointCount] = {0.0};
double pose[6] = {0.0};
double tcp_force[6] = {0.0};

if (getJointPos(joints, ip) == 0) printJoints(joints, joint_count);
if (getTcpPos(pose, ip) == 0) printPose(pose);
if (getTcpForce(tcp_force, ip) == 0) {
    std::cout << "Fx=" << tcp_force[0] << " N, Mx=" << tcp_force[3] << " Nm\n";
}
printDiagnosticCode("Last error", getLastError(ip), ip);
std::cout << "Collision: " << isCollision(ip) << "\n";
```

## Execution Results
::::{dropdown} Run output (Thor20 example)
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/02_robot_state --model thor20 --ip 192.168.10.75
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-48370,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-33573,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-44766,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-35333,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-50112,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  6
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 6 (Thor series)
Selected model: Thor20 (expected 6 axes)
Joint position:
  J1: 0.138189 rad
  J2: 0.086804 rad
  J3: 2.266177 rad
  J4: -0.021591 rad
  J5: 0.256586 rad
  J6: -0.131121 rad
Joint angular velocity (rad/s):
  J1: 0.000078
  J2: -0.000019
  J3: 0.000155
  J4: 0.000181
  J5: -0.000284
  J6: -0.000463
Joint current (A):
  J1: -0.070000
  J2: 0.140000
  J3: -0.040000
  J4: -0.070000
  J5: -0.030000
  J6: 0.070000
Joint torque (Nm):
  J1: -1.024020
  J2: 0.916410
  J3: -0.042950
  J4: -0.375750
  J5: -0.131170
  J6: 0.207110
TCP pose:
  x : 0.795304 m
  y : 0.110622 m
  z : 0.643907 m
  rx: -0.369857 rad
  ry: 2.579263 rad
  rz: -0.012099 rad
TCP external resultant force: 87.429418 N
Robot state: 5 (hold-brake)

Diagnostics:
Link state: connected (ret=0)
Last error: 0
Last warning: 0
Collision detected: no
TCP external wrench:
  Fx: -15.203647 N
  Fy: -5.760403 N
  Fz: 85.904423 N
  Mx: 5.051126 Nm
  My: 9.299372 Nm
  Mz: 3.800984 Nm
Joint external force/torque:
  J1: 0.908345
  J2: -64.001072
  J3: -43.802303
  J4: 2.052728
  J5: -2.634886
  J6: -0.130495
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} Run output (Diana7 example)
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/02_robot_state --model diana7 --ip 192.168.10.75
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-33901,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-52482,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-59848,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-39854,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-54668,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Joint position:
  J1: -0.898793 rad
  J2: -0.405306 rad
  J3: -0.145512 rad
  J4: 2.654566 rad
  J5: -0.092230 rad
  J6: -1.157964 rad
  J7: -0.014812 rad
Joint angular velocity (rad/s):
  J1: 0.000000
  J2: 0.000000
  J3: -0.000000
  J4: 0.000000
  J5: -0.000000
  J6: 0.000000
  J7: 0.000000
Joint current (A):
  J1: 0.030000
  J2: -0.020000
  J3: -0.020000
  J4: 0.030000
  J5: 0.000000
  J6: 0.000000
  J7: 0.000000
Joint torque (Nm):
  J1: 0.000000
  J2: -6.936690
  J3: 0.528065
  J4: -21.868760
  J5: 0.550995
  J6: 1.486875
  J7: -0.120330
TCP pose:
  x : 0.159665 m
  y : 0.286636 m
  z : 0.360335 m
  rx: -0.119228 rad
  ry: 0.252445 rad
  rz: 0.955710 rad
TCP external resultant force: 0.953926 N
Robot state: 5 (hold-brake)

Diagnostics:
Link state: connected (ret=0)
Last error: 0
Last warning: 0
Collision detected: no
TCP external wrench:
  Fx: 0.852372 N
  Fy: 0.285719 N
  Fz: -0.319061 N
  Mx: 0.090425 Nm
  My: 0.166779 Nm
  Mz: 0.116338 Nm
Joint external force/torque:
  J1: -0.000000
  J2: 0.197345
  J3: 0.233353
  J4: -0.094571
  J5: -0.012338
  J6: 0.063129
  J7: 0.130687
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop

```
::::

## API Usage and Call Examples

These query APIs read data from the SDK background state cache after initialization. A successful return should still be interpreted together with data freshness.

### `getJointPos` / `getJointAngularVel` / `getJointCurrent` / `getJointTorque`

````{container} api-example-block

| Function | Prototype | Return Value |
| --- | --- | --- |
| `getJointPos` | `int getJointPos(double *joints, const char *strIpAddress = "")` | `0` on success, `-1` on failure. |
| `getJointAngularVel` | `int getJointAngularVel(double *vels, const char *strIpAddress = "")` | `0` on success, `-1` on failure. |
| `getJointCurrent` | `int getJointCurrent(double *currents, const char *strIpAddress = "")` | `0` on success, `-1` on failure. |
| `getJointTorque` | `int getJointTorque(double *torques, const char *strIpAddress = "")` | `0` on success, `-1` on failure. |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `joints` | Out, `double[kMaxSupportedJointCount]` | Joint position array, in rad. |
| `vels` | Out, `double[kMaxSupportedJointCount]` | Joint angular velocity array, in rad/s. |
| `currents` | Out, `double[kMaxSupportedJointCount]` | Joint current array, in A. |
| `torques` | Out, `double[kMaxSupportedJointCount]` | Real joint torque array, in Nm; the manual describes it as the zero-offset-removed torque value. |
| `strIpAddress` | In, `const char*`, default `""` | Robot IP. An empty value is only appropriate for single-arm connections. |

These APIs output joint-space data. The examples allocate buffers with the repository's `kMaxSupportedJointCount`, then process only the number of valid elements returned by `getJointCount()`. Units are rad, rad/s, A, and Nm respectively.

```{rubric} Call Example
```

```cpp
double joints[kMaxSupportedJointCount] = {0.0};
int ret = getJointPos(joints, "192.168.10.75");
if (ret == 0) {
    printf("J1 = %f rad\n", joints[0]);
}

double vel[kMaxSupportedJointCount] = {0.0};
double current[kMaxSupportedJointCount] = {0.0};
double torque[kMaxSupportedJointCount] = {0.0};
getJointAngularVel(vel, "192.168.10.75");
getJointCurrent(current, "192.168.10.75");
getJointTorque(torque, "192.168.10.75");
```


````

### `getTcpPos` / `getTcpExternalForce` / `getTcpForce` / `getJointForce`

````{container} api-example-block

| Function | Prototype | Return Value |
| --- | --- | --- |
| `getTcpPos` | `int getTcpPos(double *pose, const char *strIpAddress = "")` | `0` on success, `-1` on failure. |
| `getTcpExternalForce` | `double getTcpExternalForce(const char *strIpAddress = "")` | Resultant external force at the TCP in the TCP coordinate system. |
| `getTcpForce` | `int getTcpForce(double *forces, const char *strIpAddress = "")` | `0` when the 6D force is obtained and valid, `-1` when it cannot be obtained or is invalid. |
| `getJointForce` | `int getJointForce(double *forces, const char *strIpAddress = "")` | `0` on success, `-1` on failure. |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `pose` | Out, `double[6]` | TCP pose `[x, y, z, rx, ry, rz]`; position is in m, orientation is axis-angle in rad. The default TCP affects this value. |
| `forces` | Out, `double[6]` or `double[kMaxSupportedJointCount]` | `getTcpForce` outputs `[Fx, Fy, Fz, Mx, My, Mz]`; `getJointForce` outputs joint-space external force/torque data. |
| `strIpAddress` | In, `const char*`, default `""` | Robot IP. An empty value is only appropriate for single-arm connections. |

`getTcpPos(pose, ip)` writes `[x, y, z, rx, ry, rz]`; translation uses m and orientation uses axis-angle rad. `getTcpExternalForce(ip)` returns the resultant TCP external force. `getTcpForce(force, ip)` writes `[Fx, Fy, Fz, Mx, My, Mz]`. `getJointForce` writes joint-space external force data; the example also uses a buffer of size `kMaxSupportedJointCount`, and it must not be mixed with TCP six-axis force data.

Do not use force readings for safety decisions when the robot is near singularity or force data validity is unknown.

```{rubric} Call Example
```

```cpp
double pose[6] = {0.0};
int ret = getTcpPos(pose, "192.168.10.75");
if (ret == 0) {
    printf("z = %f m\n", pose[2]);
}

double force[6] = {0.0};
if (getTcpForce(force, "192.168.10.75") == 0) {
    printf("Fx=%f, Fy=%f, Fz=%f\n", force[0], force[1], force[2]);
}
double resultant_force = getTcpExternalForce("192.168.10.75");
double joint_force[kMaxSupportedJointCount] = {0.0};
getJointForce(joint_force, "192.168.10.75");
```


````

### `getRobotState` / `getLinkState` / `getLastError` / `getLastWarning` / `formatError` / `isCollision`

````{container} api-example-block

| Function | Prototype | Return Value |
| --- | --- | --- |
| `getRobotState` | `char getRobotState(const char *strIpAddress = "")` | State-code meanings are listed in <a href="01_connection.html#getlibraryversion-getrobotstate-getjointcount">01 Connection and Model Detection</a>. |
| `getLinkState` | `int getLinkState(const char *strIpAddress = "")` | `0` for connected, `-1` for disconnected. |
| `getLastError` | `int getLastError(const char *strIpAddress = "")` | `0` means no error; any other value is the last error code. |
| `getLastWarning` | `int getLastWarning(const char *strIpAddress = "")` | `0` means no warning; any other value is the last warning code. |
| `formatError` | `const char *formatError(int e, const char *strIpAddress = "")` | Human-readable string for error code `e`. |
| `isCollision` | `bool isCollision(const char *strIpAddress = "")` | `true` if a collision is detected, otherwise `false`. |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `e` | In, `int` | Error code, usually from the error callback or `getLastError`. For hardware error `-2001`, the manual recommends waiting about 100 ms before calling `formatError` for detailed text. |
| `strIpAddress` | In, `const char*`, default `""` | Robot IP. An empty value is only appropriate for single-arm connections. |

`getRobotState`, `getLinkState`, and `isCollision` are used for controller, link, and collision diagnostics. When an abnormal state appears, stop business command issuance first, then handle the site condition.

`getLastError`, `getLastWarning`, and `formatError` record numeric diagnostic codes and convert them into readable text. Record the code and timestamp before clearing errors or performing recovery actions.

```{rubric} Call Example
```

```cpp
char robot_state = getRobotState("192.168.10.75");
int link_state = getLinkState("192.168.10.75");
int error = getLastError("192.168.10.75");
int warning = getLastWarning("192.168.10.75");
printf("error: %s\n", formatError(error, "192.168.10.75"));
bool collision = isCollision("192.168.10.75");
```

````

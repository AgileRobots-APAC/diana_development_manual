# 05 Kinematics

This non-motion example demonstrates forward kinematics, inverse kinematics, reference inverse kinematics, and RPY/axis-angle conversion.

```bash
./build/bin/05_kinematics --model diana7 --ip 192.168.10.75
```

| API | Purpose |
|---|---|
| `getJointPos` | Read the current joint vector as input and reference |
| `forward` | Compute TCP pose from joint angles |
| `inverse` | Compute one joint solution from a pose |
| `inverse_ext` | Use a reference joint vector to select a nearby solution |
| `rpy2Axis` / `axis2RPY` | Convert between RPY and axis-angle orientation |

## Example Call Flow

Connect and read current joints → run FK to get the pose → run ordinary IK and reference IK for that pose → print both results → convert orientation representation → release resources. For redundant robots, also read [Inverse Solutions and Configuration Continuity](../../guide/inverse_uniqueness.md).

### Key Source Snippet

```cpp
double joints[kMaxSupportedJointCount] = {0.0};
double pose[6] = {0.0};
double solution[kMaxSupportedJointCount] = {0.0};

getJointPos(joints, ip);
forward(joints, pose, nullptr, ip);
inverse(pose, solution, nullptr, ip);
inverse_ext(joints, pose, solution, nullptr, ip);

double rotation[3] = {pi, pi / 3.0, pi / 6.0};
rpy2Axis(rotation);   // rotation now contains axis-angle
axis2RPY(rotation);   // converts the same array back
```

## Execution Results
::::{dropdown} Run output (Thor20 example)
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/05_kinematics --model thor20 --ip 192.168.10.75
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-58612,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-53836,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-48736,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-33617,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-45477,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  6
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 6 (Thor series)
Selected model: Thor20 (expected 6 axes)
Forward kinematics result:
  x : 0.764014 m
  y : 0.247046 m
  z : 0.653829 m
  rx: -0.593369 rad
  ry: 2.538124 rad
  rz: 0.050312 rad
Inverse kinematics result:
  J1: 0.312822 rad
  J2: 0.076441 rad
  J3: 2.261036 rad
  J4: -0.020824 rad
  J5: 0.272180 rad
  J6: -0.131779 rad
Inverse solution near current joints (inverse_ext):
  J1: 0.312822 rad
  J2: 0.076441 rad
  J3: 2.261036 rad
  J4: -0.020824 rad
  J5: 0.272180 rad
  J6: -0.131779 rad
RPY input: 3.141593, 1.047198, 0.523599
Axis-angle vector: 2.431323, 0.651471, -1.403725
Converted back to RPY: -3.141593, 1.047198, 0.523599
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} Run output (Diana7 example)
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/05_kinematics --model diana7 --ip 192.168.10.75
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-53153,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-44348,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-58997,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-35753,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-50455,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Forward kinematics result:
  x : 0.206998 m
  y : 0.254580 m
  z : 0.370319 m
  rx: -0.095556 rad
  ry: 0.258593 rad
  rz: 0.782323 rad
Inverse kinematics result:
  J1: -0.724507 rad
  J2: -0.420814 rad
  J3: -0.143115 rad
  J4: 2.640125 rad
  J5: -0.091403 rad
  J6: -1.187960 rad
  J7: -0.014621 rad
Inverse solution near current joints (inverse_ext):
  J1: -0.724506 rad
  J2: -0.420814 rad
  J3: -0.143115 rad
  J4: 2.640125 rad
  J5: -0.091404 rad
  J6: -1.187960 rad
  J7: -0.014621 rad
RPY input: 3.141593, 1.047198, 0.523599
Axis-angle vector: 2.431323, 0.651471, -1.403725
Converted back to RPY: -3.141593, 1.047198, 0.523599
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::



## API Usage and Call Examples

### `getJointPos` / `forward` / `inverse` / `inverse_ext`

````{container} api-example-block

| Function | Prototype | Return Value |
| --- | --- | --- |
| `getJointPos` | `int getJointPos(double *joints, const char *strIpAddress = "")` | `0` on success, `-1` on failure. Full parameter notes are in <a href="02_robot_state.html#getjointpos-getjointangularvel-getjointcurrent-getjointtorque">02 Robot State Reading</a>. |
| `forward` | `int forward(double *joints, double *pose, double *active_tcp = nullptr, const char *strIpAddress = "")` | `0` on success, `-1` on failure. |
| `inverse` | `int inverse(double *pose, double *joints, double *active_tcp = nullptr, const char *strIpAddress = "")` | `0` on success, `-1` on failure. |
| `inverse_ext` | `int inverse_ext(double *ref_joints, double *pose, double *joints, double *active_tcp = nullptr, const char *strIpAddress = "")` | `0` on success, `-1` on failure. |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `joints` | In or out, `double[kMaxSupportedJointCount]` | Joint positions, in rad. It is input for `forward` and output for `inverse` / `inverse_ext`. |
| `ref_joints` | In, `double[kMaxSupportedJointCount]` | Reference joint positions, in rad. `inverse_ext` uses them to choose the nearest IK solution. |
| `pose` | In or out, `double[6]` | TCP pose `[x, y, z, rx, ry, rz]`; position is in m, orientation is axis-angle in rad. |
| `active_tcp` | In, `double[6]` or `nullptr` | Tool coordinate pose. `nullptr` uses the controller's default TCP. |
| `strIpAddress` | In, `const char*`, default `""` | Robot IP. An empty value is only appropriate for single-arm connections. |

`getJointPos(joints, ip)` reads the current robot's joint angles in rad; the example uses a `kMaxSupportedJointCount` buffer. `forward(joints, pose, active_tcp, ip)` computes a TCP pose from joint angles; `active_tcp=nullptr` uses the default TCP, and orientation is axis-angle rad.

`inverse(pose, joints, active_tcp, ip)` computes one joint solution from a six-dimensional pose. Redundant robots may have multiple solutions, and ordinary IK does not guarantee configuration continuity. `inverse_ext(ref_joints, pose, joints, active_tcp, ip)` uses `ref_joints` to select the solution with the smallest Euclidean distance. This example uses the current joint angles as the reference; a path application should keep updating the reference value for every segment.

```{rubric} Call Example
```

```cpp
double joints[kMaxSupportedJointCount] = {0.0};
double pose[6] = {0.0};
getJointPos(joints, "192.168.10.75");
forward(joints, pose, nullptr, "192.168.10.75");

double result[kMaxSupportedJointCount] = {0.0};
inverse(pose, result, nullptr, "192.168.10.75");
inverse_ext(joints, pose, result, nullptr, "192.168.10.75");
```


````

### `rpy2Axis` / `axis2RPY`

````{container} api-example-block

| Function | Prototype | Return Value |
| --- | --- | --- |
| `rpy2Axis` | `int rpy2Axis(double *arr)` | `0` on success, `-1` on failure. |
| `axis2RPY` | `int axis2RPY(double *arr)` | `0` on success, `-1` on failure. |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `arr` | In/out, `double[3]` | Three-element rotation array. `rpy2Axis` converts RPY to axis-angle in place; `axis2RPY` converts axis-angle to RPY in place. Units are rad. |

`rpy2Axis(rotation)` and `axis2RPY(rotation)` modify a three-element rotation array in place. Input and output units are rad. Avoid repeated conversions and never pass degree values directly. Confirm whether the current array is RPY or axis-angle before converting.

```{rubric} Call Example
```

```cpp
double rpy[3] = {PI, PI / 3, PI / 6};
if (rpy2Axis(rpy) == 0) {
    // rpy now holds the axis-angle vector in place
    axis2RPY(rpy);
}
```

````

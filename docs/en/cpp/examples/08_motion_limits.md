# 08 Motion Limits

This read-only example prints the currently active joint and Cartesian motion limits. It does not call any `set*Limit` API.

```bash
./build/bin/08_motion_limits --model thor12 --ip 192.168.10.75
```

| API | Purpose |
|---|---|
| `getJointsPositionRange` | Read joint position ranges |
| `getMaxJointsVel` / `getMaxJointsAcc` | Read maximum joint velocity and acceleration |
| `getMaxCartTranslationVel` / `getMaxCartTranslationAcc` | Read Cartesian translation velocity and acceleration limits |
| `getMaxCartRotationVel` / `getMaxCartRotationAcc` | Read Cartesian rotation velocity and acceleration limits |

## Example Call Flow

Connect and validate joint count → query joint limits as a group → query Cartesian limits as a group → print current controller values → release resources. Motion planning should use the actual values read from the controller.

### Key Source Snippet

```cpp
double min_pos[kMaxSupportedJointCount] = {0.0};
double max_pos[kMaxSupportedJointCount] = {0.0};
double max_vel[kMaxSupportedJointCount] = {0.0};
double max_acc[kMaxSupportedJointCount] = {0.0};

getJointsPositionRange(min_pos, max_pos, ip);
getMaxJointsVel(max_vel, ip);
getMaxJointsAcc(max_acc, ip);

double translation_vel = 0.0, rotation_vel = 0.0;
getMaxCartTranslationVel(translation_vel, ip);
getMaxCartRotationVel(rotation_vel, ip);
```

## Execution Results
::::{dropdown} Run output (Thor20 example)
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/08_motion_limits --model thor20 --ip 192.168.10.75
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-51811,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-50389,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-51937,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-40042,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-39932,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  6
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 6 (Thor series)
Selected model: Thor20 (expected 6 axes)
Joint limits (rad, rad/s, rad/s^2):
  J1: [-6.28319, 6.28319], vel=2.0944, acc=6.10865
  J2: [-3.14159, 3.14159], vel=2.0944, acc=1.22173
  J3: [-2.96706, 2.96706], vel=2.61799, acc=4.36332
  J4: [-6.28319, 6.28319], vel=3.66519, acc=34.9066
  J5: [-6.28319, 6.28319], vel=3.66519, acc=34.9066
  J6: [-6.28319, 6.28319], vel=3.66519, acc=34.9066
Cartesian limits: translation vel=2.8 m/s, acc=8.7 m/s^2; rotation vel=3.66519 rad/s, acc=34.9066 rad/s^2
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} Run output (Diana7 example)
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/08_motion_limits --model diana7 --ip 192.168.10.75
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-42043,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-33672,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-37122,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-43992,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-49633,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Joint limits (rad, rad/s, rad/s^2):
  J1: [-3.12414, 3.12414], vel=2.96706, acc=11.8682
  J2: [-1.5708, 1.5708], vel=2.61799, acc=9.42478
  J3: [-3.12414, 3.12414], vel=2.61799, acc=9.42478
  J4: [0, 3.05433], vel=2.61799, acc=9.42478
  J5: [-3.12414, 3.12414], vel=3.14159, acc=15.708
  J6: [-3.12414, 0.523599], vel=3.14159, acc=15.708
  J7: [-3.12414, 3.12414], vel=3.14159, acc=15.708
Cartesian limits: translation vel=1.5 m/s, acc=5 m/s^2; rotation vel=3.14159 rad/s, acc=12.5664 rad/s^2
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::



## API Usage and Call Examples

### `getJointsPositionRange` / `getMaxJointsVel` / `getMaxJointsAcc`

````{container} api-example-block

| Function | Prototype | Return Value |
| --- | --- | --- |
| `getJointsPositionRange` | `int getJointsPositionRange(double *dblMinPos, double *dblMaxPos, const char *strIpAddress = "")` | `0` on success, `-1` on failure. |
| `getMaxJointsVel` | `int getMaxJointsVel(double *dblVel, const char *strIpAddress = "")` | `0` on success, `-1` on failure. |
| `getMaxJointsAcc` | `int getMaxJointsAcc(double *dblAcc, const char *strIpAddress = "")` | `0` on success, `-1` on failure. |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `dblMinPos` | Out, `double[kMaxSupportedJointCount]` | Per-joint software lower position limits, in rad. |
| `dblMaxPos` | Out, `double[kMaxSupportedJointCount]` | Per-joint software upper position limits, in rad. |
| `dblVel` | Out, `double[kMaxSupportedJointCount]` | Per-joint maximum velocity, in rad/s. |
| `dblAcc` | Out, `double[kMaxSupportedJointCount]` | Per-joint maximum acceleration, in rad/s². |
| `strIpAddress` | In, `const char*`, default `""` | Robot IP. An empty value is only appropriate for single-arm connections. |

`getJointsPositionRange(min, max, ip)` writes lower and upper joint position limits in rad. `getMaxJointsVel(max_vel, ip)` and `getMaxJointsAcc(max_acc, ip)` write per-joint maximum velocity in rad/s and acceleration in rad/s². The example allocates `kMaxSupportedJointCount` elements and processes only the actual joint count.

These are active software limits, not mechanical limits or process-specific safe limits.

```{rubric} Call Example
```

```cpp
double min[kMaxSupportedJointCount] = {0.0};
double max[kMaxSupportedJointCount] = {0.0};
double joint_vel[kMaxSupportedJointCount] = {0.0};
double joint_acc[kMaxSupportedJointCount] = {0.0};

getJointsPositionRange(min, max, "192.168.10.75");
getMaxJointsVel(joint_vel, "192.168.10.75");
getMaxJointsAcc(joint_acc, "192.168.10.75");
```


````

### `getMaxCartTranslationVel` / `getMaxCartTranslationAcc` / `getMaxCartRotationVel` / `getMaxCartRotationAcc`

````{container} api-example-block

| Function | Prototype | Return Value |
| --- | --- | --- |
| `getMaxCartTranslationVel` | `int getMaxCartTranslationVel(double &dblMaxCartTranslationVel, const char *strIpAddress = "")` | `0` on success, `-1` on failure. |
| `getMaxCartTranslationAcc` | `int getMaxCartTranslationAcc(double &dblMaxCartTranslationAcc, const char *strIpAddress = "")` | `0` on success, `-1` on failure. |
| `getMaxCartRotationVel` | `int getMaxCartRotationVel(double &dblMaxCartRotationVel, const char *strIpAddress = "")` | `0` on success, `-1` on failure. |
| `getMaxCartRotationAcc` | `int getMaxCartRotationAcc(double &dblMaxCartRotationAcc, const char *strIpAddress = "")` | `0` on success, `-1` on failure. |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `dblMaxCartTranslationVel` | Out reference, `double&` | Maximum Cartesian translation velocity, in m/s. |
| `dblMaxCartTranslationAcc` | Out reference, `double&` | Maximum Cartesian translation acceleration, in m/s². |
| `dblMaxCartRotationVel` | Out reference, `double&` | Maximum Cartesian rotation velocity, in rad/s. |
| `dblMaxCartRotationAcc` | Out reference, `double&` | Maximum Cartesian rotation acceleration, in rad/s². |
| `strIpAddress` | In, `const char*`, default `""` | Robot IP. An empty value is only appropriate for single-arm connections. |

`getMaxCartTranslationVel/Acc` return Cartesian translation limits in m/s and m/s². `getMaxCartRotationVel/Acc` return Cartesian rotation limits in rad/s and rad/s². Even if Cartesian parameters satisfy the limits, IK may still produce joint speeds that exceed joint limits, so planners must check both sets of constraints.

```{rubric} Call Example
```

```cpp
double translation_vel = 0.0;
double translation_acc = 0.0;
double rotation_vel = 0.0;
double rotation_acc = 0.0;

getMaxCartTranslationVel(translation_vel, "192.168.10.75");
getMaxCartTranslationAcc(translation_acc, "192.168.10.75");
getMaxCartRotationVel(rotation_vel, "192.168.10.75");
getMaxCartRotationAcc(rotation_acc, "192.168.10.75");
```

````

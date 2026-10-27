# 08 Motion Limits

This example reads the actual motion limits from the controller, including joint ranges, maximum joint velocity/acceleration, and maximum Cartesian velocity/acceleration. It is read-only by default.

```bash
python3 examples/08_motion_limits/main.py --model diana7 --ip 192.168.10.75
```

| API | Purpose |
|---|---|
| `getJointsPositionRange` | Read joint position limits |
| `getMaxJointsVel` / `getMaxJointsAcc` | Read maximum joint velocity and acceleration |
| `getMaxCartTranslationVel` / `getMaxCartTranslationAcc` | Read maximum Cartesian translation velocity and acceleration |
| `getMaxCartRotationVel` / `getMaxCartRotationAcc` | Read maximum Cartesian rotation velocity and acceleration |

## Example Call Flow

Initialize the connection → validate the model and joint count → read joint position ranges, maximum joint velocity, and maximum joint acceleration → print them for the actual joint count → read Cartesian translation/rotation velocity and acceleration limits → release resources.

### Key Source Snippet

```python
min_pos = [0.0] * MAX_SUPPORTED_JOINT_COUNT
max_pos = [0.0] * MAX_SUPPORTED_JOINT_COUNT
max_vel = [0.0] * MAX_SUPPORTED_JOINT_COUNT
max_acc = [0.0] * MAX_SUPPORTED_JOINT_COUNT

api.getJointsPositionRange(min_pos, max_pos, args.ip)
api.getMaxJointsVel(max_vel, args.ip)
api.getMaxJointsAcc(max_acc, args.ip)

translation_vel = api.getMaxCartTranslationVel(args.ip)
translation_acc = api.getMaxCartTranslationAcc(args.ip)
rotation_vel = api.getMaxCartRotationVel(args.ip)
rotation_acc = api.getMaxCartRotationAcc(args.ip)
```

## Execution Results
::::{dropdown} Run Output (Thor20 example)
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/08_motion_limits/main.py --model thor20 --ip 192.168.10.75
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-50119,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-44513,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-42530,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-47834,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-40641,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  6
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 6 (Thor series)
Selected model: Thor20 (expected 6 axes)
Joint limits (rad, rad/s, rad/s^2):
  J1: [-6.283185, 6.283185], vel=2.094395, acc=6.108652
  J2: [-3.141593, 3.141593], vel=2.094395, acc=1.221730
  J3: [-2.967060, 2.967060], vel=2.617994, acc=4.363323
  J4: [-6.283185, 6.283185], vel=3.665191, acc=34.906585
  J5: [-6.283185, 6.283185], vel=3.665191, acc=34.906585
  J6: [-6.283185, 6.283185], vel=3.665191, acc=34.906585
Cartesian limits: translation vel=(True, 2.8) m/s, acc=(True, 8.7) m/s^2, rotation vel=(True, 3.6651914289999996) rad/s, acc=(True, 34.906585) rad/s^2
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop

```
::::
::::{dropdown} Run Output (Diana7 example)
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/08_motion_limits/main.py --model diana7 --ip 192.168.10.75
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-60396,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-42599,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-58478,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-36851,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-43014,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Joint limits (rad, rad/s, rad/s^2):
  J1: [-3.124139, 3.124139], vel=2.967060, acc=11.868239
  J2: [-1.570796, 1.570796], vel=2.617994, acc=9.424778
  J3: [-3.124139, 3.124139], vel=2.617994, acc=9.424778
  J4: [0.000000, 3.054326], vel=2.617994, acc=9.424778
  J5: [-3.124139, 3.124139], vel=3.141593, acc=15.707963
  J6: [-3.124139, 3.124139], vel=3.141593, acc=15.707963
  J7: [-3.124139, 3.124139], vel=3.141593, acc=15.707963
Cartesian limits: translation vel=(True, 1.5) m/s, acc=(True, 5.0) m/s^2, rotation vel=(True, 3.1415926535900005) rad/s, acc=(True, 12.566370614400002) rad/s^2
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::

## API Usage and Call Examples

### `getJointsPositionRange` / `getMaxJointsVel` / `getMaxJointsAcc`

````{container} api-example-block

| Function | Prototype | Return Value |
|---|---|---|
| `getJointsPositionRange` | `getJointsPositionRange(arrMin, arrMax, ipAddress = '')` | `True` on success; `False` on failure |
| `getMaxJointsVel` | `getMaxJointsVel(arrVel, ipAddress = '')` | `True` on success; `False` on failure |
| `getMaxJointsAcc` | `getMaxJointsAcc(arrAcc, ipAddress = '')` | `True` on success; `False` on failure |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `arrMin` | Out, `list[float]` (length `JOINT_NUM`) | Per-joint lower position limits, in rad. The wrapper fills as many elements as the list holds. |
| `arrMax` | Out, `list[float]` (length `JOINT_NUM`) | Per-joint upper position limits, in rad. The wrapper fills as many elements as the list holds. |
| `arrVel` | Out, `list[float]` (length `JOINT_NUM`) | Per-joint maximum soft velocity, in rad/s; filled in place. |
| `arrAcc` | Out, `list[float]` (length `JOINT_NUM`) | Per-joint maximum soft acceleration, in rad/s²; filled in place. |
| `ipAddress` | In, `str`, default `''` | Robot IP. An empty value is only appropriate for single-arm connections. Shared by all three functions. |

Joint position ranges are in rad, joint velocities in rad/s, and joint accelerations in rad/s². The example reads the controller's current configuration, not the theoretical values given in the documentation.

```python
min_pos = [0.0] * MAX_SUPPORTED_JOINT_COUNT
max_pos = [0.0] * MAX_SUPPORTED_JOINT_COUNT
api.getJointsPositionRange(min_pos, max_pos, ip)
```

````

### `getMaxCartTranslationVel` / `getMaxCartTranslationAcc` / `getMaxCartRotationVel` / `getMaxCartRotationAcc`

````{container} api-example-block

| Function | Prototype | Return Value |
|---|---|---|
| `getMaxCartTranslationVel` | `getMaxCartTranslationVel(ipAddress = '')` | Returns `(success, value)` |
| `getMaxCartTranslationAcc` | `getMaxCartTranslationAcc(ipAddress = '')` | Returns `(success, value)` |
| `getMaxCartRotationVel` | `getMaxCartRotationVel(ipAddress = '')` | Returns `(success, value)` |
| `getMaxCartRotationAcc` | `getMaxCartRotationAcc(ipAddress = '')` | Returns `(success, value)` |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `ipAddress` | In, `str`, default `''` | Robot IP. An empty value is only appropriate for single-arm connections. The only parameter of all four functions. The limit comes back as the `float` second element of the result tuple: translation velocity in m/s, translation acceleration in m/s², rotation velocity in rad/s, rotation acceleration in rad/s². |

These four Python wrapper functions return a `(success, value)` tuple; check the Boolean before using the numeric value. Translation limits are expressed in m/s and m/s², and rotation limits in rad/s and rad/s². The speed that is actually usable is further constrained by the safety configuration, payload, trajectory planning, and the on-site risk assessment.

```python
ok, translation_vel = api.getMaxCartTranslationVel(ip)
ok, translation_acc = api.getMaxCartTranslationAcc(ip)
ok, rotation_vel = api.getMaxCartRotationVel(ip)
ok, rotation_acc = api.getMaxCartRotationAcc(ip)
```

````

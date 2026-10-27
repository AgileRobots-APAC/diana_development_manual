# 05 Kinematics

This example demonstrates forward kinematics, inverse kinematics, reference inverse kinematics, and RPY/axis-angle conversion. It does not move the robot by default.

```bash
python3 examples/05_kinematics/main.py --model diana7 --ip 192.168.10.75
```

| API | Purpose |
|---|---|
| `getJointPos` | Read the current joints as calculation input |
| `forward` | Calculate TCP pose from joints |
| `inverse` / `inverse_ext` | Calculate joint solutions from TCP pose |
| `rpy2Axis` / `axis2RPY` | Convert orientation representations |

## Example Call Flow

Initialize the connection → validate the model and joint count → read the current joint angles → call `forward` to calculate the TCP pose → call `inverse` to solve one inverse solution → call `inverse_ext` to solve a reference inverse solution near the current joints → demonstrate RPY/axis-angle conversion → release resources.

### Key Source Snippet

```python
joints = [0.0] * MAX_SUPPORTED_JOINT_COUNT
pose = [0.0] * 6
inverse_joints = [0.0] * MAX_SUPPORTED_JOINT_COUNT
reference_solution = [0.0] * MAX_SUPPORTED_JOINT_COUNT

api.getJointPos(joints, args.ip)
api.forward(joints, pose, args.ip)
api.inverse(pose, inverse_joints, args.ip)
api.inverse_ext(joints, pose, reference_solution, args.ip)

rotation = [math.pi, math.pi / 3.0, math.pi / 6.0]
api.rpy2Axis(rotation)
api.axis2RPY(rotation)
```

## Execution Results
::::{dropdown} Run Output (Thor20 example)
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/05_kinematics/main.py --model thor20 --ip 192.168.10.75
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-60285,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-52335,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-53390,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-44814,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-39161,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  6
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 6 (Thor series)
Selected model: Thor20 (expected 6 axes)
Forward kinematics result:
  x : 0.709453 m
  y : 0.375831 m
  z : 0.663533 m
  rx: -0.813242 rad
  ry: 2.480505 rad
  rz: 0.112341 rad
Inverse kinematics result:
  J1: 0.487324 rad
  J2: 0.066365 rad
  J3: 2.255955 rad
  J4: -0.020274 rad
  J5: 0.287691 rad
  J6: -0.132209 rad
Inverse solution near current joints (inverse_ext):
  J1: 0.487324 rad
  J2: 0.066365 rad
  J3: 2.255955 rad
  J4: -0.020274 rad
  J5: 0.287691 rad
  J6: -0.132209 rad
Original RPY: 3.141593, 1.047198, 0.523599
Axis-angle vector: 2.431323, 0.651471, -1.403725
Converted back to RPY: -3.141593, 1.047198, 0.523599
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} Run Output (Diana7 example)
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/05_kinematics/main.py --model diana7 --ip 192.168.10.75
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-34890,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-42965,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-39521,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-57192,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-34704,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Forward kinematics result:
  x : 0.376637 m
  y : 0.059488 m
  z : 0.500142 m
  rx: -0.042819 rad
  ry: -0.060398 rad
  rz: 0.199418 rad
Inverse kinematics result:
  J1: -0.143903 rad
  J2: -0.491833 rad
  J3: -0.016611 rad
  J4: 2.442997 rad
  J5: 0.042358 rad
  J6: -1.133012 rad
  J7: 0.023880 rad
Inverse solution near current joints (inverse_ext):
  J1: -0.143918 rad
  J2: -0.491832 rad
  J3: -0.016598 rad
  J4: 2.442997 rad
  J5: 0.042364 rad
  J6: -1.133012 rad
  J7: 0.023873 rad
Original RPY: 3.141593, 1.047198, 0.523599
Axis-angle vector: 2.431323, 0.651471, -1.403725
Converted back to RPY: -3.141593, 1.047198, 0.523599
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::

## API Usage and Call Examples

### `forward` / `inverse` / `inverse_ext`

````{container} api-example-block

| Function | Prototype | Return Value |
|---|---|---|
| `forward` | `forward(joints, pose, ipAddress='')` | `True` on success; otherwise `False` |
| `inverse` | `inverse(pose, joints, ipAddress='')` | `True` on success; otherwise `False` |
| `inverse_ext` | `inverse_ext(ref_joints, pose, joints, ipAddress='')` | `True` on success; otherwise `False` |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `joints` | In or out, `list[float]` (length `JOINT_NUM`) | Joint positions, in rad. Input for `forward`; output for `inverse` / `inverse_ext`, where the wrapper writes the solution into the list in place, so pass a mutable list. |
| `ref_joints` | In, `list[float]` (length `JOINT_NUM`) | Reference joint positions, in rad. `inverse_ext` uses them to choose the IK solution with the smallest Euclidean distance. |
| `pose` | In or out, `list[float]` (length 6) | TCP pose `[x, y, z, rx, ry, rz]`; position is in m, orientation is axis-angle in rad. Output for `forward` (6 elements written in place); input for `inverse` / `inverse_ext`. The Python wrapper does not expose `active_tcp` and always passes a null pointer, so the controller's current default TCP is used. |
| `ipAddress` | In, `str`, default `''` | Robot IP. An empty value is only appropriate for single-arm connections. Shared by `forward`, `inverse`, and `inverse_ext`. |

`forward(joints, pose, ip)` calculates the TCP pose from joint angles and writes a six-element pose. `inverse(pose, joints, ip)` solves joints for a target pose; `inverse_ext(ref_joints, pose, joints, ip)` uses reference joint angles to select a solution closer to the current configuration, which suits cases where configuration continuity matters. Still validate limits and the resulting path before motion.

```python
current = [0.0] * MAX_SUPPORTED_JOINT_COUNT
pose = [0.0] * 6
solution = [0.0] * MAX_SUPPORTED_JOINT_COUNT

api.getJointPos(current, ip)
if api.forward(current, pose, ip):
    api.inverse_ext(current, pose, solution, ip)
```

````

### `rpy2Axis` / `axis2RPY`

````{container} api-example-block

| Function | Prototype | Return Value |
|---|---|---|
| `rpy2Axis` | `rpy2Axis(arr)` | `True` on success; otherwise `False` |
| `axis2RPY` | `axis2RPY(arr)` | `True` on success; otherwise `False` |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `arr` | In/out, `list[float]` (length 3) | Rotation array, in rad. `rpy2Axis` takes RPY and returns axis-angle; `axis2RPY` takes axis-angle and returns RPY. The wrapper writes the result back into the list in place, so a tuple cannot be used. |

The Python conversion calls modify the supplied array in place. Before calling `rpy2Axis`, the array holds RPY values; after a successful call, the same array holds the axis-angle vector. The reverse call `axis2RPY` works the same way. Preserve a copy when both the original and converted representations are needed.

```python
rotation = [math.pi, math.pi / 3.0, math.pi / 6.0]
if api.rpy2Axis(rotation):
    print("axis-angle:", rotation)
if api.axis2RPY(rotation):
    print("rpy:", rotation)
```

````

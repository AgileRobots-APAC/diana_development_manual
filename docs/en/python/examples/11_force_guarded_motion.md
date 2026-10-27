# 11 Force-Guarded Stop

This example polls TCP force during low-speed Cartesian motion and stops when the threshold or timeout is reached. It is dry-run by default; `--run` executes motion.

```bash
python3 examples/11_force_guarded_motion/main.py --model diana7 --ip 192.168.10.75
python3 examples/11_force_guarded_motion/main.py --model diana7 --ip 192.168.10.75 --run
```

| API | Purpose |
|---|---|
| `speedL` | Low-speed Cartesian velocity command |
| `getTcpForce` | Poll TCP force |
| `stop` | Stop after threshold or timeout |

```{warning}
Force-threshold stop is not a replacement for emergency stop. Complete site force-control and collision-risk review before running.
```

## Example Call Flow

Validate `--model` and axis count → print the force-guarded stop settings → exit in dry-run mode → `releaseBrake` and wait 2 seconds → call `speedL` to move slowly along base-frame X → poll `getTcpForce` every 10 ms → call `stop` when `|Fx| >= 5 N` or after a 10 s timeout → hold the brake and release resources.

### Key Source Snippet

```python
ret = api.speedL([0.01, 0.0, 0.0, 0.0, 0.0, 0.0], [0.02, 0.05], 10.0, args.ip)
force = [0.0] * 6
deadline = time.monotonic() + 10.0

while ret and time.monotonic() < deadline:
    if api.getTcpForce(force, args.ip):
        if abs(force[0]) >= 5.0:
            break
    time.sleep(0.01)

api.stop(args.ip)
api.holdBrake(args.ip)
```
## Execution Results
::::{dropdown} Run Output
:class-container: api-example-block
```bash
~/work/diana_examples_python$ python3 examples/11_force_guarded_motion/main.py --model diana7 --ip 192.168.10.75 --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-35237,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-53529,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-44042,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-56733,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-39260,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Guarded move: base X at 0.01 m/s, stop at |Fx| >= 5.0 N.
Stopped by force threshold: Fx=-5.085770490242117 N (threshold=+/-5.0 N).
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::

## API Usage and Call Examples

### `speedL`

````{container} api-example-block

| Function | Prototype | Return Value |
|---|---|---|
| `speedL` | `speedL(speed, acc, t=0.0, ipAddress='')` | `True` on success; otherwise `False` |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `speed` | In, `list[float]` (length 6) | TCP speed `[vx, vy, vz, wx, wy, wz]`; the first three values are in m/s, the last three in rad/s. The wrapper fixes `active_tcp` to null, so the default TCP is used. |
| `acc` | In, `list[float]` (length 2) | `acc[0]` is translation acceleration in m/s²; `acc[1]` is rotation acceleration in rad/s². |
| `t` | In, `float`, default `0.0` | Time, in s. When non-zero, the function returns after `t` whether or not the target speed is reached; when `0`, it returns once the target speed is reached. Call `stop` to stop the motion. The example passes `10.0`. |
| `ipAddress` | In, `str`, default `''` | Robot IP. An empty value is only appropriate for single-arm connections. |

`speedL(speed, acc, t, ip)` sends a Cartesian velocity command. In this example the speed vector is `[0.01, 0, 0, 0, 0, 0]`, which moves along base-frame +X at `0.01 m/s`; the acceleration pair is `[0.02, 0.05]`, and the command lasts at most `10 s`.

```python
api.speedL([0.01, 0.0, 0.0, 0.0, 0.0, 0.0], [0.02, 0.05], 10.0, ip)
```

````

### `getTcpForce` / `stop`

````{container} api-example-block

| Function | Prototype | Return Value |
|---|---|---|
| `getTcpForce` | `getTcpForce(tcpForce, ipAddress='')` | `True` on success; otherwise `False` |
| `stop` | `stop(ipAddress='')` | `True` on success; otherwise `False` |

| Parameter | Direction / Type | Meaning |
| --- | --- | --- |
| `tcpForce` | In/out, `list[float]` (length ≥ 6) | Pre-allocated list; the wrapper writes the external six-axis force/torque at the TCP `[Fx, Fy, Fz, Mx, My, Mz]` into its first 6 elements. The example only uses `tcpForce[0]` (Fx). |
| `ipAddress` | In, `str`, default `''` | Robot IP, used by `getTcpForce` and `stop`. An empty value is only appropriate for single-arm connections. |

The example polls the six-axis TCP wrench `[Fx, Fy, Fz, Mx, My, Mz]` (N and Nm) and uses only the X-axis force `force[0]` for the threshold check. Call `stop` whenever the threshold is reached, the timeout expires, or a command fails.

```python
force = [0.0] * 6
if api.getTcpForce(force, ip) and abs(force[0]) >= 5.0:
    api.stop(ip)
```

```{warning}
Force-guarded stopping relies on application-level polling. It is not deterministic and does not replace controller safety functions or a hardware emergency stop.
```

````

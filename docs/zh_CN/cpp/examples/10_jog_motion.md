# 10 点动运动

该示例默认以低速正向点动 J1；通过 `--mode` 可选择 TCP 沿基坐标系 +X 平移或绕基坐标系 +Z 旋转。时长由 `--duration` 控制在 0.1–2.0 秒；默认 dry-run。

```bash
./build/bin/10_jog_motion --model diana7 --ip 192.168.10.75
./build/bin/10_jog_motion --model diana7 --ip 192.168.10.75 --mode joint --duration=0.5 --run
./build/bin/10_jog_motion --model diana7 --ip 192.168.10.75 --mode tcp --duration=0.5 --run
./build/bin/10_jog_motion --model diana7 --ip 192.168.10.75 --mode rotate --duration=0.5 --run
```

| API | 用途 |
|---|---|
| `releaseBrake` | 点动前上使能 |
| `moveJoint` / `moveTcp_ex` / `rotationTCP_ex` | 按 `--mode` 分别执行 J1 点动、基坐标系 +X 平移或基坐标系 +Z 旋转 |
| `stop` | 到达指定时长后始终停止 |
| `holdBrake` | 停止后抱闸 |

## Example 调用流程

检查型号、模式和时长 → 初始化/校验 → 打印点动计划 → dry-run 或上使能 → 按模式下发点动 → 等待指定时长 → `stop` → 抱闸、释放。

### 关键源码片段

```cpp
if (releaseBrake(ip) < 0) return 6;
std::this_thread::sleep_for(std::chrono::seconds(2));

int ret = 0;
if (mode == JogMode::Joint) {
    ret = moveJoint(T_MOVE_UP, 0, 0.05, 0.10, ip);
} else if (mode == JogMode::Tcp) {
    ret = moveTcp_ex(E_BASE_COORDINATE, T_MOVE_X_UP, 0.01, 0.02, ip);
} else {
    ret = rotationTCP_ex(E_BASE_COORDINATE, T_MOVE_Z_UP, 0.10, 0.20, ip);
}
std::this_thread::sleep_for(
    std::chrono::milliseconds(static_cast<int>(seconds * 1000)));

stop(ip);       // moveJoint does not stop itself
holdBrake(ip);
return ret < 0 ? 7 : 0;
```

## 执行效果
::::{dropdown} 运行输出（无参数）
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/10_jog_motion --model diana7 --ip 192.168.10.75
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-56992,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-55761,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-33285,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-32860,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-37918,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Warning] -20006:_interpolaterPosition warning:SPD_UNREACHABLE.
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Jog J1 positive for 0.5 s at low speed.
DRY RUN
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} 运行输出（--mode joint --duration=0.5 --run）
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/10_jog_motion --model diana7 --ip 192.168.10.75 --mode joint --duration=0.5 --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-48859,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-55242,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-43536,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-54001,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-50762,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Warning] -20006:_interpolaterPosition warning:SPD_UNREACHABLE.
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Jog J1 positive for 0.5 s at low speed.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} 运行输出（--mode tcp --duration=0.5 --run）
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/10_jog_motion --model diana7 --ip 192.168.10.75 --mode tcp --duration=0.5 --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-57406,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-45504,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-57263,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-53911,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-48143,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Warning] -20006:_interpolaterPosition warning:SPD_UNREACHABLE.
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Jog TCP along base +X for 0.5 s at low speed.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} 运行输出（--mode rotate --duration=0.5 --run）
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/10_jog_motion --model diana7 --ip 192.168.10.75 --mode rotate --duration=0.5 --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-46396,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-45755,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-57564,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-35831,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-59706,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Warning] -20006:_interpolaterPosition warning:SPD_UNREACHABLE.
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Rotate TCP about base +Z for 0.5 s at low speed.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::

## 逐项 API 用法与调用案例

### `moveJoint` / `moveTcp_ex` / `rotationTCP_ex` / `stop`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `moveJoint` | `int moveJoint(joint_direction_e d, int i, double v, double a, const char *strIpAddress = "")` | `0` 表示成功下发，`-1` 表示失败；成功返回不表示点动已停止。 |
| `moveTcp_ex` | `int moveTcp_ex(coordinate_e c, tcp_direction_e d, double v, double a, const char *strIpAddress = "")` | `0` 表示成功下发，`-1` 表示失败；成功返回不表示点动已停止。 |
| `rotationTCP_ex` | `int rotationTCP_ex(coordinate_e c, tcp_direction_e d, double v, double a, const char *strIpAddress = "")` | `0` 表示成功下发，`-1` 表示失败；成功返回不表示点动已停止。 |
| `stop` | `int stop(const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `d` | 输入，`joint_direction_e` 或 `tcp_direction_e` | 关节点动方向取 `T_MOVE_UP` / `T_MOVE_DOWN`；TCP 方向取 `T_MOVE_X_UP`、`T_MOVE_X_DOWN`、`T_MOVE_Y_UP`、`T_MOVE_Y_DOWN`、`T_MOVE_Z_UP`、`T_MOVE_Z_DOWN`。 |
| `i` | 输入，`int` | 关节索引，从 `0` 开始；`0` 对应 J1。 |
| `c` | 输入，`coordinate_e` | TCP 点动坐标系；可取 `E_BASE_COORDINATE`、`E_TOOL_COORDINATE`、`E_WORK_PIECE_COORDINATE`、`E_VIEW_COORDINATE`。 |
| `v` | 输入，`double` | 点动速度；关节点动单位 rad/s，TCP 平移单位 m/s，TCP 旋转单位 rad/s。 |
| `a` | 输入，`double` | 点动加速度；关节点动单位 rad/s²，TCP 平移单位 m/s²，TCP 旋转单位 rad/s²。 |
| `strIpAddress` | 输入，`const char*`，默认 `""` | 机械臂 IP；为空时仅适合单臂连接场景。 |

`moveJoint(direction, index, v, a, ip)` 是手动关节点动接口：`direction` 指定正/负向，`index` 从 `0` 开始，因此本例的 `0` 对应 J1；`v`、`a` 的单位为 rad/s、rad/s²。

`moveTcp_ex(E_BASE_COORDINATE, T_MOVE_X_UP, 0.01, 0.02, ip)` 按基坐标系 +X 方向点动 TCP；`rotationTCP_ex(E_BASE_COORDINATE, T_MOVE_Z_UP, 0.10, 0.20, ip)` 按基坐标系 +Z 方向旋转 TCP。`--mode` 只能取 `joint`（默认）、`tcp` 或 `rotate`。

该接口立即返回，且不会自行在给定时长结束后停止。本例由应用线程计时后显式调用 `stop(ip)`，因此时长只是一项业务控制条件，不是 API 的位置精度保证。调用前 `releaseBrake` 成功后需等待约 2 s；结束时先 `stop` 再 `holdBrake`。异常路径也必须走同样的停止逻辑，不能只依赖进程退出。

```{rubric} 调用案例
```

```cpp
move_direct_e direction = T_MOVE_UP;
int joint_index = 0;
double vel = 0.2;
double acc = 0.8;

int ret = moveJoint(direction, joint_index, vel, acc, "192.168.10.75");
if (ret < 0) printf("moveJoint failed!\n");
sleep(3);
stop("192.168.10.75");
```

````

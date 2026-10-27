# 04 笛卡尔运动

该示例读取当前 TCP 位姿，将基坐标系 Z 方向增加 10 mm，并通过 `moveLToPose` 下发直线运动。

```bash
./build/bin/04_cartesian_motion --model diana7 --ip 192.168.10.75       # dry-run
./build/bin/04_cartesian_motion --model thor12 --ip 192.168.10.75 --run
```

| API | 用途 |
|---|---|
| `getTcpPos` | 读取当前 TCP 位姿，作为目标计算基准 |
| `releaseBrake` / `holdBrake` | 运动前上使能、结束后抱闸 |
| `moveLToPose` | 按目标 TCP 位姿、速度和加速度下发直线运动 |
| `stop` / `waitMove` | 异常停止或等待运动结束 |

## Example 调用流程

初始化和型号校验 → 读取当前位姿 → 计算 Z + 0.01 m 的目标并打印 → dry-run 或上使能 → `moveLToPose` → 等待、抱闸、释放。

### 关键源码片段

```cpp
double start[6] = {0.0};
getTcpPos(start, ip);

double target[6];
for (int i = 0; i < 6; ++i) target[i] = start[i];
target[2] += 0.010;  // Base Z + 10 mm

releaseBrake(ip);
std::this_thread::sleep_for(std::chrono::seconds(2));
const int ret = moveLToPose(target, 0.02, 0.05, nullptr,
                            0, 0.0, 0.0, false, ip);
if (ret < 0) stop(ip); else waitMove(ip);
holdBrake(ip);
```

```{warning}
目标相对当前 TCP 计算，不检查工件、夹具或奇异位形。执行前必须确认路径净空。
```
## 执行效果
::::{dropdown} 运行输出（Thor20示例）
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/04_cartesian_motion --model thor20 --ip 192.168.10.75 --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-57532,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-42180,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-60821,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-40814,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-38603,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  6
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 6 (Thor series)
Selected model: Thor20 (expected 6 axes)
Current TCP pose:
  x : 0.764005 m
  y : 0.247087 m
  z : 0.643907 m
  rx: -0.593565 rad
  ry: 2.537922 rad
  rz: 0.050321 rad
Example target (Base Z + 10 mm):
  x : 0.764005 m
  y : 0.247087 m
  z : 0.653907 m
  rx: -0.593565 rad
  ry: 2.537922 rad
  rz: 0.050321 rad
Motion finished.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} 运行输出（Diana7示例）
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/04_cartesian_motion --model diana7 --ip 192.168.10.75 --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-45616,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-57528,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-35788,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-59074,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-60060,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Current TCP pose:
  x : 0.207016 m
  y : 0.254568 m
  z : 0.360338 m
  rx: -0.095515 rad
  ry: 0.258551 rad
  rz: 0.782288 rad
Example target (Base Z + 10 mm):
  x : 0.207016 m
  y : 0.254568 m
  z : 0.370338 m
  rx: -0.095515 rad
  ry: 0.258551 rad
  rz: 0.782288 rad
Motion finished.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop

```
::::

## 逐项 API 用法与调用案例

### `getTcpPos`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `getTcpPos` | `int getTcpPos(double *pose, const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败；完整参数说明见 <a href="02_robot_state.html#gettcppos-gettcpexternalforce-gettcpforce-getjointforce">02 机器人状态读取</a>。 |

`getTcpPos(pose, ip)` 返回 `[x, y, z, rx, ry, rz]`。位置单位为 m，姿态为轴角 rad。本例只对 `z` 增加 `0.01`，即基坐标系方向的 10 mm；姿态分量保持 API 返回值。

```{rubric} 调用案例
```

```cpp
double pose[6] = {0.0};
int ret = getTcpPos(pose, "192.168.10.75");
if (ret == 0) {
    pose[2] += 0.010;  // Base Z + 10 mm
}
```


````

### `moveLToPose`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `moveLToPose` | `int moveLToPose(double *pose, double v, double a, double *active_tcp = nullptr, int zv_shaper_order = 0, double zv_shaper_frequency = 0, double zv_shaper_damping_ratio = 0, bool avoid_singular = false, const char *strIpAddress = "")` | `0` 表示成功下发，`-1` 表示失败；成功返回不表示运动已经结束。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `pose` | 输入，`double[6]` | 目标 TCP 位姿 `[x, y, z, rx, ry, rz]`；位置单位 m，姿态为轴角 rad。 |
| `v` | 输入，`double` | 直线运动平移速度，单位 m/s。 |
| `a` | 输入，`double` | 直线运动平移加速度，单位 m/s²。 |
| `active_tcp` | 输入，`double[6]` 或 `nullptr` | 指定参与运动计算的 TCP 位姿；`nullptr` 表示使用当前默认 TCP。 |
| `zv_shaper_order` / `zv_shaper_frequency` / `zv_shaper_damping_ratio` | 输入，默认 `0` / `0.0` / `0.0` | 零振动整形参数；本例不启用。 |
| `avoid_singular` | 输入，`bool`，默认 `false` | 是否启用避奇异处理；本例传 `false`。 |
| `strIpAddress` | 输入，`const char*`，默认 `""` | 机械臂 IP；为空时仅适合单臂连接场景。 |

`moveLToPose(pose, v, a, active_tcp, zv_shaper_order, zv_shaper_frequency, zv_shaper_damping_ratio, avoid_singular, ip)` 以 TCP 位姿执行直线运动。`v`、`a` 分别为平移速度 m/s 与加速度 m/s²；`active_tcp=nullptr` 表示使用当前默认 TCP。

本例将整形参数置零，并将 `avoid_singular=false`。这不是安全保证：API 仍可能因不可达、奇异、关节限制或路径碰撞相关条件失败，应检查返回值并保留错误码。函数立即返回，`waitMove` 只用于确认执行结束；发生失败时先 `stop`，随后抱闸和释放服务。

```{rubric} 调用案例
```

```cpp
double pose[6] = {0.4221, 0.0, 0.9403, 0.0, 0.0, 0.0};
double vel = 0.2;  // m/s
double acc = 0.2;  // m/s²
int ret = moveLToPose(pose, vel, acc, nullptr,
                      0, 0.0, 0.0, false, "192.168.10.75");
if (ret < 0) {
    printf("moveLToPose failed! Return value = %d\n", ret);
} else {
    wait_move("192.168.10.75");
}
```

````

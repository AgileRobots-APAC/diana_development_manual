# 12 ServoL 实时下发

该示例读取当前 TCP，并生成以其为中心、基坐标系 Z 方向 ±5 cm 的正弦往复轨迹；以 10 ms 周期连续下发 20 秒（共 2000 次）`servoL_ex`，最后回到起点；默认 dry-run。

```bash
./build/bin/12_servoL_realtime --model diana7 --ip 192.168.10.75
./build/bin/12_servoL_realtime --model diana7 --ip 192.168.10.75 --run
```

| API | 用途 |
|---|---|
| `getTcpPos` | 获取当前 TCP 位姿并生成目标 |
| `servoL_ex` | 以 `time=0.01`、`look_ahead_time=0.01`、`gain=2000` 下发笛卡尔伺服目标 |
| `stop` / `holdBrake` | 循环结束或报错时停止并抱闸 |

## 实时控制前提

以下约束适用于 C++ SDK 的 `servoJ` / `servoL` / `speedJ` / `speedL` 及其扩展接口；本例使用其中的 `servoL_ex`。

对 `servoJ` 和 `servoL`，上位机调用周期应小于等于设置的 `time`：

- `time` 大于调用周期时，新指令会打断上一条指令；
- 两者相等时理论上最优，但依赖控制 PC 的实时性能；
- `time` 小于调用周期时，下一条指令迟到可能触发减速或安全处理。

`look_ahead_time` 推荐范围为 0.03–0.2 s，`gain` 推荐范围为 100–2000。较激进的参数不能替代软件速度/加速度限制检查、网络质量和实时性保障。`servoJ` 使用关节目标；`servoL` 还涉及 `pose`、`scale` 和 `active_tcp` 等笛卡尔参数，即使 TCP 速度和加速度满足软件限制，逆解后的关节速度仍可能超限。`speedJ` / `speedL` 根据目标速度和允许加速度规划变速段；高速或高频使用时，网络波动和系统延时可能放大位置偏差。

```{warning}
高速或高频控制前，应先在安全速度下验证网络抖动、上位机调度和轨迹连续性。若软件限制无法满足目标跟踪需求，可能出现超调或运动错误。
```

```{hint}
普通 Linux 不保证硬实时。如有必要，请根据控制 PC 所使用的 Ubuntu 系统版本安装对应的实时内核。
```

## Example 调用流程

连接/校验 → 读取当前 TCP → 生成以当前 TCP 为中心、Z 方向 ±0.05 m 的正弦轨迹 → dry-run 或上使能 → 每 10 ms 调用一次 servoL_ex，连续 20 秒（共 2000 次）→ stop → holdBrake → 释放连接

### 关键源码片段

```cpp
double start_pose[6] = {0.0};
getTcpPos(start_pose, ip);

int ret = 0;
for (int i = 0; i < kServoCycleCount && ret == 0; ++i) {
    const double phase = 2.0 * kPi * i / (kServoCycleCount - 1);
    double target_pose[6] = {
        start_pose[0], start_pose[1], start_pose[2] + kZAmplitudeMeters * std::sin(phase),
        start_pose[3], start_pose[4], start_pose[5],
    };
    ret = servoL_ex(target_pose, 0.01, 0.01, 2000, 1.0, false, nullptr, ip);
    std::this_thread::sleep_for(std::chrono::milliseconds(kServoPeriodMilliseconds));
}
stop(ip);
holdBrake(ip);
```

```{warning}
本例只用于验证基本调用流程，不能直接作为生产实时控制器。
```

## 执行效果
::::{dropdown} 运行输出
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/12_servoL_realtime --model diana7 --ip 192.168.10.75 --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-57381,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-36468,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-59682,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-46332,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-45325,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Servo trajectory: base Z sine wave centered at the current TCP, +/-50 mm, 2000 cycles at 10 ms (20 s).
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

`getTcpPos(pose, ip)` 读取 `[x,y,z,rx,ry,rz]`，位置单位 m，姿态为轴角 rad。本例以当前 TCP 为基准生成 Z 方向 ±`0.05` m 的正弦轨迹，因此每次验证前都应读取当前实际位姿，避免把历史目标当作实时起点。

```{rubric} 调用案例
```

```cpp
double start_pose[6] = {0.0};
int ret = getTcpPos(start_pose, "192.168.10.75");
```


````

### `servoL_ex`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `servoL_ex` | `int servoL_ex(double *pose, double time, double look_ahead_time, double gain, double scale, bool realiable, double *active_tcp = nullptr, const char *strIpAddress = "")` | `0` 表示成功下发，`-1` 表示失败；循环中任意一次失败都应退出并停止。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `pose` | 输入，`double[6]` | 每个控制周期的目标 TCP 位姿 `[x, y, z, rx, ry, rz]`；位置单位 m，姿态为轴角 rad。 |
| `time` | 输入，`double` | 控制周期参数，单位 s；应用实际调用周期必须不大于该值。 |
| `look_ahead_time` | 输入，`double` | 前瞻时间，影响目标平滑与跟踪；手册经验范围为 `0.03-0.2 s`。 |
| `gain` | 输入，`double` | 跟踪增益；手册经验范围为 `100-2000`。 |
| `scale` | 输入，`double` | 轨迹缩放系数；本例传 `1.0` 表示不额外缩放。 |
| `realiable` | 输入，`bool` | 扩展接口的反馈/可靠性开关；当前 Example 源码传 `false`。 |
| `active_tcp` | 输入，`double[6]` 或 `nullptr` | 工具坐标系位姿；为空时使用控制器默认 TCP。 |
| `strIpAddress` | 输入，`const char*`，默认 `""` | 机械臂 IP；为空时仅适合单臂连接场景。 |

`servoL_ex(pose, time, look_ahead_time, gain, scale, realiable, active_tcp, ip)` 用于短位移、高频连续下发的笛卡尔位置伺服。`pose` 为 `[x,y,z,rx,ry,rz]`（m、轴角 rad），每次调用都应提供连续的目标。

`time=0.01` 是控制周期参数；应用实际调用周期必须不大于它。本例以 10 ms sleep 演示调用链，但普通 Linux 调度不构成硬实时保证。`look_ahead_time` 影响目标平滑与跟踪，`gain` 影响跟踪增益；手册给出的经验范围为 0.03–0.2 s 和 100–2000。示例的 `0.01` 前瞻时间仅用于最小验证，不能直接作为生产参数。

`scale=1.0` 表示不额外缩放；`realiable` 为扩展接口的反馈开关，具体数据行为以当前 SDK 头文件为准。循环中任何一次返回负值都必须退出并 `stop`，随后抱闸。

```{rubric} 调用案例
```

```cpp
double start_pose[6] = {0.0};
getTcpPos(start_pose, "192.168.10.75");

for (int i = 0; i < 2000; ++i) {
    const double phase = 2.0 * kPi * i / 1999.0;
    double target_pose[6] = {
        start_pose[0], start_pose[1], start_pose[2] + 0.05 * std::sin(phase),
        start_pose[3], start_pose[4], start_pose[5],
    };
    int ret = servoL_ex(target_pose, 0.01, 0.01, 2000, 1.0, false, nullptr, "192.168.10.75");
    if (ret < 0) break;
    std::this_thread::sleep_for(std::chrono::milliseconds(10));
}
stop("192.168.10.75");
holdBrake("192.168.10.75");
```

````

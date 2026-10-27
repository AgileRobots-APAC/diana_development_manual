# 11 力阈值停止

该示例以基坐标 X 方向 0.01 m/s 低速运动，检测到 `|Fx| ≥ 5 N` 或 10 秒超时即停止；默认 dry-run。运行结束会报告力阈值触发、正常超时或运动指令失败，并给出触发或最后有效采样的 `Fx`。

```bash
./build/bin/11_force_guarded_motion --model diana7 --ip 192.168.10.75
./build/bin/11_force_guarded_motion --model diana7 --ip 192.168.10.75 --run
```

| API | 用途 |
|---|---|
| `speedL` | 下发基坐标系 X 方向速度，最长 10 秒 |
| `getTcpForce` | 每 10 ms 读取 TCP 六维力，检查 Fx 阈值 |
| `stop` / `holdBrake` | 阈值、超时或结束后停止并抱闸 |

## Example 调用流程

初始化和型号校验 → 输出速度/阈值计划 → dry-run 或上使能 → `speedL` → 最多循环 1000 次读取力 → 阈值触发或超时 → 停止、抱闸、释放并报告停止原因与 Fx。

### 关键源码片段

```cpp
double v[6] = {0.01, 0, 0, 0, 0, 0};
double a[2] = {0.02, 0.05};
double f[6] = {0.0};

const int ret = speedL(v, a, 10.0, nullptr, ip);
bool stopped_by_force = false;
bool has_force_sample = false;
double last_fx = 0.0;
for (int i = 0; ret == 0 && i < 1000; ++i) {
    if (getTcpForce(f, ip) == 0) {
        last_fx = f[0];
        has_force_sample = true;
        if (last_fx >= 5.0 || last_fx <= -5.0) {
            stopped_by_force = true;
            break;
        }
    }
    std::this_thread::sleep_for(std::chrono::milliseconds(10));
}
stop(ip);
holdBrake(ip);
```

```{danger}
此示例不能替代碰撞保护或安全功能。仅在力传感、负载、速度、工作空间和急停均完成评审后使用。
```
## 执行效果
::::{dropdown} 运行输出
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/11_force_guarded_motion --model diana7 --ip 192.168.10.75 --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-57869,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-44051,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-51738,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-48802,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-43919,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Guarded move: base X at 0.01 m/s, stop at |Fx| >= 5 N or after 10 s.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
 
Stopped by force threshold: Fx=-5.34248 N (threshold=+/-5 N).
```
::::

## 逐项 API 用法与调用案例

### `speedL`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `speedL` | `int speedL(double *speed, double *a, double t, double *active_tcp = nullptr, const char *strIpAddress = "")` | `0` 表示成功下发，`-1` 表示失败；成功返回不表示速度模式已经结束。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `speed` | 输入，`double[6]` | TCP 速度 `[vx, vy, vz, wx, wy, wz]`；前三项单位 m/s，后三项单位 rad/s。 |
| `a` | 输入，`double[2]` | 加速度数组；`a[0]` 为平移加速度，单位 m/s²；`a[1]` 为旋转加速度，单位 rad/s²。 |
| `t` | 输入，`double` | 速度指令持续时间参数，单位 s；`0` 或较长时间都不应替代应用层停止条件。 |
| `active_tcp` | 输入，`double[6]` 或 `nullptr` | 工具坐标系位姿；为空时使用控制器默认 TCP。 |
| `strIpAddress` | 输入，`const char*`，默认 `""` | 机械臂 IP；为空时仅适合单臂连接场景。 |

`speedL(speed, a, t, active_tcp, ip)` 进入笛卡尔速度模式。`speed` 是 `[vx,vy,vz,wx,wy,wz]`，前三项单位 m/s，后三项单位 rad/s；本例仅给基坐标 X 方向 `0.01 m/s`。`a` 是线/角加速度数组，本例传 `[0.02, 0.05]`；`t=10.0` 设定最长持续时间。

该接口立即返回，且 `t` 不是碰撞保护或安全停止机制。速度模式下应用层必须明确停止条件，并在异常路径调用 `stop(ip)`。

```{rubric} 调用案例
```

```cpp
double speeds[6] = {0.1, 0.0, 0.0, 0.0, 0.0, 0.0};
double acc[2] = {0.30, 0.50};
int ret = speedL(speeds, acc, 0, nullptr, "192.168.10.75");
if (ret < 0) printf("speedL failed!\n");
```


````

### `getTcpForce` / `stop`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `getTcpForce` | `int getTcpForce(double *forces, const char *strIpAddress = "")` | `0` 表示获取到六维力且数据有效，`-1` 表示获取失败或六维力数值无效；完整参数说明见 <a href="02_robot_state.html#gettcppos-gettcpexternalforce-gettcpforce-getjointforce">02 机器人状态读取</a>。 |
| `stop` | `int stop(const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败；`strIpAddress` 为空时仅适合单臂连接场景。 |

`getTcpForce(force, ip)` 输出 `[Fx,Fy,Fz,Mx,My,Mz]`。本例每 10 ms 检查 `|Fx| >= 5 N`，只是一条业务阈值；力数据的有效性、坐标意义、工具负载和奇异状态都必须单独确认。

无论力阈值、超时还是读取失败，流程都调用 `stop` 与 `holdBrake`。不要以此模式代替碰撞检测、急停或安全控制系统。

```{rubric} 调用案例
```

```cpp
double force[6] = {0.0};
if (getTcpForce(force, "192.168.10.75") == 0 && force[0] >= 5.0) {
    stop("192.168.10.75");
}
```

````

# 03 关节运动

该示例以当前关节角为起点，仅让 J1 增加 10°，通过 `moveJToTarget` 演示关节目标运动。

```bash
./build/bin/03_joint_motion --model diana7 --ip 192.168.10.75       # dry-run
./build/bin/03_joint_motion --model diana7 --ip 192.168.10.75 --run
```

| API | 用途 |
|---|---|
| `getJointPos` | 获取当前关节角并生成目标 |
| `releaseBrake` | 运动前上使能 |
| `moveJToTarget` | 以目标关节角、速度和加速度下发关节运动 |
| `getRobotState`（公共 `waitMove`） | 轮询控制器，等待运动结束 |
| `stop` / `holdBrake` | 失败时停止；结束后抱闸 |

## Example 调用流程

校验 `--model` 与轴数 → 读取并打印起点/目标 → 未指定 `--run` 时退出 → 上使能并等待 2 秒 → 下发运动 → 等待完成 → 抱闸、释放资源。

### 关键源码片段

```cpp
double start[kMaxSupportedJointCount] = {0.0};
getJointPos(start, ip);
double target[kMaxSupportedJointCount] = {0.0};
for (int i = 0; i < joint_count; ++i) target[i] = start[i];
target[0] += 10.0 * 3.14159265358979323846 / 180.0;

releaseBrake(ip);
std::this_thread::sleep_for(std::chrono::seconds(2));
const int ret = moveJToTarget(target, 0.10, 0.20, 0, 0.0, 0.0, ip);
if (ret < 0) stop(ip); else waitMove(ip);
holdBrake(ip);
```

```{warning}
这是真机运动示例。仅在完成人员隔离、负载、速度、净空和急停检查后使用 `--run`。
```
## 执行效果
::::{dropdown} 运行输出（Thor20示例）
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/03_joint_motion --model thor20 --ip 192.168.10.75 --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-34530,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-40279,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-43493,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-49897,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-51516,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  6
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 6 (Thor series)
Selected model: Thor20 (expected 6 axes)
Current joints:
  J1: 0.138225 rad
  J2: 0.086804 rad
  J3: 2.266153 rad
  J4: -0.021567 rad
  J5: 0.256526 rad
  J6: -0.131168 rad
Example target (J1 + 10 deg):
  J1: 0.312757 rad
  J2: 0.086804 rad
  J3: 2.266153 rad
  J4: -0.021567 rad
  J5: 0.256526 rad
  J6: -0.131168 rad
Motion finished.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} 运行输出（Diana7示例）
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/03_joint_motion --model diana7 --ip 192.168.10.75 --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-42154,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-50175,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-53591,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-50845,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-43160,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Current joints:
  J1: -0.898793 rad
  J2: -0.405294 rad
  J3: -0.145524 rad
  J4: 2.654542 rad
  J5: -0.092266 rad
  J6: -1.157964 rad
  J7: -0.014824 rad
Example target (J1 + 10 deg):
  J1: -0.724260 rad
  J2: -0.405294 rad
  J3: -0.145524 rad
  J4: 2.654542 rad
  J5: -0.092266 rad
  J6: -1.157964 rad
  J7: -0.014824 rad
Motion finished.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop

```
::::

## 逐项 API 用法与调用案例

### `getJointPos`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `getJointPos` | `int getJointPos(double *joints, const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败；完整参数说明见 <a href="02_robot_state.html#getjointpos-getjointangularvel-getjointcurrent-getjointtorque">02 机器人状态读取</a>。 |

`getJointPos(joints, ip)` 读取当前机械臂的关节角，单位 rad。Example 使用 `kMaxSupportedJointCount` 分配缓冲区，并按 `getJointCount()` 返回的实际轴数处理。本例只修改 J1 的目标值，因此必须先读取整组起点，再复制并调整目标数组；不能以假设姿态直接拼出整组关节值。

```{rubric} 调用案例
```

```cpp
double joints[kMaxSupportedJointCount] = {0.0};
int ret = getJointPos(joints, "192.168.10.75");
if (ret == 0) {
    joints[0] += 2.0 * PI / 180.0;
}
```


````

### `moveJToTarget`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `moveJToTarget` | `int moveJToTarget(double *joints, double v, double a, int zv_shaper_order = 0, double zv_shaper_frequency = 0, double zv_shaper_damping_ratio = 0, const char *strIpAddress = "")` | `0` 表示成功下发，`-1` 表示失败；成功返回不表示运动已经结束。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `joints` | 输入，`double[kMaxSupportedJointCount]` | 目标关节角，单位 rad；有效元素数量由实际轴数决定。 |
| `v` | 输入，`double` | 关节运动速度，单位 rad/s。 |
| `a` | 输入，`double` | 关节运动加速度，单位 rad/s²。 |
| `zv_shaper_order` | 输入，`int`，默认 `0` | 零振动整形阶数；本例传 `0` 表示不启用。 |
| `zv_shaper_frequency` | 输入，`double`，默认 `0.0` | 零振动整形频率；未启用整形时传 `0.0`。 |
| `zv_shaper_damping_ratio` | 输入，`double`，默认 `0.0` | 零振动整形阻尼比；未启用整形时传 `0.0`。 |
| `strIpAddress` | 输入，`const char*`，默认 `""` | 机械臂 IP；为空时仅适合单臂连接场景。 |

`moveJToTarget(joints, v, a, zv_shaper_order, zv_shaper_frequency, zv_shaper_damping_ratio, ip)` 以关节目标数组执行 `moveJ`。`joints` 为 rad，`v` 为 rad/s，`a` 为 rad/s²。后三个零振动整形参数在本例均传 `0`，即不启用。

该调用下发后立即返回，并不表示机器人已到达目标。本例通过公共 `waitMove` 轮询状态等待完成；失败返回负值时立即执行 `stop`，不要继续等待或发送下一条运动。`releaseBrake` / `holdBrake` 的生命周期用法见 [01 连接与型号识别](01_connection.md)。

```{rubric} 调用案例
```

```cpp
double joints[kMaxSupportedJointCount] = {0.0};
double vel = 0.1;  // rad/s
double acc = 0.2;  // rad/s²
int ret = moveJToTarget(joints, vel, acc,
                         0, 0.0, 0.0, "192.168.10.75");
if (ret < 0) {
    printf("moveJToTarget failed! Return value = %d\n", ret);
} else {
    wait_move("192.168.10.75");
}
```

````

# 08 运动限制

该示例只读显示控制器当前生效的关节和笛卡尔运动限制，不调用任何 `set*Limit` 接口。

```bash
./build/bin/08_motion_limits --model thor12 --ip 192.168.10.75
```

| API | 用途 |
|---|---|
| `getJointsPositionRange` | 读取关节位置范围 |
| `getMaxJointsVel` / `getMaxJointsAcc` | 读取关节最大速度和加速度 |
| `getMaxCartTranslationVel` / `getMaxCartTranslationAcc` | 读取笛卡尔平移速度和加速度 |
| `getMaxCartRotationVel` / `getMaxCartRotationAcc` | 读取笛卡尔旋转速度和加速度 |

## Example 调用流程

连接、校验轴数 → 成组查询关节限制 → 成组查询笛卡尔限制 → 输出当前控制器值 → 释放服务。规划运动前应使用实际读取值，而不是假设默认限制。

### 关键源码片段

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

## 执行效果
::::{dropdown} 运行输出（Thor20示例）
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
::::{dropdown} 运行输出（Diana7示例）
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


## 逐项 API 用法与调用案例

### `getJointsPositionRange` / `getMaxJointsVel` / `getMaxJointsAcc`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `getJointsPositionRange` | `int getJointsPositionRange(double *dblMinPos, double *dblMaxPos, const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败。 |
| `getMaxJointsVel` | `int getMaxJointsVel(double *dblVel, const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败。 |
| `getMaxJointsAcc` | `int getMaxJointsAcc(double *dblAcc, const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `dblMinPos` | 输出，`double[kMaxSupportedJointCount]` | 各关节软件位置下限，单位 rad。 |
| `dblMaxPos` | 输出，`double[kMaxSupportedJointCount]` | 各关节软件位置上限，单位 rad。 |
| `dblVel` | 输出，`double[kMaxSupportedJointCount]` | 各关节最大速度，单位 rad/s。 |
| `dblAcc` | 输出，`double[kMaxSupportedJointCount]` | 各关节最大加速度，单位 rad/s²。 |
| `strIpAddress` | 输入，`const char*`，默认 `""` | 机械臂 IP；为空时仅适合单臂连接场景。 |

`getJointsPositionRange(min, max, ip)` 向两个关节数组写入当前位置下/上限，单位 rad。`getMaxJointsVel(max_vel, ip)` 与 `getMaxJointsAcc(max_acc, ip)` 输出逐关节最大速度 rad/s 和最大加速度 rad/s²。Example 使用 `kMaxSupportedJointCount` 分配缓冲区，再按实际轴数读取有效元素。

这些是当前生效的软件限制读数，不等于机械极限或风险评估后的工艺限值。

```{rubric} 调用案例
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

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `getMaxCartTranslationVel` | `int getMaxCartTranslationVel(double &dblMaxCartTranslationVel, const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败。 |
| `getMaxCartTranslationAcc` | `int getMaxCartTranslationAcc(double &dblMaxCartTranslationAcc, const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败。 |
| `getMaxCartRotationVel` | `int getMaxCartRotationVel(double &dblMaxCartRotationVel, const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败。 |
| `getMaxCartRotationAcc` | `int getMaxCartRotationAcc(double &dblMaxCartRotationAcc, const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `dblMaxCartTranslationVel` | 输出引用，`double&` | 笛卡尔最大平移速度，单位 m/s。 |
| `dblMaxCartTranslationAcc` | 输出引用，`double&` | 笛卡尔最大平移加速度，单位 m/s²。 |
| `dblMaxCartRotationVel` | 输出引用，`double&` | 笛卡尔最大旋转速度，单位 rad/s。 |
| `dblMaxCartRotationAcc` | 输出引用，`double&` | 笛卡尔最大旋转加速度，单位 rad/s²。 |
| `strIpAddress` | 输入，`const char*`，默认 `""` | 机械臂 IP；为空时仅适合单臂连接场景。 |

`getMaxCartTranslationVel/Acc` 返回笛卡尔平移的 m/s、m/s² 限制；`getMaxCartRotationVel/Acc` 返回笛卡尔旋转的 rad/s、rad/s² 限制。笛卡尔参数满足限制后，逆解得到的关节速度仍可能超限，因此规划器必须同时检查两类约束。

```{rubric} 调用案例
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

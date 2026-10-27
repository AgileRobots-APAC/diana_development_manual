# 02 机器人状态与诊断

该示例只读采集状态与诊断信息，不会改变机器人状态。

```bash
./build/bin/02_robot_state --model diana7 --ip 192.168.10.75
```

| API | 用途 |
|---|---|
| `getJointPos` / `getJointAngularVel` / `getJointCurrent` / `getJointTorque` | 读取关节位置、速度、电流和力矩 |
| `getTcpPos` / `getTcpExternalForce` / `getTcpForce` / `getJointForce` | 读取 TCP 位姿、TCP 六维力/合外力和关节外力 |
| `getRobotState` / `getLinkState` | 读取控制器状态和链路状态 |
| `getLastError` / `getLastWarning` / `formatError` / `isCollision` | 输出最近错误/警告及碰撞状态 |

## Example 调用流程

初始化并校验轴数 → 依次读取关节、TCP、链路和诊断数据 → 按实际轴数输出数组 → 释放服务。错误码应结合[错误码](../../reference/error_codes.md)分析。

### 关键源码片段

```cpp
double joints[kMaxSupportedJointCount] = {0.0};
double pose[6] = {0.0};
double tcp_force[6] = {0.0};

if (getJointPos(joints, ip) == 0) printJoints(joints, joint_count);
if (getTcpPos(pose, ip) == 0) printPose(pose);
if (getTcpForce(tcp_force, ip) == 0) {
    std::cout << "Fx=" << tcp_force[0] << " N, Mx=" << tcp_force[3] << " Nm\n";
}
printDiagnosticCode("Last error", getLastError(ip), ip);
std::cout << "Collision: " << isCollision(ip) << "\n";
```
## 执行效果
::::{dropdown} 运行输出（Thor20示例）
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/02_robot_state --model thor20 --ip 192.168.10.75
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-48370,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-33573,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-44766,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-35333,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-50112,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  6
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 6 (Thor series)
Selected model: Thor20 (expected 6 axes)
Joint position:
  J1: 0.138189 rad
  J2: 0.086804 rad
  J3: 2.266177 rad
  J4: -0.021591 rad
  J5: 0.256586 rad
  J6: -0.131121 rad
Joint angular velocity (rad/s):
  J1: 0.000078
  J2: -0.000019
  J3: 0.000155
  J4: 0.000181
  J5: -0.000284
  J6: -0.000463
Joint current (A):
  J1: -0.070000
  J2: 0.140000
  J3: -0.040000
  J4: -0.070000
  J5: -0.030000
  J6: 0.070000
Joint torque (Nm):
  J1: -1.024020
  J2: 0.916410
  J3: -0.042950
  J4: -0.375750
  J5: -0.131170
  J6: 0.207110
TCP pose:
  x : 0.795304 m
  y : 0.110622 m
  z : 0.643907 m
  rx: -0.369857 rad
  ry: 2.579263 rad
  rz: -0.012099 rad
TCP external resultant force: 87.429418 N
Robot state: 5 (hold-brake)

Diagnostics:
Link state: connected (ret=0)
Last error: 0
Last warning: 0
Collision detected: no
TCP external wrench:
  Fx: -15.203647 N
  Fy: -5.760403 N
  Fz: 85.904423 N
  Mx: 5.051126 Nm
  My: 9.299372 Nm
  Mz: 3.800984 Nm
Joint external force/torque:
  J1: 0.908345
  J2: -64.001072
  J3: -43.802303
  J4: 2.052728
  J5: -2.634886
  J6: -0.130495
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} 运行输出（Diana7示例）
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/02_robot_state --model diana7 --ip 192.168.10.75
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-33901,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-52482,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-59848,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-39854,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-54668,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Joint position:
  J1: -0.898793 rad
  J2: -0.405306 rad
  J3: -0.145512 rad
  J4: 2.654566 rad
  J5: -0.092230 rad
  J6: -1.157964 rad
  J7: -0.014812 rad
Joint angular velocity (rad/s):
  J1: 0.000000
  J2: 0.000000
  J3: -0.000000
  J4: 0.000000
  J5: -0.000000
  J6: 0.000000
  J7: 0.000000
Joint current (A):
  J1: 0.030000
  J2: -0.020000
  J3: -0.020000
  J4: 0.030000
  J5: 0.000000
  J6: 0.000000
  J7: 0.000000
Joint torque (Nm):
  J1: 0.000000
  J2: -6.936690
  J3: 0.528065
  J4: -21.868760
  J5: 0.550995
  J6: 1.486875
  J7: -0.120330
TCP pose:
  x : 0.159665 m
  y : 0.286636 m
  z : 0.360335 m
  rx: -0.119228 rad
  ry: 0.252445 rad
  rz: 0.955710 rad
TCP external resultant force: 0.953926 N
Robot state: 5 (hold-brake)

Diagnostics:
Link state: connected (ret=0)
Last error: 0
Last warning: 0
Collision detected: no
TCP external wrench:
  Fx: 0.852372 N
  Fy: 0.285719 N
  Fz: -0.319061 N
  Mx: 0.090425 Nm
  My: 0.166779 Nm
  Mz: 0.116338 Nm
Joint external force/torque:
  J1: -0.000000
  J2: 0.197345
  J3: 0.233353
  J4: -0.094571
  J5: -0.012338
  J6: 0.063129
  J7: 0.130687
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop

```
::::
## 逐项 API 用法与调用案例

这些查询接口在 API 初始化后从 SDK 的后台状态缓存读取，因此返回成功也应结合状态更新时间判断数据是否仍新鲜。

### `getJointPos` / `getJointAngularVel` / `getJointCurrent` / `getJointTorque`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `getJointPos` | `int getJointPos(double *joints, const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败。 |
| `getJointAngularVel` | `int getJointAngularVel(double *vels, const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败。 |
| `getJointCurrent` | `int getJointCurrent(double *currents, const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败。 |
| `getJointTorque` | `int getJointTorque(double *torques, const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `joints` | 输出，`double[kMaxSupportedJointCount]` | 关节角数组，单位 rad。 |
| `vels` | 输出，`double[kMaxSupportedJointCount]` | 关节角速度数组，单位 rad/s。 |
| `currents` | 输出，`double[kMaxSupportedJointCount]` | 关节电流数组，单位 A。 |
| `torques` | 输出，`double[kMaxSupportedJointCount]` | 关节真实扭矩数组，单位 Nm；手册说明该值为减去零偏后的数据。 |
| `strIpAddress` | 输入，`const char*`，默认 `""` | 机械臂 IP；为空时仅适合单臂连接场景。 |

这组接口输出关节空间数据。Example 使用仓库定义的 `kMaxSupportedJointCount` 分配缓冲区，再按 `getJointCount()` 返回的实际轴数处理有效元素。`getJointPos` 的单位为 rad，`getJointAngularVel` 为 rad/s，`getJointCurrent` 为 A，`getJointTorque` 为 Nm。

```{rubric} 调用案例
```

```cpp
double joints[kMaxSupportedJointCount] = {0.0};
int ret = getJointPos(joints, "192.168.10.75");
if (ret == 0) {
    printf("J1 = %f rad\n", joints[0]);
}

double vel[kMaxSupportedJointCount] = {0.0};
double current[kMaxSupportedJointCount] = {0.0};
double torque[kMaxSupportedJointCount] = {0.0};
getJointAngularVel(vel, "192.168.10.75");
getJointCurrent(current, "192.168.10.75");
getJointTorque(torque, "192.168.10.75");
```


````

### `getTcpPos` / `getTcpExternalForce` / `getTcpForce` / `getJointForce`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `getTcpPos` | `int getTcpPos(double *pose, const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败。 |
| `getTcpExternalForce` | `double getTcpExternalForce(const char *strIpAddress = "")` | TCP 坐标系下实际感受到的合力大小。 |
| `getTcpForce` | `int getTcpForce(double *forces, const char *strIpAddress = "")` | `0` 表示获取到六维力且数据有效，`-1` 表示获取失败或六维力数值无效。 |
| `getJointForce` | `int getJointForce(double *forces, const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `pose` | 输出，`double[6]` | TCP 位姿 `[x, y, z, rx, ry, rz]`；位置单位 m，姿态为轴角 rad。默认 TCP 会影响该返回值。 |
| `forces` | 输出，`double[6]` 或 `double[kMaxSupportedJointCount]` | `getTcpForce` 输出 TCP 六维力/力矩 `[Fx, Fy, Fz, Mx, My, Mz]`；`getJointForce` 输出关节空间外力数组。 |
| `strIpAddress` | 输入，`const char*`，默认 `""` | 机械臂 IP；为空时仅适合单臂连接场景。 |

`getTcpPos(pose, ip)` 写入 `[x, y, z, rx, ry, rz]`，位置单位 m，后三项是轴角向量、单位 rad。`getTcpExternalForce(ip)` 返回 TCP 合外力标量；`getTcpForce(force, ip)` 输出 `[Fx, Fy, Fz, Mx, My, Mz]` 六维力/力矩。`getJointForce` 输出关节空间外力信息，Example 同样使用 `kMaxSupportedJointCount` 大小的缓冲区，不能与 TCP 六维力混用。

接近奇异位形或力数据无效时，不应将读数用于安全决策。

```{rubric} 调用案例
```

```cpp
double pose[6] = {0.0};
int ret = getTcpPos(pose, "192.168.10.75");
if (ret == 0) {
    printf("z = %f m\n", pose[2]);
}

double force[6] = {0.0};
if (getTcpForce(force, "192.168.10.75") == 0) {
    printf("Fx=%f, Fy=%f, Fz=%f\n", force[0], force[1], force[2]);
}
double resultant_force = getTcpExternalForce("192.168.10.75");
double joint_force[kMaxSupportedJointCount] = {0.0};
getJointForce(joint_force, "192.168.10.75");
```


````

### `getRobotState` / `getLinkState` / `getLastError` / `getLastWarning` / `formatError` / `isCollision`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `getRobotState` | `char getRobotState(const char *strIpAddress = "")` | 状态码含义见 <a href="01_connection.html#getlibraryversion-getrobotstate-getjointcount">01 连接与型号识别</a>。 |
| `getLinkState` | `int getLinkState(const char *strIpAddress = "")` | `0` 表示链路正常，`-1` 表示链路断开。 |
| `getLastError` | `int getLastError(const char *strIpAddress = "")` | `0` 表示没有错误，其它值为最近一次错误码。 |
| `getLastWarning` | `int getLastWarning(const char *strIpAddress = "")` | `0` 表示没有警告，其它值为最近一次警告码。 |
| `formatError` | `const char *formatError(int e, const char *strIpAddress = "")` | 错误码 `e` 对应的字符串描述。 |
| `isCollision` | `bool isCollision(const char *strIpAddress = "")` | `true` 表示发生碰撞，`false` 表示未发生碰撞。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `e` | 输入，`int` | 错误码，可来自错误回调或 `getLastError`。手册建议硬件错误 `-2001` 延时约 100 ms 后再调用 `formatError` 查询具体描述。 |
| `strIpAddress` | 输入，`const char*`，默认 `""` | 机械臂 IP；为空时仅适合单臂连接场景。 |

`getRobotState`、`getLinkState`、`isCollision` 分别用于业务状态、链路和碰撞诊断。出现异常时先停止业务下发，再处理现场。

`getLastError`、`getLastWarning` 与 `formatError` 用于记录错误/警告码并转换为可读文本。应先记录错误/警告码和发生时刻，再做清错或恢复动作。

```{rubric} 调用案例
```

```cpp
char robot_state = getRobotState("192.168.10.75");
int link_state = getLinkState("192.168.10.75");
int error = getLastError("192.168.10.75");
int warning = getLastWarning("192.168.10.75");
printf("error: %s\n", formatError(error, "192.168.10.75"));
bool collision = isCollision("192.168.10.75");
```

````

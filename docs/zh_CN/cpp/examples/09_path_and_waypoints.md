# 09 路径与路点

该示例从当前关节角生成“偏移后目标 → 返回起点”的两路点路径。默认只打印路点；`--run` 才创建和执行路径，`--complex` 使用复杂路径 API。

```bash
./build/bin/09_path_and_waypoints --model diana7 --ip 192.168.10.75
./build/bin/09_path_and_waypoints --model diana7 --ip 192.168.10.75 --run
./build/bin/09_path_and_waypoints --model diana7 --ip 192.168.10.75 --complex --run
```

| 模式 | API 顺序 |
|---|---|
| 基础路径 | `createPath` → 两次 `addMoveJ` → `runPath` → `destroyPath` |
| 复杂路径 | `createComplexPath` → 两次 `addMoveJByTarget` → `runComplexPath` → `destroyComplexPath` |

## Example 调用流程

连接并读取当前关节角 → 生成 J1 偏移 10°（复杂路径 15°）的目标 → dry-run 或上使能 → 创建、添加路点、执行 → `waitMove` → 销毁路径 → 抱闸并释放；失败时调用 `stop`。

### 关键源码片段

```cpp
unsigned int path_id = 0;
int ret = createPath(1, path_id, ip);  // 1 = moveJ path
if (ret == 0) ret = addMoveJ(path_id, target, 0.10, 0.20, 0.0, ip);
if (ret == 0) ret = addMoveJ(path_id, start, 0.10, 0.20, 0.0, ip);
if (ret == 0) ret = runPath(path_id, ip);

if (ret < 0) stop(ip); else waitMove(ip);
destroyPath(path_id, ip);
```

复杂路径在同一位置改用下面这一组调用，不能与基础路径 API 混用：

```cpp
int ret = createComplexPath(0, path_id, ip);
if (ret == 0) ret = addMoveJByTarget(path_id, target,
                                      0.10, 0.20, 0.0, 0, 0.0, 0.0, ip);
if (ret == 0) ret = runComplexPath(path_id, ip);
destroyComplexPath(path_id, ip);
```

```{warning}
路点基于当前姿态生成，执行前请确认完整往返路径的净空、关节限位和现场安全。
```

## 执行效果
::::{dropdown} 运行输出（无参数）
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/09_path_and_waypoints --model diana7 --ip 192.168.10.75
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-43939,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-47870,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-37959,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-35350,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-34298,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Warning] -20006:_interpolaterPosition warning:SPD_UNREACHABLE.
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Path waypoint 1 (J1 + 10 deg):
  J1: -0.706849 rad
  J2: -0.420826 rad
  J3: -0.143115 rad
  J4: 2.640281 rad
  J5: -0.091499 rad
  J6: -1.187948 rad
  J7: -0.014585 rad
Path waypoint 2 (return to current joints):
  J1: -0.724302 rad
  J2: -0.420826 rad
  J3: -0.143115 rad
  J4: 2.640281 rad
  J5: -0.091499 rad
  J6: -1.187948 rad
  J7: -0.014585 rad
DRY RUN: no path is created or executed. Add --model <name> --run after checking the workspace.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} 运行输出（--run）
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/09_path_and_waypoints --model diana7 --ip 192.168.10.75 --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-55800,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-48597,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-56755,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-39723,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-34760,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Warning] -20006:_interpolaterPosition warning:SPD_UNREACHABLE.
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Path waypoint 1 (J1 + 10 deg):
  J1: -0.706981 rad
  J2: -0.420838 rad
  J3: -0.143115 rad
  J4: 2.640221 rad
  J5: -0.091511 rad
  J6: -1.187948 rad
  J7: -0.014621 rad
Path waypoint 2 (return to current joints):
  J1: -0.724434 rad
  J2: -0.420838 rad
  J3: -0.143115 rad
  J4: 2.640221 rad
  J5: -0.091511 rad
  J6: -1.187948 rad
  J7: -0.014621 rad
 [Debug] [runPath] new custom command is created, id = 2 
 
 [Debug] [runPath] custom command is filled, id = 2 
 
 [Debug] [runPath] custom command is running, id = 2 
 
 [Debug] 192.168.10.75 [destroyCustomCommand] custom command is destroyed, id = 2 
 
Path finished.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} 运行输出（--complex --run）
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/09_path_and_waypoints --model diana7 --ip 192.168.10.75 --complex --run
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-52107,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-52120,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-59351,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-57495,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-50791,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Warning] -20006:_interpolaterPosition warning:SPD_UNREACHABLE.
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Complex-path waypoint 1 (J1 + 15 deg):
  J1: -0.689456 rad
  J2: -0.420826 rad
  J3: -0.143103 rad
  J4: 2.640233 rad
  J5: -0.091487 rad
  J6: -1.187984 rad
  J7: -0.014597 rad
Path waypoint 2 (return to current joints):
  J1: -0.724362 rad
  J2: -0.420826 rad
  J3: -0.143103 rad
  J4: 2.640233 rad
  J5: -0.091487 rad
  J6: -1.187984 rad
  J7: -0.014597 rad
Path finished.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::



## 逐项 API 用法与调用案例

### `createPath` / `addMoveJ` / `runPath` / `destroyPath`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `createPath` | `int createPath(int type, unsigned int &id_path, const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败；成功时通过 `id_path` 输出路径 ID。 |
| `addMoveJ` | `int addMoveJ(unsigned int id_path, double *joints, double vel_percent, double acc_percent, double blendradius_percent, const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败。 |
| `runPath` | `int runPath(unsigned int id_path, const char *strIpAddress = "")` | `0` 表示成功下发，`-1` 表示失败；成功返回不表示路径已经执行结束。 |
| `destroyPath` | `int destroyPath(unsigned int id_path, const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `type` | 输入，`int` | 基础路径类型；手册定义 `1` 为 `moveJ`，`2` 为 `moveL`。 |
| `id_path` | 输出或输入，`unsigned int` | `createPath` 输出的基础路径 ID；后续添加、运行和销毁必须使用同一个 ID。 |
| `joints` | 输入，`double[kMaxSupportedJointCount]` | 路径点的目标关节角，单位 rad；有效元素数量由实际轴数决定。 |
| `vel_percent` | 输入，`double` | 速度百分比参数。 |
| `acc_percent` | 输入，`double` | 加速度百分比参数。 |
| `blendradius_percent` | 输入，`double` | 交融半径百分比参数。 |
| `strIpAddress` | 输入，`const char*`，默认 `""` | 机械臂 IP；为空时仅适合单臂连接场景。 |

`createPath(type, path_id, ip)` 创建基础路段；`type=1` 表示 `moveJ`、`type=2` 表示 `moveL`。`path_id` 由 API 输出，后续添加、运行和销毁必须使用同一 ID。

`addMoveJ(path_id, joints, vel_percent, acc_percent, blendradius_percent, ip)` 向基础关节路径追加一个关节目标；Example 使用 `kMaxSupportedJointCount` 大小的缓冲区。V3.3 定义这三个控制量为速度百分比、加速度百分比和交融半径百分比，并非 rad/s、rad/s²。`runPath(path_id, ip)` 开始执行，`destroyPath(path_id, ip)` 释放基础路径对象。执行 API 立即返回，因此仍需 `waitMove`；无论哪一步失败，都要保证释放已创建对象。

```{rubric} 调用案例
```

```cpp
unsigned int path_id = 0;
double joints[kMaxSupportedJointCount] = {0.0};
createPath(1, path_id, "192.168.10.75");  // 1: moveJ
addMoveJ(path_id, joints, 0.2, 0.2, 0.3, "192.168.10.75");
runPath(path_id, "192.168.10.75");
waitMove("192.168.10.75");
destroyPath(path_id, "192.168.10.75");
```


````

### `createComplexPath` / `addMoveJByTarget` / `runComplexPath` / `destroyComplexPath`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `createComplexPath` | `int createComplexPath(int complex_path_type, unsigned int &complex_path_id, const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败；成功时通过 `complex_path_id` 输出复杂路径 ID。 |
| `addMoveJByTarget` | `int addMoveJByTarget(unsigned int complex_path_id, double *target_joints, double vel_percent, double acc_percent, double blendradius_percent, int zv_shaper_order = 0, double zv_shaper_frequency = 0, double zv_shaper_damping_ratio = 0, const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败。 |
| `runComplexPath` | `int runComplexPath(unsigned int complex_path_id, const char *strIpAddress = "")` | `0` 表示成功下发，`-1` 表示失败；成功返回不表示路径已经执行结束。 |
| `destroyComplexPath` | `int destroyComplexPath(unsigned int complex_path_id, const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `complex_path_type` | 输入，`int` | 复杂路径类型；本例使用 `NORMAL_JOINT_PATH`。 |
| `complex_path_id` | 输出或输入，`unsigned int` | `createComplexPath` 输出的复杂路径 ID；后续接口必须使用同一个 ID。 |
| `target_joints` | 输入，`double[kMaxSupportedJointCount]` | 目标关节角，单位 rad；有效元素数量由实际轴数决定。 |
| `vel_percent` / `acc_percent` / `blendradius_percent` | 输入，`double` | 速度、加速度和交融半径百分比参数。 |
| `zv_shaper_order` / `zv_shaper_frequency` / `zv_shaper_damping_ratio` | 输入，默认 `0` / `0.0` / `0.0` | 零振动整形参数；本例不启用。 |
| `strIpAddress` | 输入，`const char*`，默认 `""` | 机械臂 IP；为空时仅适合单臂连接场景。 |

复杂路径的 `createComplexPath`、`addMoveJByTarget`、`runComplexPath`、`destroyComplexPath` 属于另一套对象生命周期，只能彼此配对。`addMoveJByTarget` 的目标、速度、加速度和整形参数含义以 V3.3 头文件为准，不能和基础路径对象混用。

基础路径的 `createPath` 类型为 `2` 时对应 `moveL`，应改用 `addMoveL` 并传入 m/s、m/s² 和 m 为单位的线速度、加速度、交融半径。

```{rubric} 调用案例
```

```cpp
unsigned int path_id = 0;
int ret = createComplexPath(0, path_id, "192.168.10.75");
if (ret == 0) ret = addMoveJByTarget(path_id, joints,
                                     0.10, 0.20, 0.0, 0, 0.0, 0.0,
                                     "192.168.10.75");
if (ret == 0) ret = runComplexPath(path_id, "192.168.10.75");
destroyComplexPath(path_id, "192.168.10.75");
```

````

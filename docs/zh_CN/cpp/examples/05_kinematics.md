# 05 运动学

该示例不运动，展示正解、逆解、带参考构型的逆解，以及 RPY 与轴角转换。

```bash
./build/bin/05_kinematics --model diana7 --ip 192.168.10.75
```

| API | 用途 |
|---|---|
| `getJointPos` | 读取当前关节角作为输入和参考构型 |
| `forward` | 由关节角求 TCP 位姿 |
| `inverse` | 由位姿求一组关节解 |
| `inverse_ext` | 使用当前关节角作为参考，选择接近当前构型的解 |
| `rpy2Axis` / `axis2RPY` | 在 RPY 与轴角表达之间转换 |

## Example 调用流程

连接并读取当前关节角 → 正解得到位姿 → 对该位姿执行普通逆解和参考逆解 → 输出两类结果 → 转换姿态表达 → 释放服务。冗余机械臂的路径设计还应阅读[逆解选择](../../guide/inverse_uniqueness.md)。

### 关键源码片段

```cpp
double joints[kMaxSupportedJointCount] = {0.0};
double pose[6] = {0.0};
double solution[kMaxSupportedJointCount] = {0.0};

getJointPos(joints, ip);
forward(joints, pose, nullptr, ip);
inverse(pose, solution, nullptr, ip);
inverse_ext(joints, pose, solution, nullptr, ip);

double rotation[3] = {pi, pi / 3.0, pi / 6.0};
rpy2Axis(rotation);   // rotation now contains axis-angle
axis2RPY(rotation);   // converts the same array back
```
## 执行效果
::::{dropdown} 运行输出（Thor20示例）
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/05_kinematics --model thor20 --ip 192.168.10.75
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-58612,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-53836,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-48736,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-33617,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-45477,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  6
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 6 (Thor series)
Selected model: Thor20 (expected 6 axes)
Forward kinematics result:
  x : 0.764014 m
  y : 0.247046 m
  z : 0.653829 m
  rx: -0.593369 rad
  ry: 2.538124 rad
  rz: 0.050312 rad
Inverse kinematics result:
  J1: 0.312822 rad
  J2: 0.076441 rad
  J3: 2.261036 rad
  J4: -0.020824 rad
  J5: 0.272180 rad
  J6: -0.131779 rad
Inverse solution near current joints (inverse_ext):
  J1: 0.312822 rad
  J2: 0.076441 rad
  J3: 2.261036 rad
  J4: -0.020824 rad
  J5: 0.272180 rad
  J6: -0.131779 rad
RPY input: 3.141593, 1.047198, 0.523599
Axis-angle vector: 2.431323, 0.651471, -1.403725
Converted back to RPY: -3.141593, 1.047198, 0.523599
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} 运行输出（Diana7示例）
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/05_kinematics --model diana7 --ip 192.168.10.75
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-53153,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-44348,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-58997,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-35753,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-50455,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Forward kinematics result:
  x : 0.206998 m
  y : 0.254580 m
  z : 0.370319 m
  rx: -0.095556 rad
  ry: 0.258593 rad
  rz: 0.782323 rad
Inverse kinematics result:
  J1: -0.724507 rad
  J2: -0.420814 rad
  J3: -0.143115 rad
  J4: 2.640125 rad
  J5: -0.091403 rad
  J6: -1.187960 rad
  J7: -0.014621 rad
Inverse solution near current joints (inverse_ext):
  J1: -0.724506 rad
  J2: -0.420814 rad
  J3: -0.143115 rad
  J4: 2.640125 rad
  J5: -0.091404 rad
  J6: -1.187960 rad
  J7: -0.014621 rad
RPY input: 3.141593, 1.047198, 0.523599
Axis-angle vector: 2.431323, 0.651471, -1.403725
Converted back to RPY: -3.141593, 1.047198, 0.523599
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::


## 逐项 API 用法与调用案例

### `getJointPos` / `forward` / `inverse` / `inverse_ext`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `getJointPos` | `int getJointPos(double *joints, const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败；完整参数说明见 <a href="02_robot_state.html#getjointpos-getjointangularvel-getjointcurrent-getjointtorque">02 机器人状态读取</a>。 |
| `forward` | `int forward(double *joints, double *pose, double *active_tcp = nullptr, const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败。 |
| `inverse` | `int inverse(double *pose, double *joints, double *active_tcp = nullptr, const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败。 |
| `inverse_ext` | `int inverse_ext(double *ref_joints, double *pose, double *joints, double *active_tcp = nullptr, const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `joints` | 输入或输出，`double[kMaxSupportedJointCount]` | 关节角数组，单位 rad；在 `forward` 中为输入，在 `inverse` / `inverse_ext` 中为输出。 |
| `ref_joints` | 输入，`double[kMaxSupportedJointCount]` | 参考关节角，单位 rad；`inverse_ext` 用它选择欧氏距离最近的逆解。 |
| `pose` | 输入或输出，`double[6]` | TCP 位姿 `[x, y, z, rx, ry, rz]`；位置单位 m，姿态为轴角 rad。 |
| `active_tcp` | 输入，`double[6]` 或 `nullptr` | 工具坐标系位姿；为空时使用控制器默认 TCP。 |
| `strIpAddress` | 输入，`const char*`，默认 `""` | 机械臂 IP；为空时仅适合单臂连接场景。 |

`getJointPos(joints, ip)` 读取当前机械臂的关节角，单位 rad；Example 使用 `kMaxSupportedJointCount` 大小的缓冲区。`forward(joints, pose, active_tcp, ip)` 由关节角计算 TCP 六维位姿；`active_tcp=nullptr` 使用默认 TCP，输出姿态为轴角 rad。

`inverse(pose, joints, active_tcp, ip)` 由六维位姿求一组关节解。冗余机械臂可能存在多解，普通逆解不保证与当前构型连续。`inverse_ext(ref_joints, pose, joints, active_tcp, ip)` 以 `ref_joints` 为参考，选择欧氏距离最近的逆解。本例把当前关节角作为参考；路径应用应在每段持续更新参考值。

```{rubric} 调用案例
```

```cpp
double joints[kMaxSupportedJointCount] = {0.0};
double pose[6] = {0.0};
getJointPos(joints, "192.168.10.75");
forward(joints, pose, nullptr, "192.168.10.75");

double result[kMaxSupportedJointCount] = {0.0};
inverse(pose, result, nullptr, "192.168.10.75");
inverse_ext(joints, pose, result, nullptr, "192.168.10.75");
```


````

### `rpy2Axis` / `axis2RPY`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `rpy2Axis` | `int rpy2Axis(double *arr)` | `0` 表示成功，`-1` 表示失败。 |
| `axis2RPY` | `int axis2RPY(double *arr)` | `0` 表示成功，`-1` 表示失败。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `arr` | 输入输出，`double[3]` | 长度为 3 的旋转数组；`rpy2Axis` 输入 RPY、输出轴角，`axis2RPY` 输入轴角、输出 RPY；单位均为 rad，函数会原地修改数组。 |

`rpy2Axis(rotation)` 和 `axis2RPY(rotation)` 均原地修改长度为 3 的旋转数组，输入/输出均为 rad。调用前要明确该数组当前是 RPY 还是轴角，避免重复转换或把单位为度的数据直接传入。

```{rubric} 调用案例
```

```cpp
double rpy[3] = {PI, PI / 3, PI / 6};
if (rpy2Axis(rpy) == 0) {
    // rpy 数组已原地变为轴角向量
    axis2RPY(rpy);
}
```

````

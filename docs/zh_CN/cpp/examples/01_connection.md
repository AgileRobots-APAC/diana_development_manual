# 01 连接与型号识别

该示例演示 API 生命周期、SDK 版本读取、机器人状态读取和所选型号的轴数校验；默认不使能或运动。

```bash
./build/bin/01_connection --list-models
./build/bin/01_connection --model diana7 --ip 192.168.10.75
./build/bin/01_connection --model diana7 --ip 192.168.10.75 --enable
```

| API | 用途 |
|---|---|
| `initSrvNetInfo` / `initSrv` | 设置控制器 IP，注册错误和状态回调并建立服务 |
| `getJointCount` | 读取实际轴数，检查 `--model` 所属系列的预期轴数是否匹配 |
| `getLibraryVersion` / `getRobotState` | 读取 SDK 库版本和当前机器人状态 |
| `releaseBrake` / `holdBrake` | 仅在 `--enable` 时演示上使能后再抱闸 |
| `destroySrv` | 释放服务资源 |

## Example 调用流程

解析型号和 IP → 初始化网络结构与服务 → 等待状态回调 → 校验轴数 → 输出版本和状态 → 可选上使能/抱闸 → 释放服务。连接成功不代表允许运动。

### 关键源码片段

```cpp
srv_net_st net_info;
initSrvNetInfo(&net_info);
std::strcpy(net_info.SrvIp, ip);

const int init_ret = initSrv(errorCallback, stateCallback, &net_info);
if (init_ret < 0) return 2;

const unsigned short version = getLibraryVersion();
const char state = getRobotState(ip);

if (enable && releaseBrake(ip) == 0) {
    std::this_thread::sleep_for(std::chrono::seconds(2));
    holdBrake(ip);
}
destroySrv(ip);
```
## 执行效果
### 型号轴数匹配并指定 `--enable`：释放后重新抱闸
::::{dropdown} 运行输出（Thor20示例）
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ export LD_LIBRARY_PATH="$PWD/third_party/diana_sdk_cpp/lib:$LD_LIBRARY_PATH"
~/work/diana_examples_cpp$ ./build/bin/01_connection --model thor20 --ip 192.168.10.75 --enable
Robot IP: 192.168.10.75
Requested model: Thor20
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-56945,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-54423,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-37044,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-44760,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-39350,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  6
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 6 (Thor series)
Selected model: Thor20 (expected 6 axes)
Diana API library version(raw): 769
Robot state: 5 (hold-brake)
Calling releaseBrake()...
Calling holdBrake()...
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
::::{dropdown} 运行输出（Diana7示例）
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ export LD_LIBRARY_PATH="$PWD/third_party/diana_sdk_cpp/lib:$LD_LIBRARY_PATH"
~/work/diana_examples_cpp$ ./build/bin/01_connection --model diana7 --ip 192.168.10.75 --enable
Robot IP: 192.168.10.75
Requested model: Diana7
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-37239,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-51228,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-53366,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-39892,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-33812,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  7
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 7 (Diana series)
Selected model: Diana7 (expected 7 axes)
Diana API library version(raw): 769
Robot state: 5 (hold-brake)
Calling releaseBrake()...
Calling holdBrake()...
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
### 型号轴数不匹配：在抱闸操作前退出
::::{dropdown} 运行输出
:class-container: api-example-block
```bash
~/work/diana_examples_cpp$ ./build/bin/01_connection --model diana7 --ip 192.168.10.75 --enable
Robot IP: 192.168.10.75
Requested model: Diana7
find library libGenericAlgorithm.so
 [Info] [CRobotApiSystem::createRobotApi]create ok:192.168.10.75,initRef:1
 [Info] [CSessionUDP::initSession] ret： 1 session type: 0 local ip-port: 0.0.0.0-49780,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 1 local ip-port: 0.0.0.0-46105,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 2 local ip-port: 0.0.0.0-57686,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 3 local ip-port: 0.0.0.0-42316,remoteipPort:-0
 [Info] [CSessionUDP::initSession] ret： 1 session type: 4 local ip-port: 0.0.0.0-40461,remoteipPort:-0
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CThreadProcessorBase::start] start thread processor
 [Info] [CRobotApiImp::requestJointCount] joint count is  6
 [Info] [CRobotApiSystem::initRobotApi]init default ip:192.168.10.75
Detected joint count: 6 (Thor series)
Selected model: Diana7 (expected 7 axes)
Robot model mismatch: selected Diana7 expects 7 axes, but the connected robot reports 6.
 [Info] [CRobotApiSystem::destroyRobotApi]192.168.10.75, refCount:1, InitRef:0
 [Info] [CRobotStatusThreadProcessor::run] robot status thread stop

 [Info] [CHeartbeatThreadProcessor::run] heartbeat thread stop
```
::::
## 逐项 API 用法与调用案例

以下说明以《思灵机器人工业版 API 手册（C/C++ 版）V3.4.0》为准。

### `initSrvNetInfo` / `initSrv` / `destroySrv`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `initSrvNetInfo` | `void initSrvNetInfo(srv_net_st *pinfo)` | 无返回值。 |
| `initSrv` | `int initSrv(FNCERRORCALLBACK fnError, FNCSTATECALLBACK fnState, srv_net_st *pinfo)` | `0` 表示成功，`-1` 表示失败。 |
| `destroySrv` | `int destroySrv(const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `pinfo` / `pInfo` | 输入输出，`srv_net_st*` | 网络配置结构体，包含 `SrvIp` 以及本地心跳、状态推送、服务、实时服务和透传服务端口。端口为 `0` 时由系统自动分配；推荐先调用 `initSrvNetInfo` 初始化，再写入 `SrvIp`。 |
| `fnError` | 输入，`FNCERRORCALLBACK` | 错误回调，形参为错误码和机械臂 IP。回调在线程中触发，避免阻塞、运动指令或耗时 I/O。 |
| `fnState` | 输入，`FNCSTATECALLBACK` | 状态回调，形参为 `StrRobotStateInfo*` 和机械臂 IP；结构体中包含关节、TCP、力、碰撞、错误和警告等状态缓存。 |
| `strIpAddress` | 输入，`const char*`，默认 `""` | 机械臂 IP；为空时仅适合单臂连接场景。`destroySrv("")` 会释放已成功初始化的全部机械臂资源。 |

`initSrvNetInfo(srv_net_st* pInfo)` 初始化网络结构并随机分配所需端口；随后必须写入 `pInfo->SrvIp`，不要自行只初始化部分字段。

`initSrv(fnError, fnState, srv_net_st* pInfo)` 是其余 API 的初始化前置条件，返回 `0` 表示成功、负值表示失败。错误回调只应记录错误码/置位状态；状态回调由后台推送线程调用，应避免阻塞、运动指令或耗时 I/O。

`destroySrv(ip)` 在连接退出时释放 API 服务；任何初始化成功后的提前返回路径也应调用它。

```{rubric} 调用案例
```

```cpp
srv_net_st* pInfo = new srv_net_st();
initSrvNetInfo(pInfo);
strcpy(pInfo->SrvIp, "192.168.10.75");

int ret = initSrv(fnError, fnState, pInfo);
if (ret < 0) {
    printf("initSrv failed! Return value = %d\n", ret);
}
// ... 使用其他 API
destroySrv("192.168.10.75");
delete pInfo;
```


````

### `getLibraryVersion` / `getRobotState` / `getJointCount`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `getLibraryVersion` | `unsigned short getLibraryVersion()` | 当前库版本号，高 8 位为主版本号，低 8 位为次版本号。 |
| `getRobotState` | `char getRobotState(const char *strIpAddress = "")` | 状态码：`0` running，`1` paused，`2` idle，`3` free-driving，`4` zero-space-free-driving，`5` hold-brake，`6` error，`7` handling-error，`8` rescueMode。 |
| `getJointCount` | `int getJointCount(const char *strIpAddress = "")` | 指定机械臂的关节数量。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `strIpAddress` | 输入，`const char*`，默认 `""` | 机械臂 IP；为空时仅适合单臂连接场景。 |

`getLibraryVersion()` 返回运行时库版本的原始数值，用于留档和排障，不能替代 SDK `version` 文件及头文件的版本核对。

`getRobotState(ip)` 读取当前控制器状态，`getJointCount(ip)` 读取实际轴数。示例在连接完成后比较所选 profile 的预期轴数与控制器报告值，因此可以发现 Diana/Thor 系列选错，但不能区分轴数相同的具体型号。连接成功本身不代表已上使能或可以运动。

```{rubric} 调用案例
```

```cpp
unsigned short version = getLibraryVersion();
char state = getRobotState("192.168.10.75");
int joint_count = getJointCount("192.168.10.75");
```


````

### `releaseBrake` / `holdBrake`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `releaseBrake` | `int releaseBrake(const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败。 |
| `holdBrake` | `int holdBrake(const char *strIpAddress = "")` | `0` 表示成功，`-1` 表示失败。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `strIpAddress` | 输入，`const char*`，默认 `""` | 机械臂 IP；为空时仅适合单臂连接场景。 |

`releaseBrake(ip)` 打开抱闸并启动机械臂；手册要求成功后等待约 2 s 再执行其他操作。`holdBrake(ip)` 合抱闸并停止机械臂。本例的 `--enable` 仅验证这对调用，不下发运动。

```{rubric} 调用案例
```

```cpp
int ret = releaseBrake("192.168.10.75");
if (ret < 0) printf("releaseBrake failed!\n");
sleep(2);  // 手册要求上使能后延时
holdBrake("192.168.10.75");
```

````

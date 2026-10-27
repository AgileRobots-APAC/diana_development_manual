# 快速开始（Linux）

目标是在 Linux 上完成一个最小 C++ 工程：找到 SDK、链接动态库、初始化服务、读取一次关节位置并释放资源。

## 1. 获取并放置 SDK

Example 仓库默认将 SDK 作为子模块放在以下目录：

```text
diana_examples_cpp/
└── third_party/diana_sdk_cpp/
    ├── include/    # DianaAPI.h 等头文件
    ├── lib/        # libDianaApi.so 及其依赖
    └── version     # SDK 发布版本
```

获取示例及 SDK：

```bash
git clone --recurse-submodules https://github.com/AgileRobots-APAC/diana_examples_cpp.git
cd diana_examples_cpp
```

已有主仓库时执行：

```bash
git submodule update --init --recursive
```

## 2. 配置 CMake 并链接 SDK

SDK 在仓库内时直接构建：

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -- -j"$(getconf _NPROCESSORS_ONLN)"
```

SDK 位于外部目录时，目录至少应包含 `include/DianaAPI.h` 和 `lib/libDianaApi.so`，并在配置时指定：

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release \
  -DDIANA_SDK_DIR=/path/to/diana_sdk_cpp
cmake --build build -- -j"$(getconf _NPROCESSORS_ONLN)"
```

在自有 CMake 工程中，至少需要查找头文件和 `DianaApi` 库，并将它们链接到目标程序：

```cmake
find_package(Threads REQUIRED)
find_path(DIANA_INCLUDE_DIR NAMES DianaAPI.h
  PATHS "${DIANA_SDK_DIR}/include" NO_DEFAULT_PATH)
find_library(DIANA_API_LIBRARY NAMES DianaApi libDianaApi
  PATHS "${DIANA_SDK_DIR}/lib" NO_DEFAULT_PATH)
target_include_directories(my_app PRIVATE "${DIANA_INCLUDE_DIR}")
target_link_libraries(my_app PRIVATE "${DIANA_API_LIBRARY}" Threads::Threads)
```

运行前让动态链接器能找到 SDK 的库文件：

```bash
export LD_LIBRARY_PATH="$PWD/third_party/diana_sdk_cpp/lib:$LD_LIBRARY_PATH"
```

如果程序启动时提示找不到 `libDianaApi.so`、`libToolSdk.so` 或 `libGenericAlgorithm.so`，先检查动态库及其依赖：

```bash
LD_LIBRARY_PATH="$PWD/third_party/diana_sdk_cpp/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" \
  ldd "$PWD/third_party/diana_sdk_cpp/lib/libDianaApi.so"
```

输出中不应出现 `not found`。如果仍然失败，请确认 `include/`、`lib/` 和 `version` 来自同一个、与当前系统架构匹配的 SDK 包。

## 3. 最小初始化与读取

```cpp
#include <cstdio>
#include <cstring>
#include <vector>
#include "DianaAPI.h"

void onError(int e, const char*) { std::printf("error: %d\n", e); }
void onState(StrRobotStateInfo*, const char*) {}

int main() {
  const char* robot_ip = "192.168.10.75";
  srv_net_st net{};
  initSrvNetInfo(&net);
  std::strcpy(net.SrvIp, robot_ip);

  const int ret = initSrv(onError, onState, &net);
  if (ret < 0) return ret;

  const int joint_count = getJointCount(robot_ip);
  if (joint_count <= 0) {
    destroySrv(robot_ip);
    return 2;
  }

  std::vector<double> joints(static_cast<std::size_t>(joint_count), 0.0);
  if (getJointPos(joints.data(), robot_ip) < 0) {
    destroySrv(robot_ip);
    return 3;
  }
  destroySrv(robot_ip);
  return 0;
}
```

错误和状态回调可能在实时线程中触发，不要在回调中执行 `sleep`、文件 I/O 或耗时计算等阻塞操作。连接顺序与资源释放的详细说明见 API Reference。

## 4. 连接生命周期

每台机械臂按以下顺序管理资源：

```text
initSrvNetInfo → 设置 srv_net_st::SrvIp → initSrv / initSrvV2
    → 使用其他 API → destroySrv
```

`initSrvNetInfo` 会初始化网络结构体；`initSrv` 注册错误回调、状态回调和网络结构体。结束时调用 `destroySrv(robot_ip)` 释放该机械臂的资源；空 IP 的清理行为以 SDK 当前版本的函数说明为准。

## 5. 运行示例

先查看支持型号，不触发运动：

```bash
./build/bin/01_connection --list-models
```

连接 Diana7：

```bash
./build/bin/01_connection --model diana7 --ip 192.168.10.75
```

连接 Thor12：

```bash
./build/bin/01_connection --model thor12 --ip 192.168.10.75
```

下一步运行不会触发运动的 [Example](examples/index.md)，确认型号、网络和 SDK 加载均正常。

# Quick Start (Linux)

The goal is a minimal Linux C++ project: locate the SDK, link its shared library, initialize the service, read joint positions once, then release resources.

## 1. Obtain and place the SDK

The example repository places the SDK as a submodule:

```text
diana_examples_cpp/
└── third_party/diana_sdk_cpp/
    ├── include/    # DianaAPI.h and headers
    ├── lib/        # libDianaApi.so and dependencies
    └── version     # SDK release version
```

Obtain the examples and SDK:

```bash
git clone --recurse-submodules https://github.com/AgileRobots-APAC/diana_examples_cpp.git
cd diana_examples_cpp
```

For an existing checkout:

```bash
git submodule update --init --recursive
```

## 2. Configure CMake and link the SDK

Build directly when the SDK is in the repository:

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -- -j"$(getconf _NPROCESSORS_ONLN)"
```

For an external SDK directory containing `include/DianaAPI.h` and `lib/libDianaApi.so`:

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release \
  -DDIANA_SDK_DIR=/path/to/diana_sdk_cpp
cmake --build build -- -j"$(getconf _NPROCESSORS_ONLN)"
```

In an application CMake project, locate the header and `DianaApi` library and link both to the target:

```cmake
find_package(Threads REQUIRED)
find_path(DIANA_INCLUDE_DIR NAMES DianaAPI.h
  PATHS "${DIANA_SDK_DIR}/include" NO_DEFAULT_PATH)
find_library(DIANA_API_LIBRARY NAMES DianaApi libDianaApi
  PATHS "${DIANA_SDK_DIR}/lib" NO_DEFAULT_PATH)
target_include_directories(my_app PRIVATE "${DIANA_INCLUDE_DIR}")
target_link_libraries(my_app PRIVATE "${DIANA_API_LIBRARY}" Threads::Threads)
```

Before running, expose the shared libraries:

```bash
export LD_LIBRARY_PATH="$PWD/third_party/diana_sdk_cpp/lib:$LD_LIBRARY_PATH"
```

If startup reports that `libDianaApi.so`, `libToolSdk.so`, or `libGenericAlgorithm.so` cannot be found, inspect the library and its dependencies:

```bash
LD_LIBRARY_PATH="$PWD/third_party/diana_sdk_cpp/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" \
  ldd "$PWD/third_party/diana_sdk_cpp/lib/libDianaApi.so"
```

The output must not contain `not found`. If it does, confirm that `include/`, `lib/`, and `version` come from one SDK package matching the host architecture.

## 3. Initialize and read state

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

Error and state callbacks can run in a real-time thread: do not block them with `sleep`, file I/O, or expensive calculations. See the API reference for details of the connection sequence and resource release.

## 4. Connection Lifecycle

Manage resources for each robot in the following order:

```text
initSrvNetInfo → set srv_net_st::SrvIp → initSrv / initSrvV2
    → use other APIs → destroySrv
```

`initSrvNetInfo` initializes the network structure; `initSrv` registers the error callback, the state callback, and the network structure. Call `destroySrv(robot_ip)` when finished to release the resources of that robot; the cleanup behavior with an empty IP follows the function description of the current SDK version.

## 5. Run Examples

List supported models without moving the robot:

```bash
./build/bin/01_connection --list-models
```

Connect to a Diana7:

```bash
./build/bin/01_connection --model diana7 --ip 192.168.10.75
```

Connect to a Thor12:

```bash
./build/bin/01_connection --model thor12 --ip 192.168.10.75
```

Next, run the non-motion [Examples](examples/index.md) to confirm model selection, networking, and SDK loading.

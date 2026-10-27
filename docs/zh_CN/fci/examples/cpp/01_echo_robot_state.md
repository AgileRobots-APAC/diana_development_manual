# 01 连续状态读取

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

源文件：`libfranka/examples/<model>/echo_robot_state.cpp`。

该程序通过 `robot.read()` 连续读取并打印 `franka::RobotState`，约 101 次回调后退出；不调用 `control()`，不发送运动或力矩命令。

`<model>` 为已应用补丁的 `diana3`、`diana7` 或 `diana7G2`。

```bash
./build/libfranka/examples/<model>/echo_robot_state <robot-ip>
```

| 使用的接口 | 本示例中的用途 |
|---|---|
| `franka::Robot` | 建立 FCI 会话。 |
| `Robot::read()` | 连续接收状态数据。 |
| `franka::RobotState` | 提供并输出机器人状态。 |
## Example 调用流程

解析机器人地址 → 创建 `franka::Robot` → 进入 `read()` 回调 → 输出状态 → 回调计数结束 → 释放会话。

### 关键源码片段

```cpp
size_t count = 0;
robot.read([&count](const franka::RobotState& robot_state) {
  std::cout << robot_state << std::endl;
  return count++ < 100;
});
```

(fci-zh-cpp-01_echo_robot_state-api)=
## 逐项 API 用法与调用案例
(fci-zh-cpp-01_echo_robot_state-api-1)=
### `franka::Robot`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `franka::Robot` | `explicit Robot(const std::string& franka_address, RealtimeConfig realtime_config = RealtimeConfig::kEnforce, size_t log_size = 50)` | 构造成功后得到机器人连接对象；失败时抛出网络、版本或实时配置相关异常。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `franka_address` | 输入，`const std::string&` | 机器人控制器的 IP 地址或主机名。 |
| `realtime_config` | 输入，`RealtimeConfig`，默认 `kEnforce` | 是否要求当前线程能设置实时优先级。 |
| `log_size` | 输入，`size_t`，默认 `50` | 发生 `ControlException` 时保留的最近状态日志数量。 |

`franka::Robot` 负责维护到机器人控制器的网络连接，并提供状态读取、模型加载和控制入口。`realtime_config` 默认为强制实时；没有配置实时权限时可在示例中按需要改为 `RealtimeConfig::kIgnore`。

```{rubric} 调用案例
```

```cpp
franka::Robot robot(argv[1]);
```


````
(fci-zh-cpp-01_echo_robot_state-api-2)=
### `Robot::read()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Robot::read` | `void read(std::function<bool(const RobotState&)> read_callback)` | 无返回值；回调返回 `true` 时继续读取，返回 `false` 时结束；控制冲突、网络中断或机器人错误会抛出异常。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `read_callback` | 输入，`std::function<bool(const RobotState&)>` | 每收到一帧状态调用一次；返回 `true` 继续读取，返回 `false` 结束。 |

`read()` 用于连续接收机器人状态，不发送运动或力矩命令。回调参数是当前 `RobotState`；示例在回调中打印状态并返回布尔值控制循环是否继续。

```{rubric} 调用案例
```

```cpp
robot.read([](const franka::RobotState& state) {
  std::cout << state << std::endl;
  return true;
});
```


````
(fci-zh-cpp-01_echo_robot_state-api-124)=
### `franka::RobotState`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `franka::RobotState` | `struct RobotState` | 状态结构体本身无函数返回值；由 `Robot::readOnce()`、`Robot::read()` 或控制回调提供。 |
| `operator<<` | `std::ostream& operator<<(std::ostream& ostream, const franka::RobotState& robot_state)` | 返回传入的输出流，便于链式输出。 |

`RobotState` 是机器人状态快照，包含关节位置、速度、力矩、位姿矩阵、碰撞/接触标志等字段。本例在 `read()` 回调中通过 `operator<<` 将整个状态结构体输出到标准输出，不修改该对象。

```{rubric} 调用案例
```

```cpp
robot.read([&count](const franka::RobotState& robot_state) {
  std::cout << robot_state << std::endl;
  return count++ < 100;
});
```


````

```{warning}
风险级别：只读。该示例仅读取状态，不发送运动或力矩命令。
```

```{note}
本页的代码片段改编自 libfranka 的示例（Copyright (c) 2023 Franka Robotics GmbH，Apache License 2.0），已针对 Diana 机械臂做了修改；改编部分 Copyright (c) 2026 Agile Robots SE。详见[手册概述](/about/overview.md)中的“许可证与第三方声明”。
```

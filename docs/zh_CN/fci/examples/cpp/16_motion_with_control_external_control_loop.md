# 16 运动与力矩组合外部控制循环

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

源文件：`libfranka/examples/<model>/motion_with_control_external_control_loop.cpp`。

将关节速度运动生成和力矩控制组合在同一个显式外部循环中，并记录控制日志。

`<model>` 为已应用补丁的 `diana3`、`diana7` 或 `diana7G2`。

```bash
./build/libfranka/examples/<model>/motion_with_control_external_control_loop <robot-ip>
```

| 使用的接口 | 本示例中的用途 |
|---|---|
| `Torques` | 封装力矩控制命令。 |
| `logToCSV()` | 控制结束后导出记录。 |
## Example 调用流程

移至初始姿态 → startJointVelocityControl() → 每周期读取状态、计算速度/力矩、写入命令 → 记录 Record 并导出 CSV。

### 关键源码片段

```cpp
auto [state, period] = active_control->readOnce();
auto velocities = motion_callback(state, period);
auto torques = torque_callback(state, period);
active_control->writeOnce(velocities, torques);
```

(fci-zh-cpp-16_motion_with_control_external_control_loop-api)=
## 逐项 API 用法与调用案例
(fci-zh-cpp-16_motion_with_control_external_control_loop-api-62)=
### `Torques`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `franka::Torques` | `Torques(const std::array<double, 7>& torques)` | 返回关节力矩命令对象；initializer list 数量错误时会抛出 `std::invalid_argument`。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `torques` | 输入，`std::array<double,7>` | 期望关节力矩，单位 Nm。 |

`Torques` 封装 7 轴关节力矩命令，单位 Nm。头文件说明该命令不包含重力和摩擦补偿；示例通常结合模型项和控制律生成目标力矩。

```{rubric} 调用案例
```

```cpp
franka::Torques tau_d(tau_d_array);
```


````
(fci-zh-cpp-16_motion_with_control_external_control_loop-api-65)=
### `logToCSV()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `franka::logToCSV` | `std::string logToCSV(const std::vector<Record>& log)` | 返回 CSV 格式的字符串；写入文件由调用方负责。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `log` | 输入，`const std::vector<franka::Record>&` | 需要导出的记录，通常来自 `franka::ControlException::log`。 |

`franka::logToCSV()` 由 libfranka 在 `franka/logging/robot_state_log.hpp` 中提供，把 `Record` 日志转换为 CSV 字符串。示例在捕获 `ControlException` 后把结果写入临时日志文件。它不参与实时控制，应在控制结束后调用，避免阻塞 1 kHz 回调。

```{rubric} 调用案例
```

```cpp
std::ofstream log_stream(log_file.path().c_str());
log_stream << franka::logToCSV(e.log);
```


````

```{warning}
风险级别：力矩。该示例会发送控制命令；运行前请确认工作空间、急停与碰撞阈值。
```

```{note}
本页的代码片段改编自 libfranka 的示例（Copyright (c) 2023 Franka Robotics GmbH，Apache License 2.0），已针对 Diana 机械臂做了修改；改编部分 Copyright (c) 2026 Agile Robots SE。详见[手册概述](/about/overview.md)中的“许可证与第三方声明”。
```

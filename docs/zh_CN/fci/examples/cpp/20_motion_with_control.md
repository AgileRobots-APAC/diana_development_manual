# 20 运动生成与力矩控制组合

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

源文件：`libfranka/examples/<model>/motion_with_control.cpp`。

在一个 robot.control() 会话中组合关节速度运动回调与力矩控制回调，控制异常时导出日志记录。

`<model>` 为已应用补丁的 `diana3`、`diana7` 或 `diana7G2`。

```bash
./build/libfranka/examples/<model>/motion_with_control <robot-ip>
```

| 使用的接口 | 本示例中的用途 |
|---|---|
| `Robot::control()` | 启动组合运动生成和力矩控制回调。 |
| `Record` | 控制异常携带的日志记录，异常时导出为 CSV。 |
## Example 调用流程

移至初始姿态 → 定义速度与力矩回调 → 组合 robot.control() → 捕获 ControlException → 用 logToCSV() 导出 e.log。

### 关键源码片段

```cpp
try {
  robot.control(
      [&](const franka::RobotState& robot_state, franka::Duration) -> franka::Torques {
        return controller.step(robot_state);
      },
      [&](const franka::RobotState&, franka::Duration period) -> franka::JointVelocities {
        // ... joint-velocity trajectory ...
      });
} catch (const franka::ControlException& e) {
  writeLogToFile(e.log);  // log_stream << franka::logToCSV(log);
}
```

(fci-zh-cpp-20_motion_with_control-api)=
## 逐项 API 用法与调用案例
(fci-zh-cpp-20_motion_with_control-api-82)=
### `Robot::control()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Robot::control` | `void control(std::function<Torques(const RobotState&, franka::Duration)> control_callback, std::function<JointVelocities(const RobotState&, franka::Duration)> motion_generator_callback, bool limit_rate = false, double cutoff_frequency = kDefaultCutoffFrequency)` | 无返回值；控制结束由回调返回 `MotionFinished(...)` 表示；控制冲突、实时配置失败、网络中断或命令非法会抛出异常。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `control_callback` | 输入，`std::function` | 每个控制周期返回 `Torques` 力矩命令。 |
| `motion_generator_callback` | 输入，`std::function` | 每个控制周期返回 `JointVelocities` 运动生成命令。 |
| `limit_rate` | 输入，`bool`，默认 `false` | 是否启用限幅；可能改变轨迹。 |
| `cutoff_frequency` | 输入，`double` | 低通滤波截止频率。 |

`control()` 启动 1 kHz FCI 控制循环。本示例使用“力矩控制 + 关节速度运动生成”重载：运动生成回调按预先生成的轨迹给单个关节下发速度，力矩回调由示例中的控制器计算关节力矩。一次只能有一个控制/运动生成循环处于活动状态。

```{rubric} 调用案例
```

```cpp
robot.control(
    [&](const franka::RobotState& robot_state, franka::Duration) -> franka::Torques {
      return controller.step(robot_state);
    },
    [&](const franka::RobotState&, franka::Duration period) -> franka::JointVelocities {
      index += period.toMSec();
      if (index >= trajectory.size()) {
        index = trajectory.size() - 1;
      }
      franka::JointVelocities velocities{{0, 0, 0, 0, 0, 0, 0}};
      velocities.dq[joint_number] = trajectory[index];
      if (index >= trajectory.size() - 1) {
        return franka::MotionFinished(velocities);
      }
      return velocities;
    });
```


````
(fci-zh-cpp-20_motion_with_control-api-86)=
### `Record`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `franka::Record` | `struct Record { RobotState state; RobotCommand command; }` | 数据结构，无返回值。 |

| 成员 | 类型 | 含义 |
| --- | --- | --- |
| `state` | `RobotState` | 时间步 n+1 的机器人状态。 |
| `command` | `RobotCommand` | 时间步 n 的机器人命令（若启用限幅，为限幅后的命令）。 |

`Record` 是 libfranka 的日志记录结构，定义在 `franka/logging/robot_state_log.hpp`。控制失败时抛出的 `ControlException` 在成员 `log`（`std::vector<franka::Record>`）中携带最近的记录；示例在捕获异常后调用 `franka::logToCSV(log)` 把它转成 CSV 字符串并写入临时目录下的日志文件。

```{rubric} 调用案例
```

```cpp
} catch (const franka::ControlException& e) {
  std::cout << e.what() << std::endl;
  writeLogToFile(e.log);  // const std::vector<franka::Record>&
  return -1;
}
// in writeLogToFile():
log_stream << franka::logToCSV(log);
```


````

```{note}
本页的代码片段改编自 libfranka 的示例（Copyright (c) 2023 Franka Robotics GmbH，Apache License 2.0），已针对 Diana 机械臂做了修改；改编部分 Copyright (c) 2026 Agile Robots SE。详见[手册概述](/about/overview.md)中的“许可证与第三方声明”。
```

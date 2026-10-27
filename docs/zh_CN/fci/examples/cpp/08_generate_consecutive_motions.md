# 08 连续关节速度运动

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

源文件：`libfranka/examples/<model>/generate_consecutive_motions.cpp`。

连续执行多段关节速度轨迹，并演示控制异常后的自动恢复。

`<model>` 为已应用补丁的 `diana3`、`diana7` 或 `diana7G2`。

```bash
./build/libfranka/examples/<model>/generate_consecutive_motions <robot-ip>
```

| 使用的接口 | 本示例中的用途 |
|---|---|
| `ControlException` | 捕获控制过程中的异常。 |
| `automaticErrorRecovery()` | 在异常后请求自动错误恢复。 |
## Example 调用流程

准备与碰撞配置 → 多次调用控制回调 → 捕获 ControlException → automaticErrorRecovery() 后继续下一段。

### 关键源码片段

```cpp
try {
  robot.control(velocity_callback);
} catch (const franka::ControlException& e) {
  std::cout << e.what() << std::endl;
  robot.automaticErrorRecovery();
}
```

(fci-zh-cpp-08_generate_consecutive_motions-api)=
## 逐项 API 用法与调用案例
(fci-zh-cpp-08_generate_consecutive_motions-api-24)=
### `ControlException`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `franka::ControlException` | `class ControlException : public Exception` | 异常对象；捕获后可读取 `what()` 和状态日志。 |

`ControlException` 表示控制或运动生成过程中发生错误。连续运动示例捕获该异常后进行错误恢复，避免把机器人留在错误状态。

```{rubric} 调用案例
```

```cpp
try {
  robot.control(callback);
} catch (const franka::ControlException& e) {
  std::cerr << e.what() << std::endl;
}
```


````
(fci-zh-cpp-08_generate_consecutive_motions-api-25)=
### `automaticErrorRecovery()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Robot::automaticErrorRecovery` | `void automaticErrorRecovery()` | 无返回值；网络中断或恢复失败会抛出异常。 |

`automaticErrorRecovery()` 请求机器人从可恢复错误状态恢复。示例只在捕获控制异常并确认现场安全后调用。

```{rubric} 调用案例
```

```cpp
robot.automaticErrorRecovery();
```


````

```{warning}
风险级别：运动。该示例会发送控制命令；运行前请确认工作空间、急停与碰撞阈值。
```

```{note}
本页的代码片段改编自 libfranka 的示例（Copyright (c) 2023 Franka Robotics GmbH，Apache License 2.0），已针对 Diana 机械臂做了修改；改编部分 Copyright (c) 2026 Agile Robots SE。详见[手册概述](/about/overview.md)中的“许可证与第三方声明”。
```

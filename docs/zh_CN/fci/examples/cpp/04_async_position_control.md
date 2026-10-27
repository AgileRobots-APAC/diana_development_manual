# 04 异步关节位置控制

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

源文件：`libfranka/examples/<model>/async_position_control.cpp`。

以 50 Hz 向实验性异步位置控制器发送七轴位置目标；十秒后停止。

`<model>` 为已应用补丁的 `diana3`、`diana7` 或 `diana7G2`。

```bash
./build/libfranka/examples/<model>/async_position_control <robot-ip>
```

| 使用的接口 | 本示例中的用途 |
|---|---|
| `AsyncPositionControlHandler::configure()` | 创建异步关节位置控制处理器。 |
| `getTargetFeedback()` | 查询异步目标的执行状态。 |
| `setJointPositionTarget()` | 下发下一组七轴关节位置目标。 |
| `stopControl()` | 停止异步位置控制。 |
## Example 调用流程

创建 Robot(..., RealtimeConfig::kIgnore) → 配置 AsyncPositionControlHandler → 每 20 ms 获取反馈并发送 JointPositionTarget → stopControl()。

### 关键源码片段

```cpp
auto result = franka::AsyncPositionControlHandler::configure(
    robot, joint_position_control_configuration);
auto target = calculate_joint_position_target(time_step);
auto command_result = result.handler->setJointPositionTarget(target);
```

(fci-zh-cpp-04_async_position_control-api)=
## 逐项 API 用法与调用案例
(fci-zh-cpp-04_async_position_control-api-5)=
### `AsyncPositionControlHandler::configure()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `AsyncPositionControlHandler::configure` | `static ConfigurationResult configure(const std::shared_ptr<Robot>& robot, const Configuration& configuration)` | 返回 `ConfigurationResult`；成功时 `handler` 有值，失败时 `error_message` 描述原因。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `robot` | 输入，`std::shared_ptr<Robot>` | 共享机器人连接对象。 |
| `configuration` | 输入，`Configuration` | 最大关节速度、目标容差等配置。 |

`configure()` 创建异步关节位置控制处理器。`Configuration` 可设置最大关节速度和目标容差；异步控制适合一边查询目标状态，一边下发下一组关节位置。

```{rubric} 调用案例
```

```cpp
auto result = franka::AsyncPositionControlHandler::configure(robot, configuration);
if (result.error_message) {
  throw std::runtime_error(*result.error_message);
}
auto handler = result.handler;
```


````
(fci-zh-cpp-04_async_position_control-api-6)=
### `getTargetFeedback()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `AsyncPositionControlHandler::getTargetFeedback` | `TargetFeedback getTargetFeedback()` | 返回 `TargetFeedback`，包含 `TargetStatus` 与可选错误消息。 |

`getTargetFeedback()` 查询异步目标执行状态。示例根据 `kExecuting`、`kTargetReached`、`kAborted` 等状态决定继续等待、下发新目标或停止。

```{rubric} 调用案例
```

```cpp
auto feedback = handler->getTargetFeedback();
if (feedback.status == franka::TargetStatus::kTargetReached) {
  // target reached
}
```


````
(fci-zh-cpp-04_async_position_control-api-7)=
### `setJointPositionTarget()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `AsyncPositionControlHandler::setJointPositionTarget` | `CommandResult setJointPositionTarget(const JointPositionTarget& target)` | 返回 `CommandResult`；成功时 `was_successful=true`，并可能包含 `motion_uuid`；失败时包含 `error_message`。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `target` | 输入，`JointPositionTarget` | 目标关节位置数组，单位 rad。 |

`setJointPositionTarget()` 给异步控制器发送下一组关节位置目标。示例检查返回状态，失败时停止控制。

```{rubric} 调用案例
```

```cpp
franka::AsyncPositionControlHandler::JointPositionTarget target;
target.joint_positions = q_goal;
auto command = handler->setJointPositionTarget(target);
```


````
(fci-zh-cpp-04_async_position_control-api-8)=
### `stopControl()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `AsyncPositionControlHandler::stopControl` | `void stopControl()` | 无返回值。 |

`stopControl()` 停止异步关节位置控制。示例在目标完成、出错或退出前调用它释放控制流程。

```{rubric} 调用案例
```

```cpp
handler->stopControl();
```


````

```{warning}
风险级别：运动。该示例会发送控制命令；运行前请确认工作空间、急停与碰撞阈值。
```

```{note}
本页的代码片段改编自 libfranka 的示例（Copyright (c) 2023 Franka Robotics GmbH，Apache License 2.0），已针对 Diana 机械臂做了修改；改编部分 Copyright (c) 2026 Agile Robots SE。详见[手册概述](/about/overview.md)中的“许可证与第三方声明”。
```

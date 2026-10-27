# FCI 开发指南

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

FCI（Franka Control Interface 风格的实时控制接口）面向需要高频、低延迟控制能力的开发者。它通常用于外部控制器、实时轨迹下发、力控或更底层的闭环控制场景。

```{warning}
FCI 与普通 C++ SDK 运动接口的使用前提不同。进入 FCI 前，应先确认网络实时性、控制模式、限位、急停、负载、碰撞检测和现场安全条件；不要把普通 SDK 示例的运行方式直接套用到 FCI。
```

## 适用场景

- 需要外部控制器按固定周期下发目标。
- 需要更高实时性的数据反馈和控制闭环。
- 需要基于关节、笛卡尔位姿、速度、力或力矩的高级控制。
- 已具备机器人安全评估、实时系统配置和异常处理能力。

## 阅读顺序

1. 先完成公共[网络配置](../programming/network.md)，确保控制 PC 与控制柜通信正常。
2. 阅读[控制模型与模式选择](../guide/control_modes.md)，确认 FCI 是否适合当前任务。
3. 阅读[状态、反馈与回调](../guide/robot_state.md)，理解状态新鲜度、错误码和异常停止策略。
4. 再进入后续 FCI 接口、实时周期、示例和故障排查章节。

## 选择机械臂

在安装或运行任何示例前，先选择现场机械臂型号并应用相应 overlay 补丁：[Diana3、Diana7 和 Diana7G2](machines.md)。同一 `libfranka` 工作树一次只能应用一个机型补丁。

## 外部参考

- [`libfranka 0.18.2` 源码](https://github.com/frankarobotics/libfranka/tree/0.18.2)：查看本章所用版本的头文件、实现和上游示例。
- [`libfranka 0.18.2` C++ API Reference](https://frankarobotics.github.io/libfranka/0.18.2/index.html)：查询 `franka::Robot`、`franka::RobotState`、`franka::Model` 和控制命令类型。

Diana FCI 的支持范围、安装方式和运行要求以本章说明为准，接口签名和行为应以随 Diana FCI 发布的 `libfranka 0.18.2` 头文件为准。

## 章节目录

```{toctree}
overview
machines
development
realtime_network
control_modes
quick_start
examples/index
faq
```

# 01 打印机器人状态

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

源文件：`libfranka/pylibfranka/examples/<model>/print_robot_state.py`。

创建 Robot 后设置碰撞阈值，调用 read_once() 获取并打印 RobotState。

`<model>` 为已应用补丁的 `diana3`、`diana7` 或 `diana7G2`。

```bash
python3 libfranka/pylibfranka/examples/<model>/print_robot_state.py --ip <robot-ip>
```

| 使用的接口 | 本示例中的用途 |
|---|---|
| `Robot` | 创建机器人连接对象。 |
| `set_collision_behavior()` | 设置碰撞与接触阈值。 |
| `read_once()` | 读取一次机器人状态。 |
| `RobotState` | 保存并打印状态快照。 |
## Example 调用流程

解析 --ip → 创建 Robot → set_collision_behavior() → read_once() → 输出状态字段。

### 关键源码片段

```python
robot = Robot(args.ip)
robot.set_collision_behavior(lower_torque, upper_torque,
                             lower_force, upper_force)
robot_state = robot.read_once()
print(robot_state)
```

(fci-zh-python-01_print_robot_state-api)=
## 逐项 API 用法与调用案例
(fci-zh-python-01_print_robot_state-api-88)=
### `pylibfranka.Robot`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `pylibfranka.Robot` | `Robot(robot_ip_address: str, realtime_config: RealtimeConfig = RealtimeConfig.kEnforce)` | 返回 Python 机器人对象；连接失败、版本不兼容或实时配置失败会抛出绑定层异常。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `robot_ip_address` | 输入，str | 机器人 IP 或主机名。 |
| `realtime_config` | 输入，`RealtimeConfig`，默认 `kEnforce` | 是否强制实时优先级。 |

Python `Robot` 是 `pylibfranka.PyRobot` 的绑定入口，底层持有 `franka::Robot`。它提供状态读取、模型加载、碰撞/阻抗配置以及主动控制启动函数。

```{rubric} 调用案例
```

```python
robot = pylibfranka.Robot(robot_ip)
```


````
(fci-zh-python-01_print_robot_state-api-89)=
### `Robot.set_collision_behavior()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Robot.set_collision_behavior` | `set_collision_behavior(lower_torque_thresholds, upper_torque_thresholds, lower_force_thresholds, upper_force_thresholds)` | 无返回值；参数非法、网络中断或控制器拒绝配置会抛出异常。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `lower_torque_thresholds` | 输入，`list[float]` | 7 维关节接触阈值。 |
| `upper_torque_thresholds` | 输入，`list[float]` | 7 维关节碰撞阈值。 |
| `lower_force_thresholds` | 输入，`list[float]` | 6 维笛卡尔接触阈值。 |
| `upper_force_thresholds` | 输入，`list[float]` | 6 维笛卡尔碰撞阈值。 |

配置碰撞/接触阈值。四个数组分别对应关节力矩下/上阈值和笛卡尔力/力矩下/上阈值。示例在运动或控制前设置。

```{rubric} 调用案例
```

```python
robot.set_collision_behavior(
    [20.0] * 7, [20.0] * 7,
    [20.0] * 6, [20.0] * 6,
)
```


````
(fci-zh-python-01_print_robot_state-api-90)=
### `Robot.read_once()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Robot.read_once` | `read_once() -> RobotState` | 返回一次 `RobotState` 状态快照；控制循环运行中、网络或机器人错误会抛出异常。 |

`read_once()` 是 Python 绑定的一次性状态读取接口。只需要当前状态时使用它；持续控制示例使用主动控制对象的 `readOnce()`。

```{rubric} 调用案例
```

```python
state = robot.read_once()
print(state.q)
```


````
(fci-zh-python-01_print_robot_state-api-91)=
### `RobotState`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `RobotState` | `RobotState` | 状态对象；由 `read_once()` 或主动控制 `readOnce()` 返回。 |

`RobotState` 包含关节状态、末端位姿、命令位姿、碰撞/接触标志等字段。Python 示例读取它的字段作为打印或控制律输入。

```{rubric} 调用案例
```

```python
state = robot.read_once()
q = state.q
```


````

```{warning}
风险级别：只读。该示例不发送控制命令。
```

```{note}
本页的代码片段改编自 libfranka 的示例（Copyright (c) 2023 Franka Robotics GmbH，Apache License 2.0），已针对 Diana 机械臂做了修改；改编部分 Copyright (c) 2026 Agile Robots SE。详见[手册概述](/about/overview.md)中的“许可证与第三方声明”。
```

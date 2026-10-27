# 06 关节阻抗控制

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

源文件：`libfranka/pylibfranka/examples/<model>/joint_impedance_example.py`。

读取模型与初始状态后启动力矩控制，在外部循环中按关节阻抗控制律写入 Torques。

`<model>` 为已应用补丁的 `diana3`、`diana7` 或 `diana7G2`。

```bash
python3 libfranka/pylibfranka/examples/<model>/joint_impedance_example.py --ip <robot-ip>
```

| 使用的接口 | 本示例中的用途 |
|---|---|
| `load_model()` | 加载动力学模型，用于计算科氏力补偿。 |
| `read_once()` | 读取初始关节位置，作为第一段轨迹的起点。 |
| `start_torque_control()` | 启动力矩外部控制会话。 |
| `Torques` | 封装关节力矩命令。 |
## Example 调用流程

解析 --ip → 设置碰撞行为 → read_once() → start_torque_control() → load_model() → readOnce() / writeOnce(Torques)。

### 关键源码片段

```python
initial_state = robot.read_once()
active_control = robot.start_torque_control()
model = robot.load_model()
robot_state, _ = active_control.readOnce()
coriolis = np.array(model.coriolis(robot_state))
torque_command = Torques(tau_d.tolist())
active_control.writeOnce(torque_command)
```

(fci-zh-python-06_joint_impedance_example-api)=
## 逐项 API 用法与调用案例
(fci-zh-python-06_joint_impedance_example-api-116)=
### `load_model()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Robot.load_model` | `load_model() -> Model` | 返回模型对象；模型库加载失败或网络中断会抛出异常。 |

`load_model()` 通过 Python 绑定加载当前机器人的运动学/动力学模型。本示例在控制循环中用 `model.coriolis(robot_state)` 计算科氏力补偿项。

```{rubric} 调用案例
```

```python
model = robot.load_model()
```


````
(fci-zh-python-06_joint_impedance_example-api-117)=
### `read_once()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Robot.read_once` | `read_once() -> RobotState` | 返回一次 `RobotState` 状态快照；控制循环运行中、网络或机器人错误会抛出异常。 |

`read_once()` 是 Python 绑定的一次性状态读取接口。只需要当前状态时使用它；持续控制示例使用主动控制对象的 `readOnce()`。本示例在启动力矩控制前调用它，取得初始关节位置。

```{rubric} 调用案例
```

```python
initial_state = robot.read_once()
current_position = np.array(initial_state.q)
```


````
(fci-zh-python-06_joint_impedance_example-api-118)=
### `start_torque_control()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Robot.start_torque_control()` | `start_torque_control() -> ActiveControlBase` | 返回主动控制对象；控制冲突、网络中断或机器人错误会抛出异常。 |

启动主动控制模式。返回对象通过 `readOnce()` 读取状态和周期时间，通过 `writeOnce()` 写入 `Torques` 命令。

```{rubric} 调用案例
```

```python
active_control = robot.start_torque_control()
```


````
(fci-zh-python-06_joint_impedance_example-api-121)=
### `Torques`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Torques` | `Torques(tau_J: list[float])` | 返回关节力矩命令对象。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `tau_J` | 输入，`list[float]` | 7 轴关节力矩，单位 Nm。 |

封装 7 轴关节力矩命令，单位 Nm；`motion_finished` 属性为 `True` 时结束运动。力矩控制示例将控制律输出写入主动控制对象。

```{rubric} 调用案例
```

```python
torque_command = Torques(tau_d.tolist())
torque_command.motion_finished = False
active_control.writeOnce(torque_command)
```


````

```{warning}
风险级别：力矩。该示例发送控制命令；运行前请确认工作空间、急停与碰撞阈值。
```

```{note}
本页的代码片段改编自 libfranka 的示例（Copyright (c) 2023 Franka Robotics GmbH，Apache License 2.0），已针对 Diana 机械臂做了修改；改编部分 Copyright (c) 2026 Agile Robots SE。详见[手册概述](/about/overview.md)中的“许可证与第三方声明”。
```

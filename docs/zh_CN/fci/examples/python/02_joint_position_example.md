# 02 关节位置控制

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

源文件：`libfranka/pylibfranka/examples/<model>/joint_position_example.py`。

启动关节位置外部控制会话，在每个控制周期读取状态并写入七轴 JointPositions。

`<model>` 为已应用补丁的 `diana3`、`diana7` 或 `diana7G2`。

```bash
python3 libfranka/pylibfranka/examples/<model>/joint_position_example.py --ip <robot-ip>
```

| 使用的接口 | 本示例中的用途 |
|---|---|
| `start_joint_position_control()` | 启动关节位置外部控制会话。 |
| `ActiveControl.readOnce()` | 读取当前状态和周期时间。 |
| `ActiveControl.writeOnce()` | 写入本周期关节位置命令。 |
| `JointPositions` | 封装七轴目标关节角。 |
## Example 调用流程

解析 --ip → 设置碰撞行为 → start_joint_position_control() → readOnce() / writeOnce() 循环 → 设置 motion_finished。

### 关键源码片段

```python
active_control = robot.start_joint_position_control(
    ControllerMode.CartesianImpedance)
robot_state, duration = active_control.readOnce()
joint_positions = JointPositions(new_positions)
active_control.writeOnce(joint_positions)
```

(fci-zh-python-02_joint_position_example-api)=
## 逐项 API 用法与调用案例
(fci-zh-python-02_joint_position_example-api-94)=
### `start_joint_position_control()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Robot.start_joint_position_control()` | `start_joint_position_control(controller_mode: ControllerMode) -> ActiveControl` | 返回主动控制对象；控制冲突、网络中断或机器人错误会抛出异常。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `controller_mode` | 输入，`ControllerMode` | 内部控制器模式。 |

启动主动控制模式。返回对象通过 `readOnce()` 读取状态和周期时间，通过 `writeOnce()` 写入 `JointPositions` 命令。

```{rubric} 调用案例
```

```python
active_control = robot.start_joint_position_control(ControllerMode.CartesianImpedance)
```


````
(fci-zh-python-02_joint_position_example-api-95)=
### `ActiveControl.readOnce()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `ActiveControl.readOnce` | `readOnce() -> tuple[RobotState, Duration]` | 返回当前状态和周期时间；网络、协议或机器人错误会抛出异常。 |

主动控制读周期接口。示例先读取状态与 `Duration`，再计算本周期命令。

```{rubric} 调用案例
```

```python
state, period = active_control.readOnce()
```


````
(fci-zh-python-02_joint_position_example-api-96)=
### `ActiveControl.writeOnce()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `ActiveControl.writeOnce` | `writeOnce(command, control_input: Torques \| None = None)` | 无返回值；命令类型与当前控制模式不匹配会抛出异常。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `command` | 输入，控制命令对象 | 本周期目标命令。 |
| `control_input` | 输入，可选 `Torques` | 叠加力矩控制时使用。 |

主动控制写周期接口。写入的命令类型必须和启动的控制模式匹配，例如关节位置模式写 `JointPositions`，力矩模式写 `Torques`。

```{rubric} 调用案例
```

```python
active_control.writeOnce(pylibfranka.JointPositions(q_desired))
```


````
(fci-zh-python-02_joint_position_example-api-97)=
### `JointPositions`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `JointPositions` | `JointPositions(joint_positions: list[float])` | 返回关节位置命令对象。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `joint_positions` | 输入，`list[float]` | 7 轴目标关节角，单位 rad。 |

封装 7 轴目标关节角，单位 rad。关节位置主动控制示例每周期构造并写入该对象。

```{rubric} 调用案例
```

```python
command = pylibfranka.JointPositions(q_desired)
```


````

```{warning}
风险级别：运动。该示例发送控制命令；运行前请确认工作空间、急停与碰撞阈值。
```

```{note}
本页的代码片段改编自 libfranka 的示例（Copyright (c) 2023 Franka Robotics GmbH，Apache License 2.0），已针对 Diana 机械臂做了修改；改编部分 Copyright (c) 2026 Agile Robots SE。详见[手册概述](/about/overview.md)中的“许可证与第三方声明”。
```

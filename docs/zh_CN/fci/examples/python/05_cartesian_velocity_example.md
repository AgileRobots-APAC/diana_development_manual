# 05 笛卡尔速度控制

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

源文件：`libfranka/pylibfranka/examples/<model>/cartesian_velocity_example.py`。

设置关节阻抗后启动笛卡尔速度控制，并在外部循环中发送 CartesianVelocities。

`<model>` 为已应用补丁的 `diana3`、`diana7` 或 `diana7G2`。

```bash
python3 libfranka/pylibfranka/examples/<model>/cartesian_velocity_example.py --ip <robot-ip>
```

| 使用的接口 | 本示例中的用途 |
|---|---|
| `set_joint_impedance()` | 设置内部关节阻抗刚度。 |
| `start_cartesian_velocity_control()` | 启动笛卡尔速度外部控制会话。 |
| `CartesianVelocities` | 封装末端速度命令。 |
## Example 调用流程

解析 --ip → 设置碰撞与关节阻抗 → start_cartesian_velocity_control() → readOnce() / writeOnce() → 异常时 automatic_error_recovery()。

### 关键源码片段

```python
active_control = robot.start_cartesian_velocity_control(
    ControllerMode.JointImpedance)
robot_state, duration = active_control.readOnce()
active_control.writeOnce(CartesianVelocities(velocities))
```

(fci-zh-python-05_cartesian_velocity_example-api)=
## 逐项 API 用法与调用案例
(fci-zh-python-05_cartesian_velocity_example-api-110)=
### `set_joint_impedance()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Robot.set_joint_impedance` | `set_joint_impedance(K_theta: list[float])` | 无返回值；网络中断或配置失败会抛出异常。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `K_theta` | 输入，`list[float]` | 7 个关节刚度参数。 |

设置内部关节阻抗控制器的 7 轴刚度。笛卡尔速度示例在控制前调用它调整内部控制器行为。

```{rubric} 调用案例
```

```python
robot.set_joint_impedance([3000, 3000, 3000, 2500, 2500, 2000, 2000])
```


````
(fci-zh-python-05_cartesian_velocity_example-api-111)=
### `start_cartesian_velocity_control()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Robot.start_cartesian_velocity_control()` | `start_cartesian_velocity_control(controller_mode: ControllerMode) -> ActiveControl` | 返回主动控制对象；控制冲突、网络中断或机器人错误会抛出异常。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `controller_mode` | 输入，`ControllerMode` | 内部控制器模式。 |

启动主动控制模式。返回对象通过 `readOnce()` 读取状态和周期时间，通过 `writeOnce()` 写入 `CartesianVelocities` 命令。

```{rubric} 调用案例
```

```python
active_control = robot.start_cartesian_velocity_control(ControllerMode.CartesianImpedance)
```


````
(fci-zh-python-05_cartesian_velocity_example-api-114)=
### `CartesianVelocities`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `CartesianVelocities` | `CartesianVelocities(cartesian_velocities: list[float], elbow: list[float] \| None = None)` | 返回笛卡尔速度命令对象。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `cartesian_velocities` | 输入，`list[float]` | `x/y/z/wx/wy/wz` 速度。 |
| `elbow` | 输入，可选 `list[float]` | 2 维肘部构型。 |

封装 6 维末端速度，前三项为线速度 m/s，后三项为角速度 rad/s。

```{rubric} 调用案例
```

```python
command = pylibfranka.CartesianVelocities([0.0, 0.0, 0.05, 0.0, 0.0, 0.0])
```


````

```{warning}
风险级别：运动。该示例发送控制命令；运行前请确认工作空间、急停与碰撞阈值。
```

```{note}
本页的代码片段改编自 libfranka 的示例（Copyright (c) 2023 Franka Robotics GmbH，Apache License 2.0），已针对 Diana 机械臂做了修改；改编部分 Copyright (c) 2026 Agile Robots SE。详见[手册概述](/about/overview.md)中的“许可证与第三方声明”。
```

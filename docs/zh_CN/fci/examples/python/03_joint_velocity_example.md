# 03 关节速度控制

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

源文件：`libfranka/pylibfranka/examples/<model>/joint_velocity_example.py`。

启动关节速度外部控制会话，按周期计算并发送 JointVelocities。

`<model>` 为已应用补丁的 `diana3`、`diana7` 或 `diana7G2`。

```bash
python3 libfranka/pylibfranka/examples/<model>/joint_velocity_example.py --ip <robot-ip>
```

| 使用的接口 | 本示例中的用途 |
|---|---|
| `start_joint_velocity_control()` | 启动关节速度外部控制会话。 |
| `JointVelocities` | 封装七轴目标关节速度。 |
## Example 调用流程

解析 --ip → 设置碰撞行为 → start_joint_velocity_control() → readOnce() / writeOnce() 循环。

### 关键源码片段

```python
active_control = robot.start_joint_velocity_control(
    ControllerMode.CartesianImpedance)
robot_state, duration = active_control.readOnce()
active_control.writeOnce(JointVelocities(velocities))
```

(fci-zh-python-03_joint_velocity_example-api)=
## 逐项 API 用法与调用案例
(fci-zh-python-03_joint_velocity_example-api-100)=
### `start_joint_velocity_control()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Robot.start_joint_velocity_control()` | `start_joint_velocity_control(controller_mode: ControllerMode) -> ActiveControl` | 返回主动控制对象；控制冲突、网络中断或机器人错误会抛出异常。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `controller_mode` | 输入，`ControllerMode` | 内部控制器模式。 |

启动主动控制模式。返回对象通过 `readOnce()` 读取状态和周期时间，通过 `writeOnce()` 写入 `JointVelocities` 命令。

```{rubric} 调用案例
```

```python
active_control = robot.start_joint_velocity_control(ControllerMode.CartesianImpedance)
```


````
(fci-zh-python-03_joint_velocity_example-api-103)=
### `JointVelocities`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `JointVelocities` | `JointVelocities(joint_velocities: list[float])` | 返回关节速度命令对象。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `joint_velocities` | 输入，`list[float]` | 7 轴目标关节速度，单位 rad/s。 |

封装 7 轴目标关节速度，单位 rad/s。

```{rubric} 调用案例
```

```python
command = pylibfranka.JointVelocities([0.0] * 7)
```


````

```{warning}
风险级别：运动。该示例发送控制命令；运行前请确认工作空间、急停与碰撞阈值。
```

```{note}
本页的代码片段改编自 libfranka 的示例（Copyright (c) 2023 Franka Robotics GmbH，Apache License 2.0），已针对 Diana 机械臂做了修改；改编部分 Copyright (c) 2026 Agile Robots SE。详见[手册概述](/about/overview.md)中的“许可证与第三方声明”。
```

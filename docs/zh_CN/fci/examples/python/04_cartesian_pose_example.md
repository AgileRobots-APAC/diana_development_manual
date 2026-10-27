# 04 笛卡尔位姿控制

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

源文件：`libfranka/pylibfranka/examples/<model>/cartesian_pose_example.py`。

启动笛卡尔位姿外部控制会话，在末端初始位姿基础上生成圆形目标轨迹。

`<model>` 为已应用补丁的 `diana3`、`diana7` 或 `diana7G2`。

```bash
python3 libfranka/pylibfranka/examples/<model>/cartesian_pose_example.py --ip <robot-ip>
```

| 使用的接口 | 本示例中的用途 |
|---|---|
| `start_cartesian_pose_control()` | 启动笛卡尔位姿外部控制会话。 |
| `CartesianPose` | 封装末端目标位姿。 |
## Example 调用流程

解析 --ip → 设置碰撞行为 → start_cartesian_pose_control() → readOnce() → 计算 CartesianPose → writeOnce()。

### 关键源码片段

```python
active_control = robot.start_cartesian_pose_control(
    ControllerMode.JointImpedance)
robot_state, duration = active_control.readOnce()
active_control.writeOnce(CartesianPose(new_pose))
```

(fci-zh-python-04_cartesian_pose_example-api)=
## 逐项 API 用法与调用案例
(fci-zh-python-04_cartesian_pose_example-api-105)=
### `start_cartesian_pose_control()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Robot.start_cartesian_pose_control()` | `start_cartesian_pose_control(controller_mode: ControllerMode) -> ActiveControl` | 返回主动控制对象；控制冲突、网络中断或机器人错误会抛出异常。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `controller_mode` | 输入，`ControllerMode` | 内部控制器模式。 |

启动主动控制模式。返回对象通过 `readOnce()` 读取状态和周期时间，通过 `writeOnce()` 写入 `CartesianPose` 命令。

```{rubric} 调用案例
```

```python
active_control = robot.start_cartesian_pose_control(ControllerMode.CartesianImpedance)
```


````
(fci-zh-python-04_cartesian_pose_example-api-108)=
### `CartesianPose`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `CartesianPose` | `CartesianPose(cartesian_pose: list[float], elbow: list[float] \| None = None)` | 返回笛卡尔位姿命令对象。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `cartesian_pose` | 输入，`list[float]` | 16 维位姿矩阵，列主序。 |
| `elbow` | 输入，可选 `list[float]` | 2 维肘部构型。 |

封装末端相对于 base frame 的 4x4 目标位姿矩阵，按列主序展开；可选 elbow 指定肘部构型。

```{rubric} 调用案例
```

```python
command = pylibfranka.CartesianPose(target_pose)
```


````

```{warning}
风险级别：运动。该示例发送控制命令；运行前请确认工作空间、急停与碰撞阈值。
```

```{note}
本页的代码片段改编自 libfranka 的示例（Copyright (c) 2023 Franka Robotics GmbH，Apache License 2.0），已针对 Diana 机械臂做了修改；改编部分 Copyright (c) 2026 Agile Robots SE。详见[手册概述](/about/overview.md)中的“许可证与第三方声明”。
```

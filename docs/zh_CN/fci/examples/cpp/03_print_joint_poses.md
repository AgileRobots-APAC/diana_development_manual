# 03 打印各关节坐标系

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

源文件：`libfranka/examples/<model>/print_joint_poses.cpp`。

读取一次状态，使用模型计算 base 到 Joint1…末端执行器的位姿矩阵。

`<model>` 为已应用补丁的 `diana3`、`diana7` 或 `diana7G2`。

```bash
./build/libfranka/examples/<model>/print_joint_poses <robot-ip>
```

| 使用的接口 | 本示例中的用途 |
|---|---|
| `Robot::readOnce()` | 读取当前机器人状态。 |
| `Robot::loadModel()` | 加载当前机器人对应的运动学模型。 |
| `Model::pose()` | 计算指定关节或末端坐标系相对基座的位姿矩阵。 |
## Example 调用流程

Robot::readOnce() → Robot::loadModel() → 枚举 Frame::kJoint1 至 Frame::kEndEffector → Model::pose()。

### 关键源码片段

```cpp
franka::RobotState state = robot.readOnce();
franka::Model model(robot.loadModel());
for (franka::Frame frame = franka::Frame::kJoint1;
     frame <= franka::Frame::kEndEffector; frame++) {
  std::cout << model.pose(frame, state) << std::endl;
}
```

(fci-zh-cpp-03_print_joint_poses-api)=
## 逐项 API 用法与调用案例
(fci-zh-cpp-03_print_joint_poses-api-1)=
### `franka::RobotState`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `franka::RobotState` | `struct RobotState` | 状态结构体本身无函数返回值；由 `Robot::readOnce()`、`Robot::read()` 或控制回调提供。 |

`RobotState` 是机器人状态快照，包含关节位置、速度、力矩、位姿矩阵、碰撞/接触标志等字段。本例把它作为模型计算输入，不修改该对象。

```{rubric} 调用案例
```

```cpp
franka::RobotState state = robot.readOnce();
std::cout << state.q << std::endl;
```


````
(fci-zh-cpp-03_print_joint_poses-api-2)=
### `Robot::readOnce()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Robot::readOnce` | `virtual RobotState readOnce()` | 返回一次 `franka::RobotState` 状态快照；控制循环运行中、网络中断或机器人错误会抛出异常。 |

`readOnce()` 只读取当前一帧状态，适合示例中获取起点、模型计算输入或一次性诊断。头文件建议连续读取状态时使用 `Robot::read()`。

```{rubric} 调用案例
```

```cpp
franka::RobotState state = robot.readOnce();
```


````
(fci-zh-cpp-03_print_joint_poses-api-3)=
### `Robot::loadModel()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Robot::loadModel` | `Model loadModel()` | 返回与当前机器人匹配的 `franka::Model`；模型库加载失败抛出 `ModelException`，网络中断抛出 `NetworkException`。 |

`loadModel()` 加载机器人动力学/运动学模型。示例用返回的 `Model` 计算正运动学、Jacobian、Coriolis 和重力项。

```{rubric} 调用案例
```

```cpp
franka::Model model = robot.loadModel();
```


````
(fci-zh-cpp-03_print_joint_poses-api-4)=
### `Model::pose()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Model::pose` | `std::array<double, 16> pose(Frame frame, const RobotState& robot_state) const` | 返回指定坐标系相对于基座的 4x4 齐次矩阵，按列主序展开。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `frame` | 输入，`Frame` | 要计算的坐标系，如 `Frame::kJoint1`、`Frame::kEndEffector`。 |
| `robot_state` | 输入，`const RobotState&` | 用于计算模型的状态快照。 |

`pose()` 根据给定状态计算指定 `Frame` 的正运动学位姿。本例遍历 `Frame::kJoint1` 到 `Frame::kEndEffector`，打印各关节坐标系。

```{rubric} 调用案例
```

```cpp
auto O_T_frame = model.pose(frame, state);
std::cout << O_T_frame << std::endl;
```


````

```{warning}
风险级别：只读。该示例会读取机器人状态，不发送运动或力矩命令；运行前请确认工作空间、急停与碰撞阈值。
```

```{note}
本页的代码片段改编自 libfranka 的示例（Copyright (c) 2023 Franka Robotics GmbH，Apache License 2.0），已针对 Diana 机械臂做了修改；改编部分 Copyright (c) 2026 Agile Robots SE。详见[手册概述](/about/overview.md)中的“许可证与第三方声明”。
```

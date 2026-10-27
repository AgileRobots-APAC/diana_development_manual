# 18 笛卡尔阻抗控制

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

源文件：`libfranka/examples/<model>/cartesian_impedance_control.cpp`。

基于模型雅可比矩阵和科氏项，在笛卡尔空间计算阻抗力矩。

`<model>` 为已应用补丁的 `diana3`、`diana7` 或 `diana7G2`。

```bash
./build/libfranka/examples/<model>/cartesian_impedance_control <robot-ip>
```

| 使用的接口 | 本示例中的用途 |
|---|---|
| `Model::zeroJacobian()` | 计算末端零雅可比矩阵。 |
## Example 调用流程

readOnce() 获取初态 → 加载模型 → zeroJacobian() 计算雅可比 → 计算位置/姿态误差和力矩 → robot.control()。

### 关键源码片段

```cpp
franka::RobotState initial_state = robot.readOnce();
franka::Model model(robot.loadModel());
auto jacobian = model.zeroJacobian(franka::Frame::kEndEffector, state);
return franka::Torques(tau_task + model.coriolis(state));
```

(fci-zh-cpp-18_cartesian_impedance_control-api)=
## 逐项 API 用法与调用案例
(fci-zh-cpp-18_cartesian_impedance_control-api-74)=
### `Model::zeroJacobian()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Model::zeroJacobian` | `std::array<double, 42> zeroJacobian(Frame frame, const RobotState& robot_state) const` | 返回 6x7 零空间/基座坐标系 Jacobian，按列主序展开。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `frame` | 输入，`Frame` | 目标坐标系，常用 `Frame::kEndEffector`。 |
| `robot_state` | 输入，`const RobotState&` | 当前状态快照。 |

`zeroJacobian()` 计算指定坐标系在 base frame 下的 Jacobian。阻抗和力控示例用它把笛卡尔量映射到关节空间。

```{rubric} 调用案例
```

```cpp
std::array<double, 42> jacobian_array =
    model.zeroJacobian(franka::Frame::kEndEffector, state);
```


````

```{note}
本页的代码片段改编自 libfranka 的示例（Copyright (c) 2023 Franka Robotics GmbH，Apache License 2.0），已针对 Diana 机械臂做了修改；改编部分 Copyright (c) 2026 Agile Robots SE。详见[手册概述](/about/overview.md)中的“许可证与第三方声明”。
```

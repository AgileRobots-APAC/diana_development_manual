# 19 力控制

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

源文件：`libfranka/examples/<model>/force_control.cpp`。

使用末端零雅可比和重力项实现沿指定方向的期望接触力控制。

`<model>` 为已应用补丁的 `diana3`、`diana7` 或 `diana7G2`。

```bash
./build/libfranka/examples/<model>/force_control <robot-ip>
```

| 使用的接口 | 本示例中的用途 |
|---|---|
| `Model::gravity()` | 计算初始状态下的重力项，用于去除力矩传感器偏置和估计外部力矩。 |
## Example 调用流程

加载模型 → readOnce() 取得初态 → gravity() 标定外部力矩偏置 → 力矩回调中 zeroJacobian() 将期望末端力映射为关节力矩 → 前馈 + PI 控制输出 Torques。

### 关键源码片段

```cpp
std::array<double, 7> gravity_array = model.gravity(initial_state);
initial_tau_ext = initial_tau_measured - initial_gravity;
// in the torque-control callback:
std::array<double, 42> jacobian_array =
    model.zeroJacobian(franka::Frame::kEndEffector, robot_state);
tau_ext << tau_measured - gravity - initial_tau_ext;
tau_d << jacobian.transpose() * desired_force_torque;
tau_error_integral += period.toSec() * (tau_d - tau_ext);
tau_cmd << tau_d + k_p * (tau_d - tau_ext) + k_i * tau_error_integral;
```

(fci-zh-cpp-19_force_control-api)=
## 逐项 API 用法与调用案例
(fci-zh-cpp-19_force_control-api-80)=
### `Model::gravity()`

````{container} api-example-block

| 函数 | 原型 | 返回值 |
| --- | --- | --- |
| `Model::gravity` | `std::array<double, 7> gravity(const franka::RobotState& robot_state) const noexcept` | 返回 7 维重力力矩数组，单位 Nm。 |

| 参数 | 方向/类型 | 含义 |
| --- | --- | --- |
| `robot_state` | 输入，`const franka::RobotState&` | 用于计算的机器人状态。 |

`gravity()` 根据当前位形计算重力项。本示例只在启动前用初始状态计算一次，从测得力矩 `tau_J` 中减去重力得到初始外部力矩偏置；控制回调中继续用这组重力项估计外部力矩 `tau_ext`。

```{rubric} 调用案例
```

```cpp
franka::RobotState initial_state = robot.readOnce();
std::array<double, 7> gravity_array = model.gravity(initial_state);
```


````

```{note}
本页的代码片段改编自 libfranka 的示例（Copyright (c) 2023 Franka Robotics GmbH，Apache License 2.0），已针对 Diana 机械臂做了修改；改编部分 Copyright (c) 2026 Agile Robots SE。详见[手册概述](/about/overview.md)中的“许可证与第三方声明”。
```

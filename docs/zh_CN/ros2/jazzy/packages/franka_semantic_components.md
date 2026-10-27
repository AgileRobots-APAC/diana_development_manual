# 语义组件

软件包名称：`franka_semantic_components`

## 安装

请参阅 [开发准备](../development.md)。

## 软件包概述

`franka_semantic_components` 是一个 C++ 库（命名空间 `franka_semantic_components`），把 [franka_hardware](franka_hardware.md) 导出的原始 `ros2_control` 接口封装为带类型的类。控制器使用这些类读取机器人状态、计算动力学模型、下发笛卡尔位姿或速度命令，而不必自己处理接口名和元素顺序。

| 类 | 头文件 | 封装对象 |
| --- | --- | --- |
| `FrankaSemanticComponentInterface` | `franka_semantic_component_interface.hpp` | 基类，负责借出的状态与命令接口 |
| `FrankaRobotState` | `franka_robot_state.hpp` | `robot_state` 接口，转换为 `franka_msgs/msg/FrankaRobotState` |
| `FrankaRobotModel` | `franka_robot_model.hpp` | `robot_model` 与 `robot_state` 接口，用于访问动力学模型 |
| `FrankaCartesianPoseInterface` | `franka_cartesian_pose_interface.hpp` | `cartesian_pose_command` / `cartesian_pose_state`（及肘部）接口 |
| `FrankaCartesianVelocityInterface` | `franka_cartesian_velocity_interface.hpp` | `cartesian_velocity`（及肘部）接口 |

本包依赖 `franka_hardware`、`franka_msgs`、`controller_interface`、`hardware_interface`、`urdf` 和 `eigen`。头文件安装在 `include/franka_semantic_components/` 下。

```{tip}
请在控制器中使用这些语义组件，而不是自己列出 `0/cartesian_pose_command` 之类的原始接口名。这些类会拼出正确的接口名（含 `arm_prefix`），按其预期顺序返回，并检查大小和肘部的使用。
```

## FrankaSemanticComponentInterface

笛卡尔位姿和速度接口的基类，持有借出的状态接口和命令接口。

| 方法 | 说明 |
| --- | --- |
| `FrankaSemanticComponentInterface(const std::string& name, size_t state_interface_size = 0, size_t command_interface_size = 0)` | 构造函数；`name` 为默认接口名的前缀，两个大小用于预留容量 |
| `bool assign_loaned_state_interfaces(std::vector<hardware_interface::LoanedStateInterface>& state_interfaces)` | 在控制器激活时，按已声明的接口名顺序取得借出的状态接口 |
| `bool assign_loaned_command_interfaces(std::vector<hardware_interface::LoanedCommandInterface>& command_interfaces)` | 同上，针对命令接口 |
| `void release_interfaces()` | 释放借出的接口 |
| `virtual std::vector<std::string> get_state_interface_names()` | 用于控制器的 `state_interface_configuration()`；默认实现生成 `name/1`、`name/2` ... |
| `virtual std::vector<std::string> get_command_interface_names()` | 用于控制器的 `command_interface_configuration()`；默认实现同上 |
| `std::vector<double> get_values_state_interfaces() const` | 返回所有状态接口的值 |
| `std::vector<double> get_values_command_interfaces() const` | 返回所有命令接口的值 |
| `bool set_values(const std::vector<double>& commanded_values)` | 设置所有命令接口的值；数量与借出的命令接口数不一致时返回 false |

## FrankaRobotState

读取 `robot_state` 接口，并填充 `franka_msgs/msg/FrankaRobotState` 消息。构造时需要机器人描述（URDF），它用于确定连杆与关节的顺序和消息中的坐标系名称。

| 方法 | 说明 |
| --- | --- |
| `FrankaRobotState(const std::string& name, const std::string& robot_description)` | `name` 为状态接口名，形如 `<arm_prefix>_<robot_type>/robot_state`；URDF 无法解析时抛出异常 |
| `bool assign_loaned_state_interfaces(std::vector<hardware_interface::LoanedStateInterface>& state_interfaces)` | 取得借出的接口并解析硬件导出的状态缓冲；成功返回 true |
| `void release_interfaces()` | 清除缓存的状态缓冲指针并释放借出的接口 |
| `virtual void initialize_robot_state_msg(franka_msgs::msg::FrankaRobotState& message)` | 用 URDF 中的坐标系名称初始化消息 |
| `virtual bool get_values_as_message(franka_msgs::msg::FrankaRobotState& message)` | 用当前状态填充消息；无法解析状态缓冲时返回 false |

继承自 `semantic_components::SemanticComponentInterface`，因此也提供 `get_state_interface_names()` 返回所申请的接口名。

```cpp
// on_configure()
robot_state_ = std::make_unique<franka_semantic_components::FrankaRobotState>(
    arm_prefix + "_" + robot_type + "/robot_state", get_robot_description());

// state_interface_configuration()
config.names = robot_state_->get_state_interface_names();

// on_activate() / update() / on_deactivate()
robot_state_->assign_loaned_state_interfaces(state_interfaces_);
franka_msgs::msg::FrankaRobotState msg;
robot_state_->initialize_robot_state_msg(msg);
robot_state_->get_values_as_message(msg);
robot_state_->release_interfaces();
```

上例中 `arm_prefix` 为空时，接口名为 `<robot_type>/robot_state`。[franka_robot_state_broadcaster](franka_robot_state_broadcaster.md) 即使用该类。

## FrankaRobotModel

通过 `robot_model` 和 `robot_state` 两个接口访问硬件插件持有的动力学模型。所有方法都基于最近一次读取的机器人状态（缓存最长 1 ms 后刷新）；状态接口不可用时抛出运行时异常。

| 方法 | 说明 |
| --- | --- |
| `FrankaRobotModel(const std::string& franka_model_interface_name, const std::string& franka_state_interface_name)` | 两个参数分别为 `robot_model` 和 `robot_state` 接口的完整名称 |
| `std::array<double, 49> getMassMatrix()` | 7x7 质量矩阵，列主序，单位 kg·m² |
| `std::array<double, 7> getCoriolisForceVector()` | 科氏力向量 `c = C * dq`，单位 Nm |
| `std::array<double, 7> getGravityForceVector()` | 重力向量，单位 Nm |
| `std::array<double, 16> getPoseMatrix(const franka::Frame& frame)` | 指定坐标系在基坐标系下的 4x4 位姿矩阵，列主序 |
| `std::array<double, 42> getBodyJacobian(const franka::Frame& frame)` | 6x7 体雅可比，表示在给定坐标系中，列主序 |
| `std::array<double, 42> getZeroJacobian(const franka::Frame& frame)` | 6x7 雅可比，表示在基坐标系中，列主序 |

雅可比的上三行为线速度分量，下三行为角速度分量。

```cpp
// on_configure()：接口名为 <arm_prefix>_<robot_type>/robot_model 与 .../robot_state
model_ = std::make_unique<franka_semantic_components::FrankaRobotModel>(
    prefix + robot_type + "/robot_model", prefix + robot_type + "/robot_state");

// state_interface_configuration()：返回两个接口名
config.names = model_->get_state_interface_names();

// on_activate() / update() / on_deactivate()
model_->assign_loaned_state_interfaces(state_interfaces_);
std::array<double, 49> mass = model_->getMassMatrix();
std::array<double, 16> pose = model_->getPoseMatrix(franka::Frame::kEndEffector);
model_->release_interfaces();
```

其中 `prefix` 为 `arm_prefix + "_"`（`arm_prefix` 为空时为空字符串）。

## FrankaCartesianPoseInterface

下发并读取笛卡尔末端位姿。它申请 16 个 `cartesian_pose_command` 命令接口和 16 个 `cartesian_pose_state` 状态接口，名称为 `<arm_prefix><i>/cartesian_pose_command` 与 `<arm_prefix><i>/cartesian_pose_state`（`i` 为 0 至 15）。当 `command_elbow_active = true` 时，还会申请两个 `elbow_command` 命令接口（`<arm_prefix>joint_3_position/elbow_command`、`<arm_prefix>joint_4_sign/elbow_command`）和两个 `elbow_state` 状态接口（`<arm_prefix>joint_3_position/elbow_state`、`<arm_prefix>joint_4_sign/elbow_state`）。这里的 `arm_prefix` 按原样拼接，不会自动补下划线。

| 方法 | 说明 |
| --- | --- |
| `FrankaCartesianPoseInterface(bool command_elbow_active)` 与 `FrankaCartesianPoseInterface(const std::string& arm_prefix, bool command_elbow_active)` | 构造函数；`arm_prefix` 为接口名的前缀 |
| `bool setCommand(const std::array<double, 16>& pose_command)` | 列主序 4x4 位姿；肘部激活时返回 false |
| `bool setCommand(const std::array<double, 16>& pose_command, const std::array<double, 2>& elbow)` | 位姿加肘部 `[joint_3_position, joint_4_sign]`；肘部未激活时返回 false |
| `std::array<double, 16> getCommandedPoseMatrix()` | 最近一次命令的位姿 |
| `std::array<double, 16> getCurrentPoseMatrix()` | 来自 `cartesian_pose_state` 接口的当前位姿 |
| `std::tuple<Eigen::Quaterniond, Eigen::Vector3d> getCurrentOrientationAndTranslation()` | 以四元数和平移表示的当前位姿 |
| `std::tuple<Eigen::Quaterniond, Eigen::Vector3d> getCommandedOrientationAndTranslation()` | 以四元数和平移表示的命令位姿 |
| `std::array<double, 2> getCommandedElbowConfiguration()` / `getCurrentElbowConfiguration()` | 肘部值；肘部未激活时抛出 `std::runtime_error` |

```cpp
// on_configure()：同时命令肘部
cartesian_pose_ = std::make_unique<franka_semantic_components::FrankaCartesianPoseInterface>(
    arm_prefix, /*command_elbow_active=*/true);

// command_interface_configuration() / state_interface_configuration()
config.names = cartesian_pose_->get_command_interface_names();   // 以及 get_state_interface_names()

// on_activate()
cartesian_pose_->assign_loaned_command_interfaces(command_interfaces_);
cartesian_pose_->assign_loaned_state_interfaces(state_interfaces_);

// update()：保持当前位姿，仅移动肘部的关节 3
std::array<double, 16> pose = cartesian_pose_->getCurrentPoseMatrix();
std::array<double, 2> elbow = cartesian_pose_->getCurrentElbowConfiguration();
elbow[0] += delta;
if (!cartesian_pose_->setCommand(pose, elbow)) {
  return controller_interface::return_type::ERROR;
}
```

```{warning}
下发笛卡尔位姿会使机器人运动。请相对当前位姿下发小幅、连续的变化，并确保工作空间无人员和障碍物、急停触手可及，参见[安全边界](../../../reference/safety.md)。
```

## FrankaCartesianVelocityInterface

下发笛卡尔末端速度。它申请六个 `cartesian_velocity` 命令接口，名称为 `<arm_prefix><axis>/cartesian_velocity`，`<axis>` 依次为 `vx`、`vy`、`vz`、`wx`、`wy`、`wz`；当 `command_elbow_active = true` 时，还会申请两个 `elbow_command` 命令接口和两个 `elbow_state` 状态接口（名称同上）。枚举 `VX, VY, VZ, WX, WY, WZ` 给出元素顺序。

| 方法 | 说明 |
| --- | --- |
| `FrankaCartesianVelocityInterface(bool command_elbow_active)` 与 `FrankaCartesianVelocityInterface(const std::string& arm_prefix, bool command_elbow_active)` | 构造函数，参数含义与位姿接口相同 |
| `bool setCommand(const Eigen::Vector3d& linear_velocity_command, const Eigen::Vector3d& angular_velocity_command)` | 线速度与角速度；肘部激活时返回 false |
| `bool setCommand(const Eigen::Vector3d&, const Eigen::Vector3d&, const std::array<double, 2>& elbow_command)` | 同上，带肘部；肘部未激活时返回 false |
| `std::array<double, 2> getCommandedElbowConfiguration()` | 命令的肘部值；肘部未激活时抛出 `std::runtime_error` |
| `std::array<double, 2> getCurrentElbowConfiguration()` | 当前肘部值；肘部未激活时抛出 `std::runtime_error` |

```cpp
velocity_ = std::make_unique<franka_semantic_components::FrankaCartesianVelocityInterface>(
    arm_prefix, /*command_elbow_active=*/false);

config.names = velocity_->get_command_interface_names();   // command_interface_configuration()
velocity_->assign_loaned_command_interfaces(command_interfaces_);   // on_activate()

Eigen::Vector3d linear(0.0, 0.0, 0.01);
Eigen::Vector3d angular(0.0, 0.0, 0.0);
velocity_->setCommand(linear, angular);   // update()
```

```{warning}
下发笛卡尔速度会使机器人运动。请从很小的速度开始，并确保工作空间无人员和障碍物、急停触手可及，参见[安全边界](../../../reference/safety.md)。
```

```{note}
本页的代码片段改编自 `franka_ros2`，其源码带有 Franka Robotics GmbH 的版权声明（Copyright (c) 2023 Franka Robotics GmbH，Apache License 2.0）。详见[手册概述](/about/overview.md)中的“许可证与第三方声明”。
```

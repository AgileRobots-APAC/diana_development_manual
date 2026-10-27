# 语义组件

软件包名称：`diana_semantic_components`

## 安装

请参阅 [开发准备](../development.md)。

## 软件包概述

`diana_semantic_components` 是一个 C++ 库（命名空间 `diana_semantic_components`），把 [diana_hardware](diana_hardware.md) 导出的原始 `ros2_control` 接口封装为带类型的类。控制器借助这些类读取机器人状态、计算动力学模型、下发笛卡尔位姿或速度命令，而无需自己处理接口名称和元素顺序。

| 类 | 头文件 | 封装对象 |
| --- | --- | --- |
| `DianaSemanticComponentInterface` | `diana_semantic_component_interface.hpp` | 基类，负责借用状态与命令接口 |
| `DianaRobotState` | `diana_robot_state.hpp` | `robot_state` 接口，转换为 `diana_msgs/msg/DianaRobotState` |
| `DianaRobotModel` | `diana_robot_model.hpp` | `robot_model` 与 `robot_state` 接口，提供动力学模型访问 |
| `DianaCartesianPoseInterface` | `diana_cartesian_pose_interface.hpp` | `cartesian_pose_command` / `cartesian_pose_state`（及肘部）接口 |
| `DianaCartesianVelocityInterface` | `diana_cartesian_velocity_interface.hpp` | `cartesian_velocity`（及肘部）接口 |

```{figure} ../../../../_static/images/ros2-humble-semantic-components-zh.png
:alt: 语义组件与硬件接口、使用它们的控制器之间的关系
:width: 100%

语义组件的位置：左侧是 `diana_hardware` 导出的接口，中间是本软件包的类，右侧是使用这些类的软件包和示例控制器。
```

本软件包依赖 `diana_hardware`、`diana_msgs`、`controller_interface`、`hardware_interface`、`urdf` 和 `eigen`。头文件安装在 `include/diana_semantic_components/` 下。

```{tip}
在控制器中请使用语义组件，而不是罗列 `diana3_joint1/position`、`0/cartesian_pose_command` 这样的原始接口名。这些类会生成正确的名称（包含机械臂前缀），按它们期望的顺序返回，并替你检查大小和肘部的使用方式。
```

## 调用流程

无论使用哪个类，在控制器中的用法都遵循同一条流程：在初始化或配置阶段构造类，在接口配置回调中返回它给出的接口名，在激活时把 controller manager 借出的接口交给它，在每个控制周期读写，在停用时释放。

```{figure} ../../../../_static/images/ros2-humble-semantic-flow-zh.png
:alt: 控制器回调与语义组件方法的调用顺序
:width: 80%

控制器各回调的执行顺序（左）与每个回调中调用的语义组件方法（右）。
```

```{note}
`update()` 在实时循环中运行。构造类、解析 URDF 等耗时操作应放在 `on_configure` 中完成，`update()` 里只读写接口。
```

下面按类逐个说明各方法，并给出完整的代码片段。

## DianaSemanticComponentInterface

两个笛卡尔命令类（`DianaCartesianPoseInterface`、`DianaCartesianVelocityInterface`）的基类。它是 `ros2_control` 语义组件接口的拷贝，并扩展了对命令接口的访问。

| 方法 | 说明 |
| --- | --- |
| `DianaSemanticComponentInterface(const std::string& name, size_t state_interface_size = 0, size_t command_interface_size = 0)` | 构造函数；`name` 是生成接口名时的默认前缀 |
| `std::vector<std::string> get_state_interface_names()` | 在 `state_interface_configuration()` 中返回的状态接口名 |
| `std::vector<std::string> get_command_interface_names()` | 在 `command_interface_configuration()` 中返回的命令接口名 |
| `bool assign_loaned_state_interfaces(std::vector<hardware_interface::LoanedStateInterface>&)` | 在 `on_activate` 中调用；按名称对借用的接口排序 |
| `bool assign_loaned_command_interfaces(std::vector<hardware_interface::LoanedCommandInterface>&)` | 在 `on_activate` 中调用 |
| `void release_interfaces()` | 在 `on_deactivate` 中调用 |
| `std::vector<double> get_values_state_interfaces() const` | 所有已分配状态接口的当前值 |
| `std::vector<double> get_values_command_interfaces() const` | 所有已分配命令接口的当前值 |
| `bool set_values(const std::vector<double>&)` | 写入所有命令接口；大小不匹配时返回 false |

## DianaRobotState

继承自 `semantic_components::SemanticComponentInterface<diana_msgs::msg::DianaRobotState>`。它申请一个接口 `<robot_name>/robot_state`，并据此填充 [`DianaRobotState`](diana_msgs.md) 消息。

| 方法 | 说明 |
| --- | --- |
| `DianaRobotState(const std::string& name, const std::string& robot_description)` | `name` 是完整接口名，例如 `diana3/robot_state`；机器人名取自第一个 `/` 之前的部分。会解析 URDF，解析失败时抛出 `std::runtime_error` |
| `void initialize_robot_state_msg(diana_msgs::msg::DianaRobotState& message)` | 设定数组大小并按 URDF 连杆设置 `frame_id` 字段；填充每条消息前需调用一次 |
| `bool get_values_as_message(diana_msgs::msg::DianaRobotState& message)` | 把当前机器人状态转换到 `message`；接口未分配时返回 false 并记录错误 |

[diana_robot_state_broadcaster](diana_robot_state_broadcaster.md) 使用的就是这个类。

```cpp
// 控制器类成员
std::unique_ptr<diana_semantic_components::DianaRobotState> robot_state_;
diana_msgs::msg::DianaRobotState state_msg_;

// on_configure()，robot_description 为 URDF 字符串
robot_state_ = std::make_unique<diana_semantic_components::DianaRobotState>(
    arm_prefix + robot_type + "/robot_state", robot_description);
robot_state_->initialize_robot_state_msg(state_msg_);

// state_interface_configuration()
config.names = robot_state_->get_state_interface_names();

// on_activate() / update() / on_deactivate()
robot_state_->assign_loaned_state_interfaces(state_interfaces_);
robot_state_->get_values_as_message(state_msg_);
robot_state_->release_interfaces();
```

## DianaRobotModel

继承自 `semantic_components::SemanticComponentInterface<diana_hardware::Model>`。它申请两个接口，并提供所连机器人动力学模型的访问。

| 方法 | 说明 |
| --- | --- |
| `DianaRobotModel(const std::string& diana_model_interface_name, const std::string& diana_state_interface_name)` | 完整名称，例如 `diana3/robot_model` 和 `diana3/robot_state`；默认构造函数已删除 |
| `std::array<double, 49> getMassMatrix()` | 7x7 质量矩阵，列主序，kg m^2 |
| `std::array<double, 7> getCoriolisForceVector()` | 科氏力向量，Nm |
| `std::array<double, 7> getGravityForceVector()` | 重力向量，Nm |
| `std::array<double, 16> getPoseMatrix(const franka::Frame& frame)` | 某坐标系在基坐标系下的 4x4 位姿，列主序 |
| `std::array<double, 42> getBodyJacobian(const franka::Frame& frame)` | 相对于给定坐标系的 6x7 本体雅可比，列主序 |
| `std::array<double, 42> getZeroJacobian(const franka::Frame& frame)` | 相对于基坐标系的 6x7 雅可比，列主序 |

两个接口背后的指针在第一次调用时解析。如果接口尚未分配，这些方法会抛出 `std::runtime_error`。

```cpp
// 构造模型（名称含机械臂前缀）
model_ = std::make_unique<diana_semantic_components::DianaRobotModel>(
    arm_prefix + robot_type + "/robot_model", arm_prefix + robot_type + "/robot_state");

// state_interface_configuration()：返回两个接口名
config.names = model_->get_state_interface_names();

// on_activate() / update() / on_deactivate()
model_->assign_loaned_state_interfaces(state_interfaces_);
std::array<double, 49> mass = model_->getMassMatrix();
std::array<double, 16> pose = model_->getPoseMatrix(franka::Frame::kEndEffector);
model_->release_interfaces();
```

## DianaCartesianPoseInterface

下发并读取笛卡尔末端位姿。它申请 16 个 `cartesian_pose_command` 命令接口和 16 个 `cartesian_pose_state` 状态接口（`<arm_prefix>0` ... `<arm_prefix>15`）。当 `command_elbow_active = true` 时，还会申请两个 `elbow_command` 命令接口和两个 `elbow_state` 状态接口（`joint_3_position`、`joint_4_sign`）。

| 方法 | 说明 |
| --- | --- |
| `DianaCartesianPoseInterface(bool command_elbow_active)` 与 `DianaCartesianPoseInterface(const std::string& arm_prefix, bool command_elbow_active)` | 构造函数；`arm_prefix` 为接口名的前缀 |
| `bool setCommand(const std::array<double, 16>& pose_command)` | 列主序 4x4 位姿；肘部激活时返回 false |
| `bool setCommand(const std::array<double, 16>& pose_command, const std::array<double, 2>& elbow)` | 位姿加肘部 `[joint_3_position, joint_4_sign]`；肘部未激活时返回 false |
| `bool setCommand(const Eigen::Quaterniond& quaternion, const Eigen::Vector3d& translation)` | 姿态与位置；肘部不得激活 |
| `bool setCommand(const Eigen::Quaterniond&, const Eigen::Vector3d&, const std::array<double, 2>& elbow_command)` | 同上，带肘部；肘部必须激活 |
| `std::array<double, 16> getCommandedPoseMatrix()` | 最近一次命令的位姿 |
| `std::array<double, 16> getCurrentPoseMatrix()` | 来自 `cartesian_pose_state` 接口的当前位姿 |
| `std::tuple<Eigen::Quaterniond, Eigen::Vector3d> getCurrentOrientationAndTranslation()` | 以四元数和平移表示的当前位姿 |
| `std::tuple<Eigen::Quaterniond, Eigen::Vector3d> getCommandedOrientationAndTranslation()` | 以四元数和平移表示的命令位姿 |
| `std::array<double, 2> getCommandedElbowConfiguration()` / `getCurrentElbowConfiguration()` | 肘部值；肘部未激活时抛出 `std::runtime_error` |
| `static std::vector<double> createColumnMajorTransformationMatrix(const Eigen::Quaterniond&, const Eigen::Vector3d&)` | 构造列主序矩阵的辅助函数 |

```cpp
// on_init / on_configure：同时命令肘部
cartesian_pose_ = std::make_unique<diana_semantic_components::DianaCartesianPoseInterface>(
    arm_prefix, /*command_elbow_active=*/true);

// command_interface_configuration() / state_interface_configuration()
config.names = cartesian_pose_->get_command_interface_names();   // 以及 get_state_interface_names()

// on_activate()
cartesian_pose_->assign_loaned_command_interfaces(command_interfaces_);
cartesian_pose_->assign_loaned_state_interfaces(state_interfaces_);

// update()：保持初始位姿，仅移动肘部的关节 3
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

## DianaCartesianVelocityInterface

下发笛卡尔末端速度。它申请六个 `cartesian_velocity` 命令接口（`<arm_prefix>vx`、`vy`、`vz`、`wx`、`wy`、`wz`）；当 `command_elbow_active = true` 时，还会申请两个 `elbow_command` 接口和两个 `elbow_state` 状态接口。枚举 `VX, VY, VZ, WX, WY, WZ` 给出元素顺序。

| 方法 | 说明 |
| --- | --- |
| `DianaCartesianVelocityInterface(bool command_elbow_active)` 与 `DianaCartesianVelocityInterface(const std::string& arm_prefix, bool command_elbow_active)` | 构造函数，参数含义与位姿接口相同 |
| `bool setCommand(const Eigen::Vector3d& linear_velocity_command, const Eigen::Vector3d& angular_velocity_command)` | 基坐标系下的线速度（m/s）与角速度（rad/s）；肘部不得激活 |
| `bool setCommand(const Eigen::Vector3d&, const Eigen::Vector3d&, const std::array<double, 2>& elbow_command)` | 同上，带肘部；肘部必须激活 |
| `std::array<double, 2> getCommandedElbowConfiguration()` | 命令的肘部值；肘部未激活时抛出 `std::runtime_error` |
| `std::array<double, 2> getCurrentElbowConfiguration()` | 当前肘部值；肘部未激活时抛出 `std::runtime_error` |

```cpp
velocity_ = std::make_unique<diana_semantic_components::DianaCartesianVelocityInterface>(
    arm_prefix, /*command_elbow_active=*/false);

config.names = velocity_->get_command_interface_names();   // command_interface_configuration()
velocity_->assign_loaned_command_interfaces(command_interfaces_);   // on_activate()

Eigen::Vector3d linear(0.0, 0.0, 0.01);
Eigen::Vector3d angular(0.0, 0.0, 0.0);
velocity_->setCommand(linear, angular);   // update()
```

## 转换工具

`translation_utils.hpp`（命名空间 `diana_semantic_components::translation`）包含 `DianaRobotState` 使用的转换辅助函数：`errorsToMessage`、`toWrench`、`toTwist`、`toAccel`、`toPose`、`toInertia`、`toCollisionIndicators`、`toElbow` 和 `updateTimeStamps`。它位于 `src/` 目录，属于内部实现细节，不在安装的头文件之列。

```{note}
本页的代码片段改编自 `diana_ros2`，其源码沿用了 franka_ros2 的结构并带有 Franka Robotics GmbH 的版权声明（Copyright (c) 2023 Franka Robotics GmbH，Apache License 2.0）；改编部分 Copyright (c) 2026 Agile Robots SE。详见[手册概述](/about/overview.md)中的“许可证与第三方声明”。
```

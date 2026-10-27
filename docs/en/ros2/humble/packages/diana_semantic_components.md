# `diana_semantic_components`

## Installation

See [Development Setup](../development.md).

## Package Overview

`diana_semantic_components` is a C++ library (namespace `diana_semantic_components`) that wraps the raw `ros2_control` interfaces exported by [diana_hardware](diana_hardware.md) into typed classes. Controllers use these classes to read the robot state, evaluate the dynamics model, and send Cartesian pose or velocity commands, without handling interface names and element order themselves.

| Class | Header | Wraps |
| --- | --- | --- |
| `DianaSemanticComponentInterface` | `diana_semantic_component_interface.hpp` | base class with loaned state and command interface handling |
| `DianaRobotState` | `diana_robot_state.hpp` | the `robot_state` interface, converted to `diana_msgs/msg/DianaRobotState` |
| `DianaRobotModel` | `diana_robot_model.hpp` | the `robot_model` and `robot_state` interfaces, giving access to the dynamics model |
| `DianaCartesianPoseInterface` | `diana_cartesian_pose_interface.hpp` | the `cartesian_pose_command` / `cartesian_pose_state` (and elbow) interfaces |
| `DianaCartesianVelocityInterface` | `diana_cartesian_velocity_interface.hpp` | the `cartesian_velocity` (and elbow) interfaces |

```{figure} ../../../../_static/images/ros2-humble-semantic-components-en.png
:alt: Relationship between the semantic components, the hardware interfaces and the controllers that use them
:width: 100%

Where the semantic components sit: the interfaces exported by `diana_hardware` on the left, the classes of this package in the middle, and the packages and example controllers that use them on the right.
```

The package depends on `diana_hardware`, `diana_msgs`, `controller_interface`, `hardware_interface`, `urdf` and `eigen`. Headers are installed under `include/diana_semantic_components/`.

```{tip}
Use the semantic components in your controllers instead of listing raw interface names such as `diana3_joint1/position` or `0/cartesian_pose_command`. The classes build the correct names (including the arm prefix), return them in the order they expect, and check sizes and elbow usage for you.
```

## Call Flow

Whichever class you use, the pattern inside a controller is the same: construct the class during initialization or configuration, return the interface names it gives you from the interface-configuration callbacks, hand it the interfaces the controller manager lends you on activation, read and write it in every control cycle, and release the interfaces on deactivation.

```{figure} ../../../../_static/images/ros2-humble-semantic-flow-en.png
:alt: Order in which controller callbacks call the semantic component methods
:width: 80%

The order in which the controller callbacks run (left) and the semantic component methods called in each of them (right).
```

```{note}
`update()` runs in the real-time loop. Do slow work such as constructing the classes and parsing the URDF in `on_configure`, and only read and write interfaces in `update()`.
```

Each class is described below, method by method, with a complete code snippet.

## DianaSemanticComponentInterface

Base class of the two Cartesian command classes (`DianaCartesianPoseInterface`, `DianaCartesianVelocityInterface`). It is a copy of the `ros2_control` semantic component interface extended with access to command interfaces.

| Method | Description |
| --- | --- |
| `DianaSemanticComponentInterface(const std::string& name, size_t state_interface_size = 0, size_t command_interface_size = 0)` | constructor; `name` is the default prefix of generated interface names |
| `std::vector<std::string> get_state_interface_names()` | state interface names to return from `state_interface_configuration()` |
| `std::vector<std::string> get_command_interface_names()` | command interface names to return from `command_interface_configuration()` |
| `bool assign_loaned_state_interfaces(std::vector<hardware_interface::LoanedStateInterface>&)` | call in `on_activate`; orders the loaned interfaces by name |
| `bool assign_loaned_command_interfaces(std::vector<hardware_interface::LoanedCommandInterface>&)` | call in `on_activate` |
| `void release_interfaces()` | call in `on_deactivate` |
| `std::vector<double> get_values_state_interfaces() const` | current values of all assigned state interfaces |
| `std::vector<double> get_values_command_interfaces() const` | current values of all assigned command interfaces |
| `bool set_values(const std::vector<double>&)` | write all command interfaces; returns false if the size does not match |

## DianaRobotState

Derives from `semantic_components::SemanticComponentInterface<diana_msgs::msg::DianaRobotState>`. It claims one interface, `<robot_name>/robot_state`, and fills a [`DianaRobotState`](diana_msgs.md) message from it.

| Method | Description |
| --- | --- |
| `DianaRobotState(const std::string& name, const std::string& robot_description)` | `name` is the full interface name, for example `diana3/robot_state`; the robot name is taken from the part before the first `/`. Parses the URDF and throws `std::runtime_error` if parsing fails |
| `void initialize_robot_state_msg(diana_msgs::msg::DianaRobotState& message)` | sizes the arrays and sets the `frame_id` fields from the URDF links; call once on every message before filling it |
| `bool get_values_as_message(diana_msgs::msg::DianaRobotState& message)` | converts the current robot state into `message`; returns false (and logs an error) if the interface was not assigned |

This class is what [diana_robot_state_broadcaster](diana_robot_state_broadcaster.md) uses.

```cpp
// in the controller class
std::unique_ptr<diana_semantic_components::DianaRobotState> robot_state_;
diana_msgs::msg::DianaRobotState state_msg_;

// on_configure(), robot_description holds the URDF string
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

Derives from `semantic_components::SemanticComponentInterface<diana_hardware::Model>`. It claims two interfaces and exposes the dynamics model of the connected robot.

| Method | Description |
| --- | --- |
| `DianaRobotModel(const std::string& diana_model_interface_name, const std::string& diana_state_interface_name)` | the full names, for example `diana3/robot_model` and `diana3/robot_state`; the default constructor is deleted |
| `std::array<double, 49> getMassMatrix()` | 7x7 mass matrix, column-major, kg m^2 |
| `std::array<double, 7> getCoriolisForceVector()` | Coriolis force vector, Nm |
| `std::array<double, 7> getGravityForceVector()` | gravity vector, Nm |
| `std::array<double, 16> getPoseMatrix(const franka::Frame& frame)` | 4x4 pose of a frame in the base frame, column-major |
| `std::array<double, 42> getBodyJacobian(const franka::Frame& frame)` | 6x7 body Jacobian relative to the given frame, column-major |
| `std::array<double, 42> getZeroJacobian(const franka::Frame& frame)` | 6x7 Jacobian relative to the base frame, column-major |

The pointers behind the two interfaces are resolved on the first call. If the interfaces were not assigned, the methods throw `std::runtime_error`.

```cpp
// constructor of the model (names include the arm prefix)
model_ = std::make_unique<diana_semantic_components::DianaRobotModel>(
    arm_prefix + robot_type + "/robot_model", arm_prefix + robot_type + "/robot_state");

// state_interface_configuration(): returns both interface names
config.names = model_->get_state_interface_names();

// on_activate() / update() / on_deactivate()
model_->assign_loaned_state_interfaces(state_interfaces_);
std::array<double, 49> mass = model_->getMassMatrix();
std::array<double, 16> pose = model_->getPoseMatrix(franka::Frame::kEndEffector);
model_->release_interfaces();
```

## DianaCartesianPoseInterface

Commands and reads the Cartesian end-effector pose. It claims 16 `cartesian_pose_command` command interfaces and 16 `cartesian_pose_state` state interfaces (`<arm_prefix>0` ... `<arm_prefix>15`). With `command_elbow_active = true` it additionally claims the two `elbow_command` command interfaces and the two `elbow_state` state interfaces (`joint_3_position`, `joint_4_sign`).

| Method | Description |
| --- | --- |
| `DianaCartesianPoseInterface(bool command_elbow_active)` and `DianaCartesianPoseInterface(const std::string& arm_prefix, bool command_elbow_active)` | constructors; `arm_prefix` is the prefix of the interface names |
| `bool setCommand(const std::array<double, 16>& pose_command)` | column-major 4x4 pose; returns false if the elbow is active |
| `bool setCommand(const std::array<double, 16>& pose_command, const std::array<double, 2>& elbow)` | pose and elbow `[joint_3_position, joint_4_sign]`; returns false if the elbow is not active |
| `bool setCommand(const Eigen::Quaterniond& quaternion, const Eigen::Vector3d& translation)` | orientation and position; elbow must not be active |
| `bool setCommand(const Eigen::Quaterniond&, const Eigen::Vector3d&, const std::array<double, 2>& elbow_command)` | as above with elbow; elbow must be active |
| `std::array<double, 16> getCommandedPoseMatrix()` | last commanded pose |
| `std::array<double, 16> getCurrentPoseMatrix()` | current pose from the `cartesian_pose_state` interfaces |
| `std::tuple<Eigen::Quaterniond, Eigen::Vector3d> getCurrentOrientationAndTranslation()` | current pose as quaternion and translation |
| `std::tuple<Eigen::Quaterniond, Eigen::Vector3d> getCommandedOrientationAndTranslation()` | commanded pose as quaternion and translation |
| `std::array<double, 2> getCommandedElbowConfiguration()` / `getCurrentElbowConfiguration()` | elbow values; throw `std::runtime_error` if the elbow is not active |
| `static std::vector<double> createColumnMajorTransformationMatrix(const Eigen::Quaterniond&, const Eigen::Vector3d&)` | helper that builds a column-major matrix |

```cpp
// on_init / on_configure: command the elbow too
cartesian_pose_ = std::make_unique<diana_semantic_components::DianaCartesianPoseInterface>(
    arm_prefix, /*command_elbow_active=*/true);

// command_interface_configuration() / state_interface_configuration()
config.names = cartesian_pose_->get_command_interface_names();   // and get_state_interface_names()

// on_activate()
cartesian_pose_->assign_loaned_command_interfaces(command_interfaces_);
cartesian_pose_->assign_loaned_state_interfaces(state_interfaces_);

// update(): keep the initial pose, move joint 3 of the elbow
std::array<double, 16> pose = cartesian_pose_->getCurrentPoseMatrix();
std::array<double, 2> elbow = cartesian_pose_->getCurrentElbowConfiguration();
elbow[0] += delta;
if (!cartesian_pose_->setCommand(pose, elbow)) {
  return controller_interface::return_type::ERROR;
}
```

```{warning}
Commanding a Cartesian pose moves the robot. Command small, continuous changes from the current pose, with the workspace clear and the emergency stop within reach; see [Safety Boundaries](../../../reference/safety.md).
```

## DianaCartesianVelocityInterface

Commands the Cartesian end-effector velocity. It claims the six `cartesian_velocity` command interfaces (`<arm_prefix>vx`, `vy`, `vz`, `wx`, `wy`, `wz`), and with `command_elbow_active = true` also the two `elbow_command` interfaces and the two `elbow_state` state interfaces. The enum `VX, VY, VZ, WX, WY, WZ` names the element order.

| Method | Description |
| --- | --- |
| `DianaCartesianVelocityInterface(bool command_elbow_active)` and `DianaCartesianVelocityInterface(const std::string& arm_prefix, bool command_elbow_active)` | constructors, same arguments as the pose interface |
| `bool setCommand(const Eigen::Vector3d& linear_velocity_command, const Eigen::Vector3d& angular_velocity_command)` | linear (m/s) and angular (rad/s) velocity in the base frame; elbow must not be active |
| `bool setCommand(const Eigen::Vector3d&, const Eigen::Vector3d&, const std::array<double, 2>& elbow_command)` | same with elbow; elbow must be active |
| `std::array<double, 2> getCommandedElbowConfiguration()` | commanded elbow; throws `std::runtime_error` if the elbow is not active |
| `std::array<double, 2> getCurrentElbowConfiguration()` | current elbow; throws `std::runtime_error` if the elbow is not active |

```cpp
velocity_ = std::make_unique<diana_semantic_components::DianaCartesianVelocityInterface>(
    arm_prefix, /*command_elbow_active=*/false);

config.names = velocity_->get_command_interface_names();   // command_interface_configuration()
velocity_->assign_loaned_command_interfaces(command_interfaces_);   // on_activate()

Eigen::Vector3d linear(0.0, 0.0, 0.01);
Eigen::Vector3d angular(0.0, 0.0, 0.0);
velocity_->setCommand(linear, angular);   // update()
```

## Translation Utilities

`translation_utils.hpp` (namespace `diana_semantic_components::translation`) holds the conversion helpers used by `DianaRobotState`: `errorsToMessage`, `toWrench`, `toTwist`, `toAccel`, `toPose`, `toInertia`, `toCollisionIndicators`, `toElbow` and `updateTimeStamps`. It is located in the `src/` directory and is an internal implementation detail, not part of the installed headers.

```{note}
The code excerpts on this page are adapted from `diana_ros2`, whose source follows the structure of franka_ros2 and carries the Franka Robotics GmbH copyright notice (Copyright (c) 2023 Franka Robotics GmbH, Apache License 2.0); the adapted parts are Copyright (c) 2026 Agile Robots SE. See "License and Third-Party Notices" in the [Manual Overview](/about/overview.md).
```

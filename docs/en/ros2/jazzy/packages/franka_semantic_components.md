# Semantic Components

Package name: `franka_semantic_components`

## Installation

See [Development Setup](../development.md).

## Package Overview

`franka_semantic_components` is a C++ library (namespace `franka_semantic_components`) that wraps the raw `ros2_control` interfaces exported by [franka_hardware](franka_hardware.md) into typed classes. Controllers use these classes to read the robot state, evaluate the dynamics model, and send Cartesian pose or velocity commands, without handling interface names and element order themselves.

| Class | Header | Wraps |
| --- | --- | --- |
| `FrankaSemanticComponentInterface` | `franka_semantic_component_interface.hpp` | base class with loaned state and command interface handling |
| `FrankaRobotState` | `franka_robot_state.hpp` | the `robot_state` interface, converted to `franka_msgs/msg/FrankaRobotState` |
| `FrankaRobotModel` | `franka_robot_model.hpp` | the `robot_model` and `robot_state` interfaces, giving access to the dynamics model |
| `FrankaCartesianPoseInterface` | `franka_cartesian_pose_interface.hpp` | the `cartesian_pose_command` / `cartesian_pose_state` (and elbow) interfaces |
| `FrankaCartesianVelocityInterface` | `franka_cartesian_velocity_interface.hpp` | the `cartesian_velocity` (and elbow) interfaces |

The package depends on `franka_hardware`, `franka_msgs`, `controller_interface`, `hardware_interface`, `urdf` and `eigen`. Headers are installed under `include/franka_semantic_components/`.

```{tip}
Use the semantic components in your controllers instead of listing raw interface names such as `0/cartesian_pose_command`. The classes build the correct names (including `arm_prefix`), return them in the order they expect, and check sizes and elbow usage for you.
```

## FrankaSemanticComponentInterface

Base class of the Cartesian pose and velocity interfaces; it holds the loaned state and command interfaces.

| Method | Description |
| --- | --- |
| `FrankaSemanticComponentInterface(const std::string& name, size_t state_interface_size = 0, size_t command_interface_size = 0)` | Constructor; `name` prefixes the default interface names, the two sizes reserve capacity |
| `bool assign_loaned_state_interfaces(std::vector<hardware_interface::LoanedStateInterface>& state_interfaces)` | On controller activation, obtains the loaned state interfaces in the order of the declared names |
| `bool assign_loaned_command_interfaces(std::vector<hardware_interface::LoanedCommandInterface>& command_interfaces)` | Same for the command interfaces |
| `void release_interfaces()` | Releases the loaned interfaces |
| `virtual std::vector<std::string> get_state_interface_names()` | For the controller's `state_interface_configuration()`; the default generates `name/1`, `name/2`, ... |
| `virtual std::vector<std::string> get_command_interface_names()` | For the controller's `command_interface_configuration()`; the default does the same |
| `std::vector<double> get_values_state_interfaces() const` | Returns the values of all state interfaces |
| `std::vector<double> get_values_command_interfaces() const` | Returns the values of all command interfaces |
| `bool set_values(const std::vector<double>& commanded_values)` | Sets all command interfaces; returns false if the count does not match the number of loaned command interfaces |

## FrankaRobotState

Reads the `robot_state` interface and fills a `franka_msgs/msg/FrankaRobotState` message. The constructor needs the robot description (URDF), which determines the link and joint order and the frame names in the message.

| Method | Description |
| --- | --- |
| `FrankaRobotState(const std::string& name, const std::string& robot_description)` | `name` is the state interface name, of the form `<arm_prefix>_<robot_type>/robot_state`; throws if the URDF cannot be parsed |
| `bool assign_loaned_state_interfaces(std::vector<hardware_interface::LoanedStateInterface>& state_interfaces)` | Obtains the loaned interface and resolves the state buffer exported by the hardware; returns true on success |
| `void release_interfaces()` | Drops the cached state buffer pointer and releases the loaned interfaces |
| `virtual void initialize_robot_state_msg(franka_msgs::msg::FrankaRobotState& message)` | Initializes the message with the frame names from the URDF |
| `virtual bool get_values_as_message(franka_msgs::msg::FrankaRobotState& message)` | Fills the message with the current state; returns false if the state buffer cannot be resolved |

It derives from `semantic_components::SemanticComponentInterface`, so `get_state_interface_names()` returns the claimed interface name.

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

In the example, with an empty `arm_prefix` the interface name is `<robot_type>/robot_state`. [franka_robot_state_broadcaster](franka_robot_state_broadcaster.md) uses this class.

## FrankaRobotModel

Gives access to the dynamics model held by the hardware plugin through the `robot_model` and `robot_state` interfaces. All methods work on the most recently read robot state (the cache is refreshed once it is older than 1 ms); they throw a runtime error if the state interfaces are unavailable.

| Method | Description |
| --- | --- |
| `FrankaRobotModel(const std::string& franka_model_interface_name, const std::string& franka_state_interface_name)` | The two arguments are the full names of the `robot_model` and `robot_state` interfaces |
| `std::array<double, 49> getMassMatrix()` | 7x7 mass matrix, column-major, in kg·m² |
| `std::array<double, 7> getCoriolisForceVector()` | Coriolis force vector `c = C * dq`, in Nm |
| `std::array<double, 7> getGravityForceVector()` | Gravity vector, in Nm |
| `std::array<double, 16> getPoseMatrix(const franka::Frame& frame)` | 4x4 pose matrix of the given frame in the base frame, column-major |
| `std::array<double, 42> getBodyJacobian(const franka::Frame& frame)` | 6x7 body Jacobian expressed in the given frame, column-major |
| `std::array<double, 42> getZeroJacobian(const franka::Frame& frame)` | 6x7 Jacobian expressed in the base frame, column-major |

The upper three rows of a Jacobian are the linear components, the lower three the angular components.

```cpp
// on_configure(): interface names <arm_prefix>_<robot_type>/robot_model and .../robot_state
model_ = std::make_unique<franka_semantic_components::FrankaRobotModel>(
    prefix + robot_type + "/robot_model", prefix + robot_type + "/robot_state");

// state_interface_configuration(): returns the two interface names
config.names = model_->get_state_interface_names();

// on_activate() / update() / on_deactivate()
model_->assign_loaned_state_interfaces(state_interfaces_);
std::array<double, 49> mass = model_->getMassMatrix();
std::array<double, 16> pose = model_->getPoseMatrix(franka::Frame::kEndEffector);
model_->release_interfaces();
```

Here `prefix` is `arm_prefix + "_"` (an empty string when `arm_prefix` is empty).

## FrankaCartesianPoseInterface

Sends and reads the Cartesian end-effector pose. It claims 16 `cartesian_pose_command` command interfaces and 16 `cartesian_pose_state` state interfaces, named `<arm_prefix><i>/cartesian_pose_command` and `<arm_prefix><i>/cartesian_pose_state` (`i` from 0 to 15). With `command_elbow_active = true` it also claims two `elbow_command` command interfaces (`<arm_prefix>joint_3_position/elbow_command`, `<arm_prefix>joint_4_sign/elbow_command`) and two `elbow_state` state interfaces (`<arm_prefix>joint_3_position/elbow_state`, `<arm_prefix>joint_4_sign/elbow_state`). Here `arm_prefix` is concatenated as given; no underscore is added.

| Method | Description |
| --- | --- |
| `FrankaCartesianPoseInterface(bool command_elbow_active)` and `FrankaCartesianPoseInterface(const std::string& arm_prefix, bool command_elbow_active)` | Constructors; `arm_prefix` prefixes the interface names |
| `bool setCommand(const std::array<double, 16>& pose_command)` | Column-major 4x4 pose; returns false when the elbow is active |
| `bool setCommand(const std::array<double, 16>& pose_command, const std::array<double, 2>& elbow)` | Pose plus elbow `[joint_3_position, joint_4_sign]`; returns false when the elbow is not active |
| `std::array<double, 16> getCommandedPoseMatrix()` | The last commanded pose |
| `std::array<double, 16> getCurrentPoseMatrix()` | The current pose from the `cartesian_pose_state` interfaces |
| `std::tuple<Eigen::Quaterniond, Eigen::Vector3d> getCurrentOrientationAndTranslation()` | The current pose as quaternion and translation |
| `std::tuple<Eigen::Quaterniond, Eigen::Vector3d> getCommandedOrientationAndTranslation()` | The commanded pose as quaternion and translation |
| `std::array<double, 2> getCommandedElbowConfiguration()` / `getCurrentElbowConfiguration()` | Elbow values; throw `std::runtime_error` when the elbow is not active |

```cpp
// on_configure(): command the elbow as well
cartesian_pose_ = std::make_unique<franka_semantic_components::FrankaCartesianPoseInterface>(
    arm_prefix, /*command_elbow_active=*/true);

// command_interface_configuration() / state_interface_configuration()
config.names = cartesian_pose_->get_command_interface_names();   // and get_state_interface_names()

// on_activate()
cartesian_pose_->assign_loaned_command_interfaces(command_interfaces_);
cartesian_pose_->assign_loaned_state_interfaces(state_interfaces_);

// update(): hold the current pose, move only joint 3 of the elbow
std::array<double, 16> pose = cartesian_pose_->getCurrentPoseMatrix();
std::array<double, 2> elbow = cartesian_pose_->getCurrentElbowConfiguration();
elbow[0] += delta;
if (!cartesian_pose_->setCommand(pose, elbow)) {
  return controller_interface::return_type::ERROR;
}
```

```{warning}
Sending a Cartesian pose moves the robot. Command small, continuous changes relative to the current pose, keep the workspace clear of people and obstacles, and keep the emergency stop within reach; see [Safety Boundaries](../../../reference/safety.md).
```

## FrankaCartesianVelocityInterface

Sends the Cartesian end-effector velocity. It claims six `cartesian_velocity` command interfaces named `<arm_prefix><axis>/cartesian_velocity`, with `<axis>` being `vx`, `vy`, `vz`, `wx`, `wy`, `wz` in that order. With `command_elbow_active = true` it also claims two `elbow_command` command interfaces and two `elbow_state` state interfaces (named as above). The enum `VX, VY, VZ, WX, WY, WZ` gives the element order.

| Method | Description |
| --- | --- |
| `FrankaCartesianVelocityInterface(bool command_elbow_active)` and `FrankaCartesianVelocityInterface(const std::string& arm_prefix, bool command_elbow_active)` | Constructors, same meaning of the arguments as for the pose interface |
| `bool setCommand(const Eigen::Vector3d& linear_velocity_command, const Eigen::Vector3d& angular_velocity_command)` | Linear and angular velocity; returns false when the elbow is active |
| `bool setCommand(const Eigen::Vector3d&, const Eigen::Vector3d&, const std::array<double, 2>& elbow_command)` | Same with the elbow; returns false when the elbow is not active |
| `std::array<double, 2> getCommandedElbowConfiguration()` | Commanded elbow values; throws `std::runtime_error` when the elbow is not active |
| `std::array<double, 2> getCurrentElbowConfiguration()` | Current elbow values; throws `std::runtime_error` when the elbow is not active |

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
Sending a Cartesian velocity moves the robot. Start with very small velocities, keep the workspace clear of people and obstacles, and keep the emergency stop within reach; see [Safety Boundaries](../../../reference/safety.md).
```

```{note}
The code snippets on this page are adapted from `franka_ros2`, whose source carries the Franka Robotics GmbH copyright notice (Copyright (c) 2023 Franka Robotics GmbH, Apache License 2.0). See "License and Third-Party Notices" in the [Manual Overview](/about/overview.md).
```

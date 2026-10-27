# Gazebo 仿真

软件包名称：`diana_gazebo_bringup`

## 安装

请参阅 [开发准备](../development.md)。Gazebo 仿真还需要 `diana_gazebo_bringup` 在 `package.xml` 中声明的运行依赖：`ros_gz`、`sdformat_urdf`、`joint_state_publisher_gui`、`gz_ros2_control`、`ros2controlcli`，以及 `diana_gazebo_hardware`、`diana_description`、`franka_hardware` 和 `franka_example_controllers`。`rosdep install` 会安装其中来自 apt 的部分。

## 软件包概述

`diana_gazebo_bringup` 位于源码的 `diana_gazebo/` 目录下，与 `diana_gazebo_hardware` 一起构成 Jazzy 版的 Gazebo 仿真支持。它提供：

- `launch/`：启动文件 `diana.launch.py`（模型可视化）和 `diana.example_controller.launch.py`（带示例控制器的仿真）。
- `config/controllers.yaml`：各机型共用的一份控制器配置。
- `urdf/`：Gazebo 入口 xacro `diana.gazebo.urdf.xacro`，以及它包含的 `diana_gazebo_hardware_plugins.xacro` 和 `diana_gazebo_transmissions.xacro`。
- `rviz/diana.visualize.rviz`：RViz 配置。

启动文件通过 `ros_gz_sim` 的 `gz_sim.launch.py` 启动 Gazebo Sim，用 `ros_gz_sim create` 从 `/robot_description` 话题生成机器人，并通过 `ros_gz_bridge` 的 `parameter_bridge` 桥接 `/clock`，同时启动 `robot_state_publisher`、控制器和 RViz。机器人模型来自 `diana_description`，通过源码中的 `dependency.repos` 导入，参见[开发准备](../development.md)。

```{note}
Gazebo 中使用的是仿真硬件接口，而不是真实机器人的硬件接口。`gazebo_effort` 为 `true` 时使用 `diana_gazebo_hardware` 插件，见下文同名小节。
```

## 使用方法

### 模型可视化

```bash
ros2 launch diana_gazebo_bringup diana.launch.py robot_type:=diana7
```

该文件启动 Gazebo（`empty.sdf -r`，写在文件中）、`robot_state_publisher`（使用 `diana_description` 的 `robots/<robot_type>/<robot_type>.urdf.xacro`，并传入 `gazebo:=true`、`ros2_control:=true`、`connected_to:=world`）、生成机器人、RViz（`rviz/diana.visualize.rviz`，固定坐标系 `world`），并在生成进程结束后用 `ros2 control load_controller --set-state active joint_state_broadcaster` 激活 `joint_state_broadcaster`，同时启动 `joint_state_publisher`。它不加载任何运动控制器。

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `robot_type` | `diana7`（请显式传入） | `diana3`、`diana7` 或 `diana7g2`，与所用机型一致 |
| `namespace` | 空 | 生成节点、RViz 和 `joint_state_publisher` 的命名空间 |

### 带示例控制器的仿真

```bash
ros2 launch diana_gazebo_bringup diana.example_controller.launch.py robot_type:=diana7 controller:=joint_impedance_example_controller
```

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `robot_type` | `diana7`（请显式传入） | `diana3`、`diana7` 或 `diana7g2`，与所用机型一致 |
| `controller` | `gravity_compensation_example_controller` | 要启动的控制器名，取自 [franka_example_controllers](franka_example_controllers.md)，且必须在下节的 `controllers.yaml` 中配置 |
| `namespace` | 空 | 生成节点和 RViz 的命名空间 |
| `gz_args` | `-r empty.sdf` | 转发给 `gz_sim.launch.py` 的 Gazebo 参数 |
| `rviz` | `true` | 是否启动 RViz（固定坐标系 `world`） |
| `gazebo_effort` | `true` | 是否在命令接口中加入 `effort`；为 `true` 时使用 `diana_gazebo_hardware` 插件 |

该启动文件的流程：

1. 设置 `GZ_SIM_RESOURCE_PATH`（`diana_description` 所在目录的上级目录），启动 Gazebo。
2. 用 `urdf/diana.gazebo.urdf.xacro`（传入 `robot_type` 和 `gazebo_effort`）生成机器人描述并发布。
3. 生成进程结束后，用 `controller_manager spawner` 启动 `joint_state_broadcaster` 和所选控制器，参数取自 `config/controllers.yaml`。

```{important}
`controller` 必须是 `controllers.yaml` 中已注册的名称，见下节。
```

## 控制器配置

`config/controllers.yaml` 由 `diana_gazebo_hardware_plugins.xacro` 中的 `gz_ros2_control` 插件和启动文件中的 spawner 共同加载，所有机型共用这一份文件。控制器管理器更新率为 1000 Hz。该文件中与单臂仿真相关的控制器如下（类型均取自 [franka_example_controllers](franka_example_controllers.md) 和 `joint_state_broadcaster`）：

| 控制器名 | 类型 |
| --- | --- |
| `joint_state_broadcaster` | `joint_state_broadcaster/JointStateBroadcaster` |
| `joint_position_example_controller` | `franka_example_controllers/JointPositionExampleController` |
| `joint_velocity_example_controller` | `franka_example_controllers/JointVelocityExampleController` |
| `joint_impedance_example_controller` | `franka_example_controllers/JointImpedanceExampleController` |
| `gravity_compensation_example_controller` | `franka_example_controllers/GravityCompensationExampleController` |
| `model_example_controller` | `franka_example_controllers/ModelExampleController` |
| `cartesian_impedance_example_controller` | `franka_example_controllers/CartesianImpedanceExampleController` |
| `move_to_start_example_controller` | `franka_example_controllers/MoveToStartExampleController` |
| `franka_robot_state_broadcaster` | `franka_robot_state_broadcaster/FrankaRobotStateBroadcaster` |

`joint_position_example_controller` 和 `joint_velocity_example_controller` 的参数 `gazebo` 设为 `true`。

## `diana_gazebo_hardware`

`diana_gazebo_hardware` 是一个 `gz_ros2_control` 系统插件，类名 `diana_gazebo_hardware/DianaGazeboHardwareInterface`（基类 `gz_ros2_control::GazeboSimSystemInterface`，库 `diana_gz_hardware_plugins`）。它包装标准的 `gz_ros2_control/GazeboSimSystem`，把所有关节和传感器逻辑转发给它，并在此基础上增加：

- **重力补偿**：根据机器人模型（使用 `pinocchio`）在 `write()` 中把重力力矩叠加到力矩（`effort`）命令上，使力矩控制的关节在仿真中保持重力补偿。
- **模型和状态接口**：导出 `<prefix><robot_type>` 下的 `robot_model` 与 `robot_state` 状态接口，使依赖模型的控制器（如 `model_example_controller`）能在仿真中激活。该模型由 `diana_description` 的 `robots/<robot_type>/<robot_type>.urdf.xacro` 生成。
- **TCP 力/力矩接口**：导出 `<prefix><robot_type>_tcp` 的六个状态接口 `force.x`、`force.y`、`force.z`、`torque.x`、`torque.y`、`torque.z`，数据来自由测量力矩残差估计的外部力。
- **笛卡尔位姿接口**：导出 16 个 `<prefix><i>/cartesian_pose_state` 状态接口（列主序 4x4 的 `O_T_EE`）。

命令接口原样来自被包装的系统。

`diana.gazebo.urdf.xacro` 在 `gazebo_effort` 为 `true`（`diana.example_controller.launch.py` 的默认值）时使用此插件，否则使用 `gz_ros2_control/GazeboSimSystem`。

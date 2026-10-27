# Gazebo 仿真

软件包名称：`diana_gazebo_bringup`

## 安装

请参阅 [开发准备](../development.md)。使用 Gazebo 仿真前，还需要完成其中的“安装 Gazebo 仿真依赖（可选）”。

## 软件包概述

`diana_gazebo_bringup` 位于源码的 `diana_gazebo/` 目录下，与 `diana_gazebo_hardware` 一起构成 Humble 版的 Gazebo 仿真支持。它提供：

- `launch/`：两个启动文件，`visualize_diana_robot.launch.py` 和 `gazebo_diana_arm_example_controller.launch.py`。
- `config/`：三个机型的控制器配置 `diana3_gazebo_controllers.yaml`、`diana7_gazebo_controllers.yaml`、`diana7g2_gazebo_controllers.yaml`。
- `urdf/`：`diana_arm.gazebo.xacro`（Gazebo 入口 xacro）。

启动文件通过 `ros_gz_sim` 启动 Gazebo（Humble 对应 Ignition Fortress），用 `ros_gz_sim create` 从 `/robot_description` 话题生成机器人，并启动 `robot_state_publisher`、控制器和 RViz。机器人模型来自外部软件包 `diana_description`，通过源码中的 `dependency.repos` 导入，参见[开发准备](../development.md)。

```{note}
Gazebo 中使用的是仿真硬件接口，而不是真实机器人的 `diana_hardware`。`gazebo_effort` 为 `true` 时会使用 `diana_gazebo_hardware` 插件，见下文同名小节。
```

```{figure} ../../../../_static/images/ros2-humble-gazebo-launch-zh.png
:alt: 带示例控制器的 Gazebo 仿真启动结构
:width: 70%

`gazebo_diana_arm_example_controller.launch.py` 启动的内容及其关系。
```

## 使用方法

### 模型可视化

```bash
ros2 launch diana_gazebo_bringup visualize_diana_robot.launch.py robot_type:=diana7
```

该文件启动 Gazebo（`empty.sdf -r`，写死在文件中）、`robot_state_publisher`（使用 `diana_description` 的 `robots/<robot_type>/<robot_type>.urdf.xacro`，并传入 `gazebo:=true`）、生成机器人、RViz（`diana_description` 的 `rviz/visualize_diana.rviz`，固定坐标系 `base_link`），并在生成完成后用 `ros2 control load_controller` 激活 `joint_state_broadcaster`，同时启动 `joint_state_publisher`。它不加载任何运动控制器。

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `robot_type` | 必填 | `diana3`、`diana7` 或 `diana7g2`，与所用机型一致 |
| `namespace` | 空 | 生成节点和 RViz 的命名空间 |

### 带示例控制器的仿真

```bash
ros2 launch diana_gazebo_bringup gazebo_diana_arm_example_controller.launch.py robot_type:=diana7 controller:=joint_impedance_example_controller
```

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `robot_type` | 必填 | `diana3`、`diana7` 或 `diana7g2`，与所用机型一致，决定使用的 `config/<robot_type>_gazebo_controllers.yaml` |
| `controller` | `gravity_compensation_example_controller` | 要启动的控制器名，取自 [diana_example_controllers](diana_example_controllers.md)，且必须在下节的 yaml 中配置 |
| `namespace` | 空 | 仅用于 RViz 节点的命名空间 |
| `gz_args` | `empty.sdf -r` | 转发给 `gz_sim.launch.py` 的 Gazebo 参数 |
| `rviz` | `true` | 是否启动 RViz（固定坐标系 `world`） |

```{figure} ../../../../_static/images/ros2-humble-gazebo-diana7-joint-impedance.png
:alt: diana7 在 Gazebo 和 RViz 中运行关节阻抗示例控制器
:width: 100%

`diana7` 运行 `joint_impedance_example_controller` 的画面：Gazebo（左）和 RViz（右）。Gazebo 的实体树中可以看到 `ground_plane`、`sun` 和 `diana7`。
```

该启动文件的流程：

1. 设置 `GZ_SIM_RESOURCE_PATH`（`diana_description` 的上级目录和本包的共享目录），启动 Gazebo。
2. 用 `urdf/diana_arm.gazebo.xacro`（`gazebo:=true`、`gazebo_effort:=true`）生成机器人描述并发布。
3. 生成机器人后，用 `controller_manager spawner` 启动 `joint_state_broadcaster` 和所选控制器，参数取自对应的 yaml。
4. 关闭时向 `ruby` 进程发送 `SIGINT`，以便 Gazebo 正常退出。

```{important}
`controller` 必须是上述 yaml 中已注册的名称；`diana_robot_state_broadcaster`、各类 `*_move_to_start` 控制器等没有在这些 yaml 中配置。
```

## 控制器配置

`config/<robot_type>_gazebo_controllers.yaml` 由 `diana_arm.gazebo.xacro` 中的 `gz_ros2_control` 插件和启动文件中的 spawner 共同加载。三个文件结构相同，控制器管理器更新率均为 1000 Hz，并注册了以下控制器：

| 控制器名 | 类型 |
| --- | --- |
| `joint_state_broadcaster` | `joint_state_broadcaster/JointStateBroadcaster` |
| `joint_position_example_controller` | `diana_example_controllers/JointPositionExampleController` |
| `joint_velocity_example_controller` | `diana_example_controllers/JointVelocityExampleController` |
| `joint_impedance_example_controller` | `diana_example_controllers/JointImpedanceExampleController` |
| `gravity_compensation_example_controller` | `diana_example_controllers/GravityCompensationExampleController` |
| `model_example_controller` | `diana_example_controllers/ModelExampleController` |

各机型的差异：

- `robot_type` 参数分别设为 `diana3`、`diana7`、`diana7g2`（用于 `joint_position_example_controller`、`joint_velocity_example_controller`、`joint_impedance_example_controller` 和 `model_example_controller`）；位置和速度控制器另有 `gazebo: true`，`model_example_controller` 另有 `arm_prefix: ''`。
- `joint_impedance_example_controller` 的刚度和阻尼增益（关节 1 至 7）：

| 机型 | `k_gains` | `d_gains` |
| --- | --- | --- |
| `diana3` | 24, 24, 24, 24, 10, 6, 2 | 2, 2, 2, 1, 1, 1, 0.5 |
| `diana7` | 48, 48, 48, 48, 20, 16, 12 | 4, 4, 4, 2, 2, 2, 1.5 |
| `diana7g2` | 48, 48, 48, 48, 20, 16, 12 | 4, 4, 4, 2, 2, 2, 1.5 |

## `diana_gazebo_hardware`

`diana_gazebo_hardware` 是一个 `gz_ros2_control` 系统插件，类名 `diana_gazebo_hardware/DianaGazeboHardwareInterface`（基类 `gz_ros2_control::GazeboSimSystemInterface`，库 `diana_gz_hardware_plugins`）。它包装标准的 `gz_ros2_control/GazeboSimSystem`，把所有关节和传感器逻辑转发给它，并在此基础上增加：

- **重力补偿**：用 `pinocchio` 根据 URDF 建立模型，在 `write()` 中把重力力矩叠加到力矩（`effort`）命令上，使力矩控制的关节在仿真中保持重力补偿。
- **模型和状态接口**：导出 `<prefix><robot_type>` 下的 `robot_model` 与 `robot_state` 状态接口，使依赖模型的控制器（如 `model_example_controller`）能在仿真中激活。
- **TCP 力/力矩接口**：导出 `<prefix><robot_type>_tcp` 的六个状态接口 `force.x`、`force.y`、`force.z`、`torque.x`、`torque.y`、`torque.z`，数据来自由测量力矩残差估计的外部力。
- **笛卡尔位姿接口**：导出 16 个 `<prefix><i>/cartesian_pose_state` 状态接口（列主序 4x4 的 `O_T_EE`）。

命令接口原样来自被包装的系统。

`diana_arm.gazebo.xacro` 在 `gazebo_effort` 为 `true`（`gazebo_diana_arm_example_controller.launch.py` 的设置）时使用此插件，否则使用 `gz_ros2_control/GazeboSimSystem`。

# 启动与运行配置

软件包名称：`diana_bringup`

## 安装

请参阅 [开发准备](../development.md)。

## 软件包概述

`diana_bringup` 提供启动 Diana 机械臂 ROS 2 控制栈所需的 launch 文件、控制器参数文件和 URDF 入口。它把 `diana_description`（机器人模型）、`franka_hardware`（`ros2_control` 硬件接口）、`franka_robot_state_broadcaster` 以及 `franka_example_controllers` 组合到一起，并支持带命名空间的启动。

包安装 `config`、`launch`、`urdf`、`rviz` 四个目录，并提供 Python 模块 `diana_bringup.launch_utils`（读取 YAML、解析逗号分隔参数和字符串列表）。

| 文件 | 作用 |
| --- | --- |
| `launch/diana.launch.py` | 启动单台机械臂的核心节点（见“单臂启动文件”一节） |
| `launch/diana.example_controllers.launch.py` | 读取机器人配置文件，为其中每台机器人包含 `diana.launch.py` 并加载示例控制器 |
| `launch/diana_duo.launch.py` | 双臂（Diana Duo）启动文件 |
| `config/controllers.yaml` | `ros2_control` 控制器类型与参数 |
| `config/diana.config.yaml` | 单臂机器人配置文件示例 |
| `config/diana_duo.config.yaml` | 双臂机器人配置文件示例 |
| `urdf/diana.urdf.xacro`、`urdf/diana_duo.urdf.xacro` | 在 `diana_description` 的模型之上叠加 `ros2_control` 硬件描述的 xacro 入口 |
| `rviz/diana.visualize.rviz`、`rviz/diana_duo.visualize.rviz` | RViz 显示配置 |

`urdf/diana.urdf.xacro` 根据 `use_fake_hardware` 选择硬件插件：为 `true` 时使用 `franka_hardware` 提供的模拟硬件插件，否则使用真实硬件插件并传入 `robot_ip`。

```{warning}
本页的命令在 `use_fake_hardware` 为 `false` 时会连接真实机械臂并可能使其运动。运行前请确认工作空间内无人员和障碍物、急停可随时触及、机器人已处于允许外部控制的状态，并先阅读[安全边界](../../../reference/safety.md)。FCI 与网络相关前提见 [FCI 概览](../../../fci/overview.md) 与[网络配置](../../../programming/network.md)。
```

## 单臂启动文件

`diana.launch.py` 为一台机械臂启动 `robot_state_publisher`、`ros2_control_node`、`joint_state_publisher` 和基础广播器。它根据 `urdf/diana.urdf.xacro` 生成 `robot_description`，并用 `controllers_yaml` 指定的文件作为 `ros2_control_node` 的参数文件。

### 启动参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `robot_type` | 必填（请显式传入） | 机械臂型号，取值 `diana3`、`diana7`、`diana7g2`，须与所用机型一致 |
| `robot_ip` | 必填（请显式传入） | 机器人的主机名或 IP 地址；Diana 控制器 A 网口的默认地址为 `192.168.10.75` |
| `arm_prefix` | 空字符串 | 机械臂名称前缀 |
| `namespace` | 空字符串 | 所有节点所在的命名空间 |
| `use_fake_hardware` | `false` | 是否使用模拟硬件 |
| `fake_sensor_commands` | `false` | 模拟硬件的传感器命令选项 |
| `joint_state_rate` | `30` | `joint_state_publisher` 的发布频率（Hz） |
| `load_franka_robot_state_broadcaster` | `true` | 是否在真实硬件下加载 `franka_robot_state_broadcaster` |
| `controllers_yaml` | `diana_bringup` 的 `config/controllers.yaml` | 控制器参数文件，可替换为自己的文件 |

使用真实硬件：

```bash
ros2 launch diana_bringup diana.launch.py robot_type:=diana3 robot_ip:=192.168.10.75
```

不连接机器人、使用模拟硬件：

```bash
ros2 launch diana_bringup diana.launch.py robot_type:=diana3 robot_ip:=192.168.10.75 use_fake_hardware:=true
```

### 启动的节点

`diana.launch.py` 在给定的 `namespace` 下启动：

| 启动项 | 说明 |
| --- | --- |
| `robot_state_publisher` | 发布 `robot_description` 与 TF |
| `ros2_control_node`（`controller_manager`） | 加载硬件接口并运行控制器，参数除 `controllers_yaml` 外还有 `robot_type` 和 `arm_prefix`；该进程退出时整个 launch 随之关闭 |
| `joint_state_publisher` | 以 `joint_state_rate` 发布汇总后的 `joint_states`，数据源为 `diana/joint_states` |
| `spawner joint_state_broadcaster` | 加载并激活 `joint_state_broadcaster`，其 `joint_states` 被重映射为 `diana/joint_states` |
| `spawner franka_robot_state_broadcaster` | 加载并激活 `franka_robot_state_broadcaster`；仅当 `load_franka_robot_state_broadcaster` 为 `true` 且 `use_fake_hardware` 不为 `true` 时启动 |

`spawner` 只负责加载并激活控制器，完成后就退出，因此 `ros2 node list` 中看到的是被加载的控制器节点而不是 `spawner`。`diana.launch.py` 不加载示例控制器，示例控制器由下一节的 launch 文件加载。控制器的名称与类型见“控制器配置文件”一节，广播器的说明见 [franka_robot_state_broadcaster](franka_robot_state_broadcaster.md)。

使用真实硬件时，`franka_hardware` 还会在 `ros2_control_node` 进程中创建 `service_server` 和 `action_server` 两个节点，见“非实时机器人参数设置”一节。

用下面的命令查看当前已加载的控制器及其状态：

```bash
ros2 control list_controllers
```

```{important}
`franka_hardware` 在同一时刻只按一种控制模式工作。切换到不同模式的控制器前，先停用当前控制器。各接口的说明见 [franka_hardware](franka_hardware.md)。
```

```{figure} ../../../../_static/images/ros2-jazzy-bringup-launch-zh.png
:alt: 示例控制器启动文件的启动结构
:width: 100%

`diana.example_controllers.launch.py` 读取机器人配置文件，为每台机器人包含一次 `diana.launch.py`，再加载所指定的控制器；虚线框内的项只在对应条件满足时启动。
```

### 命名空间

`namespace` 参数同时作用于 `robot_state_publisher`、`ros2_control_node`、`joint_state_publisher` 和各个 `spawner`，因此话题、服务以及 controller manager 都位于该命名空间下。默认的空字符串表示不使用命名空间。

| 对象 | 不带命名空间 | 带命名空间（以 `NS_1` 为例） |
| --- | --- | --- |
| controller manager | `/controller_manager` | `/NS_1/controller_manager` |
| 汇总后的关节状态话题 | `/joint_states` | `/NS_1/joint_states` |

带命名空间启动时，`ros2 control` 命令需要用 `-c` 指定对应的 controller manager，例如：

```bash
ros2 control list_controllers -c /NS_1/controller_manager
```

## 示例控制器启动文件

`diana.example_controllers.launch.py` 读取一个 YAML 机器人配置文件，为其中的每台机器人包含一次 `diana.launch.py`，并为每台机器人用 `spawner` 加载一个由 `controller_names` 指定的控制器。命令行参数无法区分不同机器人，因此多机器人和命名空间场景应使用这个文件。

### 示例控制器启动参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `robot_config_file` | `diana.config.yaml` | 机器人配置文件。只给文件名时在 `diana_bringup` 的 `config` 目录中查找，也可以给完整路径 |
| `controller_names` | 无（必须在命令行给出） | 逗号分隔的控制器名称，必须是 `controllers.yaml` 中声明的名称 |
| `robot_ips` | 空字符串 | 逗号分隔的 IP 列表；非空时覆盖配置文件中的 `robot_ip` |

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
  robot_ips:=192.168.10.75 \
  controller_names:=gravity_compensation_example_controller
```

`robot_type` 不是命令行参数，而是取自配置文件中每台机器人的 `robot_type` 字段，请先把它改成与实际机型一致的值。名称中含有 `controller` 的控制器会以 `--controller-manager-timeout 30` 的方式由 `spawner` 加载，参数取自 `diana_bringup` 的 `config/controllers.yaml`。各控制器的用途与前提见 [franka_example_controllers](franka_example_controllers.md)。

```{warning}
示例控制器会让机械臂运动或输出力矩。使用真实硬件前请确认净空和急停，并让机械臂处于适合运行该示例的姿态；配置文件中 `use_fake_hardware` 为 `"true"` 时不会连接真实机器人。
```

### 机器人配置文件

配置文件的顶层键是机器人的任意标识（如 `ROBOT1`），每个条目描述一台机器人。`diana.config.yaml` 中的条目如下，各字段会被传给 `diana.launch.py`：

| 字段 | 默认值 | 说明 |
| --- | --- | --- |
| `robot_type` | `"diana7"` | 机械臂型号，取值 `diana3`、`diana7`、`diana7g2` |
| `arm_prefix` | `""` | 名称前缀 |
| `fake_sensor_commands` | `"false"` | 模拟传感器命令 |
| `joint_state_rate` | `30` | 关节状态发布频率（Hz） |
| `namespace` | `""` | 该机器人的命名空间；多机器人时必须各不相同 |
| `robot_ip` | `"192.168.10.75"` | 机器人 IP 或主机名 |
| `use_fake_hardware` | `"true"` | 是否使用模拟硬件；连接真实机器人时改为 `"false"` |
| `use_rviz` | `"true"` | 为 `"true"` 时启动 RViz |

任一条目的 `use_rviz` 为 `"true"` 时，该 launch 文件会启动一个 `rviz2` 实例（配置为 `diana_bringup` 的 `rviz/diana.visualize.rviz`），多个机器人共用这一个实例。自定义配置文件时，请以 `diana.config.yaml` 为模板复制，并保留其中的全部字段。多机器人时在文件中增加条目，并为每台机器人设置不同的 `namespace` 和各自的 `robot_ip`。使用自定义配置文件：

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
  robot_config_file:=/path/to/my_robots.config.yaml \
  controller_names:=gravity_compensation_example_controller
```

### 控制器名称与机器人 IP 列表

`controller_names` 与 `robot_ips` 都是逗号分隔的列表，按配置文件中机器人的顺序一一对应：

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
  robot_ips:=<robot-ip-1>,<robot-ip-2> \
  controller_names:=gravity_compensation_example_controller,joint_impedance_example_controller
```

规则如下（见 `diana_bringup.launch_utils.get_parameter_for_config`）：

- 列表长度等于机器人数量时，第 N 个值用于第 N 个机器人；
- 长度不等时会打印警告，并对所有机器人使用第一个值；
- `robot_ips` 为空时使用配置文件中的 `robot_ip`；
- `controller_names` 为空会直接退出。

## 双臂启动文件

`diana_duo.launch.py` 用于 Diana Duo 双臂配置。它根据 `urdf/diana_duo.urdf.xacro` 为两台机械臂各生成一个 `ros2_control` 硬件组件，并在 `namespace` 下启动 `robot_state_publisher`、`ros2_control_node`、`joint_state_publisher`、`joint_state_broadcaster` 的 `spawner` 以及一个控制器的 `spawner`。双臂配置不启动 `franka_robot_state_broadcaster`。

### 双臂启动参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `robot_config_file` | `diana_bringup` 的 `config/diana_duo.config.yaml` | 双臂配置文件；只给文件名时在 `config` 目录中查找 |
| `controllers_yaml` | `diana_bringup` 的 `config/controllers.yaml` | 控制器参数文件 |
| `controller_name` | 请显式传入 | 要加载的控制器名称，双臂只支持加载一个；使用 `controllers.yaml` 中声明的 `diana_duo_joint_impedance_example_controller` |

```bash
ros2 launch diana_bringup diana_duo.launch.py \
  controller_name:=diana_duo_joint_impedance_example_controller
```

机器人型号、IP 和前缀都取自配置文件，而不是命令行参数。

```{warning}
`diana_duo_joint_impedance_example_controller` 会让两台机械臂输出力矩并运动。使用真实硬件前请确认两台机械臂周围的净空和急停，并确认配置文件中的 `use_fake_hardware` 为 `"false"`。
```

### 双臂配置文件

`diana_duo.config.yaml` 只有一个条目，必须包含 `robot_types`、`robot_ips`、`arm_prefixes` 三个字符串列表，三者长度必须相同，`arm_prefixes` 中的前缀不能重复，否则 launch 会报错退出。`urdf/diana_duo.urdf.xacro` 按顺序为第 0、1 台机械臂读取这三个列表的对应元素，并在各自的前缀后追加 `_`。

| 字段 | 默认值 | 说明 |
| --- | --- | --- |
| `robot_types` | `"['diana7','diana7']"` | 两台机械臂的型号，取值 `diana3`、`diana7`、`diana7g2` |
| `arm_prefixes` | `"['left','right']"` | 两台机械臂的前缀 |
| `robot_ips` | 两个 IP 的列表 | 两台机器人各自的 IP；第一项默认 `192.168.10.75`，请按实际填写两台机器人的地址 |
| `use_fake_hardware` | `"true"` | 是否使用模拟硬件；连接真实机器人时改为 `"false"` |
| `fake_sensor_commands` | `"false"` | 模拟传感器命令 |
| `joint_state_rate` | `1000` | 关节状态发布频率（Hz） |
| `namespace` | `""` | 命名空间 |
| `thread_priority` | `98` | 硬件接口的线程优先级 |

## 控制器配置文件

`config/controllers.yaml` 声明 `controller_manager` 的参数和各控制器的类型与参数。`diana.launch.py` 和 `diana_duo.launch.py` 把它作为 `ros2_control_node` 的参数文件，示例控制器的 `spawner` 也使用它。

`controller_manager` 的通用参数：`update_rate` 为 `1000`，`thread_priority` 为 `97`，`overruns` 下的 `manage` 与 `print_warnings` 均为 `false`。

声明了类型的控制器：

| 控制器名称 | 类型 |
| --- | --- |
| `joint_state_broadcaster` | `joint_state_broadcaster/JointStateBroadcaster` |
| `franka_robot_state_broadcaster` | `franka_robot_state_broadcaster/FrankaRobotStateBroadcaster` |
| `gravity_compensation_example_controller` | `franka_example_controllers/GravityCompensationExampleController` |
| `joint_impedance_example_controller` | `franka_example_controllers/JointImpedanceExampleController` |
| `joint_impedance_with_ik_example_controller` | `franka_example_controllers/JointImpedanceWithIKExampleController` |
| `cartesian_impedance_example_controller` | `franka_example_controllers/CartesianImpedanceExampleController` |
| `cartesian_pose_example_controller` | `franka_example_controllers/CartesianPoseExampleController` |
| `cartesian_velocity_example_controller` | `franka_example_controllers/CartesianVelocityExampleController` |
| `cartesian_orientation_example_controller` | `franka_example_controllers/CartesianOrientationExampleController` |
| `elbow_example_controller` | `franka_example_controllers/ElbowExampleController` |
| `cartesian_elbow_example_controller` | `franka_example_controllers/CartesianElbowExampleController` |
| `joint_position_example_controller` | `franka_example_controllers/JointPositionExampleController` |
| `joint_velocity_example_controller` | `franka_example_controllers/JointVelocityExampleController` |
| `model_example_controller` | `franka_example_controllers/ModelExampleController` |
| `move_to_start_example_controller` | `franka_example_controllers/MoveToStartExampleController` |
| `diana_duo_joint_impedance_example_controller` | `franka_example_controllers/DianaDuoJointImpedanceExampleController` |

文件中带有参数的控制器：

| 控制器 | 参数 |
| --- | --- |
| `joint_impedance_example_controller` | `k_gains`（`24.0, 24.0, 24.0, 24.0, 10.0, 6.0, 2.0`）、`d_gains`（`2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 0.5`） |
| `joint_impedance_with_ik_example_controller` | `k_gains`（`600.0, 600.0, 600.0, 600.0, 250.0, 150.0, 50.0`）、`d_gains`（`30.0, 30.0, 30.0, 30.0, 10.0, 10.0, 5.0`） |
| `move_to_start_example_controller` | `k_gains` 与 `d_gains`，取值与 `joint_impedance_with_ik_example_controller` 相同 |
| `franka_robot_state_broadcaster` | `convenience_publish_rate`（`1000`）；`state_interfaces` 为 `robot_state` |
| `diana_duo_joint_impedance_example_controller` | `update_rate`（`1000`）、`k_gains` 与 `d_gains`，取值与 `joint_impedance_example_controller` 相同 |

只有被 `spawner` 加载的控制器才会出现在 controller manager 中。要换用另一个控制器，先停止当前的 launch，再用另一个 `controller_names` 重新启动。各控制器的用途与前提见 [franka_example_controllers](franka_example_controllers.md)。

## 非实时机器人参数设置

使用真实硬件接口（`use_fake_hardware` 为 `false`）时，`franka_hardware` 在 `ros2_control_node` 进程中创建名为 `service_server` 的节点，提供下列非实时参数服务，类型均在 [franka_msgs](franka_msgs.md) 中定义。下表按节点相对名称列出；带命名空间启动时请以 `ros2 service list` 的实际输出为准。

### 服务列表

| 服务 | 类型 | 请求字段 |
| --- | --- | --- |
| `service_server/set_joint_stiffness` | `franka_msgs/srv/SetJointStiffness` | `joint_stiffness`（7 个值） |
| `service_server/set_cartesian_stiffness` | `franka_msgs/srv/SetCartesianStiffness` | `cartesian_stiffness`（x, y, z, roll, pitch, yaw，6 个值，在刚度坐标系方向上生效） |
| `service_server/set_tcp_frame` | `franka_msgs/srv/SetTCPFrame` | `transformation`（4x4 列主序矩阵，共 16 个值） |
| `service_server/set_stiffness_frame` | `franka_msgs/srv/SetStiffnessFrame` | `transformation`（4x4 列主序矩阵，共 16 个值） |
| `service_server/set_force_torque_collision_behavior` | `franka_msgs/srv/SetForceTorqueCollisionBehavior` | 名义力矩（7 个值）与名义力（6 个值）的上下阈值 |
| `service_server/set_full_collision_behavior` | `franka_msgs/srv/SetFullCollisionBehavior` | 加速度阶段与名义阶段的力矩（7 个值）、力（6 个值）上下阈值 |
| `service_server/set_load` | `franka_msgs/srv/SetLoad` | `mass`、`center_of_mass`（3 个值）、`load_inertia`（3x3 列主序，9 个值） |

所有服务的响应都是 `bool success` 与 `string error`。

```{warning}
负载、坐标系变换和碰撞阈值直接影响机器人的力矩估计与保护停止行为。请按实际工装设置，并在更改后以保守的速度重新验证。
```

### 错误恢复动作

`franka_hardware` 还在同一进程中创建名为 `action_server` 的节点，提供动作 `action_server/error_recovery`（类型 `franka_msgs/action/ErrorRecovery`，目标、结果和反馈均为空）。收到目标后它调用 `robot->automaticErrorRecovery()`：成功则目标成功，抛出 Franka 异常则目标被中止并在日志中记录错误。命名空间的处理与上节服务相同。

```bash
ros2 action send_goal /action_server/error_recovery franka_msgs/action/ErrorRecovery {}
```

```{important}
自动错误恢复只是清除机器人当前的可恢复错误，不能代替查明停止原因。发生碰撞、保护停止等安全相关停止时，先确认现场安全，再执行恢复，参见[安全边界](../../../reference/safety.md)。
```

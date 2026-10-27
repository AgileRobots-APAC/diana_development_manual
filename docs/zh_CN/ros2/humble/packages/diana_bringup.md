# 启动与运行配置

软件包名称：`diana_bringup`

`diana_bringup` 提供启动 Diana 机械臂 ROS 2 控制栈所需的 launch 文件、控制器配置和 URDF 入口。它把 `diana_description`（机器人模型）、`diana_hardware`（`ros2_control` 硬件接口）、`diana_robot_state_broadcaster` 以及 `diana_example_controllers` 组合到一起，并支持带命名空间的多机器人启动。

## 安装

请参阅 [开发准备](../development.md)。

## 软件包概述

`diana_bringup` 安装 `config`、`launch`、`urdf` 三个目录，并提供 Python 模块 `diana_bringup.launch_utils`（读取 YAML、解析逗号分隔参数）。

核心 launch 文件是 `diana.launch.py`：它根据 `urdf/diana_arm.urdf.xacro` 生成 `robot_description`，启动 `ros2_control` 控制栈并拉起基础广播器。该 xacro 在 `diana_description` 的机器人模型之上叠加 `diana_hardware` 的 `ros2_control` 描述：`use_fake_hardware` 为 `true` 时使用 `mock_components/GenericSystem`，否则使用 `diana_hardware/DianaHardwareInterface` 并传入 `robot_ip`。

```{warning}
本页的命令在 `use_fake_hardware` 为 `false` 时会连接真实机械臂并可能使其运动。运行前请确认工作空间内无人员和障碍物、急停可随时触及、机器人已处于允许外部控制的状态，并先阅读[安全边界](../../../reference/safety.md)。FCI 与网络相关前提见 [FCI 概览](../../../fci/overview.md) 与[网络配置](../../../programming/network.md)。
```

### 启动参数

`diana.launch.py` 的全部启动参数及其在源码中的实际默认值如下：

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `robot_type` | 必填 | 机械臂型号（xacro 参数 `robot_type`，对应 `diana_description` 中的机器人目录），取值 `diana3`、`diana7`、`diana7g2`，与所用机型一致 |
| `arm_prefix` | 空字符串 | 关节、接口和 TF 名称的前缀 |
| `namespace` | 空字符串 | 所有节点所在的命名空间 |
| `robot_ip` | `192.168.10.75` | 机器人的主机名或 IP 地址 |
| `use_fake_hardware` | `false` | 是否使用 `mock_components` 的模拟硬件 |
| `fake_sensor_commands` | `false` | 模拟硬件的 `mock_sensor_commands` 选项 |
| `joint_state_rate` | `30` | `joint_state_publisher` 的发布频率（Hz） |
| `controllers_yaml` | `diana_bringup` 的 `config/controllers.yaml` | 控制器参数文件，可替换为自己的文件 |

启动示例（`<robot-ip>` 替换为实际地址）：

```bash
ros2 launch diana_bringup diana.launch.py robot_type:=diana3 robot_ip:=<robot-ip>
```

不连接机器人、使用模拟硬件：

```bash
ros2 launch diana_bringup diana.launch.py robot_type:=diana3 use_fake_hardware:=true
```

### 启动的节点

`diana.launch.py` 在给定的 `namespace` 下启动：

| 启动项 | `ros2 node list` 中的节点 | 说明 |
| --- | --- | --- |
| `robot_state_publisher` | `/robot_state_publisher` | 发布 `robot_description` 与 TF |
| `ros2_control_node` | `/controller_manager` | 加载硬件接口并运行控制器；`joint_states` 被重映射为 `diana/joint_states`；该进程退出时整个 launch 会随之关闭 |
| `joint_state_publisher` | `/joint_state_publisher` | 汇总 `diana/joint_states`，以 `joint_state_rate` 发布 `joint_states` |
| `spawner joint_state_broadcaster` | `/joint_state_broadcaster`（控制器节点） | 加载并激活 `joint_state_broadcaster` |
| `spawner diana_robot_state_broadcaster` | `/diana_robot_state_broadcaster`（控制器节点） | 加载并激活 `diana_robot_state_broadcaster`；仅在 `use_fake_hardware` 不为 `true` 时启动 |

`spawner` 只负责加载并激活控制器，完成后就退出，所以节点列表里看不到 `spawner`，能看到的是被它加载的控制器节点。

`ros2_control_node` 的参数文件来自 `controllers_yaml`，另外还会收到 `robot_type` 和 `arm_prefix` 参数。控制器名称与类型的对应关系见 [diana_example_controllers](diana_example_controllers.md)，机器人状态广播器见 [diana_robot_state_broadcaster](diana_robot_state_broadcaster.md)。

启动后用下面的命令查看节点：

```bash
ros2 node list
```

使用模拟硬件（`use_fake_hardware:=true`）时，应当看到：

```text
/controller_manager
/joint_state_broadcaster
/joint_state_publisher
/robot_state_publisher
```

使用真实硬件时，还会多出 `/diana_robot_state_broadcaster`，以及 `diana_hardware` 创建的 `/service_server` 和 `/action_server`。带命名空间启动时，这些节点名前面都带有该命名空间，例如用 `diana.config.yaml` 默认的 `NS_1` 启动时是 `/NS_1/service_server`；只有 `rviz2` 例外，它只启动一个实例，不在命名空间下。

### 启动控制器与查看状态

`diana.launch.py` 只启动广播器（`joint_state_broadcaster` 和 `diana_robot_state_broadcaster`），不加载示例控制器。示例控制器由 `example.launch.py` 通过 `spawner` 加载：`controllers.yaml` 声明了所有控制器的类型，但只有 `controller_names` 里指定的控制器会被加载并激活。没有被指定的控制器不会出现在 controller manager 中，因此不能在运行中直接切换到它们。要换一个控制器，先停止当前的 launch，再用另一个 `controller_names` 重新启动。

用下面的命令查看当前已加载的控制器及其状态：

```bash
ros2 control list_controllers
```

如果机器人启动在命名空间下，需要用 `-c` 指定对应的 controller manager，例如 `ros2 control list_controllers -c /NS_1/controller_manager`。

```{important}
`diana_hardware` 在同一时刻只按一种控制模式工作：力矩（effort）、关节速度、关节位置、笛卡尔位姿、笛卡尔速度（后两者可附带肘部指令）。切换到不同模式的控制器前，先停用当前控制器。肘部指令接口必须与笛卡尔位姿或笛卡尔速度接口同时被占用，否则硬件接口会报错。
```

## 带命名空间的启动文件

`example.launch.py` 读取一个 YAML 配置文件，为其中的每个机器人包含一次 `diana.launch.py`，并为每个机器人启动一个由 `controller_names` 指定的控制器。它适合多机器人和命名空间场景，因为命令行参数无法区分不同机器人。

```{figure} ../../../../_static/images/ros2-humble-bringup-launch-zh.png
:alt: example.launch.py 与 diana.launch.py 启动的节点
:width: 100%

`example.launch.py` 的启动结构：读取配置文件，为每个机器人包含一次 `diana.launch.py`，再加载 `controller_names` 指定的控制器。
```

| 启动参数 | 默认值 | 说明 |
| --- | --- | --- |
| `robot_config_file` | `diana_bringup` 的 `config/diana.config.yaml` | 机器人配置文件路径 |
| `robot_ips` | 空字符串 | 逗号分隔的 IP 列表；非空时覆盖配置文件中的 `robot_ip` |
| `controller_names` | 无（必须在命令行给出） | 逗号分隔的控制器名称，必须是 `controllers.yaml` 中声明的名称 |

```bash
ros2 launch diana_bringup example.launch.py \
  controller_names:=gravity_compensation_example_controller
```

控制器会以 `--controller-manager-timeout 30` 的方式由 `spawner` 加载，参数取自 `controllers.yaml`。各控制器的用途与前提见 [diana_example_controllers](diana_example_controllers.md)。

```{warning}
示例控制器会让机械臂运动或输出力矩。使用真实硬件前请确认净空和急停，并让机械臂处于适合运行该示例的姿态；多数示例需要真实的 `diana_hardware` 接口，不能在模拟硬件下运行，详见 [diana_example_controllers](diana_example_controllers.md)。
```

### `diana.config.yaml` 字段

默认的 `config/diana.config.yaml` 只启用一个机器人 `ROBOT1`，顶层键（`ROBOT1`、`ROBOT2` 等）只是任意的助记标识。布尔值必须加引号（`"true"` / `"false"`）。每个机器人条目包含下列字段，`example.launch.py` 对这些字段都是直接取值，缺少任意一个都会报错：

| 字段 | 默认文件中的值 | 说明 |
| --- | --- | --- |
| `robot_type` | `"diana3"` | 机械臂型号，传给 `diana.launch.py`；`diana3` 只是示例值，请改成自己的机型（`diana3`、`diana7` 或 `diana7g2`） |
| `arm_prefix` | `""` | 名称前缀 |
| `fake_sensor_commands` | `"false"` | 模拟传感器指令 |
| `joint_state_rate` | `30` | 关节状态发布频率（Hz） |
| `namespace` | `"NS_1"` | 该机器人的命名空间，可为空字符串；多机器人时必须互不相同 |
| `robot_ip` | `"192.168.10.75"` | 机器人 IP 或主机名 |
| `use_fake_hardware` | `"false"` | 是否使用模拟硬件 |
| `use_rviz` | `"true"` | 是否启动 RViz |

当任意条目的 `use_rviz` 为 `"true"` 时，`example.launch.py` 只启动一个 `rviz2` 实例（配置取自 `diana_description` 的 `rviz/visualize_diana.rviz`）。只有一个条目启用 RViz 且有命名空间时，`robot_description` 话题会被重映射到 `/<namespace>/robot_description`。

### 多机器人配置

要同时启动多个机器人，在配置文件中增加条目，并给每个机器人设置不同的 `namespace`。默认文件中的 `ROBOT2`、`ROBOT3` 是被注释掉的模板，取消注释后需要把 `robot_type` 改成各自的机型，并补全各自的 `robot_ip`：

```yaml
ROBOT2:
  robot_type: "diana3"
  arm_prefix: ""
  fake_sensor_commands: "false"
  joint_state_rate: 30
  namespace: "NS_2"
  robot_ip: "<robot-ip>"
  use_fake_hardware: "false"
  use_rviz: "false"
```

使用自定义配置文件：

```bash
ros2 launch diana_bringup example.launch.py \
  robot_config_file:=/path/to/my_robots.config.yaml \
  controller_names:=gravity_compensation_example_controller
```

### 控制器名称与机器人 IP 列表

`controller_names` 与 `robot_ips` 都是逗号分隔的列表，按配置文件中机器人的顺序一一对应：

```bash
ros2 launch diana_bringup example.launch.py \
  robot_ips:=<robot-ip>,<robot-ip> \
  controller_names:=gravity_compensation_example_controller,joint_impedance_example_controller
```

规则如下（见 `diana_bringup.launch_utils.get_parameter_for_config`）：

- 列表长度等于机器人数量时，第 N 个值用于第 N 个机器人；
- 长度不等时会打印警告，并对所有机器人使用第一个值；
- `robot_ips` 为空时使用配置文件中的 `robot_ip`；
- `controller_names` 为空会直接退出。

```{important}
`example.launch.py` 在为机器人加载控制器时，是按机器人序号直接索引 `controller_names` 的原始列表。多机器人时请为每个机器人都给出一个控制器名称，不要依赖“只给一个名称用于全部机器人”的回退逻辑。名称前后不要带空格。
```

## 带 IK 的关节阻抗启动文件

`joint_impedance_with_ik_example_controller.launch.py` 在 `example.launch.py` 的基础上，固定使用 `joint_impedance_with_ik_example_controller`，并为配置文件中的每个机器人额外包含 `diana_moveit_config` 的 `move_group.launch.py`，使该控制器可以通过 MoveIt 的 `compute_ik` 服务求解逆运动学。MoveIt 的服务与机器人在同一命名空间下，例如 `/NS_1/compute_ik`、`/NS_1/compute_fk`、`/NS_1/compute_cartesian_path` 和 `/NS_1/plan_kinematic_path`。

```bash
ros2 launch diana_bringup joint_impedance_with_ik_example_controller.launch.py
```

该文件只有一个启动参数 `robot_config_file`（默认 `diana.config.yaml`）。它会读取每个条目的 `robot_ip`、`namespace`、`use_fake_hardware`、`fake_sensor_commands`、`use_rviz`、`arm_prefix`、`robot_type` 并传给 `move_group.launch.py`，所以这些字段都必须存在。

```{warning}
该控制器会以关节阻抗方式输出力矩并使机械臂做小幅运动，需要真实的 `diana_hardware` 接口和可用的 `compute_ik` 服务。运行前请确认净空和急停，且配置文件中的 `use_fake_hardware` 为 `"false"`。MoveIt 的说明见 [diana_moveit_config](diana_moveit_config.md)，控制器说明见 [diana_example_controllers](diana_example_controllers.md)。
```

## 非实时机器人参数设置

`diana_hardware` 在 `ros2_control_node` 进程中，随硬件接口一起创建一个名为 `service_server` 的节点，提供下列非实时参数服务（类型均在 [diana_msgs](diana_msgs.md) 中定义）。这些服务只在使用真实硬件接口（`use_fake_hardware` 为 `false`）时存在。服务名带有启动时的命名空间：没有命名空间时是 `/service_server/...`，用 `diana.config.yaml` 默认的 `NS_1` 启动时是 `/NS_1/service_server/...`。下表按不带命名空间的名称列出。

### 服务列表

| 服务 | 类型 | 请求字段 |
| --- | --- | --- |
| `service_server/set_joint_stiffness` | `diana_msgs/srv/SetJointStiffness` | `joint_stiffness`（7 个值） |
| `service_server/set_cartesian_stiffness` | `diana_msgs/srv/SetCartesianStiffness` | `cartesian_stiffness`（x, y, z, roll, pitch, yaw，6 个值，在刚度坐标系方向上生效） |
| `service_server/set_tcp_frame` | `diana_msgs/srv/SetTCPFrame` | `transformation`（4x4 列主序矩阵，共 16 个值，NE 到 EE 的变换 NE_T_EE） |
| `service_server/set_stiffness_frame` | `diana_msgs/srv/SetStiffnessFrame` | `transformation`（4x4 列主序矩阵，共 16 个值，EE 到 K 的变换 EE_T_K） |
| `service_server/set_force_torque_collision_behavior` | `diana_msgs/srv/SetForceTorqueCollisionBehavior` | 名义力矩（7）与名义力（6）的上下阈值 |
| `service_server/set_full_collision_behavior` | `diana_msgs/srv/SetFullCollisionBehavior` | 加速度阶段与名义阶段的力矩（7）、力（6）上下阈值 |
| `service_server/set_load` | `diana_msgs/srv/SetLoad` | `mass`、`center_of_mass`（3）、`load_inertia`（3x3 列主序，9 个值） |

所有服务的响应都是 `bool success` 与 `string error`；底层调用抛出异常时 `success` 为 `false`，`error` 中带有异常信息。

`set_tcp_frame` 与 `set_stiffness_frame` 分别设置两个相邻坐标系之间的变换：前者是名义末端坐标系 NE 到末端执行器坐标系 EE 的变换 NE_T_EE，后者是 EE 到刚度坐标系 K 的变换 EE_T_K。二者都在运行时通过服务设置。

```{figure} ../../../../_static/images/ros2-humble-frames-zh.png
:alt: NE、EE、K 三个坐标系之间的变换链
:width: 100%

NE、EE、K 之间的变换链，以及对应的两个服务。
```

```{warning}
负载、末端坐标系变换和碰撞阈值直接影响机器人的力矩估计与保护停止行为。请按实际工装设置，并在更改后以保守的速度重新验证。
```

## 非实时 ROS 2 动作

`diana_hardware` 在同一进程中还创建了名为 `action_server` 的节点，提供动作 `action_server/error_recovery`（类型 `diana_msgs/action/ErrorRecovery`，目标、结果和反馈均为空）。收到目标后它调用 `robot->automaticErrorRecovery()`：成功则目标成功，抛出异常则目标被中止并在日志中记录错误。命名空间规则与上节服务相同；下面的示例按 `NS_1` 书写，不带命名空间时去掉 `/NS_1`。

```bash
ros2 action send_goal /NS_1/action_server/error_recovery diana_msgs/action/ErrorRecovery {}
```

```{important}
自动错误恢复只是清除机器人当前的可恢复错误，不能代替查明停止原因。发生碰撞、保护停止等安全相关停止时，先确认现场安全，再执行恢复，参见[安全边界](../../../reference/safety.md)。
```

## 测试

`test/README.md` 将测试分为下列几类（只列出 Diana 源码树中存在的测试文件）：

| 类别 | 是否需要真实机器人 | 测试文件 |
| --- | --- | --- |
| 模拟硬件集成 | 否 | `test_fake_hardware_controllers.py` |
| 接口校验 | 否 | `test_diana_arm_interfaces.py`、`test_xacro_path_resolution.py`、`test_gazebo_wrapper_expansion.py` |
| launch 文件解析 | 否 | `test_launch_file_parsing.py` |
| 真实硬件冒烟测试 | 是 | `test_hardware_example_controllers.py`、`test_hardware_generic_controller.py` |

运行不需要硬件的测试：

```bash
colcon test --packages-select diana_bringup \
  --ctest-args --exclude-regex 'test_hardware'
```

硬件测试通过 CMake 变量 `ROBOT_IP` 指定机器人地址。

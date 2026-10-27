# 快速开始

```{important}
本页从已经构建好的工作空间开始。尚未安装 ROS 2、获取源码或构建时，请先完成[开发准备](development.md)。涉及真实机械臂的步骤集中在最后的“连接实机”一节，其余步骤都不需要连接机器人。
```

目标是依次完成：确认软件包可见、在 RViz 或 Gazebo 中查看机器人模型、在模拟硬件上运行第一个示例控制器，并在满足全部前提后再连接真实机械臂。

## 确认软件包可见

在新终端中加载 ROS 2 和工作空间，然后检查 Diana 软件包：

```bash
source /opt/ros/humble/setup.bash
source ~/diana_ros2_ws/install/setup.bash
ros2 pkg list | grep diana
```

输出中应包含 `diana_bringup`、`diana_example_controllers`、`diana_gazebo_bringup`、`diana_hardware`、`diana_moveit_config`、`diana_msgs`、`diana_robot_state_broadcaster` 和 `diana_semantic_components`。各软件包的用途见[软件包](packages/index.md)。

```{note}
机器人模型来自外部软件包 `diana_description`，它通过源码中的 `dependency.repos` 导入。如果下面的启动命令提示找不到该软件包，请回到[开发准备](development.md)重新导入依赖。
```

## 模型可视化与 Gazebo 仿真

本节的命令都在仿真中运行，不连接真实机械臂。`robot_type` 是必填参数，取值 `diana3`、`diana7` 或 `diana7g2`，请与自己的机型一致；下面的命令以 `diana3` 为例。仿真需要先安装 Gazebo 相关依赖，见[开发准备](development.md)中的“安装 Gazebo 仿真依赖（可选）”。

### 模型可视化

```bash
ros2 launch diana_gazebo_bringup visualize_diana_robot.launch.py robot_type:=diana3
```

该命令启动 Gazebo 的空世界、`robot_state_publisher`、RViz，并在空世界中生成机器人，同时激活 `joint_state_broadcaster`。它不加载任何运动控制器，机械臂不会自行运动。

### 带示例控制器的仿真

```bash
ros2 launch diana_gazebo_bringup gazebo_diana_arm_example_controller.launch.py \
  robot_type:=diana3 \
  controller:=joint_impedance_example_controller
```

`controller` 必须是 `diana_gazebo_bringup` 的 `config/<robot_type>_gazebo_controllers.yaml` 中已注册的控制器名称。该启动文件还提供 `gz_args`（Gazebo 参数）、`rviz`（是否启动 RViz）和 `namespace` 参数，详见 [diana_gazebo_bringup](packages/diana_gazebo_bringup.md)。

```{figure} ../../../_static/images/ros2-humble-gazebo-example-controller.png
:alt: diana3 在 Gazebo 和 RViz 中的仿真画面
:width: 100%

`diana3` 在 Gazebo（左）和 RViz（右）中的仿真画面。Gazebo 的实体树中可以看到 `ground_plane`、`sun` 和 `diana3`。
```

按 `Ctrl+C` 结束仿真。

```{tip}
想验证 MoveIt 规划而不连接机器人，可以运行 `ros2 launch diana_moveit_config moveit.launch.py robot_type:=diana3 robot_ip:=192.168.10.75 use_fake_hardware:=true`，说明见 [diana_moveit_config](packages/diana_moveit_config.md)。
```

## 在模拟硬件上运行第一个示例控制器

`example.launch.py` 读取一个 YAML 配置文件，其中的 `use_fake_hardware` 默认为 `"false"`。要在不连接机器人的情况下运行，需要把它改为 `"true"`。不要直接修改安装目录里的文件，先复制一份：

```bash
cp "$(ros2 pkg prefix diana_bringup)/share/diana_bringup/config/diana.config.yaml" ~/my_fake.config.yaml
```

用编辑器打开 `~/my_fake.config.yaml`，修改其中机器人条目（默认是 `ROBOT1`）的下列字段：

- `robot_type`：改成自己的机型（`diana3`、`diana7` 或 `diana7g2`；文件中的 `"diana3"` 只是示例值）；
- `use_fake_hardware`：改为 `"true"`（布尔值要加引号）；
- `namespace`：改为 `""`（可选），清空后后续命令不必带命名空间。

字段说明见 [diana_bringup](packages/diana_bringup.md)。

### 启动重力补偿示例

```bash
ros2 launch diana_bringup example.launch.py \
  robot_config_file:=$HOME/my_fake.config.yaml \
  controller_names:=gravity_compensation_example_controller
```

在另一个终端中检查控制器状态：

```bash
ros2 control list_controllers
```

`joint_state_broadcaster` 和 `gravity_compensation_example_controller` 都应为 `active`。配置文件中 `use_rviz` 为 `"true"` 时，会同时打开 RViz 显示机器人模型。

### 运行关节阻抗示例

在模拟硬件下，只有关节层面的两个示例可以运行：`gravity_compensation_example_controller` 和 `joint_impedance_example_controller`。`example.launch.py` 只会加载 `controller_names` 指定的控制器，没有被指定的控制器不会被加载，因此不能在运行中直接切换到它们。要换一个示例，先在运行 launch 的终端按 `Ctrl+C`，再用另一个控制器名称重新启动：

```bash
ros2 launch diana_bringup example.launch.py \
  robot_config_file:=$HOME/my_fake.config.yaml \
  controller_names:=joint_impedance_example_controller
```

```{note}
肘部和笛卡尔类示例会调用服务，并使用 `robot_time`、`elbow_state` 等接口，这些只由真实的 `diana_hardware` 提供，不能在模拟硬件上运行。各示例的前提见 [diana_example_controllers](packages/diana_example_controllers.md)。
```

### 停止

在运行 `example.launch.py` 的终端中按 `Ctrl+C`。`ros2_control_node` 退出时整个 launch 会随之关闭。

## 连接实机

```{warning}
本节会连接真实机械臂，示例控制器会让机械臂运动或输出力矩。开始前必须全部满足：

- 示教器已将机械臂切换到**协作模式**，并已满足 [FCI 概览](../../fci/overview.md) 中的运行条件；
- 控制 PC 与控制柜网络连通，配置见[网络配置](../../programming/network.md)；
- 机械臂工作空间内无人员、工件、夹具和线缆等障碍物，急停触手可及；
- 已阅读[安全边界](../../reference/safety.md)，并先使用不运动的命令确认连接。
```

实机运行需要实时权限，见[开发准备](development.md)中的“配置实时权限”。

### 先确认连接

先只启动控制栈和广播器，不加载运动控制器。将 `<robot-ip>` 替换为控制器的实际地址（默认地址为 `192.168.10.75`），`robot_type` 与机型一致：

```bash
ros2 launch diana_bringup diana.launch.py robot_type:=diana3 robot_ip:=<robot-ip>
```

在另一个终端中检查：

```bash
ros2 control list_controllers
ros2 topic list
```

此时 `joint_state_broadcaster` 和 `diana_robot_state_broadcaster` 应处于 `active`。确认可以读到机器人状态后，按 `Ctrl+C` 结束。

### 运行重力补偿示例

重力补偿示例向 7 个关节写零力矩，机械臂由内部重力补偿悬停，可被手推动，不会主动保持位置。先复制并编辑一份配置文件：

```bash
cp "$(ros2 pkg prefix diana_bringup)/share/diana_bringup/config/diana.config.yaml" ~/my_robot.config.yaml
```

在 `~/my_robot.config.yaml` 中把 `robot_type` 改成自己的机型，`robot_ip` 改成 `<robot-ip>`，并确认 `use_fake_hardware` 为 `"false"`。然后启动：

```bash
ros2 launch diana_bringup example.launch.py \
  robot_config_file:=$HOME/my_robot.config.yaml \
  controller_names:=gravity_compensation_example_controller
```

默认配置的命名空间为 `NS_1`，因此检查控制器时要指定 controller manager：

```bash
ros2 control list_controllers -c /NS_1/controller_manager
```

```{important}
首次运行请先支撑好机械臂和末端负载，保持手在急停可达范围内。运行其他会产生运动的示例之前，请阅读 [diana_example_controllers](packages/diana_example_controllers.md) 中对应的小节。
```

## 运行流程

```text
启动 launch（robot_state_publisher、ros2_control_node、广播器）
    → spawner 加载并激活控制器 → 控制器按 1 kHz 周期运行
    → Ctrl+C 关闭 launch（换示例时用另一个控制器名称重新启动）
```

`diana.launch.py` 只启动广播器；`example.launch.py` 会在其基础上用 `spawner` 加载 `controller_names` 指定的控制器，没有被指定的控制器不会被加载。控制器运行期间，`diana_hardware` 只按一种控制模式工作，详见 [diana_bringup](packages/diana_bringup.md)。

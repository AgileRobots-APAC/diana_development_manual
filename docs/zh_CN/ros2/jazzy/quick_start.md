# 快速开始

```{important}
本页从已经构建好的工作空间开始。尚未安装 ROS 2、libfranka、获取源码或构建时，请先完成[开发准备](development.md)。涉及真实机械臂的步骤集中在最后的“连接实机”一节，其余步骤都不需要连接机器人。
```

目标是依次完成：确认软件包可见、在 RViz 或 Gazebo 中查看机器人模型、在模拟硬件上运行第一个示例控制器，并在满足全部前提后再连接真实机械臂。

## 确认软件包可见

在新终端中加载 ROS 2 和工作空间，然后检查 Diana 软件包：

```bash
source /opt/ros/jazzy/setup.bash
source ~/diana_ros2_ws/install/setup.bash
ros2 pkg list | grep -E 'diana|franka'
```

输出中应包含 `diana_bringup`、`diana_description`、`diana_gazebo_bringup`、`diana_gazebo_hardware`、`diana_moveit_config`、`diana_selfcollision`、`franka_example_controllers`、`franka_hardware`、`franka_msgs`、`franka_robot_state_broadcaster` 和 `franka_semantic_components`。各软件包的用途见[软件包](packages/index.md)。

## 模型可视化与 Gazebo 仿真

本节的命令都在仿真中运行，不连接真实机械臂。`robot_type` 是必填参数，取值 `diana3`、`diana7` 或 `diana7g2`，请与自己的机型一致；下面的命令以 `diana3` 为例。

### 模型可视化

```bash
ros2 launch diana_description diana.visualize.launch.py robot_type:=diana3
```

该命令启动 `robot_state_publisher`、`joint_state_publisher_gui` 和 RViz，可以在 RViz 中拖动关节滑块查看模型。它不加载任何控制器，机械臂不会自行运动。参数和 Diana Duo 的用法见 [diana_description](packages/diana_description.md)。

### 带示例控制器的仿真

```bash
ros2 launch diana_gazebo_bringup diana.example_controller.launch.py \
  robot_type:=diana3 \
  controller:=joint_impedance_example_controller
```

`controller` 必须是 `config/controllers.yaml` 中已配置的控制器名称。该启动文件还提供 `gz_args`（Gazebo 参数）、`rviz`（是否启动 RViz）和 `namespace` 参数，详见 [diana_gazebo_bringup](packages/diana_gazebo_bringup.md)。仿真需要的依赖已经由[开发准备](development.md)中的 `rosdep install` 安装。

按 `Ctrl+C` 结束仿真。

```{tip}
想验证 MoveIt 规划而不连接机器人，可以运行 `ros2 launch diana_moveit_config moveit.launch.py robot_type:=diana3 robot_ip:=192.168.10.75 use_fake_hardware:=true`，说明见 [diana_moveit_config](packages/diana_moveit_config.md)。
```

## 在模拟硬件上运行第一个示例控制器

`diana.example_controllers.launch.py` 读取一个 YAML 机器人配置文件。不要直接修改安装目录里的文件，先复制一份：

```bash
cp "$(ros2 pkg prefix diana_bringup)/share/diana_bringup/config/diana.config.yaml" ~/my_fake.config.yaml
```

用编辑器打开 `~/my_fake.config.yaml`，检查其中机器人条目（默认是 `ROBOT1`）的下列字段：

- `robot_type`：改成自己的机型（`diana3`、`diana7` 或 `diana7g2`；文件中的默认值只是示例）；
- `use_fake_hardware`：保持 `"true"`（布尔值要加引号），此时不会连接真实机器人；
- `namespace`：保持 `""`，不使用命名空间。

字段说明见 [diana_bringup](packages/diana_bringup.md)。

### 启动重力补偿示例

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
  robot_config_file:=$HOME/my_fake.config.yaml \
  controller_names:=gravity_compensation_example_controller
```

在另一个终端中检查控制器状态：

```bash
ros2 control list_controllers
```

`joint_state_broadcaster` 和 `gravity_compensation_example_controller` 都应为 `active`。配置文件中 `use_rviz` 为 `"true"` 时，会同时打开 RViz 显示机器人模型。各示例控制器的前提和限制见 [franka_example_controllers](packages/franka_example_controllers.md)。

### 停止

在运行 `diana.example_controllers.launch.py` 的终端中按 `Ctrl+C`。`ros2_control_node` 退出时整个 launch 会随之关闭。

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

先只启动控制栈和广播器，不加载运动控制器。将 `<robot-ip>` 替换为控制器的实际地址（默认地址为 `192.168.10.75`），`robot_type` 与机型一致，并显式关闭模拟硬件：

```bash
ros2 launch diana_bringup diana.launch.py robot_type:=diana3 robot_ip:=<robot-ip> use_fake_hardware:=false
```

在另一个终端中检查：

```bash
ros2 control list_controllers
ros2 topic list
```

此时 `joint_state_broadcaster` 和 `franka_robot_state_broadcaster` 应处于 `active`。确认可以读到机器人状态后，按 `Ctrl+C` 结束。

### 运行重力补偿示例

重力补偿示例向 7 个关节写零力矩，机械臂由内部重力补偿悬停，可被手推动，不会主动保持位置。先复制并编辑一份配置文件：

```bash
cp "$(ros2 pkg prefix diana_bringup)/share/diana_bringup/config/diana.config.yaml" ~/my_robot.config.yaml
```

在 `~/my_robot.config.yaml` 中把 `robot_type` 改成自己的机型，`robot_ip` 改成 `<robot-ip>`，并把 `use_fake_hardware` 改为 `"false"`。然后启动：

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
  robot_config_file:=$HOME/my_robot.config.yaml \
  controller_names:=gravity_compensation_example_controller
```

检查控制器状态：

```bash
ros2 control list_controllers
```

如果配置文件中给 `namespace` 设置了值，需要用 `-c` 指定对应的 controller manager，例如 `ros2 control list_controllers -c /<namespace>/controller_manager`。

```{important}
首次运行请先支撑好机械臂和末端负载，保持手在急停可达范围内。运行其他会产生运动的示例之前，请阅读 [franka_example_controllers](packages/franka_example_controllers.md) 中对应的小节。
```

# MoveIt 配置

软件包名称：`diana_moveit_config`

## 安装

请参阅 [开发准备](../development.md)。

## 软件包概述

`diana_moveit_config` 提供 Diana 机械臂的 MoveIt 2 配置和启动文件，包含：

- 两个启动文件：`launch/moveit.launch.py`（完整的 MoveIt 演示栈）和 `launch/move_group.launch.py`（只启动 `move_group` 节点，供其他启动文件包含）。
- 按机型划分的配置目录 `config/diana3` 和 `config/diana7g2`，各含 5 个 yaml 文件。
- 按机型划分的 RViz 配置 `rviz/moveit_<robot_type>.rviz`。

机器人描述（URDF/xacro）和语义描述（SRDF/xacro）**不在本包内**：`moveit.launch.py` 从 `diana_bringup` 读取 `urdf/diana_arm.urdf.xacro`，并从外部软件包 `diana_description` 读取 `robots/<robot_type>/<robot_type>.srdf.xacro`。`diana_description` 通过源码中的 `dependency.repos` 导入，参见[开发准备](../development.md)。

```{note}
`moveit.launch.py` 自身会启动 `ros2_control_node`、`robot_state_publisher`、`joint_state_publisher` 和控制器，因此它是一套独立的完整栈。不要在同一台机器人上同时再运行 [diana_bringup](diana_bringup.md) 的 `diana.launch.py` / `example.launch.py`。
```

```{figure} ../../../../_static/images/ros2-humble-moveit-launch-zh.png
:alt: moveit.launch.py 启动的节点与关系
:width: 70%

`moveit.launch.py` 启动的节点及其关系：RViz 的 MotionPlanning 面板通过 MoveGroup 动作请求规划与执行，`move_group` 再把轨迹交给 `FollowJointTrajectory` 轨迹控制器。
```

## Move Group

规划组名称为 `<robot_type>_arm`，其中 `<robot_type>` 为启动参数 `robot_type` 的取值：

| `robot_type` | 规划组 | 运动学配置 | 轨迹控制器 | 关节 |
| --- | --- | --- | --- | --- |
| `diana3` | `diana3_arm` | `config/diana3/kinematics.yaml` | `diana3_arm_controller` | `diana3_joint1` ... `diana3_joint7` |
| `diana7g2` | `diana7g2_arm` | `config/diana7g2/kinematics.yaml` | `diana7g2_arm_controller` | `diana7g2_joint1` ... `diana7g2_joint7` |

两种机型的 yaml 文件结构完全一致，只有机型名前缀不同。`moveit.launch.py` 按 `robot_type` 读取 `config/<robot_type>/` 下的 yaml，只有以上两种 `robot_type` 有对应的 `config/` 目录，其他取值无法启动。

## 使用方法

### 启动参数

`moveit.launch.py` 声明以下参数（均可通过 `name:=value` 传入）：

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `robot_type` | 必填 | 机型：`diana3` 或 `diana7g2`，与所用机器人一致；目前没有 `diana7` 的 MoveIt 配置，不能使用 |
| `robot_ip` | 必填 | 机器人的主机名或 IP 地址。使用模拟硬件时不会连接该地址，但这个参数仍然必须传入 |
| `use_fake_hardware` | `false` | 使用 `mock_components/GenericSystem` 代替真实硬件 |
| `fake_sensor_commands` | `false` | 传给 xacro 的模拟传感器命令开关 |
| `use_rviz` | `true` | 是否启动 RViz（使用 `rviz/moveit_<robot_type>.rviz`） |
| `namespace` | 空 | `move_group`、`robot_state_publisher`、`ros2_control_node` 和控制器管理器所在的命名空间 |

### 仿真（fake hardware）

不连接机器人，用模拟硬件验证 MoveIt 配置。`robot_ip` 仍然必须传入，模拟硬件不会连接它，可以写 Diana 的默认地址 `192.168.10.75`：

```bash
ros2 launch diana_moveit_config moveit.launch.py robot_type:=diana3 robot_ip:=192.168.10.75 use_fake_hardware:=true
```

启动后：

- 加载 `config/<robot_type>/ros_controllers_fake.yaml`，轨迹控制器使用 `position` 命令接口。
- 不会启动 `diana_robot_state_broadcaster`。
- 在 RViz 中启用 `MotionPlanning` 显示（RViz 配置中该显示默认是关闭的，`Planning Group` 已预设为 `<robot_type>_arm`），设置目标位姿后点击 Plan / Execute。

```{figure} ../../../../_static/images/ros2-humble-moveit-rviz-startup.png
:alt: 刚启动时的 RViz，MotionPlanning 显示未勾选
:width: 100%

刚启动时的 RViz：`MotionPlanning` 显示默认没有勾选，只显示机器人模型。
```

```{figure} ../../../../_static/images/ros2-humble-moveit-rviz-motionplanning.png
:alt: 勾选 MotionPlanning 后的 RViz，出现 MotionPlanning 面板
:width: 100%

勾选 `MotionPlanning` 后：出现 MotionPlanning 面板，规划组为 `diana3_arm`，机器人末端出现交互标记，可以用 Plan、Execute、Plan & Execute 规划和执行。
```

```{tip}
没有 RViz 图形环境时加上 `use_rviz:=false`。`move_group` 节点会提供标准的 MoveIt `MoveGroup` 动作。
```

### 实机

```bash
ros2 launch diana_moveit_config moveit.launch.py robot_type:=diana3 robot_ip:=<robot-ip>
```

```{warning}
实机命令会让机械臂执行 MoveIt 规划出的轨迹。执行前请保证机械臂工作空间内无人员和障碍物、急停触手可及、机器人已满足控制模式和网络前提，并先用低速度比例在 RViz 中检查规划路径。详细要求请参阅 [安全边界](../../../reference/safety.md)、[网络配置](../../../programming/network.md) 和 [FCI 概述](../../../fci/overview.md)。
```

实机模式加载 `config/<robot_type>/ros_controllers.yaml`：轨迹控制器使用 `effort` 命令接口，同时启动 `diana_robot_state_broadcaster`。

## 配置文件

两个机型目录（以 `config/<robot_type>/` 表示）中各有以下文件：

::::{list-table}
:header-rows: 1
:widths: 24 76

* - 文件
  - 内容
* - `kinematics.yaml`
  - `<robot_type>_arm` 的运动学求解器：
    - 求解器：`lma_kinematics_plugin/LMAKinematicsPlugin`
    - `kinematics_solver_search_resolution: 0.005`
    - `kinematics_solver_timeout: 0.005`
* - `ompl_planning.yaml`
  - OMPL 的 `planner_configs`（SBL、EST、RRT、RRTConnect、RRTstar、PRM、FMT、TrajOpt 等共 24 个）及 `<robot_type>_arm` 可用的规划器列表
* - `controllers.yaml`
  - MoveIt 的 `MoveItSimpleControllerManager` 配置：
    - 控制器：`<robot_type>_arm_controller`
    - 动作命名空间：`follow_joint_trajectory`
    - 类型：`FollowJointTrajectory`
    - `default: true`
    - 关节 1 至 7
* - `ros_controllers.yaml`
  - 实机用的 ros2_control 配置：
    - 更新率 1000 Hz
    - `<robot_type>_arm_controller`：`joint_trajectory_controller/JointTrajectoryController`，命令接口 `effort`，状态接口 `position`、`velocity`，增益见下
    - `joint_state_broadcaster`
    - `diana_robot_state_broadcaster`
* - `ros_controllers_fake.yaml`
  - `use_fake_hardware:=true` 时使用：与上相同，但命令接口为 `position`，没有增益项
::::

`moveit.launch.py` 在代码中另外设定了：规划插件 `ompl_interface/OMPLPlanner`、`start_state_max_bounds_error: 0.1`、请求适配器（`AddTimeOptimalParameterization`、`ResolveConstraintFrames`、`FixWorkspaceBounds`、`FixStartStateBounds`、`FixStartStateCollision`、`FixStartStatePathConstraints`）、轨迹执行参数（`allowed_execution_duration_scaling: 1.2`、`allowed_goal_duration_margin: 0.5`、`allowed_start_tolerance: 0.01`）以及规划场景监视器的四个 `publish_*` 开关（均为 `True`）。

```{note}
[diana_example_controllers](diana_example_controllers.md) 中的 `joint_impedance_with_ik_example_controller` 的启动文件 `joint_impedance_with_ik_example_controller.launch.py`（位于 `diana_bringup`）会为每个机器人包含本包的 `move_group.launch.py`，并加载 `config/<robot_type>/kinematics.yaml`。如需更换其逆运动学求解器，修改该 yaml 中的 `kinematics_solver` 即可。`move_group.launch.py` 不能单独使用，其所需参数由包含它的启动文件传入。
```

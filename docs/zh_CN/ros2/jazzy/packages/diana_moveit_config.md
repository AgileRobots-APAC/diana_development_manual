# MoveIt 配置

软件包名称：`diana_moveit_config`

## 安装

请参阅 [开发准备](../development.md)。

## 软件包概述

`diana_moveit_config` 提供 Diana 机械臂的 MoveIt 2 配置和启动文件，包含：

- 两个启动文件：`launch/moveit.launch.py`（完整的 MoveIt 栈，含 RViz）和 `launch/move_group.launch.py`（只启动 `move_group` 节点，供其他启动文件包含）。
- 按机型划分的配置目录 `config/diana3`、`config/diana7` 和 `config/diana7g2`，各含 5 个 yaml 文件（`controllers.yaml`、`joint_limits.yaml`、`kinematics.yaml`、`ompl_planning.yaml`、`ros_controllers.yaml`）。
- RViz 配置 `rviz/moveit.rviz`。

机器人描述（URDF/xacro）和语义描述（SRDF/xacro）**不在本包内**：启动文件从 `diana_bringup` 读取 `urdf/diana_arm.urdf.xacro`，并从 `diana_description` 读取 `robots/<robot_type>/<robot_type>.srdf.xacro`。`diana_description` 通过源码中的 `dependency.repos` 导入，参见[开发准备](../development.md)。

```{note}
`moveit.launch.py` 自身会启动 `ros2_control_node`、`robot_state_publisher`、`joint_state_publisher` 等节点，因此它是一套独立的完整栈。不要在同一台机器人上同时再运行 [diana_bringup](diana_bringup.md) 的启动文件。
```

## Move Group

规划组名称为 `<robot_type>_arm`，其中 `<robot_type>` 为启动参数 `robot_type` 的取值。本包有 `config/<robot_type>/` 目录的 `robot_type` 取值只有以下三个：

| `robot_type` | 规划组 | 配置目录 | 轨迹控制器（`controllers.yaml`） | 关节 |
| --- | --- | --- | --- | --- |
| `diana3` | `diana3_arm` | `config/diana3/` | `diana3_arm_controller` | `diana3_joint1` ... `diana3_joint7` |
| `diana7` | `diana7_arm` | `config/diana7/` | `diana7_arm_controller` | `diana7_joint1` ... `diana7_joint7` |
| `diana7g2` | `diana7g2_arm` | `config/diana7g2/` | `diana7g2_arm_controller` | `diana7g2_joint1` ... `diana7g2_joint7` |

三个目录的 yaml 文件结构一致，只有机型名前缀不同。启动文件按 `robot_type` 读取 `config/<robot_type>/` 下的 yaml，其他取值没有对应的配置目录，无法启动。

MoveIt 通过 `MoveItSimpleControllerManager` 把轨迹交给 `FollowJointTrajectory` 动作（动作命名空间 `follow_joint_trajectory`，`default: true`）。

## 使用方法

### 启动参数

`moveit.launch.py` 声明以下参数（均可通过 `name:=value` 传入）。`robot_type` 和 `robot_ip` 在启动文件中虽有默认值，但请在每条命令中显式传入：

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `robot_type` | `diana7`（请显式传入） | 机型：`diana3`、`diana7` 或 `diana7g2`，与所用机器人一致 |
| `robot_ip` | `192.168.10.75`（请显式传入） | 机器人的主机名或 IP 地址（Diana 控制器 A 网口的默认地址为 `192.168.10.75`）。使用模拟硬件时不会连接该地址 |
| `namespace` | 空 | `move_group`、`robot_state_publisher`、`ros2_control_node`、`joint_state_publisher` 和控制器 spawner 所在的命名空间 |
| `use_fake_hardware` | `true` | 使用模拟硬件，不连接机器人。连接实机时请显式设为 `false` |
| `fake_sensor_commands` | `false` | 传给 xacro 的模拟传感器命令开关，仅在 `use_fake_hardware` 为 `true` 时有效 |
| `use_rviz` | `true` | 是否启动 RViz（使用 `rviz/moveit.rviz`） |

`moveit.launch.py` 会启动以下节点：`move_group`（`moveit_ros_move_group`）、`rviz2`（`use_rviz` 为 `true` 时）、`robot_state_publisher`、`ros2_control_node`、`joint_state_publisher`；`use_fake_hardware` 为 `false` 时还会通过 `controller_manager spawner` 启动 `franka_robot_state_broadcaster`。

### 模拟硬件

不连接机器人，用模拟硬件验证 MoveIt 配置。`robot_ip` 仍应传入，模拟硬件不会连接它，可以写 Diana 的默认地址 `192.168.10.75`：

```bash
ros2 launch diana_moveit_config moveit.launch.py robot_type:=diana7 robot_ip:=192.168.10.75 use_fake_hardware:=true
```

启动后在 RViz 中启用 `MotionPlanning` 显示，`Planning Group` 选择 `<robot_type>_arm`，设置目标位姿后点击 Plan / Execute。没有图形环境时加上 `use_rviz:=false`，`move_group` 节点会提供标准的 MoveIt `MoveGroup` 动作。

### 实机

```bash
ros2 launch diana_moveit_config moveit.launch.py robot_type:=diana7 robot_ip:=<robot-ip> use_fake_hardware:=false
```

```{warning}
实机命令会让机械臂执行 MoveIt 规划出的轨迹。执行前请保证机械臂工作空间内无人员和障碍物、急停触手可及、机器人已满足控制模式和网络前提，并先用低速度比例在 RViz 中检查规划路径。详细要求请参阅 [安全边界](../../../reference/safety.md)、[网络配置](../../../programming/network.md) 和 [FCI 概述](../../../fci/overview.md)。
```

## 配置文件

三个机型目录（以 `config/<robot_type>/` 表示）中各有以下文件：

::::{list-table}
:header-rows: 1
:widths: 24 76

* - 文件
  - 内容
* - `kinematics.yaml`
  - `<robot_type>_arm` 的运动学求解器：
    - 求解器：`kdl_kinematics_plugin/KDLKinematicsPlugin`
    - `kinematics_solver_search_resolution: 0.005`
    - `kinematics_solver_timeout: 0.005`
* - `joint_limits.yaml`
  - 关节 1 至 7 的加速度限制：
    - `has_acceleration_limits: true`
    - `max_acceleration` 依次为 3.75、1.875、2.5、3.125、3.75、5.0、5.0（rad/s²）
* - `ompl_planning.yaml`
  - OMPL 的 `planner_configs` 以及 `<robot_type>_arm` 可用的规划器列表
* - `controllers.yaml`
  - MoveIt 的 `MoveItSimpleControllerManager` 配置：
    - 控制器：`<robot_type>_arm_controller`
    - 动作命名空间：`follow_joint_trajectory`
    - 类型：`FollowJointTrajectory`
    - 关节 1 至 7
* - `ros_controllers.yaml`
  - ros2_control 配置：
    - 更新率 1000 Hz
    - `<robot_type>_arm_controller`：`joint_trajectory_controller/JointTrajectoryController`，命令接口 `effort`，状态接口 `position`、`velocity`
    - `joint_state_broadcaster`
    - `franka_robot_state_broadcaster`
::::

`ros_controllers.yaml` 中轨迹控制器的增益（`i` 均为 0，`i_clamp` 均为 1），三个机型相同：

| 关节 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `p` | 600 | 600 | 600 | 600 | 250 | 150 | 50 |
| `d` | 30 | 30 | 30 | 30 | 10 | 10 | 5 |

启动文件在代码中另外设定了：规划插件 `ompl_interface/OMPLPlanner`、`start_state_max_bounds_error: 0.1`、请求适配器（`ResolveConstraintFrames`、`ValidateWorkspaceBounds`、`CheckStartStateBounds`、`CheckStartStateCollision`）、响应适配器（`AddTimeOptimalParameterization`、`ValidateSolution`、`DisplayMotionPath`）、轨迹执行参数（`allowed_execution_duration_scaling: 1.2`、`allowed_goal_duration_margin: 0.5`、`allowed_start_tolerance: 0.01`）以及规划场景监视器的四个 `publish_*` 开关（均为 `True`）。

## `move_group.launch.py`

`move_group.launch.py` 只启动 `move_group` 节点（使用 `output="screen"`），并读取与 `moveit.launch.py` 相同的 `config/<robot_type>/` 下的 yaml。它不启动 RViz、`ros2_control_node` 或控制器，不能单独构成完整的栈；[diana_bringup](diana_bringup.md) 中的 `joint_impedance_with_ik_example_controller.launch.py` 会包含它。该启动文件声明以下参数：

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `robot_type` | `diana7` | 机型：`diana3`、`diana7` 或 `diana7g2` |
| `robot_ip` | `192.168.10.75` | 机器人的主机名或 IP 地址 |
| `namespace` | 空 | `move_group` 节点的命名空间 |
| `use_fake_hardware` | `true` | 传给 xacro 的模拟硬件开关 |
| `fake_sensor_commands` | `false` | 传给 xacro 的模拟传感器命令开关 |
| `arm_prefix` | 空 | 机械臂前缀（用于区分多条机械臂）；非空时，yaml 中的机型名会被替换为 `<arm_prefix>_<robot_type>` |

如需更换逆运动学求解器，修改 `config/<robot_type>/kinematics.yaml` 中的 `kinematics_solver` 即可。

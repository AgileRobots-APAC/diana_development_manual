# 硬件接口

软件包名称：`diana_hardware`

## 安装

请参阅 [开发准备](../development.md)。

## 软件包概述

`diana_hardware` 是 Diana 机器人的 `ros2_control` 硬件插件。它基于兼容 libfranka 的机器人通信实现 `hardware_interface::SystemInterface` 插件 `diana_hardware/DianaHardwareInterface`（通过 `diana_hardware.xml` 注册），同时提供用于声明插件所导出接口的 `ros2_control` xacro 宏库。

软件包包含：

- **硬件插件**：每个控制周期读取完整机器人状态，并写入所支持的某一种命令模式（关节力矩、关节速度、关节位置、笛卡尔速度、笛卡尔位姿，后两者可附带肘部）。
- `ros2_control/` 下的 **xacro 宏库**：`diana_arm.ros2_control.xacro` 与 `diana_ros2_control_macros.xacro`。
- **参数服务节点**（`service_server`）：封装 [diana_msgs](diana_msgs.md) 中的 `Set*` 服务。
- **动作服务节点**（`action_server`）：提供 `ErrorRecovery` 动作。
- **libfranka 日志桥接**：把 libfranka 的日志转发到 ROS 2 日志。

插件通常由 [diana_bringup](diana_bringup.md) 启动的 `ros2_control_node` 加载。控制器不应直接与插件通信，请使用[语义组件](diana_semantic_components.md)，而不是手写原始接口名。

```{figure} ../../../../_static/images/ros2-humble-hardware-dataflow-zh.png
:alt: 硬件插件与控制器、机器人之间的数据流
:width: 100%

`DianaHardwareInterface` 的数据流：控制器通过命令接口下发指令、通过状态接口读取状态；参数服务与错误恢复动作由插件内的两个节点直接与机器人交互。
```

```{important}
向实机下发指令会使机器人运动。激活任何控制器前，请确认工作空间无人员和障碍物、急停触手可及，并满足[安全边界](../../../reference/safety.md)与 [FCI 概览](../../../fci/overview.md)中描述的外部控制前提。
```

## 导出的接口

下文中 `<P>` 表示机械臂前缀（xacro 中的 `modified_prefix`，默认为空），`<T>` 表示 `robot_type`（`diana3`、`diana7` 或 `diana7g2`）。所有接口类型均为 `double`。下列接口集合来自 xacro 的声明以及 `diana_hardware_interface.cpp` 中 `export_state_interfaces()` / `export_command_interfaces()` 的注册。

### 关节接口

共导出 7 个关节：`<P><T>_joint1` 至 `<P><T>_joint7`。插件内关节数固定为 7。

| 接口 | 方向 | 来源 / 含义 |
| --- | --- | --- |
| `<P><T>_jointN/position` | 状态 | 关节测量位置 `q`（rad） |
| `<P><T>_jointN/velocity` | 状态 | 关节测量速度 `dq`（rad/s） |
| `<P><T>_jointN/effort` | 状态 | 关节测量力矩 `tau_J`（Nm） |
| `<P><T>_jointN/position` | 命令 | 关节位置命令 |
| `<P><T>_jointN/velocity` | 命令 | 关节速度命令 |
| `<P><T>_jointN/effort` | 命令 | 关节力矩命令；`include_effort_command` 为 true 时声明（bringup 的 xacro 设为 `true`） |

位置状态接口的 `initial_value`（供 mock 硬件使用）依次为：关节 1 至 7 分别是 `0`、`-pi/4`、`0`、`3*pi/4`、`0`、`-pi/2`（`diana7`）或 `pi/2`（其他型号）、`0`。

### 笛卡尔命令接口

笛卡尔命令以 GPIO 条目导出，其 `index` 参数指定底层命令数组中的位置。

| 接口 | 数量 | 含义 |
| --- | --- | --- |
| `<P>vx/cartesian_velocity`、`<P>vy/...`、`<P>vz/...`、`<P>wx/...`、`<P>wy/...`、`<P>wz/...` | 6（index 0 至 5） | 基坐标系下末端期望速度；线速度 m/s，角速度 rad/s |
| `<P>0/cartesian_pose_command` ... `<P>15/cartesian_pose_command` | 16（index 0 至 15） | 末端期望位姿，按列主序排列的 4x4 齐次变换矩阵 |
| `<P>0/cartesian_pose_state` ... `<P>15/cartesian_pose_state` | 16（状态） | 末端测量位姿 `O_T_EE`，列主序 |

### 肘部接口

| 接口 | 方向 | 含义 |
| --- | --- | --- |
| `<P>joint_3_position/elbow_command` | 命令（index 0） | 关节 3 的期望位置（rad） |
| `<P>joint_4_sign/elbow_command` | 命令（index 1） | 肘部（关节 4）的期望翻转方向 |
| `<P>joint_3_position/elbow_state` | 状态 | 肘部当前关节 3 位置 |
| `<P>joint_4_sign/elbow_state` | 状态 | 肘部当前翻转方向 |

肘部命令只能与笛卡尔速度或笛卡尔位姿命令接口一起申请；否则 `perform_command_mode_switch` 会以致命日志报错。

### 力/力矩传感器接口

xacro 声明了一个名为 `<P><T>_tcp` 的传感器，状态接口为 `force.x`、`force.y`、`force.z`、`torque.x`、`torque.y`、`torque.z`。插件按 xacro 中声明的顺序，用刚度坐标系下估计的外力旋量（`K_F_ext_hat_K`）填充它们。

## 附加状态接口

除关节、位姿、肘部和传感器接口外，插件还导出三个机器人级别的状态接口，用于承载无法用普通数值表示的数据：

| 接口 | 内容 |
| --- | --- |
| `<P><T>/robot_state` | 完整机器人状态结构（`franka::RobotState`）的地址，存放在 `double` 槽位中；由 [DianaRobotState](diana_semantic_components.md) 和 [diana_robot_state_broadcaster](diana_robot_state_broadcaster.md) 使用 |
| `<P><T>/robot_model` | 模型对象（`diana_hardware::Model`）的地址，由 `DianaRobotModel` 使用 |
| `<P><T>/robot_time` | 机器人时间（秒），普通 `double` |

```{warning}
`robot_state` 与 `robot_model` 是存放在 `double` 中的指针，仅在同一进程内有意义。不要把它们当作数值读取，也不要跨进程使用；请使用语义组件类完成转换。
```

## ros2_control 宏库

宏文件位于软件包的 `ros2_control/` 目录，安装到 `share/diana_hardware/ros2_control`。

### diana_arm.ros2_control.xacro

定义宏 `diana_arm_ros2_control`，生成一个名为 `<arm_prefix>DianaHardwareInterface`、类型为 `system` 的 `ros2_control` 块。

| 参数 | 默认值 | 作用 |
| --- | --- | --- |
| `robot_type` | 必填 | 写入硬件参数 `robot_type`，并用于关节、传感器和接口命名 |
| `include_effort_command` | `true` | 为每个关节声明 `effort` 命令接口 |
| `arm_prefix` | `''` | 关节与 GPIO 名称前缀；写入硬件参数 `prefix` |
| `is_async` | `false` | 作为 `is_async` 传给 `ros2_control`；为 true 时添加 `async` 属性块 |
| `thread_priority` | `50` | 异步块的线程优先级（仅 `is_async` 为 true 时使用） |
| `hardware_plugin`（块参数） | 必填 | `plugin` 标签及其参数，会被插入 `hardware` 中 |

该宏总是写入值为 `1.1.0` 的参数 `version`，然后以启用肘部、笛卡尔位姿和传感器的选项调用 `configure_arm_interfaces`（`sensor_name` 为 `<arm_prefix><robot_type>_tcp`）。

### diana_ros2_control_macros.xacro

| 宏 | 作用 |
| --- | --- |
| `configure_arm_joint` | 一个关节：`position`、`velocity` 及（可选）`effort` 命令接口，以及 `position`、`velocity`、`effort` 状态接口 |
| `configure_arm_joints` | 关节 1 至 7，使用上文所列的初始位置 |
| `general_purpose_io` | 一个带单个命令接口和 `index` 参数的 GPIO 条目 |
| `cartesian_velocity_io` | 六个 `vx` ... `wz` GPIO 条目 |
| `cartesian_pose_loop` | 递归宏，生成 16 个 `cartesian_pose_command` GPIO 条目 |
| `configure_arm_interfaces` | 完整的单臂接口集：关节、笛卡尔速度、可选肘部、可选笛卡尔位姿、可选传感器 |

### 在机器人描述中使用宏

单臂入口文件 `diana_bringup/urdf/diana_arm.urdf.xacro` 包含该宏并选择插件：

```xml
<xacro:diana_arm_ros2_control
    robot_type="$(arg robot_type)"
    include_effort_command="true"
    arm_prefix="${modified_prefix}"
    is_async="$(arg is_async)"
    thread_priority="$(arg thread_priority)">
  <hardware_plugin>
    <xacro:if value="$(arg use_fake_hardware)">
      <plugin>mock_components/GenericSystem</plugin>
      <param name="mock_sensor_commands">$(arg fake_sensor_commands)</param>
      <param name="state_following_offset">0.0</param>
    </xacro:if>
    <xacro:unless value="$(arg use_fake_hardware)">
      <plugin>diana_hardware/DianaHardwareInterface</plugin>
      <param name="robot_ip">$(arg robot_ip)</param>
      <param name="arm_prefix">${modified_prefix}</param>
    </xacro:unless>
  </hardware_plugin>
</xacro:diana_arm_ros2_control>
```

`robot_type`（必填，取值 `diana3`、`diana7` 或 `diana7g2`，与所用机型一致）、`arm_prefix`、`robot_ip` 和 `use_fake_hardware` 是该文件的 xacro 参数。`modified_prefix` 由 `diana_description` 软件包根据 `arm_prefix` 派生，该包不在本软件包内。设置 `use_fake_hardware:=true` 时使用通用 mock 系统代替 `DianaHardwareInterface`，不会连接机器人。

## 配置

### 硬件插件参数

插件在 `on_init` 中从 `hardware` 块读取以下参数：

| 参数 | 必需 | 说明 |
| --- | --- | --- |
| `version` | 是 | `ros2_control` 接口描述版本，格式 `major.minor.patch`。主版本必须为 `1`，否则初始化失败，并提示更新 URDF（`diana_description`） |
| `robot_ip` | 是 | 机器人主机名或 IP 地址；缺失或无法建立连接时初始化失败 |
| `robot_type` | 是 | 取值 `diana3`、`diana7` 或 `diana7g2`，必须与所连机器人上报的机器人名称一致，否则初始化失败 |
| `prefix` | 否 | 机器人级接口名前缀（`<P><T>/robot_state` 等）；未设置时为空。bringup 的 xacro 宏根据 `arm_prefix` 设置它 |


`on_init` 期间，插件还会在自己的执行器线程中启动两个 ROS 2 节点（见下文参数服务与动作服务两节）。

### 命令限速与滤波

`robot.hpp` 中以编译期固定值给出了可选的命令后处理默认设置，没有对应的 ROS 参数：

| 设置 | 默认值 |
| --- | --- |
| 力矩命令限速 | 开 |
| 关节速度限速 | 关 |
| 关节位置限速与低通滤波 | 关 |
| 笛卡尔速度限速与低通滤波 | 关 |
| 笛卡尔位姿限速与低通滤波 | 关 |
| 低通截止频率 | 100 Hz |

```{note}
如果进程没有运行在实时内核上，插件会打印提示并在关闭实时强制的情况下继续运行。强烈建议使用实时内核，参见[实时网络](../../../fci/realtime_network.md)。
```

## 参数服务

插件内运行一个名为 `service_server` 的节点，提供以下服务。消息定义见 [diana_msgs](diana_msgs.md)。服务名带有启动时的命名空间：下表按不带命名空间的名称列出，用 `diana.config.yaml` 默认的 `NS_1` 启动时是 `/NS_1/service_server/set_joint_stiffness` 这样的形式。

| 服务 | 类型 |
| --- | --- |
| `/service_server/set_joint_stiffness` | `diana_msgs/srv/SetJointStiffness` |
| `/service_server/set_cartesian_stiffness` | `diana_msgs/srv/SetCartesianStiffness` |
| `/service_server/set_tcp_frame` | `diana_msgs/srv/SetTCPFrame` |
| `/service_server/set_stiffness_frame` | `diana_msgs/srv/SetStiffnessFrame` |
| `/service_server/set_force_torque_collision_behavior` | `diana_msgs/srv/SetForceTorqueCollisionBehavior` |
| `/service_server/set_full_collision_behavior` | `diana_msgs/srv/SetFullCollisionBehavior` |
| `/service_server/set_load` | `diana_msgs/srv/SetLoad` |

每个响应都包含 `success` 和 `error` 字符串；底层库的异常会在其中报告，而不会使插件崩溃。

## 错误恢复

### 出错时的行为

- 读取机器人状态时若抛出控制异常，`read()` 会记录日志、停止当前控制会话并返回 `ERROR`。
- 任一命令值不是有限数时，`write()` 返回 `ERROR`。
- 在命令模式切换期间写入时若出现运行时错误，只记录警告并跳过本次写入，避免模式切换拖垮全部硬件。
- 启动控制会话（`initializeTorqueInterface` 及同类函数）时，若机器人报告控制异常，插件会执行一次自动错误恢复并重试一次。
- `on_deactivate` 会停止机器人控制会话。

```{important}
插件本身不会停用控制器。不要依赖 Humble 版本的 controller manager 在硬件报错后自动停用或重启控制器：出错后请自行检查控制器状态，并按下文步骤显式重新激活。
```

### 恢复步骤

```{warning}
重新激活运动控制器会再次向机器人下发指令。开始前请先排除出错原因，确认工作空间无人员和障碍物、急停触手可及。不要在循环中反复尝试恢复，参见[安全边界](../../../reference/safety.md)。
```

1. 查明机器人停止的原因（[机器人状态](diana_robot_state_broadcaster.md)中的 `robot_mode`、`current_errors`、`last_motion_errors` 字段）并排除。
2. 检查哪些控制器仍处于激活状态（机器人运行在命名空间下时，所有 `ros2 control` 命令都要加 `-c /<namespace>/controller_manager`）：

   ```bash
   ros2 control list_controllers
   ```

3. 停用此前运行的运动控制器，以便之后重新申请接口（机器人运行在命名空间下时使用 `-c /<namespace>/controller_manager`）：

   ```bash
   ros2 control switch_controllers --deactivate <controller-name>
   ```

4. 发送错误恢复目标（带命名空间时动作名前加命名空间，下例按 `NS_1` 书写）：

   ```bash
   ros2 action send_goal /NS_1/action_server/error_recovery diana_msgs/action/ErrorRecovery {}
   ```

5. 重新激活控制器：

   ```bash
   ros2 control switch_controllers --activate <controller-name>
   ```

6. 用 `ros2 control list_hardware_components` 确认硬件组件处于 `active` 状态。

### 动作服务

节点 `action_server` 提供一个动作：

| 动作 | 类型 | 行为 |
| --- | --- | --- |
| `/action_server/error_recovery` | `diana_msgs/action/ErrorRecovery` | 接受所有目标并执行机器人的自动错误恢复；恢复返回即目标成功，抛出异常则目标中止。目标、结果和反馈均为空 |

```{note}
这两个节点由插件在 `ros2_control_node` 进程内创建，名称带有启动时的命名空间。例如用 `diana.config.yaml` 默认的 `NS_1` 启动时，服务是 `/NS_1/service_server/...`，动作是 `/NS_1/action_server/error_recovery`。可以用下面的命令查看实际名称：

~~~bash
ros2 service list | grep service_server
ros2 action list | grep action_server
~~~
```

## 与控制器配合使用

控制器在 `command_interface_configuration()` 中申请接口。插件根据所申请的命令接口推断控制模式，优先级如下：

| 申请的命令接口 | 控制模式 |
| --- | --- |
| 全部 7 个关节的 `effort` | 关节力矩 |
| 全部 7 个关节的 `velocity` | 关节速度 |
| 全部 7 个关节的 `position` | 关节位置 |
| 16 个 `cartesian_pose_command`（+ 2 个 `elbow_command`） | 笛卡尔位姿（可带肘部） |
| 6 个 `cartesian_velocity`（+ 2 个 `elbow_command`） | 笛卡尔速度（可带肘部） |

`prepare_command_mode_switch` 强制执行的规则：

- 一组接口必须整组申请或整组释放（7、6、16 或 2 个）。只申请一部分会报出类似 `Invalid number of ... interfaces to start` 的错误。
- 肘部命令必须与笛卡尔位姿或速度一起申请。
- 每次模式切换都会停止当前控制会话并启动新会话。位置、位姿和肘部模式下，插件会先用机器人当前状态初始化命令，在此之前忽略命令。

```{tip}
在控制器中请使用 [diana_semantic_components](diana_semantic_components.md) 中的类（`DianaRobotState`、`DianaRobotModel`、`DianaCartesianPoseInterface`、`DianaCartesianVelocityInterface`），而不是列出原始接口名；它们会为你生成带前缀的正确名称。
```

查看当前插件导出的内容：

```bash
ros2 control list_hardware_interfaces
ros2 control list_hardware_components
```

```{note}
本页的代码片段改编自 `diana_ros2`，其源码沿用了 franka_ros2 的结构并带有 Franka Robotics GmbH 的版权声明（Copyright (c) 2023 Franka Robotics GmbH，Apache License 2.0）；改编部分 Copyright (c) 2026 Agile Robots SE。详见[手册概述](/about/overview.md)中的“许可证与第三方声明”。
```

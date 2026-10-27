# 示例控制器

软件包名称：`franka_example_controllers`

`franka_example_controllers` 是一组基于 `ros2_control` 的示例控制器插件，演示如何在 Diana 硬件接口上实现关节力矩、关节位置/速度、笛卡尔位姿/速度和肘部控制，以及如何读取机器人模型。它们是学习和参考用的示例，不是面向生产的控制器。

```{note}
本包改编自 Franka Robotics 的 `franka_ros2`，保留了 `franka_` 前缀的包名。第三方声明见手册的 NOTICE。
```

## 安装

请参阅 [开发准备](../development.md)。

## 软件包概述

该包编译为一个控制器插件库 `franka_example_controllers`，插件类型登记在 `franka_example_controllers.xml` 中，基类为 `controller_interface::ControllerInterface`。控制器名称与类型的对应关系、更新频率和增益参数由 [diana_bringup](diana_bringup.md) 的 `config/controllers.yaml` 提供：控制器管理器的 `update_rate` 为 `1000`（Hz），`thread_priority` 为 `97`。

示例控制器通过 [franka_semantic_components](franka_semantic_components.md) 访问笛卡尔位姿、笛卡尔速度、力/力矩和机器人模型接口，通过 [franka_msgs](franka_msgs.md) 调用 [franka_hardware](franka_hardware.md) 的服务。包依赖 `pinocchio`；关节阻抗 IK 示例还依赖 MoveIt（`moveit_core`、`moveit_msgs`）。

除控制器插件外，包里还有一个可执行文件 `ptp_motion_example_node`（见下文），它是普通节点，不是控制器。

## 启动示例控制器

### 单臂示例

单臂示例通过 [diana_bringup](diana_bringup.md) 的 `diana.example_controllers.launch.py` 启动。该启动文件从机器人配置文件读取机型和 IP（默认读取 `diana_bringup/config/diana.config.yaml`），启动机器人描述、`ros2_control_node`、`joint_state_broadcaster` 等基础节点，再用 `spawner` 加载 `controller_names` 指定的控制器。

| 启动参数 | 默认值 | 说明 |
|---|---|---|
| `controller_names` | 无（必填） | 要加载的控制器名称，多个名称用逗号分隔，每个名称对应配置文件中的一台机器人 |
| `robot_config_file` | `diana.config.yaml` | 配置文件名（在 `diana_bringup/config/` 中查找）或完整路径 |
| `robot_ips` | 空 | 可选，逗号分隔的 IP 列表，非空时覆盖配置文件中的 `robot_ip` |

机型 `robot_type`（`diana3`、`diana7` 或 `diana7g2`）和 `robot_ip` 都来自配置文件，运行前必须改成自己的值。建议把默认配置文件复制一份再修改：

```bash
cp $(ros2 pkg prefix diana_bringup)/share/diana_bringup/config/diana.config.yaml ~/diana_ros2_ws/my_robot.config.yaml
```

在副本里至少设置 `robot_type`、`robot_ip`；连接真实机器人时把 `use_fake_hardware` 设为 `"false"`（布尔值必须加引号），其余键保持默认文件中的写法。之后用下面的命令启动，把 `<控制器名称>` 替换为下文各小节中的名称：

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
    robot_config_file:=$HOME/diana_ros2_ws/my_robot.config.yaml \
    robot_ips:=192.168.10.75 \
    controller_names:=<控制器名称>
```

Diana 机器人的默认 IP 是 `192.168.10.75`（控制器 A 网口）。配置文件中的 `namespace` 键不为空时，控制器、服务和话题都位于该命名空间下，见下一节。

名称中含 `controller` 的项由 `spawner` 作为 `ros2_control` 控制器加载；不含 `controller` 的项（例如 `ptp_motion_example_node`）作为普通节点运行。

### 关节阻抗 IK 示例

`joint_impedance_with_ik_example_controller` 需要 MoveIt 的 `compute_ik` 服务，该服务由 [diana_moveit_config](diana_moveit_config.md) 的 `move_group` 提供，使用前必须先保证它可用。控制器本身的接口、参数和前提见下文对应的小节。

### Diana Duo 示例

双臂示例 `diana_duo_joint_impedance_example_controller` 通过 `diana_duo.launch.py` 启动，参数 `controller_name`（单数，一次只加载一个控制器）和 `robot_config_file`（默认 `diana_duo.config.yaml`）：

```bash
ros2 launch diana_bringup diana_duo.launch.py \
    robot_config_file:=$HOME/diana_ros2_ws/my_duo.config.yaml \
    controller_name:=diana_duo_joint_impedance_example_controller
```

双臂配置文件中的 `robot_types`、`arm_prefixes`、`robot_ips` 是长度相同的字符串化列表（例如 `"['diana7','diana7']"`），`arm_prefixes` 中的值必须互不相同，启动前必须改成自己的机型和 IP。双臂配置当前只支持力矩（`effort`）命令接口。

## 接口与参数约定

各示例控制器共用下面的约定。

**接口名称。** 记 `<名称>` 为 `<arm_prefix>_<robot_type>`（`arm_prefix` 为空时只有 `<robot_type>`，例如 `diana7`）。关节接口为 `<名称>_joint1` 到 `<名称>_joint7` 下的 `position`、`velocity`、`effort`；机器人时间接口为 `<名称>/robot_time`。笛卡尔位姿、笛卡尔速度和肘部接口来自语义组件，名称为（`arm_prefix` 非空时在最前面加 `<arm_prefix>_`）：

| 接口 | 名称 |
|---|---|
| 位姿命令（16 个） | `0/cartesian_pose_command` 到 `15/cartesian_pose_command` |
| 位姿状态（16 个） | `0/cartesian_pose_state` 到 `15/cartesian_pose_state` |
| 速度命令（6 个） | `vx`、`vy`、`vz`、`wx`、`wy`、`wz` 下的 `cartesian_velocity` |
| 肘部命令（2 个） | `joint_3_position/elbow_command`、`joint_4_sign/elbow_command` |
| 肘部状态（2 个） | `joint_3_position/elbow_state`、`joint_4_sign/elbow_state` |

示例控制器都按 7 个关节编写。

**通用参数。** `arm_prefix`（字符串，默认空）几乎所有控制器都有；`robot_type` 由 `diana.launch.py` 设置在 `ros2_control_node` 上，部分控制器直接读取，部分控制器在配置阶段改为从 `robot_state_publisher` 的 `robot_description` 中解析机器人名称，因此机型必须与加载的模型一致。各控制器自己的参数见各小节。

**命名空间。** 控制器调用的服务使用相对名称，例如 `service_server/set_full_collision_behavior`；配置文件的 `namespace` 为空时即该名称，不为空时为 `/<namespace>/service_server/set_full_collision_behavior`。`diana_duo_joint_impedance_example_controller` 订阅的 `collision_detected` 话题同理。

**默认碰撞行为。** 笛卡尔、肘部、关节速度和关节阻抗 IK 示例在配置阶段会调用 `service_server/set_full_collision_behavior`（类型 `franka_msgs/srv/SetFullCollisionBehavior`），把碰撞阈值设为代码中的默认值：关节力矩下阈值（标称和加速度）`25, 25, 22, 20, 19, 17, 14` Nm，上阈值 `35, 35, 32, 30, 29, 27, 24` Nm；笛卡尔力下阈值 `30, 30, 30, 25, 25, 25`，上阈值 `40, 40, 40, 35, 35, 35`（力 N、力矩 Nm）。调用失败时配置失败，控制器不会激活。该服务由真实的 `franka_hardware` 提供。

```{warning}
除 `model_example_controller` 外，这些示例都会向机器人发送力矩、速度或位置指令，机械臂会真实运动。运行前请确认工作空间内无人员和障碍物、急停可随时触及、机器人处于允许外部控制的状态，并先阅读[安全边界](../../../reference/safety.md)；FCI 与网络前提见 [FCI 概览](../../../fci/overview.md)。首次运行请保持保守姿态，随时准备按下急停。
```

## 控制器列表

下表汇总全部示例，各控制器的详细说明见下面的小节。“额外前提”一栏列出除关节接口之外代码依赖的东西，这些由真实的 `franka_hardware`（或 MoveIt）提供。

| 示例控制器 | 说明 | 命令接口 | 额外前提 |
|---|---|---|---|
| <a href="#gravity-compensation-example-controller"><code>gravity_compensation_example_controller</code></a> | 零力矩重力补偿，打印外部力估计 | 关节 `effort` | TCP 力/力矩状态接口 |
| <a href="#joint-impedance-example-controller"><code>joint_impedance_example_controller</code></a> | 关节阻抗律，关节 4、5 周期运动 | 关节 `effort` | 无 |
| <a href="#joint-impedance-with-ik-example-controller"><code>joint_impedance_with_ik_example_controller</code></a> | MoveIt 逆解 + 关节阻抗律，末端画圆弧 | 关节 `effort` | `compute_ik`、碰撞行为服务、模型和位姿接口 |
| <a href="#joint-position-example-controller"><code>joint_position_example_controller</code></a> | 关节位置指令，周期偏移 | 关节 `position` | `robot_time` |
| <a href="#joint-velocity-example-controller"><code>joint_velocity_example_controller</code></a> | 关节速度指令，关节 4、5 往复 | 关节 `velocity` | 碰撞行为服务 |
| <a href="#cartesian-velocity-example-controller"><code>cartesian_velocity_example_controller</code></a> | 笛卡尔速度指令，x、z 方向往复 | 笛卡尔速度 | 碰撞行为服务 |
| <a href="#cartesian-pose-example-controller"><code>cartesian_pose_example_controller</code></a> | 笛卡尔位姿指令，x、z 平面圆弧 | 笛卡尔位姿 | 碰撞行为服务、`robot_time` |
| <a href="#cartesian-orientation-example-controller"><code>cartesian_orientation_example_controller</code></a> | 笛卡尔位姿指令，姿态绕 x 轴周期转动 | 笛卡尔位姿 | 碰撞行为服务、`robot_time` |
| <a href="#cartesian-elbow-example-controller"><code>cartesian_elbow_example_controller</code></a> | 保持末端位姿，肘部周期变化 | 笛卡尔位姿 + 肘部 | 碰撞行为服务、`robot_time` |
| <a href="#elbow-example-controller"><code>elbow_example_controller</code></a> | 速度模式下只活动肘部 | 笛卡尔速度 + 肘部 | 碰撞行为服务、`robot_time` |
| <a href="#model-example-controller"><code>model_example_controller</code></a> | 只读取并打印机器人模型 | 无 | 机器人模型接口 |
| <a href="#move-to-start-example-controller"><code>move_to_start_example_controller</code></a> | 平滑移动到起始关节配置 | 关节 `effort` | 无 |
| <a href="#diana-duo-joint-impedance-example-controller"><code>diana_duo_joint_impedance_example_controller</code></a> | 双臂关节阻抗，两臂关节 4、5 周期运动 | 两臂关节 `effort` | `collision_detected` 话题 |
| <a href="#ptp-motion-example-node"><code>ptp_motion_example_node</code></a> | 向 PTP 运动 action 发送一串关节目标（节点，不是控制器） | 无 | `action_server/ptp_motion` |

### `gravity_compensation_example_controller`

类型 `franka_example_controllers/GravityCompensationExampleController`。只向 7 个关节的 `effort` 接口写零力矩，让机器人只补偿自身重量，并每 1000 个控制周期打印一次刚度坐标系下的外部力和力矩估计。

- 命令接口：`<名称>_joint1` 到 `<名称>_joint7` 的 `effort`。
- 状态接口：`<名称>_tcp` 的力/力矩传感器接口（`force.x/y/z`、`torque.x/y/z`，`arm_prefix` 非空时在名称前加 `<arm_prefix>_`）。
- 参数：`robot_type`、`arm_prefix`（默认空）。

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
    robot_config_file:=$HOME/diana_ros2_ws/my_robot.config.yaml \
    robot_ips:=192.168.10.75 \
    controller_names:=gravity_compensation_example_controller
```

```{warning}
机械臂处于零力矩模式，不会主动保持位置，受力后会随之移动。请先支撑好机械臂和末端负载，并保持手在急停可达范围内。
```

### `joint_impedance_example_controller`

类型 `franka_example_controllers/JointImpedanceExampleController`。用关节阻抗律输出力矩，使关节 4 和关节 5 做幅值约 π/4 rad、周期 5 秒的缓慢运动，其余关节保持激活时的初始位置，整体较为柔顺。

- 命令接口：7 个关节的 `effort`。
- 状态接口：7 个关节的 `position` 和 `velocity`。
- 参数：`robot_type`、`arm_prefix`、`k_gains`、`d_gains`（各 7 个值，必须设置，长度不对或为空时配置失败）。`controllers.yaml` 中 `k_gains` 为 `24, 24, 24, 24, 10, 6, 2`，`d_gains` 为 `2, 2, 2, 1, 1, 1, 0.5`。

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
    robot_config_file:=$HOME/diana_ros2_ws/my_robot.config.yaml \
    robot_ips:=192.168.10.75 \
    controller_names:=joint_impedance_example_controller
```

```{warning}
该控制器输出力矩并使机械臂运动，请确认关节 4、5 的运动范围内没有障碍物。
```

### `joint_impedance_with_ik_example_controller`

类型 `franka_example_controllers/JointImpedanceWithIKExampleController`。让末端位置在 x、z 平面内沿半径 0.1 m 的圆弧运动（周期 10 秒），姿态保持不变。每个控制周期向 MoveIt 的 `compute_ik` 服务（`moveit_msgs/srv/GetPositionIK`）请求目标位姿的关节解，再用关节阻抗律加科氏力补偿输出力矩。请求中的规划组为 `<名称>_arm`，位姿参考坐标系为 `<名称>_link0`。

- 命令接口：7 个关节的 `effort`。
- 状态接口：笛卡尔位姿状态、7 个关节的 `position`、`velocity`、`effort`、机器人模型接口和 `robot_time`。
- 参数：`arm_prefix`、`k_gains`、`d_gains`。`controllers.yaml` 中 `k_gains` 为 `600, 600, 600, 600, 250, 150, 50`，`d_gains` 为 `30, 30, 30, 30, 10, 10, 5`。
- 前提：配置阶段会等待 `compute_ik` 和 `service_server/set_full_collision_behavior` 两个服务，最多约 10 秒，超时则配置失败，因此必须先启动 MoveIt 的 `move_group`。逆解器可在 [diana_moveit_config](diana_moveit_config.md) 的 `kinematics.yaml` 中更换。

```{warning}
该控制器输出力矩并使机械臂在笛卡尔空间内运动，需要真实硬件和可用的 `compute_ik` 服务。逆解失败时控制器沿用上一次得到的关节解。
```

### `joint_position_example_controller`

类型 `franka_example_controllers/JointPositionExampleController`。向 7 个关节的 `position` 接口写位置指令：在激活时的初始位置上叠加一个缓慢的周期偏移（最大约 π/40 rad，周期 10 秒），关节 5 的偏移方向与其余关节相反。

- 命令接口：7 个关节的 `position`。
- 状态接口：7 个关节的 `position` 和 `robot_time`。
- 参数：`arm_prefix`；`gazebo`（布尔，默认 `false`）为 `true` 时不读取 `robot_time`，改用控制周期累计计时，供仿真使用。

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
    robot_config_file:=$HOME/diana_ros2_ws/my_robot.config.yaml \
    robot_ips:=192.168.10.75 \
    controller_names:=joint_position_example_controller
```

```{warning}
该控制器让所有关节同时运动，请确认整个工作空间无障碍物。
```

### `joint_velocity_example_controller`

类型 `franka_example_controllers/JointVelocityExampleController`。向 7 个关节的 `velocity` 接口写速度指令：关节 4 和关节 5 以最大 0.1 rad/s、周期 8 秒的角速度运动，每个周期反向一次，其余关节速度为零。

- 命令接口：7 个关节的 `velocity`。
- 状态接口：7 个关节的 `position` 和 `velocity`。
- 参数：`arm_prefix`；`gazebo`（布尔，默认 `false`）为 `true` 时不调用碰撞行为服务。
- 配置阶段会设置默认碰撞行为（`gazebo` 为 `false` 时）。

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
    robot_config_file:=$HOME/diana_ros2_ws/my_robot.config.yaml \
    robot_ips:=192.168.10.75 \
    controller_names:=joint_velocity_example_controller
```

```{warning}
该控制器通过速度接口让机械臂运动，请确认关节 4、5 的运动范围内没有障碍物。
```

### `cartesian_velocity_example_controller`

类型 `franka_example_controllers/CartesianVelocityExampleController`。通过笛卡尔速度接口在 x、z 方向给出线速度：方向角 π/4，峰值 0.05 m/s，周期 4 秒，每个周期反向一次；角速度为零，不使用肘部接口。

- 命令接口：`vx`、`vy`、`vz`、`wx`、`wy`、`wz` 的 `cartesian_velocity`。
- 状态接口：无。
- 参数：`arm_prefix`。配置阶段会设置默认碰撞行为。

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
    robot_config_file:=$HOME/diana_ros2_ws/my_robot.config.yaml \
    robot_ips:=192.168.10.75 \
    controller_names:=cartesian_velocity_example_controller
```

```{warning}
末端会在 x、z 方向上往复运动，请确认末端周围有足够净空。
```

### `cartesian_pose_example_controller`

类型 `franka_example_controllers/CartesianPoseExampleController`。通过笛卡尔位姿指令让末端在 x、z 平面内沿半径 0.1 m 的圆弧运动（周期 10 秒），姿态保持激活时的初始值。

- 命令接口：16 个笛卡尔位姿命令接口。
- 状态接口：16 个笛卡尔位姿状态接口和 `robot_time`。
- 参数：`arm_prefix`。配置阶段会设置默认碰撞行为。

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
    robot_config_file:=$HOME/diana_ros2_ws/my_robot.config.yaml \
    robot_ips:=192.168.10.75 \
    controller_names:=cartesian_pose_example_controller
```

```{warning}
末端会在 x、z 方向上运动约 0.1 m，请确认末端周围有足够净空。
```

### `cartesian_orientation_example_controller`

类型 `franka_example_controllers/CartesianOrientationExampleController`。通过笛卡尔位姿指令保持末端位置不变，使末端姿态绕基坐标系 x 轴做最大约 π/4 rad、周期 10 秒的周期转动。

- 命令接口：16 个笛卡尔位姿命令接口。
- 状态接口：16 个笛卡尔位姿状态接口和 `robot_time`。
- 参数：`arm_prefix`。配置阶段会设置默认碰撞行为。

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
    robot_config_file:=$HOME/diana_ros2_ws/my_robot.config.yaml \
    robot_ips:=192.168.10.75 \
    controller_names:=cartesian_orientation_example_controller
```

```{warning}
末端姿态会发生明显转动，请确认末端工具和线缆周围有足够空间。
```

### `cartesian_elbow_example_controller`

类型 `franka_example_controllers/CartesianElbowExampleController`。通过笛卡尔位姿指令保持末端位姿不变，同时让肘部（`joint_3_position`）在初始值附近周期变化（最大偏移约 2π/15 rad，周期 10 秒），即只活动零空间。`controllers.yaml` 中还有一个使用同一类型的名称 `cartesian_pose_elbow_example_controller`，用法相同。

- 命令接口：16 个笛卡尔位姿命令接口和 2 个肘部命令接口。
- 状态接口：16 个笛卡尔位姿状态接口、2 个肘部状态接口和 `robot_time`。
- 参数：`arm_prefix`。配置阶段会设置默认碰撞行为。

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
    robot_config_file:=$HOME/diana_ros2_ws/my_robot.config.yaml \
    robot_ips:=192.168.10.75 \
    controller_names:=cartesian_elbow_example_controller
```

```{warning}
肘部会明显摆动，请确认肘部周围有足够空间。该控制器需要真实硬件的肘部命令接口。
```

### `elbow_example_controller`

类型 `franka_example_controllers/ElbowExampleController`。通过笛卡尔速度接口给出零线速度和零角速度，同时让肘部位置做与 `cartesian_elbow_example_controller` 相同的周期变化，即在速度模式下活动零空间。

- 命令接口：6 个笛卡尔速度命令接口和 2 个肘部命令接口。
- 状态接口：2 个肘部状态接口和 `robot_time`。
- 参数：`arm_prefix`。配置阶段会设置默认碰撞行为。

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
    robot_config_file:=$HOME/diana_ros2_ws/my_robot.config.yaml \
    robot_ips:=192.168.10.75 \
    controller_names:=elbow_example_controller
```

```{warning}
肘部会明显摆动，请确认肘部周围有足够空间。该控制器需要真实硬件的肘部命令接口。
```

### `model_example_controller`

类型 `franka_example_controllers/ModelExampleController`。不发送任何指令，只读取机器人模型接口，约每秒打印一次质量矩阵、科氏力向量、重力向量、关节 4 的位姿、关节 4 的体雅可比和末端相对基坐标系的雅可比，演示如何使用 `FrankaRobotModel` 语义组件。

- 命令接口：无。
- 状态接口：`<名称>/robot_model` 和 `<名称>/robot_state` 对应的机器人模型接口。
- 参数：`robot_type`、`arm_prefix`（默认空）。

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
    robot_config_file:=$HOME/diana_ros2_ws/my_robot.config.yaml \
    robot_ips:=192.168.10.75 \
    controller_names:=model_example_controller
```

### `move_to_start_example_controller`

类型 `franka_example_controllers/MoveToStartExampleController`。用关节阻抗律输出力矩，把机械臂平滑移动到起始关节配置：运动由 `MotionGenerator` 生成，速度和加速度限制取最大值的 0.2 倍。到达后输出零力矩，并把参数 `process_finished` 设为 `true`，控制器保持激活。

- 命令接口：7 个关节的 `effort`。
- 状态接口：7 个关节的 `position` 和 `velocity`。
- 参数：

| 参数 | 默认值 | 说明 |
|---|---|---|
| `robot_type` | `diana7` | 机器人型号，用于组成接口名称 |
| `arm_prefix` | 空 | 机械臂前缀 |
| `k_gains`、`d_gains` | 空，必须设置 | 各 7 个值，`controllers.yaml` 中分别为 `600, 600, 600, 600, 250, 150, 50` 和 `30, 30, 30, 30, 10, 10, 5` |
| `start_joint_configuration` | `-π/4, 0, 0, π/2, 0, -π/2, π/4` | 目标关节角（rad） |
| `process_finished` | `false` | 运动结束后由控制器置为 `true` |

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
    robot_config_file:=$HOME/diana_ros2_ws/my_robot.config.yaml \
    robot_ips:=192.168.10.75 \
    controller_names:=move_to_start_example_controller
```

```{warning}
机械臂会从当前姿态运动到目标姿态，所有关节都可能大幅运动，请确认全部工作空间无障碍物。默认目标关节角是代码中的固定值，运行前请确认它适合你的机型，必要时在 `controllers.yaml` 中修改 `start_joint_configuration`。运动结束后控制器输出零力矩，请做好支撑准备。
```

### `diana_duo_joint_impedance_example_controller`

类型 `franka_example_controllers/DianaDuoJointImpedanceExampleController`。对双臂系统的两条机械臂同时运行关节阻抗律，两臂的关节 4、5 各自做与 `joint_impedance_example_controller` 相同的周期运动。控制器还订阅 `collision_detected`（`std_msgs/msg/Bool`，`SensorDataQoS`），把它当作自碰撞检测的结果：激活时必须已有发布者，运行中超过 0.5 秒没有收到消息或收到 `true` 都会使控制器返回错误并停止。

- 命令接口：两臂各 7 个关节的 `effort`，名称为 `<arm_prefix>_<robot_type>_joint<i>/effort`。
- 状态接口：两臂各 7 个关节的 `position` 和 `velocity`。
- 参数：`robot_types`、`arm_prefixes`（字符串数组，由 `diana_duo.launch.py` 从配置文件设置）；`k_gains`、`d_gains`（各 7 个值，两臂共用）。`controllers.yaml` 中 `k_gains` 为 `24, 24, 24, 24, 10, 6, 2`，`d_gains` 为 `2, 2, 2, 1, 1, 1, 0.5`，`update_rate` 为 `1000`。
- 前提：`collision_detected` 话题需要有发布者，发布者见 [diana_selfcollision](diana_selfcollision.md)；该话题名称是相对名称，需与控制器处于同一命名空间。

```bash
ros2 launch diana_bringup diana_duo.launch.py \
    robot_config_file:=$HOME/diana_ros2_ws/my_duo.config.yaml \
    controller_name:=diana_duo_joint_impedance_example_controller
```

```{warning}
两臂会同时运动，请确认两臂各自的工作空间以及两臂之间没有人员和障碍物。没有自碰撞检测发布者时控制器无法激活。
```

### `ptp_motion_example_node`

可执行文件 `ptp_motion_example_node`（节点名 `ptp_motion_example`），不是控制器插件。它作为 action 客户端，向 `action_server/ptp_motion`（类型 `franka_msgs/action/PTPMotion`，由 [franka_hardware](franka_hardware.md) 提供）依次发送目标：先发送固定的初始关节配置 `-0.5, -π/4, 0, -3π/4, 0, π/2, π/4`（rad），再发送 20 个目标，在关节 1、关节 3 上交替向两侧移动（幅度逐次增大），最后一个目标把这两个关节回到 0。所有目标的最大关节速度为 1.0 rad/s，容差 0.01。

由于名称不含 `controller`，用 `diana.example_controllers.launch.py` 启动时它作为普通节点运行，不需要控制器：

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
    robot_config_file:=$HOME/diana_ros2_ws/my_robot.config.yaml \
    robot_ips:=192.168.10.75 \
    controller_names:=ptp_motion_example_node
```

```{warning}
目标关节配置和运动幅度是写在代码中的固定值，机械臂会大幅运动。运行前请确认这些关节角适合你的机型，全部工作空间无人员和障碍物，并保持急停可随时触及。
```

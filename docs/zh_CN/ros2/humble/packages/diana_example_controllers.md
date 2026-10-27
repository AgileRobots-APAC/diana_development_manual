# 示例控制器

软件包名称：`diana_example_controllers`

`diana_example_controllers` 是一组基于 `ros2_control` 的示例控制器插件，演示如何在 Diana 硬件接口上实现关节、笛卡尔和肘部控制，以及如何读取机器人模型。它们是学习和参考用的示例，不是面向生产的控制器。

## 安装

请参阅 [开发准备](../development.md)。

## 软件包概述

该包编译为一个控制器插件库 `diana_example_controllers`，插件类型登记在 `diana_example_controllers.xml` 中，基类为 `controller_interface::ControllerInterface`。控制器名称与类型的对应关系、更新频率和增益参数都由 [diana_bringup](diana_bringup.md) 的 `config/controllers.yaml` 提供：控制器管理器的 `update_rate` 为 `1000`（Hz），`thread_priority` 为 `98`。

示例控制器通过 `diana_semantic_components` 访问笛卡尔位姿、笛卡尔速度和机器人模型接口，通过 `diana_msgs` 调用 `diana_hardware` 的参数服务。它们依赖 `pinocchio`；关节阻抗 IK 示例还依赖 MoveIt。

## 控制器列表

所有示例都通过同一种方式启动，把 `<控制器名称>` 替换为下面各小节中的名称（在命令中写作 `controller_names:=...`）：

```bash
ros2 launch diana_bringup example.launch.py controller_names:=gravity_compensation_example_controller
```

`example.launch.py` 的参数、命名空间与多机器人用法见 [diana_bringup](diana_bringup.md)。该启动文件从 `diana.config.yaml` 读取机器人配置，运行前请先把其中的 `robot_type` 改成自己的机型（`diana3`、`diana7` 或 `diana7g2`）。

```{warning}
除 `model_example_controller` 之外，这些控制器都会向机器人发送力矩、速度或位置指令，机械臂会真实运动。运行前请确认工作空间内无人员和障碍物、急停可随时触及、机器人处于允许外部控制的状态，并先阅读[安全边界](../../../reference/safety.md)；FCI 与网络前提见 [FCI 概览](../../../fci/overview.md)。首次运行请保持保守姿态，随时准备按下急停。
```

```{note}
按 `example.launch.py` 文件头注释，肘部和笛卡尔类示例会调用服务（例如 `set_full_collision_behavior`）并使用 `robot_time`、`elbow_state` 等接口，这些只由真实的 `diana_hardware` 提供，需要 `use_fake_hardware` 为 `"false"` 且机器人可达；使用 `mock_components` 模拟硬件时，注释建议使用关节层面的示例（`gravity_compensation_example_controller`、`joint_impedance_example_controller`）。下文没有特别说明时，均按需要真实硬件对待。
```

```{note}
`cartesian_*`、`joint_impedance_*` 等源码位于 `src/diana3/` 目录，但除各 `*_move_to_start_example_controller` 外，代码并不检查机型；它们按 7 个关节编写，机器人名称取自 `robot_description`（或启动时传入的 `robot_type` 参数）。
```

下表汇总全部示例控制器，各控制器的详细说明见下面的小节：

| 示例控制器 | 说明 | 需要实机 |
|---|---|---|
| <a href="#gravity-compensation-example-controller"><code>gravity_compensation_example_controller</code></a> | 零力矩重力补偿悬停，打印外部力估计 | 否（可在假硬件运行） |
| <a href="#joint-impedance-example-controller"><code>joint_impedance_example_controller</code></a> | 关节阻抗律，关节 4、5 缓慢周期运动 | 否（可在假硬件运行） |
| <a href="#joint-impedance-with-ik-example-controller"><code>joint_impedance_with_ik_example_controller</code></a> | 经 MoveIt `compute_ik` 求解，末端在 x、z 方向画圆弧 | 是 |
| <a href="#joint-position-example-controller"><code>joint_position_example_controller</code></a> | 关节位置指令，周期偏移 | 是 |
| <a href="#joint-velocity-example-controller"><code>joint_velocity_example_controller</code></a> | 关节速度指令，关节 4、5 往复 | 是 |
| <a href="#cartesian-velocity-example-controller"><code>cartesian_velocity_example_controller</code></a> | 笛卡尔速度指令，x、z 方向往复 | 是 |
| <a href="#cartesian-pose-example-controller"><code>cartesian_pose_example_controller</code></a> | 笛卡尔位姿指令，x、z 方向圆弧 | 是 |
| <a href="#cartesian-orientation-example-controller"><code>cartesian_orientation_example_controller</code></a> | 笛卡尔位姿指令，姿态绕 x 轴周期转动 | 是 |
| <a href="#cartesian-elbow-example-controller"><code>cartesian_elbow_example_controller</code></a> | 保持末端位姿，肘部（零空间）周期变化 | 是 |
| <a href="#elbow-example-controller"><code>elbow_example_controller</code></a> | 速度模式下仅活动肘部（零空间） | 是 |
| <a href="#model-example-controller"><code>model_example_controller</code></a> | 只读取机器人模型并打印，不发送指令 | 是（需要模型接口） |
| <a href="#diana3-move-to-start-example-controller"><code>diana3_move_to_start_example_controller</code></a> | 平滑移动到起始关节配置，仅 `diana3` | 是 |
| <a href="#diana7-move-to-start-example-controller"><code>diana7_move_to_start_example_controller</code></a> | 平滑移动到起始关节配置，仅 `diana7` | 是 |
| <a href="#diana7g2-move-to-start-example-controller"><code>diana7g2_move_to_start_example_controller</code></a> | 平滑移动到起始关节配置，仅 `diana7g2` | 是 |

### `gravity_compensation_example_controller`

只向 7 个关节的 `effort` 接口写零力矩，让机器人由内部重力补偿悬停（机械臂可被手推动），并每 100 个控制周期打印一次刚度坐标系下的外部力和力矩估计。需要 `<robot_type>_tcp` 力/力矩传感器状态接口。

```bash
ros2 launch diana_bringup example.launch.py controller_names:=gravity_compensation_example_controller
```

```{warning}
机械臂处于零力矩模式，不会主动保持位置，受力后会随之移动。请先支撑好机械臂和末端负载，并保持手在急停可达范围内。
```

### `joint_impedance_example_controller`

用关节阻抗律输出力矩，使关节 4 和关节 5 做幅值约 π/8 rad 的缓慢周期运动，其余关节保持初始位置。`k_gains` 和 `d_gains`（各 7 个值）从 `controllers.yaml` 读取，默认 `k_gains` 为 `50, 50, 50, 50, 20, 10, 5`，`d_gains` 为 `4, 4, 4, 2, 2, 2, 1`，即较为柔顺。

```bash
ros2 launch diana_bringup example.launch.py controller_names:=joint_impedance_example_controller
```

```{warning}
该控制器输出力矩并使机械臂运动，请确认关节 4、5 的运动范围内没有障碍物。
```

### `joint_impedance_with_ik_example_controller`

让末端位置在 x、z 方向上画出半径 0.1 m 的小幅圆弧轨迹，通过 MoveIt 的 `compute_ik` 服务（OrocosKDL LMA）求解逆运动学，再用关节阻抗律加科氏力补偿输出力矩。默认增益在 `controllers.yaml` 中，`k_gains` 为 `600, 600, 600, 600, 250, 150, 50`，`d_gains` 为 `30, 30, 30, 30, 10, 10, 5`。它需要 `compute_ik` 和 `set_full_collision_behavior` 服务可用，因此要使用专门的启动文件，该文件会同时启动 MoveIt：

```bash
ros2 launch diana_bringup joint_impedance_with_ik_example_controller.launch.py
```

```{warning}
该控制器输出力矩并使机械臂在笛卡尔空间内运动，需要真实硬件和可用的 `compute_ik` 服务。启动文件的细节与前提见 [diana_bringup](diana_bringup.md)。
```

### `joint_position_example_controller`

向 7 个关节的 `position` 接口写位置指令：在初始位置基础上叠加一个缓慢的周期偏移，关节 4、5 与其余关节的偏移方向相反。使用 `robot_time` 状态接口计时；参数 `gazebo`（默认 `false`）用于 Gazebo 仿真，此时改用控制周期计时。

```bash
ros2 launch diana_bringup example.launch.py controller_names:=joint_position_example_controller
```

```{warning}
该控制器让所有关节同时运动，请确认整个工作空间无障碍物。
```

### `joint_velocity_example_controller`

向 7 个关节的 `velocity` 接口写速度指令：关节 4 和关节 5 以最大 0.1 rad/s、周期 8 秒的往复角速度反向运动，其余关节速度为零。参数 `gazebo`（默认 `false`）与位置示例相同。

```bash
ros2 launch diana_bringup example.launch.py controller_names:=joint_velocity_example_controller
```

```{warning}
该控制器通过速度接口让机械臂运动，请确认关节 4、5 的运动范围内没有障碍物。
```

### `cartesian_velocity_example_controller`

通过笛卡尔速度 GPIO 接口给出 x 和 z 方向的线速度（方向角 π/4，最大 0.05 m/s，每 4 秒反向一次），角速度为零。

```bash
ros2 launch diana_bringup example.launch.py controller_names:=cartesian_velocity_example_controller
```

```{warning}
末端会在 x、z 方向上往复运动，请确认末端周围有足够净空。
```

### `cartesian_pose_example_controller`

通过笛卡尔位姿指令让末端在 x、z 方向上沿半径 0.1 m 的圆弧运动（周期约 10 秒），姿态保持不变。

```bash
ros2 launch diana_bringup example.launch.py controller_names:=cartesian_pose_example_controller
```

```{warning}
末端会在 x、z 方向上运动约 0.1 m，请确认末端周围有足够净空。
```

### `cartesian_orientation_example_controller`

通过笛卡尔位姿指令保持末端位置不变，使末端姿态绕 x 轴做最大约 π/4 rad 的周期转动。

```bash
ros2 launch diana_bringup example.launch.py controller_names:=cartesian_orientation_example_controller
```

```{warning}
末端姿态会发生明显转动，请确认末端工具和线缆周围有足够空间。
```

### `cartesian_elbow_example_controller`

通过笛卡尔位姿指令保持末端位姿不变，同时让肘部（关节 3 位置）在初始值附近周期变化（最大偏移约 2π/15 rad），即只活动零空间。`controllers.yaml` 里还有一个同类型的别名 `cartesian_pose_elbow_example_controller`，两者使用同一个类。

```bash
ros2 launch diana_bringup example.launch.py controller_names:=cartesian_elbow_example_controller
```

```{warning}
肘部会明显摆动，请确认肘部周围有足够空间。该控制器需要真实硬件的肘部指令接口。
```

### `elbow_example_controller`

通过笛卡尔速度接口给出零线速度和零角速度，同时让肘部位置做与 `cartesian_elbow_example_controller` 相同的周期变化，即用速度模式活动零空间。

```bash
ros2 launch diana_bringup example.launch.py controller_names:=elbow_example_controller
```

```{warning}
肘部会明显摆动，请确认肘部周围有足够空间。该控制器需要真实硬件的肘部指令接口。
```

### `model_example_controller`

不发送任何指令，只读取机器人模型接口，约每秒打印一次质量矩阵、科氏力向量、重力向量、关节 4 的位姿和雅可比，以及末端雅可比，用来演示如何使用 `DianaRobotModel`。若指定的 `robot_type` 与加载的 `robot_description` 不一致，配置会失败。

```bash
ros2 launch diana_bringup example.launch.py controller_names:=model_example_controller
```

### `diana3_move_to_start_example_controller`

用关节阻抗律输出力矩，把机械臂平滑移动到起始关节配置（参数 `start_joint_configuration`，默认 `0, -π/4, 0, 3π/4, 0, π/2, 0`；运动速度限制取最大值的 0.2 倍）。到达后输出零力矩，并把参数 `process_finished` 设为 `true`。仅支持 `robot_type` 为 `diana3` 的机器人，否则配置失败；`k_gains`、`d_gains` 必须各为 7 个值（`controllers.yaml` 已提供）。

```bash
ros2 launch diana_bringup example.launch.py controller_names:=diana3_move_to_start_example_controller
```

```{warning}
机械臂会从当前姿态运动到起始姿态，路径上的所有关节都可能大幅运动，请确认全部工作空间无障碍物。
```

### `diana7_move_to_start_example_controller`

与上一个控制器相同，但仅支持 `robot_type` 为 `diana7` 的机器人，默认起始配置为 `0, -π/4, 0, 3π/4, 0, -π/2, 0`（关节 6 的符号与 Diana3 不同）。

```bash
ros2 launch diana_bringup example.launch.py controller_names:=diana7_move_to_start_example_controller
```

```{warning}
机械臂会从当前姿态运动到起始姿态，请确认全部工作空间无障碍物。
```

### `diana7g2_move_to_start_example_controller`

与上一个控制器相同，但仅支持 `robot_type` 为 `diana7g2` 的机器人，默认起始配置为 `0, -π/4, 0, 3π/4, 0, π/2, 0`。

```bash
ros2 launch diana_bringup example.launch.py controller_names:=diana7g2_move_to_start_example_controller
```

```{warning}
机械臂会从当前姿态运动到起始姿态，请确认全部工作空间无障碍物。
```

## 编写自定义控制器

自定义控制器需要在 `command_interface_configuration()` 和 `state_interface_configuration()` 中列出所需的接口名称。Diana 硬件接口实际提供的接口由 `diana_hardware/ros2_control/diana_arm.ros2_control.xacro` 与硬件接口源码决定（下表中 `arm_prefix` 为 `arm_prefix` 参数加下划线，无前缀时为空）。

| 接口 | 名称 | 说明 |
| --- | --- | --- |
| 关节命令 | `<robot_type>_joint<1..7>/position`、`/velocity`、`/effort` | 关节位置、速度、力矩；`diana_bringup` 的 xacro 默认包含力矩命令 |
| 关节状态 | `<robot_type>_joint<1..7>/position`、`/velocity`、`/effort` | 关节状态 |
| 笛卡尔速度命令 | `vx`、`vy`、`vz`、`wx`、`wy`、`wz`（均带 `arm_prefix`）下的 `cartesian_velocity` | 6 个 GPIO 条目 |
| 笛卡尔位姿命令 | `0` 到 `15`（带 `arm_prefix`）下的 `cartesian_pose_command` | 16 个 GPIO 条目，4x4 位姿矩阵 |
| 肘部命令 | `joint_3_position`、`joint_4_sign`（带 `arm_prefix`）下的 `elbow_command` | 必须与笛卡尔位姿或速度命令同时占用 |
| 笛卡尔位姿状态 | `0` 到 `15`（带 `arm_prefix`）下的 `cartesian_pose_state` | 当前位姿矩阵 |
| 肘部状态 | `joint_3_position`、`joint_4_sign`（带 `arm_prefix`）下的 `elbow_state` | 当前肘部配置 |
| 机器人状态与模型 | `arm_prefix` + `<robot_type>` 下的 `robot_state`、`robot_model`、`robot_time` | 完整机器人状态、动力学模型句柄和机器人时间 |
| 力/力矩传感器 | `arm_prefix` + `<robot_type>_tcp` 下的 `force.x`、`force.y`、`force.z`、`torque.x`、`torque.y`、`torque.z` | 刚度坐标系下估计的外部力和力矩 |

```{important}
`robot_state`、`robot_model` 和 `robot_time` 等状态接口，以及肘部和笛卡尔 GPIO 的实际行为，由 `diana_hardware/DianaHardwareInterface` 提供。模拟硬件（`mock_components/GenericSystem`）不提供这些接口，依赖它们的控制器只能在真实硬件上运行。硬件接口的细节见 [diana_hardware](diana_hardware.md)。
```

```{important}
`robot_state`、`robot_model` 这类句柄型接口不能直接当作普通的 `double` 使用，也不建议自己拼装位姿、肘部和模型接口的名称。请使用 `diana_semantic_components` 提供的语义组件（`DianaRobotState`、`DianaRobotModel`、`DianaCartesianPoseInterface`、`DianaCartesianVelocityInterface`），它们负责生成接口名称并读写这些数据，示例控制器就是这样用的。参见 [diana_semantic_components](diana_semantic_components.md)。机器人状态也可以通过 [diana_robot_state_broadcaster](diana_robot_state_broadcaster.md) 以话题形式获得。
```

编写时可参考示例控制器的做法：

- 在 `on_init()` 中声明 `arm_prefix` 等参数，在 `on_configure()` 中读取；
- 机器人名称从 `robot_state_publisher` 的 `robot_description` 参数解析，使接口名称与已加载的模型一致；
- 在 `on_activate()` 中用语义组件的 `assign_loaned_*_interfaces()` 绑定接口，在 `on_deactivate()` 中 `release_interfaces()`；
- 需要设置碰撞行为等非实时参数时，通过 `service_server/...` 服务调用（见 [diana_bringup](diana_bringup.md)）；
- 同一时刻 `diana_hardware` 只接受一种控制模式，设计控制器时避免多个控制器占用不同模式的命令接口。

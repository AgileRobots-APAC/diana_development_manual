# 机器人描述

软件包名称：`diana_description`

## 概述

`diana_description` 提供 Diana 机械臂的三维模型和机器人参数，用于仿真、可视化以及生成机器人的 URDF 和 SRDF。它只包含描述类内容：xacro、网格、yaml 参数、launch 文件和 RViz 配置。

`diana_bringup`、`diana_moveit_config` 和 Gazebo 仿真都通过这个软件包获取机器人模型。

## 支持的机型

| `robot_type` | 说明 | 目录 |
| --- | --- | --- |
| `diana3` | Diana3 | `robots/diana3/` |
| `diana7` | Diana7 | `robots/diana7/` |
| `diana7g2` | Diana7G2 | `robots/diana7g2/` |

三个机型都是 7 个关节。`robot_type` 要与现场机械臂一致，所有命令都需要显式传入。

## 软件包内容

- **三维模型**：`meshes/` 下按机型分别提供可视化和碰撞网格。
- **机器人参数**：`robots/<机型>/` 下的 yaml 文件给出各机型的关节限位、运动学、动力学、惯量和碰撞胶囊体参数。
- **URDF 与 SRDF 生成**：`robots/<机型>/<机型>.urdf.xacro` 和 `<机型>.srdf.xacro` 是各机型的入口，可以直接用 xacro 展开，也可以用 `scripts/create_urdf.sh` 生成文件。
- **可视化**：`launch/visualize_diana.launch.py` 与 `rviz/visualize_diana.rviz` 用于在 RViz 中查看模型。

| 目录 | 内容 |
| --- | --- |
| `robots/<机型>/` | 机型入口 xacro，以及下表中的参数文件 |
| `robots/common/` | 各机型共用的 xacro 宏 |
| `robots/<机型>_duo/` | 双臂模型的 xacro |
| `accessories/` | 附件的 xacro 与参数，目前有 `diana_head` 和 `diana_duo_mount` |
| `meshes/` | 三维模型（`robots/`、`accessories/`） |
| `launch/` | `visualize_diana.launch.py` |
| `rviz/` | `visualize_diana.rviz` |
| `scripts/` | `create_urdf.sh` 与 `create_urdf.py` |

### 机型参数文件

| 文件 | 内容 |
| --- | --- |
| `joint_limits.yaml` | 每个关节的位置、速度和力矩限位 |
| `kinematics.yaml` | 每个关节相对上一个坐标系的位置（x、y、z）和姿态（roll、pitch、yaw） |
| `dynamics.yaml` | 每个关节的动力学参数 |
| `inertials.yaml` | 每个连杆的质量、质心和惯量 |
| `collision_capsule.yaml` | 每个连杆的碰撞胶囊体（位置、方向、长度、半径） |
| `accelerometers.yaml` | 加速度计配置 |

连杆命名为 `<前缀>link0` 至 `link8`，关节为 `<前缀>joint1` 至 `joint7`（旋转关节）和固定的 `joint8`，其中前缀默认是 `<robot_type>_`，例如 `diana3_joint1`。

## 前提条件

生成 URDF 的脚本通过 Docker 运行，需要先安装 Docker。可视化使用 ROS 2，需要已经按[开发准备](../development.md)构建了包含 `diana_description` 的工作空间，并安装了 `xacro`、`rviz2` 和 `joint_state_publisher_gui`。

## 生成 URDF

在 `diana_description` 源码目录中执行：

```bash
./scripts/create_urdf.sh <robot_type>
```

脚本会先构建名为 `urdf_creation` 的 Docker 镜像（基于 `osrf/ros:humble-desktop`，需要能访问 Docker 镜像仓库），再在容器内调用 `scripts/create_urdf.py`，用法如下：

```text
usage: create_urdf.py [-h] [--with-sc] [--abs-path] [--host-dir HOST_DIR]
                      [--no-prefix] robot_model

positional arguments:
  robot_model          id of the robot model (accepted values are: diana3,
                       diana7, diana7g2)

optional arguments:
  -h, --help           show this help message and exit
  --with-sc            Include self-collision volumes in the urdf model.
  --abs-path           Use absolute paths.
  --host-dir HOST_DIR  Provide a host directory for the absolute path.
  --no-prefix          Override the robot prefix of links, joints and visuals
                       in the urdf file.
```

| 参数 | 含义 |
| --- | --- |
| `robot_model` | 机型，取值 `diana3`、`diana7`、`diana7g2`，必须指定 |
| `--with-sc` | 在 URDF 中加入自碰撞体积（取自 `collision_capsule.yaml`） |
| `--abs-path` | 把 `package://diana_description` 替换成绝对路径 |
| `--host-dir` | 与 `--abs-path` 一起使用，指定写入 URDF 的主机目录 |
| `--no-prefix` | 去掉连杆、关节和可视化名称中的机型前缀 |

生成的 `<robot_type>.urdf` 和 `<robot_type>.srdf` 写入 `diana_description` 目录下的 `urdfs/` 目录。例如：

```bash
./scripts/create_urdf.sh diana3 --with-sc
```

## 在 ROS 2 中可视化

加载工作空间后启动：

```bash
ros2 launch diana_description visualize_diana.launch.py robot_type:=diana3
```

该启动文件启动 `robot_state_publisher`（使用 `robots/<robot_type>/<robot_type>.urdf.xacro`）、`joint_state_publisher_gui` 和 RViz（配置 `rviz/visualize_diana.rviz`，固定坐标系为 `base`）。在 `joint_state_publisher_gui` 的滑块里拖动关节，可以在 RViz 中查看对应的姿态。它不连接机械臂，也不会让机械臂运动。

| 启动参数 | 取值 | 说明 |
| --- | --- | --- |
| `robot_type` | `diana3`、`diana7`、`diana7g2` | 机型，必须与现场机械臂一致 |

## xacro 参数

机型入口 xacro 支持下列参数，可以在展开时用 `名称:=值` 的形式传入：

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `arm_prefix` | 空 | 连杆和关节名称的前缀，多个机械臂时用来区分 |
| `no_prefix` | `false` | 为 `true` 时去掉机型前缀 |
| `with_sc` | `false` | 为 `true` 时加入自碰撞体积 |
| `gazebo` | `false` | 为 `true` 时加入 `world` 链接、世界固定关节和 Gazebo 所需的标签 |
| `xyz`、`rpy` | `0 0 0` | `gazebo` 为 `true` 时，机械臂基座相对世界的位置和姿态 |

例如，展开 `diana3` 并加入自碰撞体积：

```bash
ros2 run xacro xacro \
  $(ros2 pkg prefix diana_description)/share/diana_description/robots/diana3/diana3.urdf.xacro \
  with_sc:=true
```

## 许可证

`diana_description` 的 `package.xml` 声明使用 Apache License 2.0。

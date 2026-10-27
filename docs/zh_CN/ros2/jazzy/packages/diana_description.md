# 机器人描述

软件包名称：`diana_description`

## 安装

请参阅 [开发准备](../development.md)。

## 软件包概述

`diana_description` 提供 Diana 机械臂的三维模型和机器人参数，用于可视化、仿真以及生成机器人的 URDF 和 SRDF。它只包含描述类内容：xacro、网格、yaml 参数、launch 文件和 RViz 配置。在 Jazzy 版本中，它与其他 `diana_*` 软件包位于同一个源码仓库（`<diana-ros2-repository-url>`）中，版本号见其 `package.xml`（当前为 `2.0.0`），许可证为 Apache License 2.0。

`diana_bringup`、`diana_moveit_config` 和 `diana_gazebo_bringup` 都通过这个软件包获取机器人模型，详见本页“被其他软件包使用”一节。

## 支持的机型

| `robot_type` | 说明 | 目录 |
| --- | --- | --- |
| `diana3` | Diana3 | `robots/diana3/` |
| `diana7` | Diana7 | `robots/diana7/` |
| `diana7g2` | Diana7G2 | `robots/diana7g2/` |
| （双臂） | Diana Duo，由两条机械臂和一个固定底座组成 | `robots/diana_duo/` |

三个单臂机型都是 7 个旋转关节（`joint1` 至 `joint7`）。`robot_type` 要与现场机械臂一致，所有命令都需要显式传入。

## 软件包内容

::::{list-table}
:header-rows: 1
:widths: 26 74

* - 目录
  - 内容
* - `robots/<机型>/`
  - 单臂机型的入口 xacro（`<机型>.urdf.xacro`、`<机型>.srdf.xacro`）和下表中的 yaml 参数文件
* - `robots/common/`
  - 各机型共用的 xacro 宏
* - `robots/diana_duo/`
  - Diana Duo 的 xacro：
    - 整机：`diana_duo.urdf.xacro`、`diana_duo.srdf.xacro`
    - 单臂：`diana_duo_arm.urdf.xacro`
    - 固定底座：`diana_duo_fixed_structure.urdf.xacro`
    - 安装座：`diana_duo_mount/`（安装座的 xacro、惯量和两条机械臂的安装位姿）
* - `meshes/`
  - 三维模型（`robots/`、`accessories/diana_duo_mount/`）
* - `launch/`
  - `diana.visualize.launch.py` 与 `diana_duo.visualize.launch.py`
* - `rviz/`
  - `diana.visualize.rviz` 与 `diana_duo.visualize.rviz`
* - `scripts/`
  - 在 Docker 中生成 URDF 与启动可视化的辅助脚本
::::

### 机型参数文件

| 文件 | 内容 |
| --- | --- |
| `joint_limits.yaml` | 每个关节的位置（`lower`、`upper`）、速度（`velocity`）和力矩（`effort`）限位 |
| `kinematics.yaml` | 每个关节相对上一个坐标系的位置（`x`、`y`、`z`）和姿态（`roll`、`pitch`、`yaw`） |
| `dynamics.yaml` | 每个关节的动力学参数 |
| `inertials.yaml` | 每个连杆的质量、质心和惯量 |
| `collision_capsule.yaml` | 每个连杆的自碰撞胶囊体（位置 `xyz`、方向 `direction`、长度 `length`、半径 `radius`） |
| `accelerometers.yaml` | 加速度计配置 |

连杆命名为 `<前缀>link0` 至 `link8`，关节为 `<前缀>joint1` 至 `joint7`（旋转关节）和固定的 `joint8`。默认前缀为 `<robot_type>_`，例如 `diana3_joint1`；指定 `arm_prefix` 后为 `<arm_prefix>_<robot_type>_`，例如 `left_diana7_joint1`；`no_prefix:=true` 时没有前缀。

## 在 RViz 中可视化

可视化只加载模型，不连接机械臂，也不会让机械臂运动。先按[开发准备](../development.md)构建并加载包含 `diana_description` 的工作空间；`diana_description` 依赖 `xacro`、`rviz2` 和 `joint_state_publisher_gui`。

### 单臂

```bash
ros2 launch diana_description diana.visualize.launch.py robot_type:=diana3
```

该启动文件展开 `robots/<robot_type>/<robot_type>.urdf.xacro`，启动 `robot_state_publisher`、`joint_state_publisher_gui` 和 RViz（配置 `rviz/diana.visualize.rviz`，固定坐标系为 `base`）。在 `joint_state_publisher_gui` 的滑块里拖动关节，可以在 RViz 中查看对应的姿态。

| 启动参数 | 取值 | 说明 |
| --- | --- | --- |
| `robot_type` | `diana3`、`diana7`、`diana7g2` | 机型。启动文件的默认值为 `diana7`，请显式传入并与现场机械臂保持一致 |

### Diana Duo

```bash
ros2 launch diana_description diana_duo.visualize.launch.py robot_type:=diana7
```

该启动文件分别为固定底座和左、右两条机械臂各启动一个 `robot_state_publisher`，命名空间依次为 `fixed_structure_`、`arm_left` 和 `arm_right`；两条机械臂各有一个 `joint_state_publisher_gui`，并启动 RViz（配置 `rviz/diana_duo.visualize.rviz`）。两条机械臂使用同一个 `robot_type`。

| 启动参数 | 默认值 | 说明 |
| --- | --- | --- |
| `robot_type` | `diana7` | 机械臂型号，取值 `diana3`、`diana7`、`diana7g2`；请显式传入 |
| `connected_to` | `base` | 底座坐标系的名称 |

## xacro 参数

入口 xacro 可以直接展开，参数用 `名称:=值` 的形式传入。

### 单臂机型入口

适用于 `robots/<机型>/<机型>.urdf.xacro`（`diana3`、`diana7`、`diana7g2` 相同）：

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `robot_type` | 与入口文件对应的机型 | 机型标识 |
| `arm_prefix` | 空 | 连杆和关节名称的前缀；非空时自动在末尾补一个下划线，多个机械臂时用来区分 |
| `no_prefix` | `false` | 为 `true` 时去掉连杆、关节和可视化名称中的前缀 |
| `with_sc` | `false` | 为 `true` 时为每个连杆增加 `<连杆名>_sc` 子连杆，其中包含 `collision_capsule` 定义的自碰撞胶囊体 |
| `gazebo` | `false` | 为 `true` 时去掉 `base` 坐标系，并加入 Gazebo 仿真所需的传动和标签 |
| `connected_to` | `base` | 机械臂基座 `link0` 所连接的父坐标系名称 |
| `description_pkg` | `diana_description` | 网格所在的描述软件包名称 |

例如，展开 `diana3` 并加入自碰撞胶囊体：

```bash
ros2 run xacro xacro \
  $(ros2 pkg prefix diana_description)/share/diana_description/robots/diana3/diana3.urdf.xacro \
  with_sc:=true
```

### Diana Duo 入口

`robots/diana_duo/diana_duo.urdf.xacro` 在同一个固定底座上放置两条机械臂，两条机械臂相对底座的位姿来自 `robots/diana_duo/diana_duo_mount/kinematics.yaml` 中的 `left` 和 `right`。

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `robot_types` | `['diana7','diana7']` | 左、右机械臂的机型列表 |
| `arm_prefixes` | `['left','right']` | 左、右机械臂的名称前缀列表 |
| `no_prefix` | `false` | 为 `true` 时去掉连杆、关节和可视化名称中的前缀 |
| `with_sc` | `false` | 为 `true` 时加入自碰撞胶囊体，含义同单臂入口 |
| `gazebo` | `false` | 为 `true` 时加入 Gazebo 仿真所需的传动和标签 |
| `connected_to` | `base` | 底座所连接的父坐标系名称 |
| `description_pkg` | `diana_description` | 网格所在的描述软件包名称 |
| `robot_ips` | 按现场填写 | 左、右机械臂的 IP 列表，仅在启用 `ros2_control` 时使用 |

对应的 SRDF 入口为 `robots/diana_duo/diana_duo.srdf.xacro`，使用 `robot_types` 和 `arm_prefixes` 两个参数，默认值与上表相同。

```{note}
Diana Duo 的 `robot_ips` 需要与现场两条机械臂的实际地址一致。
```

## 被其他软件包使用

| 软件包 | 使用方式 |
| --- | --- |
| [`diana_bringup`](diana_bringup.md) | `urdf/diana.urdf.xacro` 包含 `robots/<robot_type>/<robot_type>.urdf.xacro`，再加上 ros2_control 配置；`urdf/diana_duo.urdf.xacro` 包含 `robots/diana_duo/diana_duo.urdf.xacro`；`diana_duo.launch.py` 展开 `robots/diana_duo/diana_duo.srdf.xacro` 作为语义描述 |
| [`diana_moveit_config`](diana_moveit_config.md) | 启动文件展开 `robots/<robot_type>/<robot_type>.srdf.xacro` 作为 `robot_description_semantic` |
| [`diana_gazebo_bringup`](diana_gazebo_bringup.md) | 其 URDF 与启动文件包含 `robots/<robot_type>/<robot_type>.urdf.xacro`，并把 `diana_description` 所在目录加入 Gazebo 的资源搜索路径 |
| `diana_selfcollision` | 运行时依赖本软件包，见 [自碰撞检测](diana_selfcollision.md) |

用户自己的软件包可以用同样的方式引用，例如在 xacro 中使用 `$(find diana_description)/robots/diana3/diana3.urdf.xacro`。

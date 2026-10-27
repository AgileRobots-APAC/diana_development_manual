# 软件包

`diana_ros2` Jazzy 由下列软件包组成。每个软件包一页，按软件包名查阅。

## 软件包列表

| 软件包 | 版本 | 作用 |
| --- | --- | --- |
| `diana_ros2` | 3.5.3 | 元包，组织其余 Diana ROS 2 软件包 |
| [`diana_description`](diana_description.md) | 2.0.0 | 机器人描述、meshes 和 RViz 配置，随源码一起提供 |
| [`diana_bringup`](diana_bringup.md) | 3.5.3 | `ros2_control` 启动文件与运行时配置 |
| [`franka_example_controllers`](franka_example_controllers.md) | 3.5.3 | 示例控制器 |
| [`diana_moveit_config`](diana_moveit_config.md) | 3.5.3 | MoveIt 2 规划配置与启动文件 |
| [`diana_gazebo_bringup`](diana_gazebo_bringup.md)、[`diana_gazebo_hardware`](diana_gazebo_bringup.md) | 3.4.1、3.5.3 | Gazebo 启动文件、仿真世界与仿真硬件插件 |
| [`franka_hardware`](franka_hardware.md) | 3.5.3 | 基于 libfranka 的 `ros2_control` 硬件接口 |
| [`franka_msgs`](franka_msgs.md) | 3.5.3 | 消息、服务与动作 |
| [`franka_robot_state_broadcaster`](franka_robot_state_broadcaster.md) | 3.5.3 | 机器人状态广播器 |
| [`franka_semantic_components`](franka_semantic_components.md) | 3.5.3 | 语义组件，供控制器访问状态与指令接口 |
| [`diana_selfcollision`](diana_selfcollision.md) | 1.0.0 | 自碰撞检测 |

`diana_gazebo_bringup` 与 `diana_gazebo_hardware` 位于源码的 `diana_gazebo/` 目录下，不是顶层目录。软件包名中 `franka_*` 的部分沿用了上游命名，目前仍保持不变。

## 依赖关系

```{figure} ../../../../_static/images/ros2-jazzy-package-deps-zh.png
:alt: Diana ROS 2 Jazzy 软件包之间的依赖关系
:width: 80%

软件包之间的依赖关系，箭头由依赖方指向被依赖方，依据各软件包的 `package.xml`；元包 `diana_ros2` 依赖其余全部软件包，图中未画出。
```

```{toctree}
:hidden:
:maxdepth: 1

diana_bringup
diana_description
franka_example_controllers
diana_moveit_config
diana_gazebo_bringup
franka_hardware
franka_msgs
franka_robot_state_broadcaster
franka_semantic_components
diana_selfcollision
```

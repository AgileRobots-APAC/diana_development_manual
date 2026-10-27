# 软件包

`diana_ros2` Humble 由下列软件包组成。每个软件包一页，按软件包名查阅。

## 软件包列表

| 软件包 | 版本 | 作用 |
| --- | --- | --- |
| `diana_ros2` | 2.5.0 | 元包，组织其余 Diana ROS 2 软件包 |
| [`diana_description`](diana_description.md) | 由 `dependency.repos` 固定 | 机器人描述、meshes 和 RViz 配置（外部软件包，不在本源码树内） |
| [`diana_bringup`](diana_bringup.md) | 2.7.0 | `ros2_control` 启动文件与运行时配置 |
| [`diana_example_controllers`](diana_example_controllers.md) | 2.7.0 | 示例控制器 |
| [`diana_hardware`](diana_hardware.md) | 2.7.0 | 基于 libfranka 的 `ros2_control` 硬件接口 |
| [`diana_moveit_config`](diana_moveit_config.md) | 2.7.0 | MoveIt 2 规划配置与启动文件 |
| [`diana_gazebo_bringup`](diana_gazebo_bringup.md)、[`diana_gazebo_hardware`](diana_gazebo_bringup.md) | 2.7.0 | Gazebo 启动文件、仿真世界与仿真硬件插件 |
| [`diana_msgs`](diana_msgs.md) | 2.5.0 | Diana 专用消息、服务与动作 |
| [`diana_robot_state_broadcaster`](diana_robot_state_broadcaster.md) | 2.7.0 | 机器人状态广播器 |
| [`diana_semantic_components`](diana_semantic_components.md) | 2.7.0 | 语义组件，供控制器访问状态与指令接口 |

`diana_gazebo_bringup` 与 `diana_gazebo_hardware` 位于源码的 `diana_gazebo/` 目录下，不是顶层目录。

## 依赖关系

```{figure} ../../../../_static/images/ros2-humble-package-deps-zh.png
:alt: Diana ROS 2 Humble 软件包之间的依赖关系
:width: 80%

软件包之间的依赖关系，箭头由依赖方指向被依赖方；元包 `diana_ros2` 依赖其余全部软件包，图中未画出。
```

```{toctree}
:hidden:
:maxdepth: 1

diana_bringup
diana_description
diana_example_controllers
diana_moveit_config
diana_gazebo_bringup
diana_hardware
diana_msgs
diana_robot_state_broadcaster
diana_semantic_components
```

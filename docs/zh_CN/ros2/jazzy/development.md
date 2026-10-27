# 开发准备

以下步骤在 Ubuntu 24.04 开发 PC 上进行。仅做模型可视化或仿真时不需要连接真实机械臂；连接实机前请先完成[网络配置](../../programming/network.md)。不要在 Jazzy 工作空间中使用 Humble 的命令。

## 版本要求

```{important}
ROS 2 Jazzy 基于 Ubuntu 24.04，强烈建议在 Ubuntu 24.04 上使用 `diana_ros2` Jazzy。
```

| 组件 | 支持的版本 |
| --- | --- |
| Ubuntu | 24.04 |
| ROS 2 | Jazzy |
| libfranka | 0.18.2（Agile Robots 适配版本，目前唯一支持的版本） |
| diana_description | 随源码一起提供，不需要单独获取 |

不支持其他版本的 libfranka。

## 安装 ROS 2 与开发工具

先按 [ROS 2 Jazzy 官方安装说明](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html)配置软件源，然后安装桌面版（需要 RViz 图形界面）或基础版，并安装开发工具：

```bash
sudo apt install ros-jazzy-desktop ros-dev-tools
source /opt/ros/jazzy/setup.bash
```

只需要命令行环境时，可以用 `ros-jazzy-ros-base` 代替 `ros-jazzy-desktop`。

## 安装 libfranka

构建 `franka_hardware` 等软件包需要 Agile Robots 适配的 libfranka 0.18.2，请向 Agile Robots 支持团队获取，并按随附说明安装到开发 PC。

## 获取源码和外部依赖

创建工作空间，并把 Diana ROS 2 源码仓库克隆到 `src`：

```bash
mkdir -p ~/diana_ros2_ws
cd ~/diana_ros2_ws
git clone <diana-ros2-repository-url> src
```

源码根目录的 `dependency.repos` 记录了不在仓库内的外部依赖，用 `vcs` 导入：

```bash
vcs import src < src/dependency.repos --recursive --skip-existing
```

```{important}
不要只获取主源码就直接构建，否则会缺少构建所需的外部软件包。`diana_description` 与 `diana_*`、`franka_*` 软件包一起在主源码中，不需要单独导入。
```

## 安装依赖并构建

```bash
rosdep update
rosdep install --from-paths src --ignore-src --rosdistro jazzy -y
colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTS=OFF
source install/setup.bash
```

`--symlink-install` 可以减少磁盘占用，并方便修改源码后重新构建。在新终端中需要重新加载 `/opt/ros/jazzy/setup.bash` 和工作空间的 `install/setup.bash`。

Gazebo 仿真所需的 `ros_gz`、`gz_ros2_control` 等依赖在软件包的 `package.xml` 中声明，由上面的 `rosdep install` 一并安装，不需要单独执行 `apt`。仿真的使用方法见 [diana_gazebo_bringup](packages/diana_gazebo_bringup.md)。

## 配置实时权限

`controller_manager` 以 1 kHz 运行，并使用较高的实时线程优先级（`diana_bringup/config/controllers.yaml` 中 `update_rate` 为 `1000`，`thread_priority` 为 `97`）。在实机上运行时，运行用户需要有足够高的实时调度权限。下面是一组可用的限制值：

```text
@realtime soft rtprio 99
@realtime soft priority 99
@realtime soft memlock 102400
@realtime hard rtprio 99
@realtime hard priority 99
@realtime hard memlock 102400
```

在主机上，创建 `realtime` 用户组、把当前用户加入该组，并把上述限制写入 `/etc/security/limits.conf`，然后重新登录使其生效：

```bash
sudo groupadd realtime
sudo usermod -aG realtime $USER
sudo tee -a /etc/security/limits.conf <<'EOF'
@realtime soft rtprio 99
@realtime soft priority 99
@realtime soft memlock 102400
@realtime hard rtprio 99
@realtime hard priority 99
@realtime hard memlock 102400
EOF
```

内核实时性、网络和线程配置的详细说明参见[实时网络与系统配置](../../fci/realtime_network.md)。

## 检查安装

加载工作空间后，确认软件包可见：

```bash
ros2 pkg list | grep -E 'diana|franka'
```

随后可以按[快速开始](quick_start.md)和各软件包页面中的命令验证模型可视化、仿真或控制器；实机相关的命令在各页面中都带有安全提示。

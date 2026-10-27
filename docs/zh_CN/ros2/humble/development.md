# 开发准备

以下步骤在 Ubuntu 22.04 开发 PC 上进行。仅做模型可视化或仿真时不需要连接真实机械臂；连接实机前请先完成[网络配置](../../programming/network.md)。

## 版本要求

```{important}
ROS 2 Humble 基于 Ubuntu 22.04，强烈建议在 Ubuntu 22.04 上使用 `diana_ros2` Humble。
```

| 组件 | 支持的版本 |
| --- | --- |
| Ubuntu | 22.04 |
| ROS 2 | Humble |
| libfranka | 0.18.2（目前唯一支持的版本） |
| diana_description | 所检出源码根目录 `dependency.repos` 中固定的版本 |

不支持其他版本的 libfranka；`dependency.repos` 已将 libfranka 固定为 0.18.2（由 vcs 导入）。

## 安装 ROS 2 与开发工具

先按 [ROS 2 Humble 官方安装说明](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html)配置软件源，然后安装桌面版（需要 RViz 图形界面）或基础版，并安装开发工具：

```bash
sudo apt install ros-humble-desktop ros-dev-tools
source /opt/ros/humble/setup.bash
```

只需要命令行环境时，可以用 `ros-humble-ros-base` 代替 `ros-humble-desktop`。

## 获取源码和外部依赖

创建工作空间，并把 Diana ROS 2 源码仓库克隆到 `src`：

```bash
mkdir -p ~/diana_ros2_ws
cd ~/diana_ros2_ws
git clone <diana-ros2-repository-url> src
```

源码根目录的 `dependency.repos` 记录了不在仓库内的依赖，包括固定到 `0.18.2` 的 libfranka 和 `diana_description`。用 `vcs` 导入：

```bash
vcs import src < src/dependency.repos --recursive --skip-existing
```

```{important}
不要只获取主源码就直接构建，否则会缺少机器人描述等软件包。获取源码和导入 `diana_description` 需要相应的访问权限。
```

## 安装依赖并构建

```bash
rosdep update
rosdep install --from-paths src --ignore-src --rosdistro humble -y
colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release
source install/setup.bash
```

在新终端中需要重新加载 `/opt/ros/humble/setup.bash` 和工作空间的 `install/setup.bash`。

## 安装 Gazebo 仿真依赖（可选）

只有使用 Gazebo 仿真时才需要这一步，例如[快速开始](quick_start.md)中的“模型可视化与 Gazebo 仿真”和 [diana_gazebo_bringup](packages/diana_gazebo_bringup.md)。仅使用真实机械臂或模拟硬件时可以跳过。Gazebo 仿真需要以下 apt 软件包（与源码 `Dockerfile` 中的安装命令一致）：

```bash
sudo apt update
sudo apt install -y \
  ros-humble-ros-gz \
  ros-humble-gz-ros2-control \
  ros-humble-sdformat-urdf \
  ros-humble-joint-state-publisher \
  ros-humble-joint-state-broadcaster \
  ros-humble-ros2controlcli \
  ros-humble-controller-manager \
  ros-humble-rviz2 \
  ros-humble-xacro \
  libignition-gazebo6-dev \
  libignition-plugin-dev
```

`diana_gazebo_hardware` 还依赖 `pinocchio`、`libfranka`、`hardware_interface`、`realtime_tools` 等，它们已经由上一步的 `rosdep install` 安装。使用下文的容器时，这些依赖已经包含在镜像中。

## 配置实时权限

`controller_manager` 以 1 kHz 运行，并使用较高的实时线程优先级（`diana_bringup/config/controllers.yaml` 中 `update_rate` 为 `1000`，`thread_priority` 为 `98`）。在实机上运行时，运行用户需要有实时调度权限，源码根目录的 `limits.conf` 给出了所需的限制：

```text
@realtime soft rtprio 99
@realtime soft priority 99
@realtime soft memlock 102400
@realtime hard rtprio 99
@realtime hard priority 99
@realtime hard memlock 102400
```

在主机上，创建 `realtime` 用户组、把当前用户加入该组，并把这些限制写入 `/etc/security/limits.conf`，然后重新登录使其生效：

```bash
sudo groupadd realtime
sudo usermod -aG realtime $USER
sudo tee -a /etc/security/limits.conf < src/limits.conf
```

内核实时性、网络和线程配置的详细说明参见[实时网络与系统配置](../../fci/realtime_network.md)。

## 使用容器（可选）

源码自带 `Dockerfile`、`docker-compose.yml`、`.devcontainer/devcontainer.json` 和 `diana_entrypoint.sh`，基础镜像为 `ros:humble-ros-base`。使用容器时不必在主机安装 ROS 2。

```bash
cd <source-directory>
docker compose up -d diana_ros2_humble
docker exec -it <container-name> bash
```

容器的行为如下：

- 源码目录挂载到 `/ros2_ws/src`，容器使用 `host` 网络并以 `privileged` 模式运行，`limits.conf` 挂载为容器内的 `/etc/security/limits.conf`。
- 容器获得 `SYS_NICE` 能力，`rtprio` 限制为 `99`。
- `diana_entrypoint.sh` 在启动时自动执行 `vcs import` 导入 `dependency.repos`。
- 容器名由源码目录下 `.env` 中的 `CONTAINER_NAME` 决定，默认值为 `src_humble`。
- 图形界面（RViz、Gazebo）依赖 `DISPLAY` 与 `/tmp/.X11-unix` 挂载。

进入容器后，仍需在 `/ros2_ws` 下执行 `colcon build` 并加载 `install/setup.bash`。使用 VS Code 时，也可以通过 Dev Containers 的 `Reopen in Container` 打开 `.devcontainer/devcontainer.json`。

## 检查安装

加载工作空间后，确认软件包可见：

```bash
ros2 pkg list | grep diana
```

随后可以按各软件包页面中的命令验证模型可视化、仿真或控制器；实机相关的命令在各页面中都带有安全提示。

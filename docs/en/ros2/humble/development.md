# Development Setup

The following steps are performed on an Ubuntu 22.04 development PC. A real robot is not needed for model visualization or simulation; before connecting to a real robot, complete the [Network Setup](../../programming/network.md) first.

## Version Requirements

```{important}
ROS 2 Humble is based on Ubuntu 22.04, and we strongly recommend using `diana_ros2` Humble with Ubuntu 22.04.
```

| Component | Supported version |
| --- | --- |
| Ubuntu | 22.04 |
| ROS 2 | Humble |
| libfranka | 0.18.2 (the only version currently supported) |
| diana_description | The version pinned by `dependency.repos` in the root of the source you check out |

Other libfranka versions are not supported; `dependency.repos` fixes libfranka to 0.18.2 (vcs imports it).

## Install ROS 2 and Development Tools

Set up the package sources by following the [official ROS 2 Humble installation guide](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html), then install the desktop edition (needed for the RViz GUI) or the base edition, together with the development tools:

```bash
sudo apt install ros-humble-desktop ros-dev-tools
source /opt/ros/humble/setup.bash
```

For a command-line-only environment, `ros-humble-ros-base` can replace `ros-humble-desktop`.

## Get the Source and External Dependencies

Create a workspace and clone the Diana ROS 2 source repository into `src`:

```bash
mkdir -p ~/diana_ros2_ws
cd ~/diana_ros2_ws
git clone <diana-ros2-repository-url> src
```

The `dependency.repos` file in the source root lists dependencies that are not part of the repository, including libfranka pinned to `0.18.2` and `diana_description`. Import them with `vcs`:

```bash
vcs import src < src/dependency.repos --recursive --skip-existing
```

```{important}
Do not build after fetching only the main source; packages such as the robot description would be missing. Fetching the source and importing `diana_description` requires the corresponding access permissions.
```

## Install Dependencies and Build

```bash
rosdep update
rosdep install --from-paths src --ignore-src --rosdistro humble -y
colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release
source install/setup.bash
```

In every new terminal, source `/opt/ros/humble/setup.bash` and the workspace's `install/setup.bash` again.

## Install Gazebo Simulation Dependencies (Optional)

This step is only needed for Gazebo simulation, for example the "Model Visualization and Gazebo Simulation" part of the [Quick Start](quick_start.md) and [diana_gazebo_bringup](packages/diana_gazebo_bringup.md). You can skip it if you only use a real robot or fake hardware. Gazebo simulation needs the following apt packages (matching the install command in the source `Dockerfile`):

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

`diana_gazebo_hardware` additionally depends on `pinocchio`, `libfranka`, `hardware_interface`, `realtime_tools` and others, which the `rosdep install` step above has already installed. When you use the container described below, these dependencies are already included in the image.

## Configure Realtime Permissions

The `controller_manager` runs at 1 kHz with a high realtime thread priority (`update_rate` is `1000` and `thread_priority` is `98` in `diana_bringup/config/controllers.yaml`). When running on a real robot, the user needs realtime scheduling permissions. The `limits.conf` file in the source root gives the required limits:

```text
@realtime soft rtprio 99
@realtime soft priority 99
@realtime soft memlock 102400
@realtime hard rtprio 99
@realtime hard priority 99
@realtime hard memlock 102400
```

On the host, create a `realtime` group, add the current user to it, and add these limits to `/etc/security/limits.conf`, then log in again for them to take effect:

```bash
sudo groupadd realtime
sudo usermod -aG realtime $USER
sudo tee -a /etc/security/limits.conf < src/limits.conf
```

For kernel, network, and thread configuration in detail, see [Realtime Network and System Configuration](../../fci/realtime_network.md).

## Use a Container (Optional)

The source includes a `Dockerfile`, `docker-compose.yml`, `.devcontainer/devcontainer.json`, and `diana_entrypoint.sh`, based on the `ros:humble-ros-base` image. With a container, ROS 2 does not need to be installed on the host.

```bash
cd <source-directory>
docker compose up -d diana_ros2_humble
docker exec -it <container-name> bash
```

The container behaves as follows:

- The source directory is mounted at `/ros2_ws/src`. The container uses the `host` network and runs in `privileged` mode, and `limits.conf` is mounted as `/etc/security/limits.conf` inside the container.
- The container has the `SYS_NICE` capability, and `rtprio` is limited to `99`.
- `diana_entrypoint.sh` runs `vcs import` on `dependency.repos` at startup.
- The container name comes from `CONTAINER_NAME` in the `.env` file in the source directory; the default is `src_humble`.
- GUI applications (RViz, Gazebo) rely on `DISPLAY` and the `/tmp/.X11-unix` mount.

Inside the container, you still need to run `colcon build` under `/ros2_ws` and source `install/setup.bash`. With VS Code, you can also open `.devcontainer/devcontainer.json` through Dev Containers using `Reopen in Container`.

## Check the Installation

After sourcing the workspace, confirm that the packages are visible:

```bash
ros2 pkg list | grep diana
```

You can then verify model visualization, simulation, or controllers with the commands on each package page; commands that involve a real robot carry safety notes on those pages.

# Development Setup

The following steps are performed on an Ubuntu 24.04 development PC. Model visualization and simulation do not need a real robot; complete the [Network Setup](../../programming/network.md) before connecting to a real robot. Do not use Humble commands in a Jazzy workspace.

## Version Requirements

```{important}
ROS 2 Jazzy is based on Ubuntu 24.04. Using `diana_ros2` Jazzy on Ubuntu 24.04 is strongly recommended.
```

| Component | Supported version |
| --- | --- |
| Ubuntu | 24.04 |
| ROS 2 | Jazzy |
| libfranka | 0.18.2 (Agile Robots adapted build; the only supported version) |
| diana_description | Provided with the source; no separate download |

Other libfranka versions are not supported.

## Install ROS 2 and Development Tools

Configure the package sources by following the [official ROS 2 Jazzy installation guide](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html), then install the desktop edition (needed for the RViz GUI) or the base edition, plus the development tools:

```bash
sudo apt install ros-jazzy-desktop ros-dev-tools
source /opt/ros/jazzy/setup.bash
```

For a command-line-only environment, use `ros-jazzy-ros-base` instead of `ros-jazzy-desktop`.

## Install libfranka

Building `franka_hardware` and the other packages requires the Agile Robots adapted libfranka 0.18.2. Obtain it from the Agile Robots support team and install it on the development PC according to the accompanying instructions.

## Get the Source and External Dependencies

Create a workspace and clone the Diana ROS 2 source repository into `src`:

```bash
mkdir -p ~/diana_ros2_ws
cd ~/diana_ros2_ws
git clone <diana-ros2-repository-url> src
```

`dependency.repos` in the source root lists the external dependencies that are not part of the repository. Import them with `vcs`:

```bash
vcs import src < src/dependency.repos --recursive --skip-existing
```

```{important}
Do not build only the main source: the external packages needed for the build would be missing. `diana_description` is part of the main source together with the `diana_*` and `franka_*` packages and does not need to be imported separately.
```

## Install Dependencies and Build

```bash
rosdep update
rosdep install --from-paths src --ignore-src --rosdistro jazzy -y
colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTS=OFF
source install/setup.bash
```

`--symlink-install` reduces disk usage and makes rebuilding after source changes easier. In a new terminal, source `/opt/ros/jazzy/setup.bash` and the workspace `install/setup.bash` again.

The dependencies needed by the Gazebo simulation, such as `ros_gz` and `gz_ros2_control`, are declared in the `package.xml` files and installed by the `rosdep install` command above, so no separate `apt` step is needed. See [diana_gazebo_bringup](packages/diana_gazebo_bringup.md) for how to use the simulation.

## Configure Real-Time Permissions

`controller_manager` runs at 1 kHz with a high real-time thread priority (`update_rate` is `1000` and `thread_priority` is `97` in `diana_bringup/config/controllers.yaml`). On a real robot, the user running it needs sufficiently high real-time scheduling permissions. The following limits work:

```text
@realtime soft rtprio 99
@realtime soft priority 99
@realtime soft memlock 102400
@realtime hard rtprio 99
@realtime hard priority 99
@realtime hard memlock 102400
```

On the host, create the `realtime` group, add the current user to it, and write the limits to `/etc/security/limits.conf`, then log in again for them to take effect:

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

For details on kernel real-time behavior, networking, and thread configuration, see [Realtime Network and System Configuration](../../fci/realtime_network.md).

## Check the Installation

After sourcing the workspace, confirm that the packages are visible:

```bash
ros2 pkg list | grep -E 'diana|franka'
```

Then verify model visualization, simulation, or controllers with the commands in the [Quick Start](quick_start.md) and the package pages. Commands that involve a real robot carry safety notes on each page.

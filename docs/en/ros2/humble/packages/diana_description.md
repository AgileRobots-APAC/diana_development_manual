# `diana_description`

## Overview

`diana_description` provides the 3D models and robot parameters of Diana robots, for simulation, visualization, and generating the URDF and SRDF of a robot. It contains only description content: xacro, meshes, yaml parameters, a launch file, and an RViz configuration.

`diana_bringup`, `diana_moveit_config`, and the Gazebo simulation all obtain the robot model from this package.

## Supported Robot Models

| `robot_type` | Description | Directory |
| --- | --- | --- |
| `diana3` | Diana3 | `robots/diana3/` |
| `diana7` | Diana7 | `robots/diana7/` |
| `diana7g2` | Diana7G2 | `robots/diana7g2/` |

All three models have 7 joints. `robot_type` must match the robot on site and must be passed explicitly in every command.

## Package Contents

- **3D models**: `meshes/` provides visual and collision meshes for each model.
- **Robot parameters**: the yaml files in `robots/<model>/` give the joint limits, kinematics, dynamics, inertia, and collision-capsule parameters of each model.
- **URDF and SRDF generation**: `robots/<model>/<model>.urdf.xacro` and `<model>.srdf.xacro` are the entry points of each model. They can be expanded directly with xacro, or generated into files with `scripts/create_urdf.sh`.
- **Visualization**: `launch/visualize_diana.launch.py` and `rviz/visualize_diana.rviz` are used to view the model in RViz.

| Directory | Content |
| --- | --- |
| `robots/<model>/` | Model entry xacro and the parameter files in the table below |
| `robots/common/` | xacro macros shared by all models |
| `robots/<model>_duo/` | xacro of the dual-arm models |
| `accessories/` | xacro and parameters of accessories; currently `diana_head` and `diana_duo_mount` |
| `meshes/` | 3D models (`robots/`, `accessories/`) |
| `launch/` | `visualize_diana.launch.py` |
| `rviz/` | `visualize_diana.rviz` |
| `scripts/` | `create_urdf.sh` and `create_urdf.py` |

### Model Parameter Files

| File | Content |
| --- | --- |
| `joint_limits.yaml` | Position, velocity, and effort limits of each joint |
| `kinematics.yaml` | Position (x, y, z) and orientation (roll, pitch, yaw) of each joint relative to the previous frame |
| `dynamics.yaml` | Dynamic parameters of each joint |
| `inertials.yaml` | Mass, center of mass, and inertia of each link |
| `collision_capsule.yaml` | Collision capsules of each link (position, direction, length, radius) |
| `accelerometers.yaml` | Accelerometer configuration |

Links are named `<prefix>link0` to `link8`, and joints `<prefix>joint1` to `joint7` (revolute) plus the fixed `joint8`. The prefix defaults to `<robot_type>_`, for example `diana3_joint1`.

## Prerequisites

The URDF generation script runs through Docker, so Docker must be installed first. Visualization uses ROS 2: you need a workspace that contains `diana_description`, built as described in the [Development Setup](../development.md), with `xacro`, `rviz2`, and `joint_state_publisher_gui` installed.

## Generating the URDF

Run the following in the `diana_description` source directory:

```bash
./scripts/create_urdf.sh <robot_type>
```

The script first builds a Docker image named `urdf_creation` (based on `osrf/ros:humble-desktop`, which requires access to a Docker image registry) and then calls `scripts/create_urdf.py` inside the container. Its usage is:

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

| Argument | Meaning |
| --- | --- |
| `robot_model` | Robot model: `diana3`, `diana7`, or `diana7g2`; required |
| `--with-sc` | Include self-collision volumes in the URDF (taken from `collision_capsule.yaml`) |
| `--abs-path` | Replace `package://diana_description` with an absolute path |
| `--host-dir` | Used together with `--abs-path` to set the host directory written into the URDF |
| `--no-prefix` | Remove the model prefix from link, joint, and visual names |

The generated `<robot_type>.urdf` and `<robot_type>.srdf` are written to the `urdfs/` directory inside the `diana_description` directory. For example:

```bash
./scripts/create_urdf.sh diana3 --with-sc
```

## Visualizing in ROS 2

After sourcing the workspace, start:

```bash
ros2 launch diana_description visualize_diana.launch.py robot_type:=diana3
```

The launch file starts `robot_state_publisher` (using `robots/<robot_type>/<robot_type>.urdf.xacro`), `joint_state_publisher_gui`, and RViz (configuration `rviz/visualize_diana.rviz`, fixed frame `base`). Drag the joints in the sliders of `joint_state_publisher_gui` to see the corresponding pose in RViz. It does not connect to a robot and does not move any robot.

| Launch argument | Values | Description |
| --- | --- | --- |
| `robot_type` | `diana3`, `diana7`, `diana7g2` | Robot model; must match the robot on site |

## xacro Arguments

The model entry xacro supports the following arguments, which can be passed as `name:=value` when expanding:

| Argument | Default | Description |
| --- | --- | --- |
| `arm_prefix` | empty | Prefix of link and joint names, used to tell several arms apart |
| `no_prefix` | `false` | When `true`, remove the model prefix |
| `with_sc` | `false` | When `true`, include self-collision volumes |
| `gazebo` | `false` | When `true`, add the `world` link, the fixed world joint, and the tags Gazebo needs |
| `xyz`, `rpy` | `0 0 0` | When `gazebo` is `true`, the position and orientation of the arm base relative to the world |

For example, to expand `diana3` with self-collision volumes:

```bash
ros2 run xacro xacro \
  $(ros2 pkg prefix diana_description)/share/diana_description/robots/diana3/diana3.urdf.xacro \
  with_sc:=true
```

## License

The `package.xml` of `diana_description` declares the Apache License 2.0.

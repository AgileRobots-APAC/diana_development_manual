# Robot Description

Package name: `diana_description`

## Installation

See [Development Setup](../development.md).

## Package Overview

`diana_description` provides the 3D models and robot parameters of Diana robots, for visualization, simulation, and generating the URDF and SRDF of a robot. It contains only description content: xacro, meshes, yaml parameters, launch files, and RViz configurations. In the Jazzy version it lives in the same source repository (`<diana-ros2-repository-url>`) as the other `diana_*` packages; its version is given in its `package.xml` (currently `2.0.0`) and it is licensed under the Apache License 2.0.

`diana_bringup`, `diana_moveit_config`, and `diana_gazebo_bringup` all obtain the robot model from this package; see the section "Use by Other Packages" on this page.

## Supported Robot Models

| `robot_type` | Description | Directory |
| --- | --- | --- |
| `diana3` | Diana3 | `robots/diana3/` |
| `diana7` | Diana7 | `robots/diana7/` |
| `diana7g2` | Diana7G2 | `robots/diana7g2/` |
| (dual-arm) | Diana Duo, made of two arms and a fixed base structure | `robots/diana_duo/` |

All three single-arm models have 7 revolute joints (`joint1` to `joint7`). `robot_type` must match the robot on site and must be passed explicitly in every command.

## Package Contents

::::{list-table}
:header-rows: 1
:widths: 26 74

* - Directory
  - Content
* - `robots/<model>/`
  - Entry xacro of a single-arm model (`<model>.urdf.xacro`, `<model>.srdf.xacro`) and the yaml parameter files in the table below
* - `robots/common/`
  - xacro macros shared by all models
* - `robots/diana_duo/`
  - xacro of the Diana Duo:
    - whole robot: `diana_duo.urdf.xacro`, `diana_duo.srdf.xacro`
    - single arm: `diana_duo_arm.urdf.xacro`
    - fixed base structure: `diana_duo_fixed_structure.urdf.xacro`
    - mount: `diana_duo_mount/` (xacro and inertia of the mount, and the mounting poses of the two arms)
* - `meshes/`
  - 3D models (`robots/`, `accessories/diana_duo_mount/`)
* - `launch/`
  - `diana.visualize.launch.py` and `diana_duo.visualize.launch.py`
* - `rviz/`
  - `diana.visualize.rviz` and `diana_duo.visualize.rviz`
* - `scripts/`
  - Helper scripts that generate URDF files and start the visualization inside Docker
::::

### Model Parameter Files

| File | Content |
| --- | --- |
| `joint_limits.yaml` | Position (`lower`, `upper`), velocity (`velocity`), and torque (`effort`) limits of each joint |
| `kinematics.yaml` | Position (`x`, `y`, `z`) and orientation (`roll`, `pitch`, `yaw`) of each joint relative to the previous frame |
| `dynamics.yaml` | Dynamic parameters of each joint |
| `inertials.yaml` | Mass, center of mass, and inertia of each link |
| `collision_capsule.yaml` | Self-collision capsules of each link (position `xyz`, direction `direction`, length `length`, radius `radius`) |
| `accelerometers.yaml` | Accelerometer configuration |

Links are named `<prefix>link0` to `link8`; joints are `<prefix>joint1` to `joint7` (revolute) and the fixed `joint8`. The default prefix is `<robot_type>_`, for example `diana3_joint1`; with `arm_prefix` set it is `<arm_prefix>_<robot_type>_`, for example `left_diana7_joint1`; with `no_prefix:=true` there is no prefix.

## Visualization in RViz

Visualization only loads the model. It does not connect to the robot and never moves it. First build and source a workspace that contains `diana_description` as described in [Development Setup](../development.md); `diana_description` depends on `xacro`, `rviz2`, and `joint_state_publisher_gui`.

### Single Arm

```bash
ros2 launch diana_description diana.visualize.launch.py robot_type:=diana3
```

This launch file expands `robots/<robot_type>/<robot_type>.urdf.xacro` and starts `robot_state_publisher`, `joint_state_publisher_gui`, and RViz (configuration `rviz/diana.visualize.rviz`, fixed frame `base`). Drag the sliders in `joint_state_publisher_gui` to see the corresponding pose in RViz.

| Launch argument | Values | Description |
| --- | --- | --- |
| `robot_type` | `diana3`, `diana7`, `diana7g2` | Robot model. The default in the launch file is `diana7`; pass it explicitly and keep it consistent with the robot on site |

### Diana Duo

```bash
ros2 launch diana_description diana_duo.visualize.launch.py robot_type:=diana7
```

This launch file starts one `robot_state_publisher` each for the fixed base structure and the left and right arms, in the namespaces `fixed_structure_`, `arm_left`, and `arm_right`; each arm also gets a `joint_state_publisher_gui`, and RViz is started (configuration `rviz/diana_duo.visualize.rviz`). Both arms use the same `robot_type`.

| Launch argument | Default | Description |
| --- | --- | --- |
| `robot_type` | `diana7` | Arm model, one of `diana3`, `diana7`, `diana7g2`; pass it explicitly |
| `connected_to` | `base` | Name of the base frame |

## xacro Arguments

The entry xacro files can be expanded directly; pass arguments as `name:=value`.

### Single-Arm Entry

Applies to `robots/<model>/<model>.urdf.xacro` (identical for `diana3`, `diana7`, and `diana7g2`):

| Argument | Default | Description |
| --- | --- | --- |
| `robot_type` | The model of the entry file | Model identifier |
| `arm_prefix` | empty | Prefix of link and joint names; an underscore is appended automatically when non-empty; used to tell several arms apart |
| `no_prefix` | `false` | If `true`, the prefix is removed from link, joint, and visual names |
| `with_sc` | `false` | If `true`, each link gets a `<link name>_sc` child link containing the self-collision capsules defined by `collision_capsule` |
| `gazebo` | `false` | If `true`, the `base` frame is dropped and the transmissions and tags required by Gazebo simulation are added |
| `connected_to` | `base` | Name of the parent frame that the arm base `link0` is attached to |
| `description_pkg` | `diana_description` | Name of the description package that holds the meshes |

For example, expand `diana3` with the self-collision capsules:

```bash
ros2 run xacro xacro \
  $(ros2 pkg prefix diana_description)/share/diana_description/robots/diana3/diana3.urdf.xacro \
  with_sc:=true
```

### Diana Duo Entry

`robots/diana_duo/diana_duo.urdf.xacro` places two arms on one fixed base structure. The pose of each arm relative to the base comes from `left` and `right` in `robots/diana_duo/diana_duo_mount/kinematics.yaml`.

| Argument | Default | Description |
| --- | --- | --- |
| `robot_types` | `['diana7','diana7']` | List of the models of the left and right arms |
| `arm_prefixes` | `['left','right']` | List of the name prefixes of the left and right arms |
| `no_prefix` | `false` | If `true`, the prefix is removed from link, joint, and visual names |
| `with_sc` | `false` | If `true`, the self-collision capsules are added; same meaning as in the single-arm entry |
| `gazebo` | `false` | If `true`, the transmissions and tags required by Gazebo simulation are added |
| `connected_to` | `base` | Name of the parent frame that the base structure is attached to |
| `description_pkg` | `diana_description` | Name of the description package that holds the meshes |
| `robot_ips` | Fill in per site | List of the IP addresses of the left and right arms; only used when `ros2_control` is enabled |

The matching SRDF entry is `robots/diana_duo/diana_duo.srdf.xacro`. It takes the two arguments `robot_types` and `arm_prefixes`, with the same defaults as above.

```{note}
`robot_ips` of the Diana Duo must match the actual addresses of the two arms on site.
```

## Use by Other Packages

| Package | How it is used |
| --- | --- |
| [`diana_bringup`](diana_bringup.md) | `urdf/diana.urdf.xacro` includes `robots/<robot_type>/<robot_type>.urdf.xacro` and adds the ros2_control configuration; `urdf/diana_duo.urdf.xacro` includes `robots/diana_duo/diana_duo.urdf.xacro`; `diana_duo.launch.py` expands `robots/diana_duo/diana_duo.srdf.xacro` as the semantic description |
| [`diana_moveit_config`](diana_moveit_config.md) | Its launch files expand `robots/<robot_type>/<robot_type>.srdf.xacro` as `robot_description_semantic` |
| [`diana_gazebo_bringup`](diana_gazebo_bringup.md) | Its URDF and launch files include `robots/<robot_type>/<robot_type>.urdf.xacro` and add the parent directory of `diana_description` to the Gazebo resource search path |
| `diana_selfcollision` | Runtime dependency on this package; see [Self-Collision Checking](diana_selfcollision.md) |

Your own packages can reference it the same way, for example `$(find diana_description)/robots/diana3/diana3.urdf.xacro` in xacro.

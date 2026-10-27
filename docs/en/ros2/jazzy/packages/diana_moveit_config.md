# MoveIt Configuration

Package name: `diana_moveit_config`

## Installation

See [Development Setup](../development.md).

## Package Overview

`diana_moveit_config` provides the MoveIt 2 configuration and launch files for Diana arms. It contains:

- Two launch files: `launch/moveit.launch.py` (the complete MoveIt stack including RViz) and `launch/move_group.launch.py` (starts only the `move_group` node, meant to be included by other launch files).
- Per-robot-type configuration directories `config/diana3`, `config/diana7` and `config/diana7g2`, each with five yaml files (`controllers.yaml`, `joint_limits.yaml`, `kinematics.yaml`, `ompl_planning.yaml`, `ros_controllers.yaml`).
- The RViz configuration `rviz/moveit.rviz`.

The robot description (URDF/xacro) and the semantic description (SRDF/xacro) are **not part of this package**: the launch files read `urdf/diana_arm.urdf.xacro` from `diana_bringup` and `robots/<robot_type>/<robot_type>.srdf.xacro` from `diana_description`. `diana_description` is imported through the `dependency.repos` file in the source tree, see [Development Setup](../development.md).

```{note}
`moveit.launch.py` itself starts `ros2_control_node`, `robot_state_publisher`, `joint_state_publisher` and other nodes, so it is a self-contained stack. Do not additionally run a launch file of [diana_bringup](diana_bringup.md) for the same robot.
```

## Move Group

The planning group is called `<robot_type>_arm`, where `<robot_type>` is the value of the launch argument `robot_type`. Only the following three `robot_type` values have a `config/<robot_type>/` directory in this package:

| `robot_type` | Planning group | Config directory | Trajectory controller (`controllers.yaml`) | Joints |
| --- | --- | --- | --- | --- |
| `diana3` | `diana3_arm` | `config/diana3/` | `diana3_arm_controller` | `diana3_joint1` ... `diana3_joint7` |
| `diana7` | `diana7_arm` | `config/diana7/` | `diana7_arm_controller` | `diana7_joint1` ... `diana7_joint7` |
| `diana7g2` | `diana7g2_arm` | `config/diana7g2/` | `diana7g2_arm_controller` | `diana7g2_joint1` ... `diana7g2_joint7` |

The yaml files of the three directories have the same structure and differ only in the robot type prefix. The launch files read the yaml files under `config/<robot_type>/`; any other value has no configuration directory and cannot be launched.

MoveIt hands trajectories to a `FollowJointTrajectory` action through `MoveItSimpleControllerManager` (action namespace `follow_joint_trajectory`, `default: true`).

## Usage

### Launch Arguments

`moveit.launch.py` declares the following arguments (pass them as `name:=value`). `robot_type` and `robot_ip` have defaults in the launch file, but please pass them explicitly in every command:

| Argument | Default | Description |
| --- | --- | --- |
| `robot_type` | `diana7` (pass explicitly) | Robot type: `diana3`, `diana7` or `diana7g2`, matching your robot |
| `robot_ip` | `192.168.10.75` (pass explicitly) | Hostname or IP address of the robot (the default address of the A network port of the Diana controller is `192.168.10.75`). Not connected when fake hardware is used |
| `namespace` | empty | Namespace of `move_group`, `robot_state_publisher`, `ros2_control_node`, `joint_state_publisher` and the controller spawner |
| `use_fake_hardware` | `true` | Use fake hardware without connecting to a robot. Set it to `false` explicitly for a real robot |
| `fake_sensor_commands` | `false` | Fake sensor command switch passed to xacro; only effective when `use_fake_hardware` is `true` |
| `use_rviz` | `true` | Whether to start RViz (uses `rviz/moveit.rviz`) |

`moveit.launch.py` starts these nodes: `move_group` (`moveit_ros_move_group`), `rviz2` (when `use_rviz` is `true`), `robot_state_publisher`, `ros2_control_node` and `joint_state_publisher`; when `use_fake_hardware` is `false` it also starts `franka_robot_state_broadcaster` through the `controller_manager spawner`.

### Fake Hardware

Verify the MoveIt configuration without a robot. `robot_ip` should still be passed; fake hardware does not connect to it, so you can use the Diana default address `192.168.10.75`:

```bash
ros2 launch diana_moveit_config moveit.launch.py robot_type:=diana7 robot_ip:=192.168.10.75 use_fake_hardware:=true
```

After startup, enable the `MotionPlanning` display in RViz, choose `<robot_type>_arm` as `Planning Group`, set a goal pose and click Plan / Execute. Without a graphical environment add `use_rviz:=false`; the `move_group` node provides the standard MoveIt `MoveGroup` action.

### Real Robot

```bash
ros2 launch diana_moveit_config moveit.launch.py robot_type:=diana7 robot_ip:=<robot-ip> use_fake_hardware:=false
```

```{warning}
The real-robot command makes the arm execute trajectories planned by MoveIt. Before executing, make sure the workspace is free of people and obstacles, the emergency stop is within reach, the robot meets the control-mode and network prerequisites, and check the planned path in RViz at a low velocity scaling first. See [Safety Boundaries](../../../reference/safety.md), [Network Configuration](../../../programming/network.md) and the [FCI Overview](../../../fci/overview.md) for details.
```

## Configuration Files

Each of the three robot type directories (written as `config/<robot_type>/`) contains these files:

::::{list-table}
:header-rows: 1
:widths: 24 76

* - File
  - Content
* - `kinematics.yaml`
  - Kinematics solver of `<robot_type>_arm`:
    - solver: `kdl_kinematics_plugin/KDLKinematicsPlugin`
    - `kinematics_solver_search_resolution: 0.005`
    - `kinematics_solver_timeout: 0.005`
* - `joint_limits.yaml`
  - Acceleration limits of joints 1 to 7:
    - `has_acceleration_limits: true`
    - `max_acceleration` is 3.75, 1.875, 2.5, 3.125, 3.75, 5.0, 5.0 (rad/s²)
* - `ompl_planning.yaml`
  - The OMPL `planner_configs` and the list of planners available to `<robot_type>_arm`
* - `controllers.yaml`
  - MoveIt `MoveItSimpleControllerManager` configuration:
    - controller: `<robot_type>_arm_controller`
    - action namespace: `follow_joint_trajectory`
    - type: `FollowJointTrajectory`
    - joints 1 to 7
* - `ros_controllers.yaml`
  - ros2_control configuration:
    - update rate 1000 Hz
    - `<robot_type>_arm_controller`: `joint_trajectory_controller/JointTrajectoryController`, command interface `effort`, state interfaces `position` and `velocity`
    - `joint_state_broadcaster`
    - `franka_robot_state_broadcaster`
::::

Gains of the trajectory controller in `ros_controllers.yaml` (`i` is 0 and `i_clamp` is 1 for all joints), identical for the three robot types:

| Joint | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `p` | 600 | 600 | 600 | 600 | 250 | 150 | 50 |
| `d` | 30 | 30 | 30 | 30 | 10 | 10 | 5 |

The launch files additionally set in code: the planning plugin `ompl_interface/OMPLPlanner`, `start_state_max_bounds_error: 0.1`, the request adapters (`ResolveConstraintFrames`, `ValidateWorkspaceBounds`, `CheckStartStateBounds`, `CheckStartStateCollision`), the response adapters (`AddTimeOptimalParameterization`, `ValidateSolution`, `DisplayMotionPath`), the trajectory execution parameters (`allowed_execution_duration_scaling: 1.2`, `allowed_goal_duration_margin: 0.5`, `allowed_start_tolerance: 0.01`) and the four `publish_*` switches of the planning scene monitor (all `True`).

## `move_group.launch.py`

`move_group.launch.py` starts only the `move_group` node (with `output="screen"`) and reads the same yaml files under `config/<robot_type>/` as `moveit.launch.py`. It does not start RViz, `ros2_control_node` or controllers and cannot form a complete stack on its own; `joint_impedance_with_ik_example_controller.launch.py` in [diana_bringup](diana_bringup.md) includes it. It declares these arguments:

| Argument | Default | Description |
| --- | --- | --- |
| `robot_type` | `diana7` | Robot type: `diana3`, `diana7` or `diana7g2` |
| `robot_ip` | `192.168.10.75` | Hostname or IP address of the robot |
| `namespace` | empty | Namespace of the `move_group` node |
| `use_fake_hardware` | `true` | Fake hardware switch passed to xacro |
| `fake_sensor_commands` | `false` | Fake sensor command switch passed to xacro |
| `arm_prefix` | empty | Arm prefix (used to tell several arms apart); when non-empty, the robot type name in the yaml files is replaced by `<arm_prefix>_<robot_type>` |

To change the inverse kinematics solver, edit `kinematics_solver` in `config/<robot_type>/kinematics.yaml`.

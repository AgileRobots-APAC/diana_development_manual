# `diana_moveit_config`

## Installation

See [Development Setup](../development.md).

## Package Overview

`diana_moveit_config` provides the MoveIt 2 configuration and launch files for Diana arms. It contains:

- Two launch files: `launch/moveit.launch.py` (a complete MoveIt demo stack) and `launch/move_group.launch.py` (starts only the `move_group` node, meant to be included by other launch files).
- Per-robot-type configuration directories `config/diana3` and `config/diana7g2`, each with 5 yaml files.
- Per-robot-type RViz configurations `rviz/moveit_<robot_type>.rviz`.

The robot description (URDF/xacro) and the semantic description (SRDF/xacro) are **not part of this package**: `moveit.launch.py` reads `urdf/diana_arm.urdf.xacro` from `diana_bringup` and `robots/<robot_type>/<robot_type>.srdf.xacro` from the external package `diana_description`. `diana_description` is imported through the `dependency.repos` file in the source tree, see [Development Setup](../development.md).

```{note}
`moveit.launch.py` starts its own `ros2_control_node`, `robot_state_publisher`, `joint_state_publisher` and controllers, so it is a self-contained stack. Do not run `diana.launch.py` / `example.launch.py` from [diana_bringup](diana_bringup.md) on the same robot at the same time.
```

```{figure} ../../../../_static/images/ros2-humble-moveit-launch-en.png
:alt: Nodes started by moveit.launch.py and how they relate
:width: 70%

The nodes started by `moveit.launch.py`: the RViz MotionPlanning panel requests planning and execution through the MoveGroup action, and `move_group` hands the trajectory to the `FollowJointTrajectory` trajectory controller.
```

## Move Group

The planning group is named `<robot_type>_arm`, where `<robot_type>` is the value of the `robot_type` launch argument:

| `robot_type` | Planning group | Kinematics config | Trajectory controller | Joints |
| --- | --- | --- | --- | --- |
| `diana3` | `diana3_arm` | `config/diana3/kinematics.yaml` | `diana3_arm_controller` | `diana3_joint1` ... `diana3_joint7` |
| `diana7g2` | `diana7g2_arm` | `config/diana7g2/kinematics.yaml` | `diana7g2_arm_controller` | `diana7g2_joint1` ... `diana7g2_joint7` |

The yaml files of the two robot types are structurally identical and differ only in the robot-type prefix. `moveit.launch.py` reads the yaml files in `config/<robot_type>/` for the given `robot_type`; only these two `robot_type` values have a `config/` directory, and any other value cannot be launched.

## Usage

### Launch Arguments

`moveit.launch.py` declares the following arguments (pass them as `name:=value`):

| Argument | Default | Description |
| --- | --- | --- |
| `robot_type` | Required | Robot type: `diana3` or `diana7g2`, matching your robot; there is currently no MoveIt configuration for `diana7`, so it cannot be used |
| `robot_ip` | Required | Hostname or IP address of the robot. With fake hardware the address is not connected to, but the argument must still be passed |
| `use_fake_hardware` | `false` | Use `mock_components/GenericSystem` instead of real hardware |
| `fake_sensor_commands` | `false` | Fake sensor command switch passed to xacro |
| `use_rviz` | `true` | Whether to start RViz (using `rviz/moveit_<robot_type>.rviz`) |
| `namespace` | empty | Namespace of `move_group`, `robot_state_publisher`, `ros2_control_node` and the controller manager |

### Fake Hardware

Verify the MoveIt configuration without a robot, using mock hardware. `robot_ip` must still be passed; mock hardware does not connect to it, so you can use the Diana default address `192.168.10.75`:

```bash
ros2 launch diana_moveit_config moveit.launch.py robot_type:=diana3 robot_ip:=192.168.10.75 use_fake_hardware:=true
```

After startup:

- `config/<robot_type>/ros_controllers_fake.yaml` is loaded, and the trajectory controller uses the `position` command interface.
- `diana_robot_state_broadcaster` is not started.
- Enable the `MotionPlanning` display in RViz (it is saved as disabled in the RViz configuration, and `Planning Group` is preset to `<robot_type>_arm`), set a goal pose, then click Plan / Execute.

```{figure} ../../../../_static/images/ros2-humble-moveit-rviz-startup.png
:alt: RViz right after startup, with the MotionPlanning display unchecked
:width: 100%

RViz right after startup: the `MotionPlanning` display is unchecked by default, and only the robot model is shown.
```

```{figure} ../../../../_static/images/ros2-humble-moveit-rviz-motionplanning.png
:alt: RViz with MotionPlanning checked, showing the MotionPlanning panel
:width: 100%

After checking `MotionPlanning`: the MotionPlanning panel appears with the planning group `diana3_arm`, and an interactive marker appears at the end of the robot. Use Plan, Execute, and Plan & Execute to plan and execute.
```

```{tip}
Add `use_rviz:=false` if no graphical environment is available. The `move_group` node serves the standard MoveIt `MoveGroup` action.
```

### Real Robot

```bash
ros2 launch diana_moveit_config moveit.launch.py robot_type:=diana3 robot_ip:=<robot-ip>
```

```{warning}
The real-robot command makes the arm execute trajectories planned by MoveIt. Before running it, make sure the workspace is free of people and obstacles, the emergency stop is within reach, and the robot meets the control-mode and network prerequisites. Check planned paths in RViz first and start with a low velocity scaling. See [Safety Boundaries](../../../reference/safety.md), [Network Configuration](../../../programming/network.md) and the [FCI Overview](../../../fci/overview.md).
```

In real-robot mode `config/<robot_type>/ros_controllers.yaml` is loaded: the trajectory controller uses the `effort` command interface, and `diana_robot_state_broadcaster` is started.

## Configuration Files

Each of the two robot-type directories (written as `config/<robot_type>/`) contains these files:

::::{list-table}
:header-rows: 1
:widths: 24 76

* - File
  - Content
* - `kinematics.yaml`
  - Kinematics solver of `<robot_type>_arm`:
    - solver: `lma_kinematics_plugin/LMAKinematicsPlugin`
    - `kinematics_solver_search_resolution: 0.005`
    - `kinematics_solver_timeout: 0.005`
* - `ompl_planning.yaml`
  - OMPL `planner_configs` (24 entries including SBL, EST, RRT, RRTConnect, RRTstar, PRM, FMT and TrajOpt) and the planner list available to `<robot_type>_arm`
* - `controllers.yaml`
  - MoveIt `MoveItSimpleControllerManager` configuration:
    - controller: `<robot_type>_arm_controller`
    - action namespace: `follow_joint_trajectory`
    - type: `FollowJointTrajectory`
    - `default: true`
    - joints 1 to 7
* - `ros_controllers.yaml`
  - ros2_control configuration for the real robot:
    - update rate 1000 Hz
    - `<robot_type>_arm_controller`: `joint_trajectory_controller/JointTrajectoryController`, command interface `effort`, state interfaces `position` and `velocity`, gains below
    - `joint_state_broadcaster`
    - `diana_robot_state_broadcaster`
* - `ros_controllers_fake.yaml`
  - Used with `use_fake_hardware:=true`: same as above, but the command interface is `position` and there are no gains
::::

`moveit.launch.py` additionally sets in code: the planning plugin `ompl_interface/OMPLPlanner`, `start_state_max_bounds_error: 0.1`, the request adapters (`AddTimeOptimalParameterization`, `ResolveConstraintFrames`, `FixWorkspaceBounds`, `FixStartStateBounds`, `FixStartStateCollision`, `FixStartStatePathConstraints`), the trajectory execution parameters (`allowed_execution_duration_scaling: 1.2`, `allowed_goal_duration_margin: 0.5`, `allowed_start_tolerance: 0.01`) and the four `publish_*` switches of the planning scene monitor (all `True`).

```{note}
For the `joint_impedance_with_ik_example_controller` of [diana_example_controllers](diana_example_controllers.md), its launch file `joint_impedance_with_ik_example_controller.launch.py` (in `diana_bringup`) includes this package's `move_group.launch.py` for every robot and loads `config/<robot_type>/kinematics.yaml`. To change its inverse-kinematics solver, edit `kinematics_solver` in that yaml. `move_group.launch.py` cannot be used on its own; the arguments it needs are passed by the including launch file.
```

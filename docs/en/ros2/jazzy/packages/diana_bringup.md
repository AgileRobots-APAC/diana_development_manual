# Bringup and Runtime Configuration

Package name: `diana_bringup`

## Installation

See [Development Setup](../development.md).

## Package Overview

`diana_bringup` provides the launch files, controller parameter files, and URDF entry points needed to bring up the Diana arm ROS 2 control stack. It combines `diana_description` (the robot model), `franka_hardware` (the `ros2_control` hardware interface), `franka_robot_state_broadcaster`, and `franka_example_controllers`, and supports namespaced launches.

The package installs the `config`, `launch`, `urdf`, and `rviz` directories and provides the Python module `diana_bringup.launch_utils` (YAML loading, parsing of comma-separated parameters and string lists).

| File | Purpose |
| --- | --- |
| `launch/diana.launch.py` | Starts the core nodes for a single arm (see the section "Single-Arm Launch File") |
| `launch/diana.example_controllers.launch.py` | Reads a robot configuration file, includes `diana.launch.py` for each robot in it, and loads example controllers |
| `launch/diana_duo.launch.py` | Dual-arm (Diana Duo) launch file |
| `config/controllers.yaml` | `ros2_control` controller types and parameters |
| `config/diana.config.yaml` | Example single-arm robot configuration file |
| `config/diana_duo.config.yaml` | Example dual-arm robot configuration file |
| `urdf/diana.urdf.xacro`, `urdf/diana_duo.urdf.xacro` | xacro entry points that add the `ros2_control` hardware description on top of the `diana_description` model |
| `rviz/diana.visualize.rviz`, `rviz/diana_duo.visualize.rviz` | RViz display configurations |

`urdf/diana.urdf.xacro` selects the hardware plugin from `use_fake_hardware`: when it is `true`, the mock hardware plugin provided by `franka_hardware` is used; otherwise the real hardware plugin is used with `robot_ip`.

```{warning}
With `use_fake_hardware` set to `false`, the commands on this page connect to a real arm and may make it move. Before running them, make sure the workspace is clear of people and obstacles, the emergency stop is within reach, and the robot is in a state that allows external control, and read [Safety Boundaries](../../../reference/safety.md) first. For FCI and network prerequisites see the [FCI Overview](../../../fci/overview.md) and [Network Configuration](../../../programming/network.md).
```

## Single-Arm Launch File

`diana.launch.py` starts `robot_state_publisher`, `ros2_control_node`, `joint_state_publisher`, and the basic broadcasters for one arm. It generates `robot_description` from `urdf/diana.urdf.xacro` and uses the file given by `controllers_yaml` as the parameter file of `ros2_control_node`.

### Launch Arguments

| Argument | Default | Description |
| --- | --- | --- |
| `robot_type` | Required (pass it explicitly) | Arm model: `diana3`, `diana7`, or `diana7g2`; must match your arm |
| `robot_ip` | Required (pass it explicitly) | Hostname or IP address of the robot; the default address of the A network port of the Diana controller is `192.168.10.75` |
| `arm_prefix` | Empty string | Arm name prefix |
| `namespace` | Empty string | Namespace of all nodes |
| `use_fake_hardware` | `false` | Whether to use simulated hardware |
| `fake_sensor_commands` | `false` | Sensor command option of the simulated hardware |
| `joint_state_rate` | `30` | Publish rate of `joint_state_publisher` (Hz) |
| `load_franka_robot_state_broadcaster` | `true` | Whether to load `franka_robot_state_broadcaster` with real hardware |
| `controllers_yaml` | `config/controllers.yaml` of `diana_bringup` | Controller parameter file; may be replaced with your own |

With real hardware:

```bash
ros2 launch diana_bringup diana.launch.py robot_type:=diana3 robot_ip:=192.168.10.75
```

Without a robot, using simulated hardware:

```bash
ros2 launch diana_bringup diana.launch.py robot_type:=diana3 robot_ip:=192.168.10.75 use_fake_hardware:=true
```

### Started Nodes

`diana.launch.py` starts the following under the given `namespace`:

| Entry | Description |
| --- | --- |
| `robot_state_publisher` | Publishes `robot_description` and TF |
| `ros2_control_node` (`controller_manager`) | Loads the hardware interface and runs the controllers; besides `controllers_yaml` it receives the parameters `robot_type` and `arm_prefix`; the whole launch shuts down when this process exits |
| `joint_state_publisher` | Publishes the aggregated `joint_states` at `joint_state_rate`, with `diana/joint_states` as its source |
| `spawner joint_state_broadcaster` | Loads and activates `joint_state_broadcaster`, with its `joint_states` remapped to `diana/joint_states` |
| `spawner franka_robot_state_broadcaster` | Loads and activates `franka_robot_state_broadcaster`; started only when `load_franka_robot_state_broadcaster` is `true` and `use_fake_hardware` is not `true` |

A `spawner` only loads and activates a controller and then exits, so `ros2 node list` shows the loaded controller nodes rather than the `spawner`. `diana.launch.py` does not load example controllers; they are loaded by the launch file described in the next section. Controller names and types are listed in the section "Controller Configuration File"; see [franka_robot_state_broadcaster](franka_robot_state_broadcaster.md) for the broadcaster.

With real hardware, `franka_hardware` also creates the nodes `service_server` and `action_server` inside the `ros2_control_node` process; see the section "Non-realtime Robot Parameter Setting".

List the loaded controllers and their states with:

```bash
ros2 control list_controllers
```

```{important}
`franka_hardware` works in only one control mode at a time. Before switching to a controller of a different mode, deactivate the current one. See [franka_hardware](franka_hardware.md) for the interfaces.
```

```{figure} ../../../../_static/images/ros2-jazzy-bringup-launch-en.png
:alt: Launch structure of the example controller launch file
:width: 100%

`diana.example_controllers.launch.py` reads the robot configuration file, includes `diana.launch.py` once per robot, and then loads the requested controllers; items with a dashed outline start only when the matching condition holds.
```

### Namespaces

The `namespace` argument applies to `robot_state_publisher`, `ros2_control_node`, `joint_state_publisher`, and every `spawner`, so topics, services, and the controller manager all live in that namespace. The default empty string means no namespace.

| Object | Without namespace | With namespace (`NS_1` as an example) |
| --- | --- | --- |
| Controller manager | `/controller_manager` | `/NS_1/controller_manager` |
| Aggregated joint state topic | `/joint_states` | `/NS_1/joint_states` |

When launched in a namespace, `ros2 control` commands need `-c` to select the matching controller manager, for example:

```bash
ros2 control list_controllers -c /NS_1/controller_manager
```

## Example Controller Launch File

`diana.example_controllers.launch.py` reads a YAML robot configuration file, includes `diana.launch.py` once for each robot in it, and uses a `spawner` to load, for each robot, one controller taken from `controller_names`. Command-line arguments cannot tell different robots apart, so use this file for multi-robot and namespace setups.

### Example Controller Launch Arguments

| Argument | Default | Description |
| --- | --- | --- |
| `robot_config_file` | `diana.config.yaml` | Robot configuration file. A bare file name is looked up in the `config` directory of `diana_bringup`; a full path also works |
| `controller_names` | None (must be given on the command line) | Comma-separated controller names; must be names declared in `controllers.yaml` |
| `robot_ips` | Empty string | Comma-separated IP list; when non-empty it overrides `robot_ip` in the configuration file |

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
  robot_ips:=192.168.10.75 \
  controller_names:=gravity_compensation_example_controller
```

`robot_type` is not a command-line argument; it is taken from the `robot_type` field of each robot in the configuration file, so first change it to the model of your arm. A controller whose name contains `controller` is loaded by a `spawner` with `--controller-manager-timeout 30`, using the parameters in `config/controllers.yaml` of `diana_bringup`. See [franka_example_controllers](franka_example_controllers.md) for the purpose and prerequisites of each controller.

```{warning}
Example controllers move the arm or output torques. With real hardware, first confirm that the workspace is clear and the emergency stop is within reach, and bring the arm into a pose suitable for the example. With `use_fake_hardware` set to `"true"` in the configuration file, no real robot is connected.
```

### Robot Configuration File

The top-level keys of the configuration file are arbitrary identifiers for the robots (such as `ROBOT1`); each entry describes one robot. The entry in `diana.config.yaml` is as follows, and its fields are passed on to `diana.launch.py`:

| Field | Default | Description |
| --- | --- | --- |
| `robot_type` | `"diana7"` | Arm model: `diana3`, `diana7`, or `diana7g2` |
| `arm_prefix` | `""` | Name prefix |
| `fake_sensor_commands` | `"false"` | Simulated sensor commands |
| `joint_state_rate` | `30` | Joint state publish rate (Hz) |
| `namespace` | `""` | Namespace of this robot; must be unique across robots in a multi-robot setup |
| `robot_ip` | `"192.168.10.75"` | Robot IP or hostname |
| `use_fake_hardware` | `"true"` | Whether to use simulated hardware; change to `"false"` to connect to a real robot |
| `use_rviz` | `"true"` | Start RViz when `"true"` |

When any entry has `use_rviz` set to `"true"`, the launch file starts a single `rviz2` instance (configuration `rviz/diana.visualize.rviz` of `diana_bringup`) shared by all robots. For a custom configuration file, copy `diana.config.yaml` as a template and keep all of its fields. For several robots, add entries to the file and give each robot a different `namespace` and its own `robot_ip`. Using a custom configuration file:

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
  robot_config_file:=/path/to/my_robots.config.yaml \
  controller_names:=gravity_compensation_example_controller
```

### Controller Names and Robot IP Lists

`controller_names` and `robot_ips` are comma-separated lists that map one-to-one onto the robots in the configuration file, in order:

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
  robot_ips:=<robot-ip-1>,<robot-ip-2> \
  controller_names:=gravity_compensation_example_controller,joint_impedance_example_controller
```

The rules (see `diana_bringup.launch_utils.get_parameter_for_config`) are:

- When the list length equals the number of robots, the N-th value is used for the N-th robot;
- When the lengths differ, a warning is printed and the first value is used for all robots;
- When `robot_ips` is empty, `robot_ip` from the configuration file is used;
- An empty `controller_names` exits the launch immediately.

## Dual-Arm Launch File

`diana_duo.launch.py` is for the Diana Duo dual-arm setup. From `urdf/diana_duo.urdf.xacro` it generates one `ros2_control` hardware component per arm, and under `namespace` it starts `robot_state_publisher`, `ros2_control_node`, `joint_state_publisher`, a `spawner` for `joint_state_broadcaster`, and a `spawner` for one controller. The dual-arm setup does not start `franka_robot_state_broadcaster`.

### Dual-Arm Launch Arguments

| Argument | Default | Description |
| --- | --- | --- |
| `robot_config_file` | `config/diana_duo.config.yaml` of `diana_bringup` | Dual-arm configuration file; a bare file name is looked up in the `config` directory |
| `controllers_yaml` | `config/controllers.yaml` of `diana_bringup` | Controller parameter file |
| `controller_name` | Pass it explicitly | Name of the controller to load; only one is supported for dual-arm; use `diana_duo_joint_impedance_example_controller`, which is declared in `controllers.yaml` |

```bash
ros2 launch diana_bringup diana_duo.launch.py \
  controller_name:=diana_duo_joint_impedance_example_controller
```

Robot types, IPs, and prefixes come from the configuration file, not from command-line arguments.

```{warning}
`diana_duo_joint_impedance_example_controller` makes both arms output torques and move. With real hardware, first confirm that the space around both arms is clear and the emergency stops are within reach, and that `use_fake_hardware` in the configuration file is `"false"`.
```

### Dual-Arm Configuration File

`diana_duo.config.yaml` has a single entry. It must contain the three string lists `robot_types`, `robot_ips`, and `arm_prefixes`; all three must have the same length and the prefixes in `arm_prefixes` must be unique, otherwise the launch exits with an error. `urdf/diana_duo.urdf.xacro` reads the matching element of these lists for arm 0 and arm 1 in order, and appends `_` to each prefix.

| Field | Default | Description |
| --- | --- | --- |
| `robot_types` | `"['diana7','diana7']"` | Models of the two arms: `diana3`, `diana7`, or `diana7g2` |
| `arm_prefixes` | `"['left','right']"` | Prefixes of the two arms |
| `robot_ips` | List of two IPs | IP of each robot; the first entry defaults to `192.168.10.75`; fill in the actual addresses of both robots |
| `use_fake_hardware` | `"true"` | Whether to use simulated hardware; change to `"false"` to connect to real robots |
| `fake_sensor_commands` | `"false"` | Simulated sensor commands |
| `joint_state_rate` | `1000` | Joint state publish rate (Hz) |
| `namespace` | `""` | Namespace |
| `thread_priority` | `98` | Thread priority of the hardware interface |

## Controller Configuration File

`config/controllers.yaml` declares the `controller_manager` parameters and the type and parameters of each controller. `diana.launch.py` and `diana_duo.launch.py` use it as the parameter file of `ros2_control_node`, and the `spawner` of the example controllers uses it as well.

General `controller_manager` parameters: `update_rate` is `1000`, `thread_priority` is `97`, and `manage` and `print_warnings` under `overruns` are both `false`.

Controllers with a declared type:

| Controller name | Type |
| --- | --- |
| `joint_state_broadcaster` | `joint_state_broadcaster/JointStateBroadcaster` |
| `franka_robot_state_broadcaster` | `franka_robot_state_broadcaster/FrankaRobotStateBroadcaster` |
| `gravity_compensation_example_controller` | `franka_example_controllers/GravityCompensationExampleController` |
| `joint_impedance_example_controller` | `franka_example_controllers/JointImpedanceExampleController` |
| `joint_impedance_with_ik_example_controller` | `franka_example_controllers/JointImpedanceWithIKExampleController` |
| `cartesian_impedance_example_controller` | `franka_example_controllers/CartesianImpedanceExampleController` |
| `cartesian_pose_example_controller` | `franka_example_controllers/CartesianPoseExampleController` |
| `cartesian_velocity_example_controller` | `franka_example_controllers/CartesianVelocityExampleController` |
| `cartesian_orientation_example_controller` | `franka_example_controllers/CartesianOrientationExampleController` |
| `elbow_example_controller` | `franka_example_controllers/ElbowExampleController` |
| `cartesian_elbow_example_controller` | `franka_example_controllers/CartesianElbowExampleController` |
| `joint_position_example_controller` | `franka_example_controllers/JointPositionExampleController` |
| `joint_velocity_example_controller` | `franka_example_controllers/JointVelocityExampleController` |
| `model_example_controller` | `franka_example_controllers/ModelExampleController` |
| `move_to_start_example_controller` | `franka_example_controllers/MoveToStartExampleController` |
| `diana_duo_joint_impedance_example_controller` | `franka_example_controllers/DianaDuoJointImpedanceExampleController` |

Controllers that have parameters in the file:

| Controller | Parameters |
| --- | --- |
| `joint_impedance_example_controller` | `k_gains` (`24.0, 24.0, 24.0, 24.0, 10.0, 6.0, 2.0`), `d_gains` (`2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 0.5`) |
| `joint_impedance_with_ik_example_controller` | `k_gains` (`600.0, 600.0, 600.0, 600.0, 250.0, 150.0, 50.0`), `d_gains` (`30.0, 30.0, 30.0, 30.0, 10.0, 10.0, 5.0`) |
| `move_to_start_example_controller` | `k_gains` and `d_gains`, with the same values as `joint_impedance_with_ik_example_controller` |
| `franka_robot_state_broadcaster` | `convenience_publish_rate` (`1000`); `state_interfaces` is `robot_state` |
| `diana_duo_joint_impedance_example_controller` | `update_rate` (`1000`), `k_gains` and `d_gains`, with the same values as `joint_impedance_example_controller` |

Only controllers loaded by a `spawner` appear in the controller manager. To use a different controller, stop the current launch and start it again with another `controller_names`. See [franka_example_controllers](franka_example_controllers.md) for the purpose and prerequisites of each controller.

## Non-realtime Robot Parameter Setting

With the real hardware interface (`use_fake_hardware` set to `false`), `franka_hardware` creates a node named `service_server` inside the `ros2_control_node` process. It offers the following non-realtime parameter services; the types are defined in [franka_msgs](franka_msgs.md). The table lists names relative to the node; when launched in a namespace, rely on the actual output of `ros2 service list`.

### Service List

| Service | Type | Request fields |
| --- | --- | --- |
| `service_server/set_joint_stiffness` | `franka_msgs/srv/SetJointStiffness` | `joint_stiffness` (7 values) |
| `service_server/set_cartesian_stiffness` | `franka_msgs/srv/SetCartesianStiffness` | `cartesian_stiffness` (x, y, z, roll, pitch, yaw; 6 values, applied along the stiffness frame) |
| `service_server/set_tcp_frame` | `franka_msgs/srv/SetTCPFrame` | `transformation` (4x4 column-major matrix, 16 values) |
| `service_server/set_stiffness_frame` | `franka_msgs/srv/SetStiffnessFrame` | `transformation` (4x4 column-major matrix, 16 values) |
| `service_server/set_force_torque_collision_behavior` | `franka_msgs/srv/SetForceTorqueCollisionBehavior` | Lower and upper thresholds of the nominal torques (7 values) and nominal forces (6 values) |
| `service_server/set_full_collision_behavior` | `franka_msgs/srv/SetFullCollisionBehavior` | Lower and upper torque (7 values) and force (6 values) thresholds for the acceleration phase and the nominal phase |
| `service_server/set_load` | `franka_msgs/srv/SetLoad` | `mass`, `center_of_mass` (3 values), `load_inertia` (3x3 column-major, 9 values) |

The response of every service is `bool success` and `string error`.

```{warning}
Load, frame transformations, and collision thresholds directly affect the robot's torque estimation and protective-stop behavior. Set them according to your actual tooling and re-verify at conservative speed after any change.
```

### Error Recovery Action

`franka_hardware` also creates a node named `action_server` in the same process, offering the action `action_server/error_recovery` (type `franka_msgs/action/ErrorRecovery`; goal, result, and feedback are all empty). On receiving a goal it calls `robot->automaticErrorRecovery()`: on success the goal succeeds; if a Franka exception is thrown, the goal is aborted and the error is logged. Namespaces are handled as for the services above.

```bash
ros2 action send_goal /action_server/error_recovery franka_msgs/action/ErrorRecovery {}
```

```{important}
Automatic error recovery only clears the robot's current recoverable error; it is no substitute for finding the cause of the stop. After a collision, protective stop, or other safety-related stop, first make sure the site is safe and then recover; see [Safety Boundaries](../../../reference/safety.md).
```

# `diana_bringup`

`diana_bringup` provides the launch files, controller configuration, and URDF entry point needed to bring up the Diana arm ROS 2 control stack. It combines `diana_description` (the robot model), `diana_hardware` (the `ros2_control` hardware interface), `diana_robot_state_broadcaster`, and `diana_example_controllers`, and supports namespaced multi-robot launches.

## Installation

See [Development Setup](../development.md).

## Package Overview

`diana_bringup` installs the `config`, `launch`, and `urdf` directories and provides the Python module `diana_bringup.launch_utils` (YAML loading and comma-separated parameter parsing).

The core launch file is `diana.launch.py`. It generates `robot_description` from `urdf/diana_arm.urdf.xacro`, starts the `ros2_control` stack, and spawns the basic broadcasters. The xacro layers the `ros2_control` description from `diana_hardware` on top of the robot model from `diana_description`: when `use_fake_hardware` is `true` it uses `mock_components/GenericSystem`, otherwise it uses `diana_hardware/DianaHardwareInterface` and passes `robot_ip`.

```{warning}
With `use_fake_hardware` set to `false`, the commands on this page connect to a real arm and may make it move. Before running them, make sure the workspace is clear of people and obstacles, the emergency stop is within reach, and the robot is in a state that allows external control. Read [Safety Boundaries](../../../reference/safety.md) first. For FCI and network prerequisites see the [FCI overview](../../../fci/overview.md) and [network setup](../../../programming/network.md).
```

### Launch Arguments

All launch arguments of `diana.launch.py` with the defaults actually set in the source:

| Argument | Default | Description |
| --- | --- | --- |
| `robot_type` | Required | Arm model (xacro argument `robot_type`, matching a robot directory in `diana_description`); one of `diana3`, `diana7`, `diana7g2`, matching your robot |
| `arm_prefix` | empty string | Prefix for joint, interface, and TF names |
| `namespace` | empty string | Namespace for all nodes |
| `robot_ip` | `192.168.10.75` | Hostname or IP address of the robot |
| `use_fake_hardware` | `false` | Whether to use `mock_components` simulated hardware |
| `fake_sensor_commands` | `false` | The `mock_sensor_commands` option of the simulated hardware |
| `joint_state_rate` | `30` | Publish rate of `joint_state_publisher` (Hz) |
| `controllers_yaml` | `config/controllers.yaml` of `diana_bringup` | Controller parameter file; can be replaced with your own |

Launch example (replace `<robot-ip>` with the real address):

```bash
ros2 launch diana_bringup diana.launch.py robot_type:=diana3 robot_ip:=<robot-ip>
```

Using simulated hardware without a robot:

```bash
ros2 launch diana_bringup diana.launch.py robot_type:=diana3 use_fake_hardware:=true
```

### Started Nodes

`diana.launch.py` starts the following in the given `namespace`:

| Launch item | Node in `ros2 node list` | Description |
| --- | --- | --- |
| `robot_state_publisher` | `/robot_state_publisher` | Publishes `robot_description` and TF |
| `ros2_control_node` | `/controller_manager` | Loads the hardware interface and runs controllers; `joint_states` is remapped to `diana/joint_states`; the whole launch shuts down when this process exits |
| `joint_state_publisher` | `/joint_state_publisher` | Merges `diana/joint_states` and publishes `joint_states` at `joint_state_rate` |
| `spawner joint_state_broadcaster` | `/joint_state_broadcaster` (controller node) | Loads and activates `joint_state_broadcaster` |
| `spawner diana_robot_state_broadcaster` | `/diana_robot_state_broadcaster` (controller node) | Loads and activates `diana_robot_state_broadcaster`; started only when `use_fake_hardware` is not `true` |

A `spawner` only loads and activates a controller and then exits, so `spawner` does not appear in the node list; what you see is the controller node it loaded.

The parameter file of `ros2_control_node` comes from `controllers_yaml`; it additionally receives the `robot_type` and `arm_prefix` parameters. For controller names and types see [diana_example_controllers](diana_example_controllers.md); for the state broadcaster see [diana_robot_state_broadcaster](diana_robot_state_broadcaster.md).

After startup, list the nodes with:

```bash
ros2 node list
```

With fake hardware (`use_fake_hardware:=true`) you should see:

```text
/controller_manager
/joint_state_broadcaster
/joint_state_publisher
/robot_state_publisher
```

With real hardware, `/diana_robot_state_broadcaster` is added, together with the `/service_server` and `/action_server` created by `diana_hardware`. When launched with a namespace, all of these node names are prefixed with it; for example, with the default `NS_1` of `diana.config.yaml` the node is `/NS_1/service_server`. The only exception is `rviz2`: only one instance is started, and it is not in the namespace.

### Starting Controllers and Checking Their State

`diana.launch.py` only starts the broadcasters (`joint_state_broadcaster` and `diana_robot_state_broadcaster`); it does not load any example controller. Example controllers are loaded by `example.launch.py` through a `spawner`: `controllers.yaml` declares the type of every controller, but only the controllers named in `controller_names` are loaded and activated. A controller that is not named does not exist in the controller manager, so you cannot switch to it while the launch is running. To change the controller, stop the current launch and start it again with a different `controller_names`.

Use the following command to see the controllers that are currently loaded and their states:

```bash
ros2 control list_controllers
```

If the robot was started in a namespace, select its controller manager with `-c`, for example `ros2 control list_controllers -c /NS_1/controller_manager`.

```{important}
`diana_hardware` works in only one control mode at a time: torque (effort), joint velocity, joint position, Cartesian pose, or Cartesian velocity (the last two optionally with an elbow command). Deactivate the current controller before switching to a controller that uses a different mode. The elbow command interface must be claimed together with the Cartesian pose or Cartesian velocity interface; otherwise the hardware interface reports an error.
```

## Namespace Enabled Launch Files

`example.launch.py` reads a YAML configuration file, includes `diana.launch.py` once for each robot in it, and starts one controller per robot as given by `controller_names`. It is meant for multi-robot and namespace setups, where command-line arguments cannot distinguish between robots.

```{figure} ../../../../_static/images/ros2-humble-bringup-launch-en.png
:alt: Nodes started by example.launch.py and diana.launch.py
:width: 100%

Launch structure of `example.launch.py`: it reads the configuration file, includes `diana.launch.py` once for each robot, and then loads the controller named by `controller_names`.
```

| Launch argument | Default | Description |
| --- | --- | --- |
| `robot_config_file` | `config/diana.config.yaml` of `diana_bringup` | Path of the robot configuration file |
| `robot_ips` | empty string | Comma-separated IP list; when non-empty it overrides `robot_ip` in the configuration file |
| `controller_names` | none (must be given on the command line) | Comma-separated controller names, which must be names declared in `controllers.yaml` |

```bash
ros2 launch diana_bringup example.launch.py \
  controller_names:=gravity_compensation_example_controller
```

Controllers are loaded by a `spawner` with `--controller-manager-timeout 30`, using the parameters from `controllers.yaml`. For the purpose and prerequisites of each controller see [diana_example_controllers](diana_example_controllers.md).

```{warning}
Example controllers move the arm or output torques. With real hardware, make sure the workspace is clear and the emergency stop is reachable, and put the arm in a pose suitable for the example. Most examples need the real `diana_hardware` interface and cannot run on simulated hardware; see [diana_example_controllers](diana_example_controllers.md).
```

### `diana.config.yaml` Fields

The default `config/diana.config.yaml` enables a single robot, `ROBOT1`. Top-level keys (`ROBOT1`, `ROBOT2`, ...) are arbitrary mnemonic identifiers. Boolean values must be quoted (`"true"` / `"false"`). Each robot entry contains the following fields; `example.launch.py` reads all of them directly, so a missing one causes an error:

| Field | Value in the default file | Description |
| --- | --- | --- |
| `robot_type` | `"diana3"` | Arm model, passed to `diana.launch.py`; `diana3` is only an example value, change it to your own model (`diana3`, `diana7`, or `diana7g2`) |
| `arm_prefix` | `""` | Name prefix |
| `fake_sensor_commands` | `"false"` | Simulated sensor commands |
| `joint_state_rate` | `30` | Joint state publish rate (Hz) |
| `namespace` | `"NS_1"` | Namespace of this robot; may be an empty string; must be unique across robots in a multi-robot setup |
| `robot_ip` | `"192.168.10.75"` | Robot IP or hostname |
| `use_fake_hardware` | `"false"` | Whether to use simulated hardware |
| `use_rviz` | `"true"` | Whether to start RViz |

When any entry has `use_rviz` set to `"true"`, `example.launch.py` starts a single `rviz2` instance (configuration `rviz/visualize_diana.rviz` from `diana_description`). When only one entry enables RViz and it has a namespace, the `robot_description` topic is remapped to `/<namespace>/robot_description`.

### Multiple Robots

To start several robots at once, add entries to the configuration file and give each robot a different `namespace`. `ROBOT2` and `ROBOT3` in the default file are commented-out templates; after uncommenting them you must set `robot_type` to each robot's model and fill in each robot's own `robot_ip`:

```yaml
ROBOT2:
  robot_type: "diana3"
  arm_prefix: ""
  fake_sensor_commands: "false"
  joint_state_rate: 30
  namespace: "NS_2"
  robot_ip: "<robot-ip>"
  use_fake_hardware: "false"
  use_rviz: "false"
```

Using a custom configuration file:

```bash
ros2 launch diana_bringup example.launch.py \
  robot_config_file:=/path/to/my_robots.config.yaml \
  controller_names:=gravity_compensation_example_controller
```

### Controller Names and Robot IP Lists

`controller_names` and `robot_ips` are comma-separated lists that map one-to-one onto the robots in the configuration file, in order:

```bash
ros2 launch diana_bringup example.launch.py \
  robot_ips:=<robot-ip>,<robot-ip> \
  controller_names:=gravity_compensation_example_controller,joint_impedance_example_controller
```

The rules (see `diana_bringup.launch_utils.get_parameter_for_config`) are:

- When the list length equals the number of robots, the N-th value is used for the N-th robot;
- When the lengths differ, a warning is printed and the first value is used for all robots;
- When `robot_ips` is empty, `robot_ip` from the configuration file is used;
- An empty `controller_names` exits the launch immediately.

```{important}
When loading a controller for a robot, `example.launch.py` indexes the raw `controller_names` list by robot index. In a multi-robot setup, give one controller name per robot instead of relying on the fallback of using a single name for all robots. Do not put spaces around the names.
```

## Joint Impedance With IK Launch

`joint_impedance_with_ik_example_controller.launch.py` builds on `example.launch.py`: it always uses `joint_impedance_with_ik_example_controller` and additionally includes `move_group.launch.py` from `diana_moveit_config` for each robot in the configuration file, so that the controller can solve inverse kinematics through the MoveIt `compute_ik` service. The MoveIt services are in the same namespace as the robot, for example `/NS_1/compute_ik`, `/NS_1/compute_fk`, `/NS_1/compute_cartesian_path`, and `/NS_1/plan_kinematic_path`.

```bash
ros2 launch diana_bringup joint_impedance_with_ik_example_controller.launch.py
```

The file has a single launch argument, `robot_config_file` (default `diana.config.yaml`). It reads `robot_ip`, `namespace`, `use_fake_hardware`, `fake_sensor_commands`, `use_rviz`, `arm_prefix`, and `robot_type` from every entry and passes them to `move_group.launch.py`, so all of these fields must be present.

```{warning}
This controller outputs torques with a joint impedance law and makes the arm perform a small motion. It needs the real `diana_hardware` interface and a working `compute_ik` service. Before running it, make sure the workspace is clear, the emergency stop is reachable, and `use_fake_hardware` in the configuration file is `"false"`. For MoveIt see [diana_moveit_config](diana_moveit_config.md); for the controller see [diana_example_controllers](diana_example_controllers.md).
```

## Non-realtime Robot Parameter Setting

Together with the hardware interface, `diana_hardware` creates a node named `service_server` inside the `ros2_control_node` process. It offers the following non-realtime parameter services (types defined in [diana_msgs](diana_msgs.md)). They exist only with the real hardware interface (`use_fake_hardware` set to `false`). The service names carry the namespace the robot was launched with: `/service_server/...` without a namespace, and `/NS_1/service_server/...` with the default `NS_1` of `diana.config.yaml`. The table lists the names without a namespace.

### Service List

| Service | Type | Request fields |
| --- | --- | --- |
| `service_server/set_joint_stiffness` | `diana_msgs/srv/SetJointStiffness` | `joint_stiffness` (7 values) |
| `service_server/set_cartesian_stiffness` | `diana_msgs/srv/SetCartesianStiffness` | `cartesian_stiffness` (x, y, z, roll, pitch, yaw, 6 values, applied along the stiffness frame) |
| `service_server/set_tcp_frame` | `diana_msgs/srv/SetTCPFrame` | `transformation` (4x4 column-major matrix, 16 values, the transform NE_T_EE from NE to EE) |
| `service_server/set_stiffness_frame` | `diana_msgs/srv/SetStiffnessFrame` | `transformation` (4x4 column-major matrix, 16 values, the transform EE_T_K from EE to K) |
| `service_server/set_force_torque_collision_behavior` | `diana_msgs/srv/SetForceTorqueCollisionBehavior` | Lower and upper nominal torque (7) and nominal force (6) thresholds |
| `service_server/set_full_collision_behavior` | `diana_msgs/srv/SetFullCollisionBehavior` | Lower and upper torque (7) and force (6) thresholds for both the acceleration phase and the nominal phase |
| `service_server/set_load` | `diana_msgs/srv/SetLoad` | `mass`, `center_of_mass` (3), `load_inertia` (3x3 column-major, 9 values) |

Every response is a `bool success` plus a `string error`; if the underlying call throws, `success` is `false` and `error` carries the exception message.

`set_tcp_frame` and `set_stiffness_frame` each set the transform between two adjacent frames: the former sets the transform NE_T_EE from the nominal end-effector frame NE to the end-effector frame EE, the latter the transform EE_T_K from EE to the stiffness frame K. Both are set at runtime through services.

```{figure} ../../../../_static/images/ros2-humble-frames-en.png
:alt: Transform chain between the frames NE, EE, and K
:width: 100%

The transform chain between NE, EE, and K, and the two services that set it.
```

```{warning}
The load, the end-effector frame transforms, and the collision thresholds directly affect the robot's torque estimation and protective-stop behavior. Set them to match your actual tooling, and re-verify at conservative speeds after any change.
```

## Non-realtime ROS 2 Actions

`diana_hardware` also creates a node named `action_server` in the same process. It offers the action `action_server/error_recovery` (type `diana_msgs/action/ErrorRecovery`; goal, result, and feedback are all empty). On receiving a goal it calls `robot->automaticErrorRecovery()`: on success the goal succeeds, and if an exception is thrown the goal is aborted and the error is logged. The namespace rule is the same as for the services above; the example below uses `NS_1`, so drop `/NS_1` if you launched without a namespace.

```bash
ros2 action send_goal /NS_1/action_server/error_recovery diana_msgs/action/ErrorRecovery {}
```

```{important}
Automatic error recovery only clears the robot's current recoverable error; it does not replace finding out why the robot stopped. After a collision, protective stop, or other safety-related stop, first confirm the site is safe and then run the recovery; see [Safety Boundaries](../../../reference/safety.md).
```

## Tests

`test/README.md` groups the tests into the categories below (only test files that exist in the Diana source tree are listed):

| Category | Needs a real robot | Test files |
| --- | --- | --- |
| Fake-hardware integration | No | `test_fake_hardware_controllers.py` |
| Interface validation | No | `test_diana_arm_interfaces.py`, `test_xacro_path_resolution.py`, `test_gazebo_wrapper_expansion.py` |
| Launch file parsing | No | `test_launch_file_parsing.py` |
| Real-hardware smoke tests | Yes | `test_hardware_example_controllers.py`, `test_hardware_generic_controller.py` |

Run the tests that need no hardware:

```bash
colcon test --packages-select diana_bringup \
  --ctest-args --exclude-regex 'test_hardware'
```

The hardware tests take the robot address from the CMake variable `ROBOT_IP`.

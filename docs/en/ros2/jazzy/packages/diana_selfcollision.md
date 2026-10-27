# Self-Collision Checking

Package name: `diana_selfcollision`

## Installation

See [Development Setup](../development.md).

## Package Overview

`diana_selfcollision` provides self-collision checking for the Diana Duo; its version is given in its `package.xml` (currently `1.0.0`). The package contains:

- The shared library `diana_selfcollision`: the class `SelfCollisionChecker`, which builds a model with Pinocchio from a URDF and an SRDF and decides whether the links of the robot collide for given joint positions.
- The executable `self_collision_node`: subscribes to the joint states, runs the check above, and publishes whether a self-collision occurs.
- The parameter file `config/self_collision_node.yaml`.

The collision geometry used by the check is taken from the `<collision>` elements of the robot URDF; link pairs declared with `disable_collisions` in the SRDF are excluded. The URDF and SRDF of the Diana Duo are generated from `robots/diana_duo/` in [Robot Description](diana_description.md); `diana_selfcollision` depends on `diana_description` at runtime.

## Node

The executable `self_collision_node` is installed in `lib/diana_selfcollision/` and is run with `ros2 run`. The node name is `self_collision_monitor`.

On startup the node works as follows:

1. It loads the parameters from `config/self_collision_node.yaml`.
2. It waits for a `robot_state_publisher` node in the same namespace and reads its `robot_description` parameter as the URDF.
3. It reads its own `robot_description_semantic` parameter as the SRDF.
4. It builds the checking model from the URDF and SRDF and starts subscribing to `joint_states`.

If `robot_description` cannot be obtained, the node exits with an error; if the URDF or the SRDF is empty, the node throws an exception and terminates. For every `joint_states` message the node updates the positions of the matching joints, runs one collision check, and publishes the result.

### Topics

Topic names are relative; when the node runs in a namespace they carry the namespace prefix. Both topics use `rclcpp::SensorDataQoS()` (best effort), so the peer must use a compatible QoS.

| Topic | Type | Direction | Description |
| --- | --- | --- | --- |
| `joint_states` | `sensor_msgs/msg/JointState` | Subscribed | Joint names and positions. Only single-DoF joints of the model are used; joints that do not appear in the message stay at the neutral position |
| `collision_detected` | `std_msgs/msg/Bool` | Published | `true` means the current pose is in self-collision (or within the security margin) |

On a collision the node logs the warning `COLLISION DETECTED! Robot is in self-collision!` at most once per second.

### Parameters

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `security_margin` | double | `0.045` | Security margin in meters. Geometries closer than this value are treated as colliding |
| `print_collisions` | bool | `false` | If `true`, the pairs of colliding link geometries are logged after a collision is detected (throttled to once every 500 ms) |
| `robot_description_semantic` | string | empty | XML text of the SRDF, used to exclude link pairs that may touch. It must be supplied by the user; the node cannot start if it is empty |

The values of `security_margin` and `print_collisions` come from `config/self_collision_node.yaml` (applied to `/**`):

```yaml
/**:
    ros__parameters:
      security_margin: 0.045
      print_collisions: false
```

## Usage

The package does not provide a launch file. You need a `robot_state_publisher` node that publishes `robot_description` and a node that publishes `joint_states` in the same namespace, and you pass `robot_description_semantic` as a parameter. The following launch snippet is for the Diana Duo; the SRDF is generated from `robots/diana_duo/diana_duo.srdf.xacro` of `diana_description`:

```python
import xacro
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

srdf_path = get_package_share_directory("diana_description") + "/robots/diana_duo/diana_duo.srdf.xacro"
robot_description_semantic = xacro.process_file(srdf_path).toprettyxml(indent="  ")

self_collision_node = Node(
    package="diana_selfcollision",
    executable="self_collision_node",
    parameters=[{"robot_description_semantic": robot_description_semantic}],
)
```

If the robot model is generated with non-default arguments such as `robot_types` or `arm_prefixes`, pass the same `mappings` when generating the SRDF; otherwise the link names in the SRDF do not match the URDF.

```{important}
The link geometry in the URDF determines the result. When using the Diana Duo URDF, use the same `robot_types` and `arm_prefixes` for the SRDF.
```

To view the result:

```bash
ros2 topic echo /collision_detected --qos-reliability best_effort
```

## Relation to Diana Duo

The package description and tests target the Diana Duo: the `test/` directory holds the URDF and SRDF of the Diana Duo, and the unit tests use them to build a checking model with 14 joints. The joints and links of the model come from the URDF that is passed in, so the node itself does not hard-code a robot model; the model is determined by `robot_description`.

## License

The `package.xml` of `diana_selfcollision` declares the Apache License 2.0.

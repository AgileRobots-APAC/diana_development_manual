# 自碰撞检测

软件包名称：`diana_selfcollision`

## 安装

请参阅 [开发准备](../development.md)。

## 软件包概述

`diana_selfcollision` 为 Diana Duo 提供自碰撞检测，版本号见其 `package.xml`（当前为 `1.0.0`）。软件包包含：

- 共享库 `diana_selfcollision`：类 `SelfCollisionChecker`，用 Pinocchio 根据 URDF 和 SRDF 构建模型，判断给定关节位置下机器人各连杆之间是否碰撞。
- 可执行文件 `self_collision_node`：订阅关节状态，调用上述检测，并发布是否发生自碰撞。
- 参数文件 `config/self_collision_node.yaml`。

检测使用的碰撞几何取自机器人 URDF 中的 `<collision>` 元素，SRDF 中声明的 `disable_collisions` 连杆对不参与检测。Diana Duo 的 URDF 和 SRDF 由 [机器人描述](diana_description.md) 中的 `robots/diana_duo/` 生成；`diana_selfcollision` 在运行时依赖 `diana_description`。

## 节点

可执行文件 `self_collision_node` 位于 `lib/diana_selfcollision/`，用 `ros2 run` 运行。节点名称为 `self_collision_monitor`。

启动时，节点按以下顺序工作：

1. 加载 `config/self_collision_node.yaml` 中的参数。
2. 等待同一命名空间下的 `robot_state_publisher` 节点，并读取它的 `robot_description` 参数作为 URDF。
3. 读取自己的 `robot_description_semantic` 参数作为 SRDF。
4. 用 URDF 和 SRDF 构建检测模型，开始订阅 `joint_states`。

如果得不到 `robot_description`，节点以错误退出；如果 URDF 或 SRDF 为空，节点抛出异常并终止。每收到一条 `joint_states`，节点就更新对应关节的位置、执行一次碰撞检测，并发布结果。

### 话题

话题名称是相对名称，节点在命名空间中运行时会带上命名空间前缀。两个话题都使用 `rclcpp::SensorDataQoS()`（best effort），订阅方和发布方需使用兼容的 QoS。

| 话题 | 类型 | 方向 | 说明 |
| --- | --- | --- | --- |
| `joint_states` | `sensor_msgs/msg/JointState` | 订阅 | 关节名称和位置。只使用模型中单自由度的关节，消息中没有出现的关节保持在中性位置 |
| `collision_detected` | `std_msgs/msg/Bool` | 发布 | `true` 表示当前姿态存在自碰撞（或进入安全裕度） |

发生碰撞时，节点每秒最多输出一次警告日志 `COLLISION DETECTED! Robot is in self-collision!`。

### 参数

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `security_margin` | double | `0.045` | 安全裕度，单位米。几何体之间的距离小于该值即判为碰撞 |
| `print_collisions` | bool | `false` | 为 `true` 时，检测到碰撞后输出发生碰撞的连杆几何体对（日志限流为每 500 ms 一次） |
| `robot_description_semantic` | string | 空 | SRDF 的 XML 文本，用于排除允许碰撞的连杆对。必须由使用者提供，为空时节点无法启动 |

`security_margin` 与 `print_collisions` 的取值来自 `config/self_collision_node.yaml`（对 `/**` 生效）：

```yaml
/**:
    ros__parameters:
      security_margin: 0.045
      print_collisions: false
```

## 使用

本软件包不提供 launch 文件。使用时需要同一命名空间下有发布 `robot_description` 的 `robot_state_publisher` 节点和发布 `joint_states` 的节点，并通过参数传入 `robot_description_semantic`。下面是一个 Diana Duo 的 launch 示例片段，SRDF 由 `diana_description` 的 `robots/diana_duo/diana_duo.srdf.xacro` 生成：

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

在使用 `robot_types`、`arm_prefixes` 等非默认参数生成机器人模型时，生成 SRDF 要传入相同的 `mappings`，否则 SRDF 中的连杆名称与 URDF 对不上。

```{important}
URDF 中的连杆几何体决定检测结果。使用 Diana Duo 的 URDF 时，需要与 SRDF 使用同一组 `robot_types` 和 `arm_prefixes`。
```

查看检测结果：

```bash
ros2 topic echo /collision_detected --qos-reliability best_effort
```

## 与 Diana Duo 的关系

软件包的描述和测试针对 Diana Duo：`test/` 目录中有 Diana Duo 的 URDF 和 SRDF，单元测试用它们构建 14 个关节的检测模型。模型中的关节和连杆都来自传入的 URDF，所以节点本身不写死机型，机器人模型由 `robot_description` 决定。

## 许可证

`diana_selfcollision` 的 `package.xml` 声明使用 Apache License 2.0。

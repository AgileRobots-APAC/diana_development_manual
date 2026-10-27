"""Sidebar navigation shared by the Chinese and English sites.

Both language trees use identical document names, so the structure is defined
once here. A label of ``None`` falls back to the page's own H1 title; give an
explicit label only where the sidebar should be shorter than the title.

Every built page (except ``index``) must appear exactly once in this tree —
the theme's ``check_navigation`` warns (and the strict build fails) otherwise. When adding,
renaming or removing a page, update this file together with the toctree.
"""
from __future__ import annotations

from agile_docs_theme import Node, Section


SDK_EXAMPLES = [
    "01_connection",
    "02_robot_state",
    "03_joint_motion",
    "04_cartesian_motion",
    "05_kinematics",
    "06_io",
    "07_tcp_and_frames",
    "08_motion_limits",
    "09_path_and_waypoints",
    "10_jog_motion",
    "11_force_guarded_motion",
    "12_servoL_realtime",
]

# Sidebar labels for the C++ and Python example lists (shorter than some H1s).
SDK_EXAMPLE_LABELS = {
    "01_connection": ("01 连接与型号识别", "01 Connection and Model Identification"),
    "02_robot_state": ("02 机器人状态与诊断", "02 Robot State and Diagnostics"),
    "03_joint_motion": ("03 关节运动", "03 Joint Motion"),
    "04_cartesian_motion": ("04 笛卡尔运动", "04 Cartesian Motion"),
    "05_kinematics": ("05 运动学", "05 Kinematics"),
    "06_io": ("06 I/O", "06 I/O"),
    "07_tcp_and_frames": ("07 TCP、坐标系与负载", "07 TCP, Frames, and Payload"),
    "08_motion_limits": ("08 运动限制", "08 Motion Limits"),
    "09_path_and_waypoints": ("09 路径与路点", "09 Paths and Waypoints"),
    "10_jog_motion": ("10 点动运动", "10 Jog Motion"),
    "11_force_guarded_motion": ("11 力阈值停止", "11 Force-Guarded Stop"),
    "12_servoL_realtime": ("12 ServoL 实时下发", "12 ServoL Realtime Streaming"),
}


def _sdk_examples(prefix: str) -> tuple[Node, ...]:
    return tuple(
        Node(f"{prefix}/{name}", *SDK_EXAMPLE_LABELS[name]) for name in SDK_EXAMPLES
    )


FCI_CPP_EXAMPLES = [
    ("01_echo_robot_state", "01 连续状态读取", "01 echo_robot_state"),
    ("02_communication_test", "02 通信性能检查", "02 communication_test"),
    ("03_print_joint_poses", "03 打印预设关节位姿", "03 print_joint_poses"),
    ("04_async_position_control", "04 异步位置控制", "04 async_position_control"),
    ("05_joint_point_to_point_motion", "05 关节点到点运动", "05 joint_point_to_point_motion"),
    ("06_generate_joint_position_motion", "06 关节位置控制回调", "06 generate_joint_position_motion"),
    ("07_generate_joint_velocity_motion", "07 关节速度控制回调", "07 generate_joint_velocity_motion"),
    ("08_generate_consecutive_motions", "08 连续关节运动", "08 generate_consecutive_motions"),
    ("09_generate_elbow_motion", "09 带 Elbow 的笛卡尔运动", "09 generate_elbow_motion"),
    ("10_generate_cartesian_pose_motion", "10 笛卡尔位姿控制", "10 generate_cartesian_pose_motion"),
    ("11_generate_cartesian_velocity_motion", "11 笛卡尔速度控制", "11 generate_cartesian_velocity_motion"),
    ("12_generate_cartesian_pose_motion_external_control_loop", "12 笛卡尔位姿外部控制循环", "12 generate_cartesian_pose_motion_external_control_loop"),
    ("13_generate_cartesian_velocity_motion_external_control_loop", "13 笛卡尔速度外部控制循环", "13 generate_cartesian_velocity_motion_external_control_loop"),
    ("14_generate_joint_position_motion_external_control_loop", "14 关节位置外部控制循环", "14 generate_joint_position_motion_external_control_loop"),
    ("15_generate_joint_velocity_motion_external_control_loop", "15 关节速度外部控制循环", "15 generate_joint_velocity_motion_external_control_loop"),
    ("16_motion_with_control_external_control_loop", "16 组合控制外部控制循环", "16 motion_with_control_external_control_loop"),
    ("17_joint_impedance_control", "17 关节阻抗控制", "17 joint_impedance_control"),
    ("18_cartesian_impedance_control", "18 笛卡尔阻抗控制", "18 cartesian_impedance_control"),
    ("19_force_control", "19 力控制", "19 force_control"),
    ("20_motion_with_control", "20 运动生成与力矩控制组合", "20 motion_with_control"),
]

FCI_PYTHON_EXAMPLES = [
    ("01_print_robot_state", "01 打印机器人状态", "01 print_robot_state"),
    ("02_joint_position_example", "02 关节位置控制", "02 joint_position_example"),
    ("03_joint_velocity_example", "03 关节速度控制", "03 joint_velocity_example"),
    ("04_cartesian_pose_example", "04 笛卡尔位姿控制", "04 cartesian_pose_example"),
    ("05_cartesian_velocity_example", "05 笛卡尔速度控制", "05 cartesian_velocity_example"),
    ("06_joint_impedance_example", "06 关节阻抗控制", "06 joint_impedance_example"),
]


def _labelled(prefix: str, entries: list[tuple[str, str, str]]) -> tuple[Node, ...]:
    return tuple(Node(f"{prefix}/{name}", zh, en) for name, zh, en in entries)


def _sdk_guide(module: str, title: str) -> Node:
    return Node(
        f"{module}/index", title, title, module=module,
        children=(
            Node(f"{module}/overview", "概述与版本要求", "Overview and Version Requirements"),
            Node(f"{module}/development", "开发准备", "Development Preparation"),
            Node(f"{module}/quick_start", "快速开始", "Quick Start"),
            Node(f"{module}/examples/index", "Example 总览", "Example Overview",
                 children=_sdk_examples(f"{module}/examples")),
        ),
    )


NAVIGATION: tuple[Section, ...] = (
    Section("接口概述", "Overview", (
        Node("about/overview", "手册概述", "Manual Scope"),
        Node("about/concepts", "核心概念", "Core Concepts", children=(
            Node("guide/control_modes", "控制模型与模式选择", "Control Models and Mode Selection"),
            Node("guide/robot_state", "状态、反馈与回调", "State, Feedback, and Callbacks"),
            Node("guide/kinematics", "坐标、位姿与运动学", "Coordinates, Poses, and Kinematics", children=(
                Node("guide/inverse_uniqueness", "逆解选择与构型连续性", "Inverse Solutions and Configuration Continuity"),
            )),
        )),
        Node("about/versions", "版本与更新", "Versions and Updates", children=(
            Node("about/building_docs", "构建与发布本手册", "Building and Publishing This Manual"),
        )),
    )),
    Section("编程指南", "Programming Guide", (
        Node("programming/network", "网络配置", "Network Setup"),
        _sdk_guide("cpp", "C++ SDK"),
        _sdk_guide("python", "Python SDK"),
        Node("fci/index", "FCI", "FCI", module="fci", children=(
            Node("fci/overview", "概述与版本要求", "Overview and Version Requirements"),
            Node("fci/machines", "选择机械臂型号", "Select a Robot Model", children=(
                Node("fci/machines/diana3"),
                Node("fci/machines/diana7"),
                Node("fci/machines/diana7g2"),
            )),
            Node("fci/development", "开发准备", "Development Preparation"),
            Node("fci/realtime_network", "实时网络与系统配置", "Realtime Network and System Configuration"),
            Node("fci/control_modes", "控制模式与数据流", "Control Modes and Data Flow"),
            Node("fci/quick_start", "快速开始", "Quick Start"),
            Node("fci/examples/index", "Example 总览", "Example Overview", children=(
                Node("fci/examples/cpp/index", "C++ FCI 示例", "C++ FCI Examples",
                     children=_labelled("fci/examples/cpp", FCI_CPP_EXAMPLES)),
                Node("fci/examples/python/index", "Python FCI 示例", "Python FCI Examples",
                     children=_labelled("fci/examples/python", FCI_PYTHON_EXAMPLES)),
            )),
            Node("fci/faq", "FAQ：常见问题与解决方案", "FAQ: Common Issues and Solutions"),
        )),
        Node("ros2/index", "ROS 2", "ROS 2", module="ros2", children=(
            Node("ros2/overview", "概述与版本选择", "Overview and Distribution Selection"),
            Node("ros2/humble/index", "Humble", "Humble", module="ros2_humble", children=(
                Node("ros2/humble/development", "开发准备", "Development Setup"),
                Node("ros2/humble/quick_start", "快速开始", "Quick Start"),
                Node("ros2/humble/packages/index", "软件包", "Packages", children=(
                    Node("ros2/humble/packages/diana_bringup", "启动与运行配置", "diana_bringup"),
                    Node("ros2/humble/packages/diana_description", "机器人描述", "diana_description"),
                    Node("ros2/humble/packages/diana_example_controllers", "示例控制器", "diana_example_controllers"),
                    Node("ros2/humble/packages/diana_moveit_config", "MoveIt 配置", "diana_moveit_config"),
                    Node("ros2/humble/packages/diana_gazebo_bringup", "Gazebo 仿真", "diana_gazebo_bringup"),
                    Node("ros2/humble/packages/diana_hardware", "硬件接口", "diana_hardware"),
                    Node("ros2/humble/packages/diana_msgs", "消息、服务与动作", "diana_msgs"),
                    Node("ros2/humble/packages/diana_robot_state_broadcaster", "机器人状态广播器", "diana_robot_state_broadcaster"),
                    Node("ros2/humble/packages/diana_semantic_components", "语义组件", "diana_semantic_components"),
                )),
            )),
            Node("ros2/jazzy/index", "Jazzy", "Jazzy", module="ros2_jazzy", children=(
                Node("ros2/jazzy/development", "开发准备", "Development Setup"),
                Node("ros2/jazzy/quick_start", "快速开始", "Quick Start"),
                Node("ros2/jazzy/packages/index", "软件包", "Packages", children=(
                    Node("ros2/jazzy/packages/diana_bringup", "启动与运行配置", "diana_bringup"),
                    Node("ros2/jazzy/packages/diana_description", "机器人描述", "diana_description"),
                    Node("ros2/jazzy/packages/franka_example_controllers", "示例控制器", "franka_example_controllers"),
                    Node("ros2/jazzy/packages/diana_moveit_config", "MoveIt 配置", "diana_moveit_config"),
                    Node("ros2/jazzy/packages/diana_gazebo_bringup", "Gazebo 仿真", "diana_gazebo_bringup"),
                    Node("ros2/jazzy/packages/franka_hardware", "硬件接口", "franka_hardware"),
                    Node("ros2/jazzy/packages/franka_msgs", "消息、服务与动作", "franka_msgs"),
                    Node("ros2/jazzy/packages/franka_robot_state_broadcaster", "机器人状态广播器", "franka_robot_state_broadcaster"),
                    Node("ros2/jazzy/packages/franka_semantic_components", "语义组件", "franka_semantic_components"),
                    Node("ros2/jazzy/packages/diana_selfcollision", "自碰撞检测", "diana_selfcollision"),
                )),
            )),
        )),
    )),
    Section("参考", "Reference", (
        Node("reference/units", "单位与数据约定", "Units and Conventions"),
        Node("reference/safety", "安全边界", "Safety Notes"),
        Node("reference/io", "I/O 与映射", "I/O and Mapping"),
        Node("reference/error_codes", "错误码", "Error Codes"),
        Node("reference/troubleshooting", "故障排查", "Troubleshooting"),
    )),
)

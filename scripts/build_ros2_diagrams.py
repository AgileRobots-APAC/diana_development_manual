#!/usr/bin/env python3
"""Render the ROS 2 Humble diagrams used by the diana_bringup page.

Requires Graphviz (`dot`) and the Noto Sans CJK SC font. Writes the PNG files of the Humble package pages (Chinese and English) to docs/_static/images/.

Usage: scripts/build_ros2_diagrams.py
"""
from __future__ import annotations

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "_static" / "images"
FONT = "Noto Sans CJK SC"

BLUE = 'fillcolor="#EAF2FD" color="#2F6DB5"'
GREEN = 'fillcolor="#EAF6EA" color="#3A8A3A"'
GRAY = 'fillcolor="#F4F5F7" color="#6B7280"'
AMBER = 'fillcolor="#FFF6E5" color="#B7791F"'

HEAD = f"""
digraph G {{
  bgcolor="white"; pad=0.3; dpi=160; fontname="{FONT}";
  node [shape=box style="rounded,filled" fontname="{FONT}" fontsize=14 margin="0.22,0.14" penwidth=1.6];
  edge [color="#4B5563" penwidth=1.4 arrowsize=0.8 fontname="{FONT}" fontsize=12 fontcolor="#374151"];
"""

TEXT = {
    "zh": {
        "cfg": "diana.config.yaml\\n每个机器人一个条目",
        "read": "读取",
        "include": "为每个机器人包含一次",
        "rsp": "robot_state_publisher",
        "cm": "ros2_control_node\\ncontroller_manager、diana_hardware\\n参数：controllers.yaml",
        "jsp": "joint_state_publisher",
        "jsb": "spawner\\njoint_state_broadcaster\\n(加载并激活后退出)",
        "rsb": "spawner\\ndiana_robot_state_broadcaster\\n(加载并激活后退出)",
        "rsb_note": "使用模拟硬件时不加载",
        "ctrl": "spawner\\ncontroller_names 指定的控制器",
        "rviz": "rviz2",
        "rviz_note": "use_rviz 为 \\\"true\\\" 时启动",
        "ne": "NE\\n名义末端坐标系",
        "ee": "EE\\n末端执行器坐标系",
        "k": "K\\n刚度坐标系",
        "ne_ee": "NE_T_EE\\n服务 set_tcp_frame",
        "ee_k": "EE_T_K\\n服务 set_stiffness_frame",
        "k_note": "笛卡尔刚度（set_cartesian_stiffness）\\n在 K 的各轴方向上生效",
        "k_note2": "外力旋量话题 k_f_ext_hat_k\\n在 K 中给出",
        "sc_hw": "diana_hardware 导出的接口",
        "sc_cls": "diana_semantic_components 中的类",
        "sc_use": "使用它们的软件包 / 控制器",
        "sc_base_ros": "继承 ros2_control 的\\nSemanticComponentInterface",
        "sc_base_diana": "继承 DianaSemanticComponentInterface",
        "sc_if_state": "robot_state\\n状态接口",
        "sc_if_model": "robot_model\\n状态接口",
        "sc_if_pose": "cartesian_pose_command\\ncartesian_pose_state\\n(及 elbow 接口)",
        "sc_if_vel": "cartesian_velocity\\n(及 elbow 接口)",
        "fl_h1": "控制器的回调", "fl_h2": "在回调中调用的语义组件方法",
        "fl_cfg": "on_init / on_configure", "fl_cfg_m": "构造语义组件类\\n(传入 arm_prefix、robot_type 或 URDF)",
        "fl_ifc": "state_interface_configuration()\\ncommand_interface_configuration()", "fl_ifc_m": "get_state_interface_names()\\nget_command_interface_names()",
        "fl_act": "on_activate", "fl_act_m": "assign_loaned_state_interfaces()\\nassign_loaned_command_interfaces()",
        "fl_upd": "update()（每个控制周期，1 kHz）", "fl_upd_m": "读取：getMassMatrix()、getCurrentPoseMatrix()、\\nget_values_as_message() 等\\n写入：setCommand()",
        "fl_deact": "on_deactivate", "fl_deact_m": "release_interfaces()",
        "fl_lend": "controller manager 按返回的名称\\n借出接口",
        "dp_note": "箭头由依赖方指向被依赖方",
        "dp_ext": "外部依赖",
        "hw_ctrl": "控制器\\n(通过语义组件)", "hw_cmd": "命令接口\\n关节 / 笛卡尔 / 肘部", "hw_state": "状态接口\\n关节 / 位姿 / 肘部 / 传感器\\nrobot_state / robot_model / robot_time",
        "hw_plugin": "DianaHardwareInterface\\n(ros2_control 硬件插件)", "hw_srv": "service_server\\nSet* 参数服务", "hw_act": "action_server\\nErrorRecovery 动作", "hw_robot": "Diana 机器人控制器",
        "hw_in_cm": "同在 ros2_control_node 进程内", "hw_write": "write() 每周期写入一种命令模式", "hw_read": "read() 每周期读取完整状态",
        "bc_if": "robot_state\\n状态接口", "bc_upd": "update()\\n实时循环：拷贝状态", "bc_buf": "无锁三重缓冲区", "bc_pub": "发布线程\\nSCHED_FIFO 优先级 50", "bc_full": "~/robot_state\\n每个控制周期（1000 Hz）", "bc_conv": "便捷话题\\n每 N 个周期一次，best effort", "bc_conv_note": "N = max(1, 1000 / convenience_publish_rate)",
        "gz_launch": "gazebo_diana_arm_example_controller.launch.py", "gz_gz": "Gazebo\\n(empty.sdf -r)", "gz_rsp": "robot_state_publisher\\n发布 /robot_description", "gz_create": "ros_gz_sim create\\n生成机器人", "gz_plugin": "gz_ros2_control 插件\\n(diana_gazebo_hardware)\\n参数：<robot_type>_gazebo_controllers.yaml", "gz_spawn": "spawner\\njoint_state_broadcaster\\n及 controller 指定的控制器", "gz_rviz": "rviz2\\n(rviz 为 true 时)",
        "mv_launch": "moveit.launch.py", "mv_mg": "move_group\\n规划组 <robot_type>_arm", "mv_cm": "ros2_control_node\\n(真实或模拟硬件)", "mv_rsp": "robot_state_publisher\\njoint_state_publisher", "mv_ctrl": "轨迹控制器\\n<robot_type>_arm_controller", "mv_rviz": "rviz2\\nMotionPlanning 面板", "mv_act": "MoveGroup 动作\\n(Plan / Execute)",
    },
    "en": {
        "cfg": "diana.config.yaml\\none entry per robot",
        "read": "reads",
        "include": "included once per robot",
        "rsp": "robot_state_publisher",
        "cm": "ros2_control_node\\ncontroller_manager, diana_hardware\\nparameters: controllers.yaml",
        "jsp": "joint_state_publisher",
        "jsb": "spawner\\njoint_state_broadcaster\\n(exits after activating it)",
        "rsb": "spawner\\ndiana_robot_state_broadcaster\\n(exits after activating it)",
        "rsb_note": "not loaded with fake hardware",
        "ctrl": "spawner\\ncontroller named by controller_names",
        "rviz": "rviz2",
        "rviz_note": "started when use_rviz is \\\"true\\\"",
        "ne": "NE\\nnominal end-effector frame",
        "ee": "EE\\nend-effector frame",
        "k": "K\\nstiffness frame",
        "ne_ee": "NE_T_EE\\nservice set_tcp_frame",
        "ee_k": "EE_T_K\\nservice set_stiffness_frame",
        "k_note": "Cartesian stiffness (set_cartesian_stiffness)\\nacts along the axes of K",
        "k_note2": "external wrench topic k_f_ext_hat_k\\nis expressed in K",
        "sc_hw": "Interfaces exported by diana_hardware",
        "sc_cls": "Classes in diana_semantic_components",
        "sc_use": "Packages / controllers that use them",
        "sc_base_ros": "extends ros2_control\\nSemanticComponentInterface",
        "sc_base_diana": "extends DianaSemanticComponentInterface",
        "sc_if_state": "robot_state\\nstate interface",
        "sc_if_model": "robot_model\\nstate interface",
        "sc_if_pose": "cartesian_pose_command\\ncartesian_pose_state\\n(and elbow interfaces)",
        "sc_if_vel": "cartesian_velocity\\n(and elbow interfaces)",
        "fl_h1": "Controller callbacks", "fl_h2": "Semantic component methods called in them",
        "fl_cfg": "on_init / on_configure", "fl_cfg_m": "construct the semantic component classes\\n(pass arm_prefix, robot_type or the URDF)",
        "fl_ifc": "state_interface_configuration()\\ncommand_interface_configuration()", "fl_ifc_m": "get_state_interface_names()\\nget_command_interface_names()",
        "fl_act": "on_activate", "fl_act_m": "assign_loaned_state_interfaces()\\nassign_loaned_command_interfaces()",
        "fl_upd": "update() (every control cycle, 1 kHz)", "fl_upd_m": "read: getMassMatrix(), getCurrentPoseMatrix(),\\nget_values_as_message(), ...\\nwrite: setCommand()",
        "fl_deact": "on_deactivate", "fl_deact_m": "release_interfaces()",
        "fl_lend": "the controller manager lends the\\ninterfaces with the returned names",
        "dp_note": "Arrows point from the dependent package to the package it depends on",
        "dp_ext": "External dependencies",
        "hw_ctrl": "Controllers\\n(via the semantic components)", "hw_cmd": "Command interfaces\\njoint / Cartesian / elbow", "hw_state": "State interfaces\\njoint / pose / elbow / sensor\\nrobot_state / robot_model / robot_time",
        "hw_plugin": "DianaHardwareInterface\\n(ros2_control hardware plugin)", "hw_srv": "service_server\\nSet* parameter services", "hw_act": "action_server\\nErrorRecovery action", "hw_robot": "Diana robot controller",
        "hw_in_cm": "inside the ros2_control_node process", "hw_write": "write(): one command mode per cycle", "hw_read": "read(): full state every cycle",
        "bc_if": "robot_state\\nstate interface", "bc_upd": "update()\\nreal-time loop: copies the state", "bc_buf": "lock-free triple buffer", "bc_pub": "publisher thread\\nSCHED_FIFO priority 50", "bc_full": "~/robot_state\\nevery control cycle (1000 Hz)", "bc_conv": "convenience topics\\nevery N cycles, best effort", "bc_conv_note": "N = max(1, 1000 / convenience_publish_rate)",
        "gz_launch": "gazebo_diana_arm_example_controller.launch.py", "gz_gz": "Gazebo\\n(empty.sdf -r)", "gz_rsp": "robot_state_publisher\\npublishes /robot_description", "gz_create": "ros_gz_sim create\\nspawns the robot", "gz_plugin": "gz_ros2_control plugin\\n(diana_gazebo_hardware)\\nparameters: <robot_type>_gazebo_controllers.yaml", "gz_spawn": "spawner\\njoint_state_broadcaster\\nand the controller named by controller", "gz_rviz": "rviz2\\n(when rviz is true)",
        "mv_launch": "moveit.launch.py", "mv_mg": "move_group\\nplanning group <robot_type>_arm", "mv_cm": "ros2_control_node\\n(real or fake hardware)", "mv_rsp": "robot_state_publisher\\njoint_state_publisher", "mv_ctrl": "trajectory controller\\n<robot_type>_arm_controller", "mv_rviz": "rviz2\\nMotionPlanning panel", "mv_act": "MoveGroup action\\n(Plan / Execute)",
    },
}


def launch_dot(t: dict) -> str:
    return HEAD + f"""
  rankdir=LR; nodesep=0.3; ranksep=0.75; compound=true;
  cfg [label="{t['cfg']}" {GRAY}];
  ex  [label="example.launch.py" {BLUE}];
  subgraph cluster_robot {{
    label="{t['include']}"; labeljust="l"; fontname="{FONT}"; fontsize=13; fontcolor="#2F6DB5";
    style="rounded,dashed"; color="#2F6DB5"; penwidth=1.4; margin=18;
    dl  [label="diana.launch.py" {BLUE}];
    rsp [label="{t['rsp']}" {GREEN}];
    cm  [label="{t['cm']}" {GREEN}];
    jsp [label="{t['jsp']}" {GREEN}];
    jsb [label="{t['jsb']}" {GREEN}];
    rsb [label="{t['rsb']}\\n({t['rsb_note']})" {GREEN} style="rounded,filled,dashed"];
  }}
  ctrl [label="{t['ctrl']}" {GREEN}];
  rviz [label="{t['rviz']}\\n({t['rviz_note']})" {GREEN} style="rounded,filled,dashed"];
  cfg -> ex [label="{t['read']}"];
  ex -> dl;
  ex -> ctrl;
  ex -> rviz [style=dashed];
  dl -> rsp; dl -> cm; dl -> jsp; dl -> jsb; dl -> rsb [style=dashed];
}}
"""


def frames_dot(t: dict) -> str:
    return HEAD + f"""
  rankdir=LR; nodesep=0.5; ranksep=1.1;
  ne [label="{t['ne']}" {BLUE}];
  ee [label="{t['ee']}" {BLUE}];
  k  [label="{t['k']}" {BLUE}];
  note1 [label="{t['k_note']}" {GRAY} style="rounded,filled,dashed"];
  note2 [label="{t['k_note2']}" {GRAY} style="rounded,filled,dashed"];
  ne -> ee [label="{t['ne_ee']}" penwidth=2];
  ee -> k  [label="{t['ee_k']}" penwidth=2];
  k -> note1 [style=dashed arrowhead=none];
  k -> note2 [style=dashed arrowhead=none];
}}
"""


def semantic_dot(t: dict) -> str:
    return HEAD + f"""
  rankdir=LR; nodesep=0.28; ranksep=0.9; compound=true;
  node [fontsize=13];
  subgraph cluster_hw {{
    label="{t['sc_hw']}"; labeljust="l"; fontname="{FONT}"; fontsize=13; fontcolor="#6B7280";
    style="rounded,dashed"; color="#6B7280"; margin=14;
    i_state [label="{t['sc_if_state']}" {GRAY}];
    i_model [label="{t['sc_if_model']}" {GRAY}];
    i_pose  [label="{t['sc_if_pose']}" {GRAY}];
    i_vel   [label="{t['sc_if_vel']}" {GRAY}];
  }}
  subgraph cluster_cls {{
    label="{t['sc_cls']}"; labeljust="l"; fontname="{FONT}"; fontsize=13; fontcolor="#2F6DB5";
    style="rounded,dashed"; color="#2F6DB5"; margin=14;
    c_state [label="DianaRobotState\\n{t['sc_base_ros']}" {BLUE}];
    c_model [label="DianaRobotModel\\n{t['sc_base_ros']}" {BLUE}];
    c_pose  [label="DianaCartesianPoseInterface\\n{t['sc_base_diana']}" {BLUE}];
    c_vel   [label="DianaCartesianVelocityInterface\\n{t['sc_base_diana']}" {BLUE}];
  }}
  subgraph cluster_use {{
    label="{t['sc_use']}"; labeljust="l"; fontname="{FONT}"; fontsize=13; fontcolor="#3A8A3A";
    style="rounded,dashed"; color="#3A8A3A"; margin=14;
    u_state [label="diana_robot_state_broadcaster" {GREEN}];
    u_model [label="model_example_controller" {GREEN}];
    u_ik    [label="joint_impedance_with_ik_example_controller" {GREEN}];
    u_pose  [label="cartesian_pose_example_controller\\ncartesian_orientation_example_controller\\ncartesian_elbow_example_controller" {GREEN}];
    u_vel   [label="cartesian_velocity_example_controller\\nelbow_example_controller" {GREEN}];
  }}
  i_state -> c_state; i_state -> c_model; i_model -> c_model;
  i_pose -> c_pose; i_vel -> c_vel;
  c_state -> u_state;
  c_model -> u_model; c_model -> u_ik;
  c_pose -> u_pose; c_pose -> u_ik;
  c_vel -> u_vel;
}}
"""


def flow_dot(t: dict) -> str:
    return HEAD + f"""
  rankdir=TB; nodesep=0.5; ranksep=0.45;
  h1 [label="{t['fl_h1']}" shape=plaintext style="" fontcolor="#2F6DB5" fontsize=15];
  h2 [label="{t['fl_h2']}" shape=plaintext style="" fontcolor="#3A8A3A" fontsize=15];
  cfg [label="{t['fl_cfg']}" {BLUE}];
  ifc [label="{t['fl_ifc']}" {BLUE}];
  lend [label="{t['fl_lend']}" {GRAY} style="rounded,filled,dashed"];
  act [label="{t['fl_act']}" {BLUE}];
  upd [label="{t['fl_upd']}" {BLUE}];
  deact [label="{t['fl_deact']}" {BLUE}];
  cfg_m [label="{t['fl_cfg_m']}" {GREEN}];
  ifc_m [label="{t['fl_ifc_m']}" {GREEN}];
  act_m [label="{t['fl_act_m']}" {GREEN}];
  upd_m [label="{t['fl_upd_m']}" {GREEN}];
  deact_m [label="{t['fl_deact_m']}" {GREEN}];
  h1 -> cfg [style=invis]; h2 -> cfg_m [style=invis];
  cfg -> ifc -> lend -> act -> upd -> deact;
  {{ rank=same; h1; h2; }}
  {{ rank=same; cfg; cfg_m; }}
  {{ rank=same; ifc; ifc_m; }}
  {{ rank=same; act; act_m; }}
  {{ rank=same; upd; upd_m; }}
  {{ rank=same; deact; deact_m; }}
  cfg -> cfg_m [dir=none style=dashed]; ifc -> ifc_m [dir=none style=dashed];
  act -> act_m [dir=none style=dashed]; upd -> upd_m [dir=none style=dashed];
  deact -> deact_m [dir=none style=dashed];
}}
"""


def deps_dot(t: dict) -> str:
    return HEAD + f"""
  rankdir=TB; nodesep=0.35; ranksep=0.9;
  edge [color="#6B7280" penwidth=1.2];
  moveit [label="diana_moveit_config" {GREEN}];
  gzb    [label="diana_gazebo_bringup" {GREEN}];
  bring  [label="diana_bringup" {GREEN}];
  gzh    [label="diana_gazebo_hardware" {BLUE}];
  exa    [label="diana_example_controllers" {BLUE}];
  bc     [label="diana_robot_state_broadcaster" {BLUE}];
  sem    [label="diana_semantic_components" {BLUE}];
  hw     [label="diana_hardware" {BLUE}];
  msgs   [label="diana_msgs" {AMBER}];
  desc   [label="diana_description" {AMBER}];
  subgraph cluster_ext {{
    label="{t['dp_ext']}"; labeljust="l"; fontname="{FONT}"; fontsize=13; fontcolor="#6B7280";
    style="rounded,dashed"; color="#6B7280"; margin=12;
    ff [label="libfranka 0.18.2" {GRAY}];
  }}
  moveit -> bring; moveit -> desc; moveit -> hw;
  gzb -> gzh; gzb -> desc; gzb -> hw;
  gzh -> hw; gzh -> desc;
  bring -> exa; bring -> bc; bring -> hw; bring -> desc;
  exa -> sem; exa -> msgs;
  bc -> sem; bc -> msgs;
  sem -> hw; sem -> msgs;
  hw -> msgs; hw -> ff;
}}
"""


def hardware_dot(t: dict) -> str:
    return HEAD + f"""
  rankdir=LR; nodesep=0.4; ranksep=0.9;
  ctrl  [label="{t['hw_ctrl']}" {BLUE}];
  cmd   [label="{t['hw_cmd']}" {GRAY}];
  state [label="{t['hw_state']}" {GRAY}];
  subgraph cluster_cm {{
    label="{t['hw_in_cm']}"; labeljust="l"; fontname="{FONT}"; fontsize=13; fontcolor="#3A8A3A";
    style="rounded,dashed"; color="#3A8A3A"; margin=14;
    plugin [label="{t['hw_plugin']}" {GREEN}];
    srv [label="{t['hw_srv']}" {GREEN}];
    act [label="{t['hw_act']}" {GREEN}];
  }}
  robot [label="{t['hw_robot']}" {AMBER}];
  {{ rank=same; cmd; state; }}
  ctrl -> cmd; cmd -> plugin [label="{t['hw_write']}"];
  plugin -> state [label="{t['hw_read']}" constraint=false]; state -> ctrl [constraint=false];
  plugin -> robot [dir=both];
  srv -> robot; act -> robot;
}}
"""


def broadcaster_dot(t: dict) -> str:
    return HEAD + f"""
  rankdir=LR; nodesep=0.35; ranksep=0.8;
  i   [label="{t['bc_if']}" {GRAY}];
  u   [label="{t['bc_upd']}" {BLUE}];
  b   [label="{t['bc_buf']}" {AMBER}];
  p   [label="{t['bc_pub']}" {BLUE}];
  f   [label="{t['bc_full']}" {GREEN}];
  c   [label="{t['bc_conv']}\\n{t['bc_conv_note']}" {GREEN}];
  i -> u -> b -> p; p -> f; p -> c;
}}
"""


def gazebo_dot(t: dict) -> str:
    return HEAD + f"""
  rankdir=TB; nodesep=0.3; ranksep=0.6;
  l   [label="{t['gz_launch']}" {BLUE}];
  g   [label="{t['gz_gz']}" {GREEN}];
  rsp [label="{t['gz_rsp']}" {GREEN}];
  cr  [label="{t['gz_create']}" {GREEN}];
  pl  [label="{t['gz_plugin']}" {GREEN}];
  sp  [label="{t['gz_spawn']}" {GREEN}];
  rv  [label="{t['gz_rviz']}" {GREEN} style="rounded,filled,dashed"];
  l -> g; l -> rsp; l -> cr; l -> sp; l -> rv [style=dashed];
  rsp -> cr [label="/robot_description"];
  cr -> g [label=""]; g -> pl [style=dashed arrowhead=none];
  sp -> pl [label="controller_manager"];
}}
"""


def moveit_dot(t: dict) -> str:
    return HEAD + f"""
  rankdir=TB; nodesep=0.3; ranksep=0.6;
  l    [label="{t['mv_launch']}" {BLUE}];
  mg   [label="{t['mv_mg']}" {GREEN}];
  cm   [label="{t['mv_cm']}" {GREEN}];
  rsp  [label="{t['mv_rsp']}" {GREEN}];
  ctrl [label="{t['mv_ctrl']}" {GREEN}];
  rv   [label="{t['mv_rviz']}" {GREEN} style="rounded,filled,dashed"];
  act  [label="{t['mv_act']}" {GRAY}];
  l -> mg; l -> cm; l -> rsp; l -> rv [style=dashed];
  cm -> ctrl [label="spawner"];
  mg -> ctrl [label="FollowJointTrajectory"];
  rv -> act -> mg;
}}
"""


JAZZY_TEXT = {
    "zh": {
        "ext": "外部依赖", "note": "",
        "cfg": "机器人配置文件\\n(如 diana.config.yaml)", "read": "读取", "include": "为每个机器人包含一次",
        "cm": "ros2_control_node\\ncontroller_manager、franka_hardware\\n参数：controllers.yaml",
        "jsp": "joint_state_publisher", "rsp": "robot_state_publisher",
        "jsb": "spawner\\njoint_state_broadcaster\\n(加载并激活后退出)",
        "rsb": "spawner\\nfranka_robot_state_broadcaster\\n(加载并激活后退出)", "rsb_note": "仅真实硬件时加载",
        "ctrl": "spawner\\ncontroller_names 指定的控制器", "rviz": "rviz2", "rviz_note": "use_rviz 为 \\\"true\\\" 时启动",
    },
    "en": {
        "ext": "External dependencies", "note": "",
        "cfg": "Robot configuration file\\n(e.g. diana.config.yaml)", "read": "reads", "include": "included once per robot",
        "cm": "ros2_control_node\\ncontroller_manager, franka_hardware\\nparameters: controllers.yaml",
        "jsp": "joint_state_publisher", "rsp": "robot_state_publisher",
        "jsb": "spawner\\njoint_state_broadcaster\\n(exits after activating it)",
        "rsb": "spawner\\nfranka_robot_state_broadcaster\\n(exits after activating it)", "rsb_note": "real hardware only",
        "ctrl": "spawner\\ncontroller named by controller_names", "rviz": "rviz2", "rviz_note": "started when use_rviz is \\\"true\\\"",
    },
}


def jazzy_deps_dot(t: dict) -> str:
    return HEAD + f"""
  rankdir=TB; nodesep=0.35; ranksep=0.9;
  edge [color="#6B7280" penwidth=1.2];
  moveit [label="diana_moveit_config" {GREEN}];
  gzb    [label="diana_gazebo_bringup" {GREEN}];
  bring  [label="diana_bringup" {GREEN}];
  gzh    [label="diana_gazebo_hardware" {BLUE}];
  exa    [label="franka_example_controllers" {BLUE}];
  bc     [label="franka_robot_state_broadcaster" {BLUE}];
  sem    [label="franka_semantic_components" {BLUE}];
  hw     [label="franka_hardware" {BLUE}];
  msgs   [label="franka_msgs" {AMBER}];
  desc   [label="diana_description" {AMBER}];
  sc     [label="diana_selfcollision" {BLUE}];
  subgraph cluster_ext {{
    label="{t['ext']}"; labeljust="l"; fontname="{FONT}"; fontsize=13; fontcolor="#6B7280";
    style="rounded,dashed"; color="#6B7280"; margin=12;
    ff [label="libfranka 0.18.2" {GRAY}];
  }}
  moveit -> bring; moveit -> desc; moveit -> hw;
  gzb -> gzh; gzb -> desc; gzb -> hw; gzb -> exa;
  gzh -> hw; gzh -> desc;
  bring -> exa; bring -> bc; bring -> hw; bring -> desc;
  exa -> sem; exa -> msgs;
  bc -> sem; bc -> msgs;
  sem -> hw; sem -> msgs;
  hw -> msgs; hw -> ff;
  sc -> desc; sc -> msgs;
}}
"""


def jazzy_launch_dot(t: dict) -> str:
    return HEAD + f"""
  rankdir=LR; nodesep=0.3; ranksep=0.75; compound=true;
  cfg [label="{t['cfg']}" {GRAY}];
  ex  [label="diana.example_controllers.launch.py" {BLUE}];
  subgraph cluster_robot {{
    label="{t['include']}"; labeljust="l"; fontname="{FONT}"; fontsize=13; fontcolor="#2F6DB5";
    style="rounded,dashed"; color="#2F6DB5"; penwidth=1.4; margin=18;
    dl  [label="diana.launch.py" {BLUE}];
    rsp [label="{t['rsp']}" {GREEN}];
    cm  [label="{t['cm']}" {GREEN}];
    jsp [label="{t['jsp']}" {GREEN}];
    jsb [label="{t['jsb']}" {GREEN}];
    rsb [label="{t['rsb']}\\n({t['rsb_note']})" {GREEN} style="rounded,filled,dashed"];
  }}
  ctrl [label="{t['ctrl']}" {GREEN}];
  rviz [label="{t['rviz']}\\n({t['rviz_note']})" {GREEN} style="rounded,filled,dashed"];
  cfg -> ex [label="{t['read']}"];
  ex -> dl;
  ex -> ctrl;
  ex -> rviz [style=dashed];
  dl -> rsp; dl -> cm; dl -> jsp; dl -> jsb; dl -> rsb [style=dashed];
}}
"""


def render(dot: str, target: Path) -> None:
    subprocess.run(["dot", "-Tpng", "-o", str(target)], input=dot.encode("utf-8"), check=True)
    print(f"[diagrams] wrote {target.relative_to(ROOT)}")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for lang, t in TEXT.items():
        render(launch_dot(t), OUT / f"ros2-humble-bringup-launch-{lang}.png")
        render(frames_dot(t), OUT / f"ros2-humble-frames-{lang}.png")
        render(semantic_dot(t), OUT / f"ros2-humble-semantic-components-{lang}.png")
        render(flow_dot(t), OUT / f"ros2-humble-semantic-flow-{lang}.png")
        render(deps_dot(t), OUT / f"ros2-humble-package-deps-{lang}.png")
        render(hardware_dot(t), OUT / f"ros2-humble-hardware-dataflow-{lang}.png")
        render(broadcaster_dot(t), OUT / f"ros2-humble-broadcaster-flow-{lang}.png")
        render(gazebo_dot(t), OUT / f"ros2-humble-gazebo-launch-{lang}.png")
        render(moveit_dot(t), OUT / f"ros2-humble-moveit-launch-{lang}.png")
        jt = JAZZY_TEXT[lang]
        render(jazzy_deps_dot(jt), OUT / f"ros2-jazzy-package-deps-{lang}.png")
        render(jazzy_launch_dot(jt), OUT / f"ros2-jazzy-bringup-launch-{lang}.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())

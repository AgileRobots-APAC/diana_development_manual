# FCI Examples

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

选择现场机械臂并应用对应 overlay 补丁后，FCI 示例分为两个并列入口：

```text
FCI Examples
├── C++     libfranka/examples/<model>/
└── Python  libfranka/pylibfranka/examples/<model>/
```

| 语言 | 示例来源 | 入口 |
|---|---|---|
| C++ | `libfranka/examples/<model>/` | [C++ FCI 示例](cpp/index.md) |
| Python | `libfranka/pylibfranka/examples/<model>/` | [Python FCI 示例](python/index.md) |

`<model>` 为 `diana3`、`diana7` 或 `diana7G2`。夹爪相关的上游 C++ 与 Python 文件不受 Diana FCI 支持，均不属于本教程范围。

(fci-initial-pose)=
## 初始姿态

大多数 FCI 示例启动后会先用 `MotionGenerator` 把机械臂移到固定的初始关节角 `q_goal`，再进入各自的控制回调。这是示例的**第一个实际运动**。Diana 补丁修改了上游 libfranka 的初始姿态，且不同机型取值不同：

| 来源 | J1 | J2 | J3 | J4 | J5 | J6 | J7 |
|---|---|---|---|---|---|---|---|
| 上游 libfranka 0.18.2 | 0 | −π/4 | 0 | −3π/4 | 0 | π/2 | π/4 |
| `diana3`、`diana7G2` | 0 | −π/4 | 0 | **3π/4** | 0 | π/2 | π/4 |
| `diana7` | 0 | −π/4 | 0 | **3π/4** | 0 | **−π/2** | π/4 |

`motion_with_control` 例外：三个机型的 J4 均为 π/2，其余关节与所在机型上表一致。

会先移至初始姿态的示例：

- **C++**：`communication_test`、`generate_joint_position_motion`、`generate_joint_velocity_motion`、`generate_consecutive_motions`、`generate_elbow_motion`、`generate_cartesian_pose_motion`、`generate_cartesian_velocity_motion`、四个 `*_external_control_loop` 运动示例、`motion_with_control_external_control_loop`、`joint_impedance_control`、`motion_with_control`。
- **Python**：`joint_velocity_example`、`cartesian_velocity_example`；`diana3` 的 `cartesian_pose_example` 也会先移至初始姿态。

```{warning}
第 4 关节的方向与上游 libfranka 相反。不要按 Franka 官方资料预判机械臂的初始位置；运行前请按上表和所选机型确认工作空间净空、线缆和工装不会发生干涉。
```

```{toctree}
:hidden:

cpp/index
python/index
```

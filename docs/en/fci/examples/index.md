# FCI Examples

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

After selecting the physical robot and applying its overlay patch, FCI examples have two peer entry points:

```text
FCI Examples
├── C++     libfranka/examples/<model>/
└── Python  libfranka/pylibfranka/examples/<model>/
```

| Language | Example source | Entry point |
|---|---|---|
| C++ | `libfranka/examples/<model>/` | [C++ FCI Examples](cpp/index.md) |
| Python | `libfranka/pylibfranka/examples/<model>/` | [Python FCI Examples](python/index.md) |

`<model>` is `diana3`, `diana7`, or `diana7G2`. Gripper-related upstream C++ and Python files are unsupported by Diana FCI and outside this guide.

(fci-initial-pose)=
## Initial Pose

Most FCI examples first use `MotionGenerator` to move the robot to a fixed initial joint configuration `q_goal`, then enter their own control callback. This is the **first real motion** of the example. The Diana patches change the upstream libfranka initial pose, and the values differ by model:

| Source | J1 | J2 | J3 | J4 | J5 | J6 | J7 |
|---|---|---|---|---|---|---|---|
| Upstream libfranka 0.18.2 | 0 | −π/4 | 0 | −3π/4 | 0 | π/2 | π/4 |
| `diana3`, `diana7G2` | 0 | −π/4 | 0 | **3π/4** | 0 | π/2 | π/4 |
| `diana7` | 0 | −π/4 | 0 | **3π/4** | 0 | **−π/2** | π/4 |

`motion_with_control` is the exception: J4 is π/2 on all three models, and the other joints match that model's row above.

Examples that first move to the initial pose:

- **C++**: `communication_test`, `generate_joint_position_motion`, `generate_joint_velocity_motion`, `generate_consecutive_motions`, `generate_elbow_motion`, `generate_cartesian_pose_motion`, `generate_cartesian_velocity_motion`, the four `*_external_control_loop` motion examples, `motion_with_control_external_control_loop`, `joint_impedance_control`, and `motion_with_control`.
- **Python**: `joint_velocity_example` and `cartesian_velocity_example`; on `diana3`, `cartesian_pose_example` also moves to the initial pose first.

```{warning}
Joint 4 moves in the opposite direction from upstream libfranka. Do not predict the robot's initial position from Franka documentation; before running, use the table above and the selected model to confirm that the workspace, cables, and fixtures are clear.
```

```{toctree}
:hidden:

cpp/index
python/index
```

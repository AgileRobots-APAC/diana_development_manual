# Overview and Version Requirements

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

FCI (a Franka Control Interface-style realtime control interface) is intended for applications that need high-frequency, low-latency control. Diana FCI uses `diana_libfranka_overlay` as its project entry point: it pins an upstream `libfranka 0.18.2` submodule and provides direct C++ and Python examples through robot-specific patches, without ROS2.

## Scope

- Fixed-cycle external controllers.
- Joint position, joint velocity, Cartesian pose, and Cartesian velocity control.
- Torque control based on model terms, Jacobians, and external-torque estimates.
- Advanced applications that need realtime state, dynamics, and control feedback.

## Release Baseline

For realtime troubleshooting and application releases, record the following components as one set. The FCI overlay applies a patch per robot-model branch, so record the overlay version and the tag of the robot-model branch actually used (for example `v1.0.0-libfranka0.18.2-diana3`) rather than using a baseline from another robot model:

::::{div} release-baseline-chain
:::{div} release-baseline-step
<span class="release-baseline-index">01</span>
<div><strong>Controller software version and robot model</strong><small>Controller capability and the Diana model actually in use</small></div>
:::
:::{div} release-baseline-step
<span class="release-baseline-index">02</span>
<div><strong>Overlay version and robot-model branch tag</strong><small>For example <code>v1.0.0-libfranka0.18.2-diana3</code>, <code>v1.0.0-libfranka0.18.2-diana7</code>, or <code>v1.0.0-libfranka0.18.2-diana7g2</code></small></div>
:::
:::{div} release-baseline-step
<span class="release-baseline-index">03</span>
<div><strong>Pinned <code>libfranka 0.18.2</code> submodule, headers, and runtime</strong><small>Do not mix another libfranka release</small></div>
:::
:::{div} release-baseline-step
<span class="release-baseline-index">04</span>
<div><strong>This documentation release tag</strong><small>The documentation version that matches the components above</small></div>
:::
::::

## Versions and Project

| Item | Value |
|---|---|
| Overlay repository | [diana_libfranka_overlay](https://github.com/AgileRobots-APAC/diana_libfranka_overlay.git) |
| Overlay version | 1.0.0 (for software version 3.3.0); robot-model branch tags: `v1.0.0-libfranka0.18.2-diana3`, `v1.0.0-libfranka0.18.2-diana7`, `v1.0.0-libfranka0.18.2-diana7g2` |
| FCI interface and submodule | `libfranka 0.18.2` (pinned by the overlay) |
| Supported robots | Diana3, Diana7, and Diana7G2; each branch contains one robot patch |
| Upstream source | [`libfranka 0.18.2`](https://github.com/frankarobotics/libfranka/tree/0.18.2) |
| API documentation | [`libfranka 0.18.2` C++ API Reference](https://frankarobotics.github.io/libfranka/0.18.2/index.html) |
| Example language | C++17 |
| Build system | CMake |

## References

The FCI interfaces in this chapter are checked against the overlay work tree after applying the selected robot patch, the [`libfranka 0.18.2` source](https://github.com/frankarobotics/libfranka/tree/0.18.2), and the official [`0.18.2` C++ API Reference](https://frankarobotics.github.io/libfranka/0.18.2/index.html), with emphasis on `franka::Robot`, `franka::RobotState`, `franka::Model`, and the motion and torque command types in `control_types.h`.
```{important}
Do not mix signatures or behavior descriptions from another `libfranka` version.
```
## Relationship to the Ordinary C++ SDK

The ordinary C++ SDK examples are better suited to discrete motion commands, I/O, paths, tool frames, and controller functions. FCI examples target realtime callbacks and lower-level control inputs, where the application must provide continuous targets or torques inside the control cycle.
```{attention}
FCI should not replace all ordinary SDK functionality. Use it when realtime closed-loop control, model calculations, or torque control are genuinely needed.
```
## Prerequisites

1. The control PC has a stable network connection to the controller, and the realtime control path has been validated.
2. The robot, tool, payload, collision thresholds, and workspace have passed a safety review.
3. The application callback completes within the control period and performs no blocking I/O.
4. The application has defined abnormal-stop, error-recovery, and site emergency-stop procedures.

```{note}
This documentation is based on the selected patch result in the overlay and the `libfranka 0.18.2` API reference. Final signatures, behavior, and availability still follow the `libfranka` headers and controller software shipped with the Diana FCI release.
```

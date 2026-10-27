# FCI Development Guide

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

FCI (a Franka Control Interface-style realtime control interface) is intended for developers who need high-frequency, low-latency control. It is typically used for external controllers, realtime trajectory streaming, force-control workflows, or lower-level closed-loop control.

```{warning}
FCI has different prerequisites from ordinary C++ SDK motion APIs. Before entering FCI, confirm realtime network behavior, control mode, limits, emergency stop, payload, collision detection, and site safety. Do not apply ordinary SDK example procedures directly to FCI.
```

## Use Cases

- An external controller needs to stream targets at a fixed cycle.
- The application needs higher-rate feedback and a tighter control loop.
- The application needs advanced joint, Cartesian pose, velocity, force, or torque control.
- The team already has robot safety review, realtime-system setup, and abnormal-stop handling in place.

## Reading Order

1. Complete the shared [Network Setup](../programming/network.md) so the control PC can communicate with the controller cabinet.
2. Read [Control Models and Mode Selection](../guide/control_modes.md) to confirm whether FCI is appropriate for the task.
3. Read [State, Feedback, and Callbacks](../guide/robot_state.md) to understand data freshness, error codes, and abnormal-stop strategy.
4. Continue later with FCI interfaces, realtime cycle configuration, examples, and troubleshooting.

## Select the Robot Model

Before installing or running an example, select the physical robot and apply its overlay patch: [Diana3, Diana7, or Diana7G2](machines.md). Only one model patch may be applied in a `libfranka` work tree at a time.

## External References

- [`libfranka 0.18.2` source](https://github.com/frankarobotics/libfranka/tree/0.18.2): Headers, implementation, and upstream examples for the version used by this chapter.
- [`libfranka 0.18.2` C++ API Reference](https://frankarobotics.github.io/libfranka/0.18.2/index.html): API details for `franka::Robot`, `franka::RobotState`, `franka::Model`, and control command types.

Follow this chapter for Diana FCI support, installation, and operating requirements, and use the `libfranka 0.18.2` headers shipped with Diana FCI as the authority for signatures and behavior.

## Contents

```{toctree}
overview
machines
development
realtime_network
control_modes
quick_start
examples/index
faq
```

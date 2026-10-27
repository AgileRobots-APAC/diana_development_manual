# FAQ: Common Issues and Solutions

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

This page collects common FCI issues. Entries are grouped by topic and collapsed by default so the page stays easy to scan.

## Repository and Patches

::::{dropdown} Q: Why are the model-specific examples missing after cloning the overlay repository?
:class-container: api-example-block

**Symptom**

- `libfranka/examples/<model>/` or `libfranka/pylibfranka/examples/<model>/` is missing.
- CMake or runtime commands cannot find the expected examples.

**Possible Cause**

- The repository submodules were not initialized.
- The patch for the target robot model has not been applied.

**Fix**

1. Make sure the overlay repository and submodules are fully checked out.
2. Apply the patch for the target robot model.
3. Check that a `diana3`, `diana7`, or `diana7G2` directory now appears under `libfranka/examples/` and `libfranka/pylibfranka/examples/`.

**Safety Note**

- Do not run examples patched for a different robot model on a real robot.

::::

::::{dropdown} Q: The patch is applied, but the example paths in the documentation do not match the local tree
:class-container: api-example-block

**Symptom**

- The documentation points to `libfranka/examples/<model>/xxx.cpp`, but the local directory or file names differ.
- An entry in the example overview has no matching source file locally.

**Possible Cause**

- The overlay repository version does not match the documentation.
- The wrong robot-model patch was applied.
- Gripper-related upstream examples are outside the supported Diana FCI scope.

**Fix**

1. Check that the overlay repository version matches this documentation.
2. Make sure `<model>` is one of the supported patched directories: `diana3`, `diana7`, or `diana7G2`.
3. Use the patched example directory as the source of truth when updating the example list.

**Safety Note**

- The guide covers the supported Diana FCI example set, not every upstream `libfranka` example.

::::

## Build and Dependencies

::::{dropdown} Q: `ensurepip is not available` when creating a Python virtual environment
:class-container: api-example-block

**Symptom**

```text
The virtual environment was not created successfully because ensurepip is not available.
```

**Possible Cause**

- The Debian/Ubuntu `python3-venv` package for the active Python version is missing.

**Fix**

1. Install the matching `python3-venv` package.
2. Remove the incomplete `.venv` directory in the documentation repository.
3. Recreate the virtual environment and install dependencies.

**Safety Note**

- Only remove the incomplete `.venv` under this repository. Do not clean system Python directories.

::::

## Realtime Network and System

::::{dropdown} Q: Communication quality is unstable in `communication_test`
:class-container: api-example-block

**Symptom**

- Control command success rate is low.
- Lost control cycles increase.
- Network or realtime exceptions appear during control.

**Possible Cause**

- Realtime system configuration is incomplete.
- NIC, IRQ affinity, CPU scheduling, or power-saving settings affect the control cycle.
- The network link has problems such as a switch in the path, a non-direct connection, the cable, or the IP configuration.

**Fix**

1. Check realtime kernel, permissions, and scheduling setup.
2. Verify that the link between the application machine and the controller is stable; prefer a direct or deterministic network link.
3. Run read-only examples first to confirm stable state reading.
4. Run `communication_test` only after safety checks are complete.

**Safety Note**

- `communication_test` is not read-only. It moves to an initial pose and enters a zero-torque control session.

::::

::::{dropdown} Q: Can `echo_robot_state` replace `communication_test` for realtime-control quality checks?
:class-container: api-example-block

**Symptom**

- `echo_robot_state` prints robot state successfully, but control examples still report communication or realtime errors.

**Possible Cause**

- `echo_robot_state` only reads state and does not send motion or torque commands.
- A stable read-only link does not prove that the 1 kHz control read/write loop satisfies realtime requirements.

**Fix**

1. Use `echo_robot_state` to confirm basic connection and state reading.
2. Check the realtime network and system configuration.
3. After the safety conditions are met, use `communication_test` to evaluate the control read/write communication quality.

**Safety Note**

- Do not run motion or torque-control examples just because a read-only example works.

::::

## Running Examples Safely

::::{dropdown} Q: Which FCI examples are read-only?
:class-container: api-example-block

**Symptom**

- You need a safe connectivity check before running motion or torque examples.

**Possible Cause**

- FCI examples include read-only state access, motion generation, external control loops, and torque control.

**Fix**

1. Use `echo_robot_state` for continuous state reading.
2. Use `print_joint_poses` for one-shot state reading and model pose computation.
3. Treat all other FCI examples as motion or torque-control examples unless documented otherwise.

**Safety Note**

- For non-read-only examples, confirm E-stop, workspace clearance, load, collision thresholds, and recovery path before running.

::::

::::{dropdown} Q: What is the difference between Python FCI examples and ordinary Diana Python SDK examples?
:class-container: api-example-block

**Symptom**

- The documentation contains both ordinary Python SDK examples and Python FCI examples, with different interface names.

**Possible Cause**

- Python FCI examples use `pylibfranka` and live under `libfranka/pylibfranka/examples/<model>/`.
- Ordinary Diana Python SDK examples use the Diana SDK Python wrapper and are a different API family.

**Fix**

1. Check the current chapter title: Python examples in the FCI chapter use `pylibfranka`.
2. Follow the paths and interfaces listed in the Python FCI overview.
3. Do not apply ordinary Python SDK interface names directly to FCI examples.

**Safety Note**

- C++ FCI and Python FCI examples that enter motion or torque control both require real-robot safety checks.

::::

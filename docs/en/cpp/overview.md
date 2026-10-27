# C++ SDK Overview

This chapter is for engineers developing control-PC applications with the Diana C/C++ SDK. The SDK covers connection management, motion, state feedback, I/O, kinematics, TCP/payload, paths, and real-time control. The API reference and SDK headers for the matching release are authoritative for individual function parameters.

## Release baseline

The manual is based on Industrial API Manual **V3.4.0**. Record all of the following when diagnosing an issue or releasing an application, so that one document is not used to explain the behavior of a different binary release:

::::{div} release-baseline-chain
:::{div} release-baseline-step
<span class="release-baseline-index">01</span>
<div><strong>Controller software version</strong><small>Software actually running on the robot controller</small></div>
:::
:::{div} release-baseline-step
<span class="release-baseline-index">02</span>
<div><strong>C/C++ SDK <code>version</code> file and headers</strong><small>Compile-time interface and SDK package version</small></div>
:::
:::{div} release-baseline-step
<span class="release-baseline-index">03</span>
<div><strong>Example version and the SDK version it pins</strong><small>Reproducible example-source baseline</small></div>
:::
:::{div} release-baseline-step
<span class="release-baseline-index">04</span>
<div><strong>This documentation release tag</strong><small>Documentation version paired with the components above</small></div>
:::
::::

Function parameters, limits, and availability may change between SDK releases. Always integrate against the released SDK's `include/`, `lib/`, `version` file, and release notes.

The current SDK's `version` file records the release version; at runtime, `getLibraryVersion()` reads the library version. Save both values when releasing or troubleshooting.

When this manual was checked, the SDK `version` file contained `industry-v3.4.0.260605`, which identifies the baseline; use the SDK, API manual, and release notes installed at the customer site for actual integration.

The shared libraries bundled in the repository target Linux x86_64. Linux aarch64 or Windows users must use a complete SDK package delivered for the control PC's operating system and architecture.

## Interface revision summary

### SDK V3.4

- Added `addTcpPose`, `setTcpPoseByTcpName`, `deleteTcpPoseByTcpName`, and `switchTcpPoseByTcpName` to manage tool coordinate systems by tool name.

### SDK V3.3

- Added `moveLToPose_ex`.
- Added `powerOn`, `powerOnConfirmation`, and `powerOff`.

## Platform status

| Platform | Status | Entry point |
|---|---|---|
| Linux x64 | Preparation, project integration, and example guidance available | [Development Preparation](development.md) |

## Multi-robot integration

One application can connect multiple robots. Give every robot its own IP address, connection lifecycle, latest state, error context, and application state machine. When an interface accepts a target IP, specify it explicitly rather than relying on an implicit “current robot”.

The ability to connect multiple robots does not make parallel motion in a shared space safe. Implement workspace isolation, interlocks, and a coordinated emergency-stop strategy at the application and site level.

## Chapter contents

- **Development Preparation:** system, compiler, CMake, and network prerequisites.
- **Quick Start:** SDK placement, CMake linking, library search path, and a minimal initialization program.
- **Example Repository:** purpose of the runnable examples, safety boundaries, and the per-example pages.
- **Realtime Control:** calling constraints for `servoJ`, `servoL`, `speedJ`, and `speedL`.

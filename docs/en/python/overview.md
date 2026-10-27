# Python SDK Overview

`diana_sdk_python` exposes the official `DianaApi.py` wrapper around the native Diana API runtime library. It provides connection management, state feedback, motion control, I/O, kinematics, TCP/payload, path, and realtime-control interfaces. The final reference for parameters and behavior is the matching Python API manual, `DianaApi.py`, and native SDK release.

## Release Baseline

Python Examples 1.0.0 bundles Python SDK **3.3.0** as a submodule, laid out as below. To use SDK 3.4.0, set the `DIANA_SDK_DIR` environment variable to that SDK directory (see the README of the Example repository):

```text
diana_examples_python/
└── third_party/diana_sdk_python/
    ├── lib/
    │   └── DianaApi.py
    ├── doc/
    │   └── Python API manual V3.3.0
    └── version
```

For troubleshooting and release records, keep these versions together:

::::{div} release-baseline-chain
:::{div} release-baseline-step
<span class="release-baseline-index">01</span>
<div><strong>Controller software version</strong><small>Software actually running on the robot controller</small></div>
:::
:::{div} release-baseline-step
<span class="release-baseline-index">02</span>
<div><strong>Python SDK <code>version</code> file, <code>DianaApi.py</code>, and native runtime</strong><small>The wrapper and runtime library must come from the same SDK package</small></div>
:::
:::{div} release-baseline-step
<span class="release-baseline-index">03</span>
<div><strong>Example version and the SDK version it pins</strong><small>Reproducible source and dependency baseline</small></div>
:::
:::{div} release-baseline-step
<span class="release-baseline-index">04</span>
<div><strong>This documentation release tag</strong><small>Documentation version paired with the components above</small></div>
:::
::::

Always use the SDK, API manual, and release notes that match the customer site.

Function parameters, limits, and availability may change between SDK releases. Always use the current `lib/DianaApi.py`, native runtime library, `version` file, and release notes as the integration baseline.

The SDK `version` file records the package version, and `getLibraryVersion()` can read the runtime library version. Save both when releasing or troubleshooting applications.

## Interface Revision Summary

### SDK V3.4

- `DianaApi.py` adds `addTcpPose`, `setTcpPoseByTcpName`, `deleteTcpPoseByTcpName`, and `switchTcpPoseByTcpName` to manage tool coordinate systems by tool name.
- The manual now describes the return values of `powerOn`, `powerOnConfirmation`, and `powerOff` as `True` (success) and `False` (failure).

### SDK V3.3

- The Python SDK submodule used by the examples contains version 3.3.0.
- `DianaApi.py` exposes `moveLToPose_ex`.
- `DianaApi.py` exposes `powerOn`, `powerOnConfirmation`, and `powerOff`.

## Interface Shape

Python examples call the official wrapper with `import DianaApi`. The wrapper loads the native runtime library from the same `lib/` directory:

```text
libDianaApi.so    # Linux
DianaApi.dll      # Windows
```

The SDK submodule currently includes Linux x86_64 native libraries. For another operating system or CPU architecture, replace them with a matching vendor SDK package. Do not mix wrapper and native libraries from different releases or platforms.

## Platform Status

| Platform | Status | Entry |
|---|---|---|
| Linux x64 | Example scripts and SDK submodule are available; all examples have been verified on real robots, and each example page includes the actual run output | [Development Setup](development.md) |

## Multiple Robot Arms

Most Python SDK calls accept an `ipAddress` argument. In multi-arm applications, each robot should have its own IP, connection lifecycle, state cache, error context, and application state machine. Always pass the target IP explicitly for APIs that support it; do not rely on an empty IP or an implicit “current robot” global state.

SDK support for connecting multiple robots does not mean the site is safe for parallel robot motion. Workspace separation, interlocks, and emergency-stop strategy must be handled at the application and site-safety level.

## Contents

- **Development Setup**: System, Python, SDK paths, native libraries, and network prerequisites.
- **Quick Start**: SDK placement, environment variables, a minimal initialization program, and the connection lifecycle.
- **Examples**: Runnable scripts, safety boundaries, and per-example notes.
- **Execution Results**: Each example page includes the actual output captured on a real robot.

# Manual Overview

This documentation is for developers integrating, debugging, or maintaining Diana and Thor robot-arm applications. It covers control-PC preparation, shared control concepts, C++ and Python SDK integration, FCI development, ROS 2 integration, and common reference material. It helps developers use released interfaces; it does not replace the robot user manual, safety documentation, or SDK release notes.

## Documentation baseline

| Item | Value |
|---|---|
| C++ SDK | Industrial API Manual for C/C++ V3.3.0, original function entries 1-230 |
| Python SDK | Diana Industrial API Manual for Python V3.3.0 (2026-02-05) and the Python SDK 3.3.0 wrapper |
| FCI | Diana FCI example source and the `libfranka 0.18.2` API Reference |
| ROS 2 | `diana_ros2` Humble source (metapackage 2.5.0), Jazzy source (metapackage 3.5.3), and `libfranka 0.18.2` |
| Examples | C++ Examples 1.0.0 and Python Examples 1.0.0, compatible with SDK 3.3.0 |
| Manual version | 1.0.0 (released) |
| Formal release | Immutable Git tag |

## Content Sources

### C++ SDK Primary Source

Industrial API Manual for C/C++:

- Software version: V3.3.0
- Document version: V3.3.0
- File date: 2026-02-05
- Original function entries: 1-230
- Appendix A: DianaApi error codes
- Appendix B: ensuring inverse-kinematics solution uniqueness
- Appendix C: additional notes for realtime commands

### Python SDK Primary Sources

- Diana Industrial API Manual for Python V3.3.0, dated 2026-02-05
- `lib/DianaApi.py` and the `version` file from the Python SDK submodule
- The `diana_examples_python` source and its accompanying documentation

Python prototypes follow the current SDK wrapper. Parameter semantics and ranges are checked against the matching Python API manual. Example flow and values follow the current example source.

### FCI Primary Sources

- Diana FCI example source
- Official `libfranka 0.18.2` API Reference, type definitions, and control-interface documentation

FCI prototypes, overloads, return types, and exceptions are checked only against version 0.18.2. Documentation for another `libfranka` version must not be applied implicitly.

### ROS 2 Primary Sources

- `diana_ros2` Humble source: each package's `package.xml`, launch files, configuration files, controllers and message definitions, and the README of the `diana_description` package
- `libfranka 0.18.2`, which `diana_hardware` depends on

The ROS 2 chapter checks launch arguments, interface names, services, and actions against the Humble source and the current Jazzy source respectively.

### Web-Oriented Reorganization

Function-level API Reference is maintained on a separate site. This repository retains the structured data required to generate the error-code table and reorganizes material around development preparation, quick starts, runnable examples, API call flows, and shared references.

## Content boundaries

- **Overview:** scope, documentation entry points, network setup, core concepts, and version updates.
- **Programming Guide:** environment preparation, SDK or package integration, connection initialization, and examples by language and platform (C++, Python, FCI, ROS 2).
- **Reference:** common units, robot specifications, safety, error codes, troubleshooting, and I/O material.
- **API Reference:** function signatures and per-function parameter semantics are maintained on a separate site and are not linked from this manual.

## Scope and sources

The content is based on the matching sources above and applies to controller-software integration for Diana and Thor robots. Robot model, axis count, payload, reach, and optional hardware are defined by the equipment nameplate, controller version, and applicable product documents.

| Question | Preferred source |
|---|---|
| Installation, wiring, safety, and operation | User and safety manuals for the relevant model |
| Control-PC/controller communication | [Shared Network Setup](../programming/network.md) |
| SDK version, headers, wrapper, libraries, and project linking | The relevant C++, Python, FCI, or ROS 2 overview, development preparation, and quick start |
| Function semantics, parameters, returns, and error codes | Programming guide, reference material, and the separate API index site |
| Runnable projects | The relevant C++, Python, or FCI example overview; the ROS 2 quick start and example controllers |

```{important}
Before connecting to a physical robot, enabling it, or issuing motion commands, complete risk assessment, personnel separation, emergency-stop checks, and payload/tool confirmation. This manual does not replace the robot user manual or safety procedures.
```

## Suggested reading path

Start with [Core Concepts](concepts.md), then complete the shared [Network Setup](../programming/network.md) and SDK integration in the programming guide. For units, joint count, and pose representation use [Units and Conventions](../reference/units.md); for operating safety read the robot user manual and [Safety Boundaries](../reference/safety.md).

## License and Third-Party Notices

This repository is licensed under the Apache License 2.0; see `LICENSE` and `NOTICE` in the repository root.

The FCI and ROS 2 chapters of this manual quote and adapt material from the following third-party projects, all licensed under the Apache License 2.0:

| Project | Copyright notice | Use in this manual |
|---|---|---|
| [libfranka](https://github.com/frankaemika/libfranka) | Copyright (c) 2023 Franka Robotics GmbH | Descriptions and code excerpts of the FCI examples in the FCI chapter, adapted from the libfranka examples and modified for Diana robots |
| [franka_ros2](https://github.com/frankarobotics/franka_ros2) | Copyright (c) 2023 Franka Robotics GmbH | Package descriptions and code excerpts in the ROS 2 chapter; the source of `diana_ros2` follows the structure of franka_ros2 and carries the Franka Robotics copyright notice |

Copyright notice for the adapted parts: Copyright (c) 2026 Agile Robots SE (modifications: adapted for Diana robots). The complete licenses and notices of the upstream projects are those of their own repositories.
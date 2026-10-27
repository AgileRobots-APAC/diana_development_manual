# Versions and Updates

## Release baseline

Lock the following items together for every release so that documentation, SDK, FCI examples, and ROS 2 packages describe the same behavior:

```{figure} ../../_static/images/release-baseline-en.png
:alt: Release baseline: the diana-docs tag and controller software version; for the C++ / Python SDK the Example version, SDK version, and version file; for FCI the Diana FCI example source and libfranka 0.18.2; for ROS 2 Humble the diana_ros2 source version and dependency.repos
:width: 100%
:align: center
```

## Version compatibility

The manual, the examples, and the SDK each use an independent version number. The table records the combinations that have been checked:

| Manual | C++ Examples | Python Examples | SDK | FCI / ROS 2 baseline |
|---|---|---|---|---|
| 1.0.1 | 1.0.0 | 1.0.0 | 3.4.0 | `diana_libfranka_overlay` 1.0.0 (`libfranka 0.18.2`); `diana_ros2` Humble |
| 1.0.0 | 1.0.0 | 1.0.0 | 3.3.0 | `diana_libfranka_overlay` 1.0.0 (`libfranka 0.18.2`); `diana_ros2` Humble |

Each release of the software version (SDK 3.3.0, 3.4.0, and so on) includes, besides the SDK, the matching libfranka patches. `diana_libfranka_overlay` 1.0.0 is the `libfranka 0.18.2` patch set for software version 3.3.0, provided per robot-model branch with the tags `v1.0.0-libfranka0.18.2-diana3`, `v1.0.0-libfranka0.18.2-diana7`, and `v1.0.0-libfranka0.18.2-diana7g2`.

Manual 1.0.0 is based on the API manual of SDK 3.3.0 and manual 1.0.1 on that of SDK 3.4.0; 1.0.0 is kept as a Git tag and 1.0.1 is the current development version; both can be switched in the version selector. Examples 1.0.0 bundles SDK 3.3.0 as a submodule. When SDK 3.4.0 was checked, the interfaces used by the examples had not changed (3.4.0 only adds four tool-coordinate-system functions, and the other changes in the Python wrapper do not affect the examples), so 1.0.0 can also be used with SDK 3.4.0 by pointing `DIANA_SDK_DIR` at that SDK.

When a new SDK version is released and the examples need no change, only add that SDK version to this table and publish a manual patch release. The example version number does not need to change.

## Update history

### 1.0.1

- Updated to the API manual of SDK 3.4.0; the changes from 3.3.0 are listed in the interface revision summary of each SDK overview.
- Added the description of the four tool-coordinate-system functions. Examples 1.0.0 has been checked to work with SDK 3.4.0.

### 1.0.0

- The manual uses a version number independent of the SDK; the content is based on the API manual of SDK 3.3.0.
- Chinese, English, C++, Python, FCI, and ROS 2 documentation entries are unified.

### Before 1.0.0

- Earlier content had no unified developer manual. Refer to the matching PDF documentation and release notes; they are not repeated here.

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
| 1.0.0 | 1.0.0 | 1.0.0 | 3.3.0 | `diana_libfranka_overlay` 1.0.0 (`libfranka 0.18.2`); `diana_ros2` Humble |

Each release of the software version (SDK 3.3.0, 3.4.0, and so on) includes, besides the SDK, the matching libfranka patches. `diana_libfranka_overlay` 1.0.0 is the `libfranka 0.18.2` patch set for software version 3.3.0, provided per robot-model branch with the tags `v1.0.0-libfranka0.18.2-diana3`, `v1.0.0-libfranka0.18.2-diana7`, and `v1.0.0-libfranka0.18.2-diana7g2`.

When a new SDK version is released and the examples need no change, only add that SDK version to this table and publish a manual patch release. The example version number does not need to change.

## Update history

### 1.0.0

- The manual uses a version number independent of the SDK; the current content is based on the API manual of SDK 3.3.0.
- Chinese, English, C++, Python, FCI, and ROS 2 documentation entries are unified.

### Before 1.0.0

- Earlier content had no unified developer manual. Refer to the matching PDF documentation and release notes; they are not repeated here.

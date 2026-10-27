# 版本与更新

## 发布基线

每次发布应锁定以下内容，确保文档、SDK、FCI 示例与 ROS 2 软件包解释的是同一份接口行为：

```{figure} ../../_static/images/release-baseline-zh.png
:alt: 发布基线：diana-docs tag、控制器软件版本；C++ / Python SDK 的 Example 版本、SDK 版本与 version 文件；FCI 的 Diana FCI Example 源码与 libfranka 0.18.2；ROS 2 Humble 的 diana_ros2 源码版本与 dependency.repos
:width: 100%
:align: center
```

## 版本对应关系

本手册、Example 与 SDK 各自使用独立的版本号，下表记录经过核对的组合：

| 手册 | C++ Example | Python Example | SDK | FCI / ROS 2 基线 |
|---|---|---|---|---|
| 1.0.0 | 1.0.0 | 1.0.0 | 3.3.0 | `diana_libfranka_overlay` 1.0.0（`libfranka 0.18.2`）；`diana_ros2` Humble |

软件版本（SDK 3.3.0、3.4.0 等）的每次发布，除 SDK 外还包含与之配套的 libfranka 补丁。`diana_libfranka_overlay` 1.0.0 是软件版本 3.3.0 对应的 `libfranka 0.18.2` 补丁，按机型分支提供，对应 tag 为 `v1.0.0-libfranka0.18.2-diana3`、`v1.0.0-libfranka0.18.2-diana7`、`v1.0.0-libfranka0.18.2-diana7g2`。

SDK 发布新版本而 Example 无需修改时，只在本表追加该 SDK 版本并发布手册修订版，不需要同步修改 Example 的版本号。

## 更新记录

### 1.0.0

- 手册使用独立于 SDK 的版本号；当前内容依据 SDK 3.3.0 的 API 手册。
- 统一中文、英文、C++、Python、FCI 与 ROS 2 文档入口。

### 1.0.0 之前

- 早期的文档没有统一的开发者手册，需要参考早期对应版本的 PDF 文档和发布说明，这里不再赘述。

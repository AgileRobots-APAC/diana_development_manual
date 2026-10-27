# Diana 开发者文档

<div class="diana-hero">
  <span class="diana-badge">Diana / Thor</span>
  <span class="diana-badge">SDK 开发文档</span>
  <span class="diana-badge">中文 / English</span>
  <h1>Diana 开发者文档</h1>
  <p>面向 Diana 与 Thor 机械臂 SDK 的多语言开发者文档门户。</p>
  <p class="diana-hero-note">中文与英文文档同时发布；可选平台指南按发布节奏启用。</p>
  <div class="hero-actions">
    <a class="hero-button primary" href="about/overview.html">阅读手册概述</a>
    <a class="hero-button" href="cpp/index.html">进入 C++ 指南</a>
    <a class="hero-button" href="python/index.html">进入 Python 指南</a>
    <a class="hero-button" href="fci/index.html">进入 FCI 指南</a>
    <a class="hero-button" href="ros2/index.html">进入 ROS 2 指南</a>
  </div>
</div>

::::{grid} 1 2 2 3
:gutter: 3

:::{grid-item-card} 接口概述
:link: about/overview
:link-type: doc
:class-card: home-navigation-card
<i class="fa fa-file-text-o home-card-icon" aria-hidden="true"></i>

了解手册适用范围、资料入口、网络准备、核心概念与版本更新。
:::

:::{grid-item-card} 编程指南
:link: programming/network
:link-type: doc
:class-card: home-navigation-card
<i class="fa fa-code home-card-icon" aria-hidden="true"></i>

从网络配置开始，按启用的 SDK 模块继续完成环境准备、SDK 接入、初始化和 Example。
:::

:::{grid-item-card} 参考
:link: reference/units
:link-type: doc
:class-card: home-navigation-card
<i class="fa fa-book home-card-icon" aria-hidden="true"></i>

单位、安全、错误码、I/O 与故障排查等共用参考资料。
:::
::::

```{toctree}
:hidden:
:caption: 接口概述

about/overview
about/concepts
about/versions
about/building_docs
```

```{toctree}
:hidden:
:caption: 编程指南

programming/network
cpp/index
python/index
fci/index
ros2/index
```

```{toctree}
:hidden:
:caption: 参考

reference/units
reference/safety
reference/io
reference/error_codes
reference/troubleshooting
```

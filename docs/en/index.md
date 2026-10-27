# Diana Developer Documentation

<div class="diana-hero">
  <span class="diana-badge">Diana / Thor</span>
  <span class="diana-badge">SDK Documentation</span>
  <span class="diana-badge">English / 中文</span>
  <h1>Diana Developer Documentation</h1>
  <p>A multilingual documentation portal for developers using the Diana and Thor robot-arm SDKs.</p>
  <p class="diana-hero-note">Chinese and English documentation are published together. Optional platform guides follow the release schedule.</p>
  <div class="hero-actions">
    <a class="hero-button primary" href="about/overview.html">Read the manual overview</a>
    <a class="hero-button" href="cpp/index.html">C++ Guide</a>
    <a class="hero-button" href="python/index.html">Python Guide</a>
    <a class="hero-button" href="fci/index.html">FCI Guide</a>
    <a class="hero-button" href="ros2/index.html">ROS 2 Guide</a>
  </div>
</div>

::::{grid} 1 2 2 3
:gutter: 3

:::{grid-item-card} Overview
:link: about/overview
:link-type: doc
:class-card: home-navigation-card
<i class="fa fa-file-text-o home-card-icon" aria-hidden="true"></i>

Learn about the documentation scope, resources, network preparation, core concepts, and release updates.
:::

:::{grid-item-card} Programming Guide
:link: programming/network
:link-type: doc
:class-card: home-navigation-card
<i class="fa fa-code home-card-icon" aria-hidden="true"></i>

Start with network setup, then prepare the environment, integrate the SDK, initialize it, and run examples for the enabled SDK modules.
:::

:::{grid-item-card} Reference
:link: reference/units
:link-type: doc
:class-card: home-navigation-card
<i class="fa fa-book home-card-icon" aria-hidden="true"></i>

Shared reference material for units, safety, error codes, I/O, and troubleshooting.
:::
::::

```{toctree}
:hidden:
:caption: Overview

about/overview
about/concepts
about/versions
about/building_docs
```

```{toctree}
:hidden:
:caption: Programming Guide

programming/network
cpp/index
python/index
fci/index
ros2/index
```

```{toctree}
:hidden:
:caption: Reference

reference/units
reference/safety
reference/io
reference/error_codes
reference/troubleshooting
```

# Select a Robot Model

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

This guide uses `diana_libfranka_overlay` as the sole source for FCI examples and robot-specific adaptations. The repository pins an upstream `libfranka 0.18.2` submodule. Selecting a robot is done by choosing an overlay branch and applying that branch's patch to the submodule; it is not a runtime option.

Select exactly one model that matches the physical robot. Do not mix patches in one `libfranka` work tree.

| Robot | Overlay branch | Patch | C++ example directory after applying the patch |
|---|---|---|---|
| [Diana3](machines/diana3.md) | `diana3` | `patches/diana3.patch` | `libfranka/examples/diana3/` |
| [Diana7](machines/diana7.md) | `diana7` | `patches/diana7.patch` | `libfranka/examples/diana7/` |
| [Diana7G2](machines/diana7g2.md) | `diana7g2` | `patches/diana7g2.patch` | `libfranka/examples/diana7G2/` |

The patches also create `libfranka/pylibfranka/examples/<model>/`, `libfranka/examples/<model>/`, and the matching `rate_limiting_<model>.h`. The C++ example pages in this chapter use `libfranka/examples/<model>/` as their source, and the Python example pages use `libfranka/pylibfranka/examples/<model>/`.

```{warning}
Apply a patch only to a clean `libfranka` submodule at the commit pinned by the overlay. To switch models after applying a patch, restore the submodule first; never apply a second model patch on top of the first.
```

```{toctree}
:hidden:

machines/diana3
machines/diana7
machines/diana7g2
```

# Diana7G2 FCI Environment

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

Select branch `diana7g2` and apply the Diana7G2 patch to the upstream submodule:

```bash
git clone --recurse-submodules https://github.com/AgileRobots-APAC/diana_libfranka_overlay.git
cd diana_libfranka_overlay
git switch diana7g2
git submodule update --init --recursive
git -C libfranka apply --check ../patches/diana7g2.patch
git -C libfranka apply ../patches/diana7g2.patch
```

Prepare the environment as described in [Development Preparation](../development.md), then build:

```bash
cmake -S libfranka -B build/libfranka -DBUILD_EXAMPLES=ON
cmake --build build/libfranka
```

For a host build, the C++ examples are written to `build/libfranka/examples/diana7G2/`. When building from `libfranka/` in a container with `cmake -S . -B build -DBUILD_EXAMPLES=ON`, they are in `build/examples/diana7G2/`.

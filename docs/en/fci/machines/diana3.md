# Diana3 FCI Environment

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

Select branch `diana3` and apply the Diana3 patch to the upstream submodule:

```bash
git clone --recurse-submodules https://github.com/AgileRobots-APAC/diana_libfranka_overlay.git
cd diana_libfranka_overlay
git switch diana3
git submodule update --init --recursive
git -C libfranka apply --check ../patches/diana3.patch
git -C libfranka apply ../patches/diana3.patch
```

Prepare the environment as described in [Development Preparation](../development.md), then build:

```bash
cmake -S libfranka -B build/libfranka -DBUILD_EXAMPLES=ON
cmake --build build/libfranka
```

For a host build, the C++ examples are written to `build/libfranka/examples/diana3/`. When building from `libfranka/` in a container with `cmake -S . -B build -DBUILD_EXAMPLES=ON`, they are in `build/examples/diana3/`.

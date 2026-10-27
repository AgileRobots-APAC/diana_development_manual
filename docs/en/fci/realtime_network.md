# Realtime Network and System Configuration

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

```{attention}
FCI stability depends on API use, the control PC, the network link, and application thread behavior. `franka::Robot` requires realtime priority by default; developers may explicitly use `franka::RealtimeConfig::kIgnore` to validate a workflow on an ordinary development system. This does not make the system realtime-ready and acceleration, jerk, or velocity discontinuity errors can still occur. Production realtime applications must configure system realtime behavior according to site requirements.
```

## Ubuntu PREEMPT_RT Kernels

Choose the tab for the control PC's Ubuntu release. The two procedures use different kernel baselines and RT patches; their commands must not be mixed.

```{important}
This is a system-level change for the control PC only; never run it on the robot controller. Keep the original standard Ubuntu kernel and ensure that you can open GRUB's **Advanced options for Ubuntu**. If the new kernel does not boot, return to the original kernel there. A machine with Secure Boot enabled may not boot an unsigned, self-built kernel; confirm its state first and follow your organization's security policy.
```

::::::{tab-set}
:class: realtime-kernel-tabs

:::::{tab-item} Ubuntu 20.04 · 5.9.1-rt20

On an Ubuntu 20.04 x86_64 control PC, build and verify the realtime kernel with `Linux 5.9.1` and `PREEMPT_RT 5.9.1-rt20`. This procedure requires the patch matching the `5.9.1` baseline.

::::{container} realtime-kernel-steps
:::{container} realtime-kernel-step
### Check the environment and prepare the build directory

Check the Ubuntu release, current kernel, x86_64 architecture, Secure Boot state, and free root-filesystem space. Source and build artifacts require substantial storage; reserve several tens of GB.

```bash
lsb_release -a
uname -r
uname -m
mokutil --sb-state
df -h /

sudo apt update
sudo apt install -y \
  build-essential bc curl debhelper dpkg-dev devscripts fakeroot \
  libssl-dev libelf-dev bison flex cpio kmod rsync \
  libncurses-dev gnupg2 xz-utils mokutil
mkdir -p ~/rt-kernel
cd ~/rt-kernel
```
:::
:::{container} realtime-kernel-step
### Download and verify the source and RT patch

Download `linux-5.9.1`, its matching `patch-5.9.1-rt20`, and their signatures. If the initial verification reports a missing public key, obtain the actual key ID from the terminal output and import it.

```bash
curl -LO https://www.kernel.org/pub/linux/kernel/v5.x/linux-5.9.1.tar.xz
curl -LO https://www.kernel.org/pub/linux/kernel/v5.x/linux-5.9.1.tar.sign
curl -LO https://www.kernel.org/pub/linux/kernel/projects/rt/5.9/older/patch-5.9.1-rt20.patch.xz
curl -LO https://www.kernel.org/pub/linux/kernel/projects/rt/5.9/older/patch-5.9.1-rt20.patch.sign
xz -d linux-5.9.1.tar.xz
xz -d patch-5.9.1-rt20.patch.xz
gpg2 --verify linux-5.9.1.tar.sign linux-5.9.1.tar
gpg2 --verify patch-5.9.1-rt20.patch.sign patch-5.9.1-rt20.patch
gpg2 --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys <KEY_ID>
gpg2 --verify linux-5.9.1.tar.sign linux-5.9.1.tar
gpg2 --verify patch-5.9.1-rt20.patch.sign patch-5.9.1-rt20.patch
```

Both checks after importing the key must report `Good signature`. An `unknown` trust-level notice does not itself mean verification failed, but key provenance must still meet your organization's supply-chain policy.
:::
:::{container} realtime-kernel-step
### Apply the patch and enable PREEMPT_RT

When the current kernel is `5.9.1`, use its configuration as the baseline. The 5.9 and 6.8 Kconfig options are not identical, so an individual absent disable option does not affect the procedure; the final criterion is `CONFIG_PREEMPT_RT=y`.

```bash
tar xf linux-5.9.1.tar
cd linux-5.9.1
patch -p1 < ../patch-5.9.1-rt20.patch
cp -v /boot/config-$(uname -r) .config
scripts/config --disable DEBUG_INFO
scripts/config --disable DEBUG_KERNEL
scripts/config --disable SYSTEM_TRUSTED_KEYS
scripts/config --disable SYSTEM_REVOCATION_KEYS
scripts/config --disable PREEMPT_NONE
scripts/config --disable PREEMPT_VOLUNTARY
scripts/config --disable PREEMPT
scripts/config --enable PREEMPT_RT
make olddefconfig
grep CONFIG_PREEMPT_RT .config
grep -E 'CONFIG_SYSTEM_(TRUSTED_KEYS|REVOCATION_KEYS)' .config
make -s kernelrelease
```

Expect `CONFIG_PREEMPT_RT=y` and `5.9.1-rt20`. If `patch` reports `FAILED`, `Reject`, or `Hunk ... FAILED`, stop and verify the source and patch versions.
:::
:::{container} realtime-kernel-step
### Build and install Debian packages

For a kernel.org tarball source tree, use `bindeb-pkg`, not `deb-pkg`, which requires Git metadata. Select parallel jobs for the available CPU and memory; this example uses six jobs on an eight-logical-CPU machine.

```bash
make -j6 bindeb-pkg
ls -lh ../*.deb
cd ~/rt-kernel
sudo apt install \
  ./linux-image-5.9.1-rt20_*.deb \
  ./linux-headers-5.9.1-rt20_*.deb
ls -lh /boot/vmlinuz-5.9.1-rt20 /boot/initrd.img-5.9.1-rt20
grep -n '5.9.1-rt20' /boot/grub/grub.cfg
```

Retain `linux-image-5.9.1-rt20_*.deb` and `linux-headers-5.9.1-rt20_*.deb` at minimum. `linux-libc-dev` is optional; the large debug package is normally unnecessary. Retain the original standard kernel during installation.
:::
:::{container} realtime-kernel-step
### Reboot, verify, archive, and retain a recovery path

If the GRUB menu is hidden by default, select the realtime kernel for the next boot only:

```bash
sudo grub-reboot 'Advanced options for Ubuntu>Ubuntu, with Linux 5.9.1-rt20'
sudo grub-editenv list
sudo reboot
```

All three checks below must pass after login:

```bash
uname -r
cat /sys/kernel/realtime
grep CONFIG_PREEMPT_RT /boot/config-$(uname -r)
```

The required results are `5.9.1-rt20`, `1`, and `CONFIG_PREEMPT_RT=y`. Archive the image and headers packages after verification; delete `~/rt-kernel` only when the system is stable and packages are backed up. If the new kernel fails, boot the original standard kernel from GRUB's **Advanced options for Ubuntu**, then inspect build output, configuration, and driver compatibility.
:::
::::
:::::

:::::{tab-item} Ubuntu 22.04 · 6.8.0-rt8

On an Ubuntu 22.04 x86_64 control PC, build and verify the realtime kernel with `Linux 6.8.0` and `PREEMPT_RT 6.8-rt8`.

::::{container} realtime-kernel-steps
:::{container} realtime-kernel-step
### Check the environment and prepare the build directory

Check the OS release, current kernel, Secure Boot state, and free root-filesystem space. Kernel source, intermediate build output, and debug packages require substantial storage; reserve several tens of GB. `PREEMPT_DYNAMIC` is not `PREEMPT_RT`.

```bash
lsb_release -a
uname -r
uname -a
mokutil --sb-state
df -h /

sudo apt update
sudo apt install -y \
  build-essential bc curl debhelper dpkg-dev devscripts fakeroot \
  libssl-dev libelf-dev bison flex cpio kmod rsync \
  libncurses-dev gnupg2 xz-utils mokutil

mkdir -p ~/rt-kernel
cd ~/rt-kernel
```
:::
:::{container} realtime-kernel-step
### Download and verify the source and RT patch

The versions must match: `linux-6.8` with `patch-6.8-rt8`. Download the source, patch, and signature files:

```bash
curl -LO https://www.kernel.org/pub/linux/kernel/v6.x/linux-6.8.tar.xz
curl -LO https://www.kernel.org/pub/linux/kernel/v6.x/linux-6.8.tar.sign
curl -LO https://www.kernel.org/pub/linux/kernel/projects/rt/6.8/older/patch-6.8-rt8.patch.xz
curl -LO https://www.kernel.org/pub/linux/kernel/projects/rt/6.8/older/patch-6.8-rt8.patch.sign

gpg2 --keyserver hkp://keyserver.ubuntu.com:80 \
  --recv-keys 647F28654894E3BD457199BE38DBBDC86092693E
gpg2 --keyserver hkp://keyserver.ubuntu.com:80 \
  --recv-keys 57892E705233051337F6FDD105641F175712FA5B

xz -d linux-6.8.tar.xz
xz -d patch-6.8-rt8.patch.xz
gpg2 --verify linux-6.8.tar.sign linux-6.8.tar
gpg2 --verify patch-6.8-rt8.patch.sign patch-6.8-rt8.patch
```

Both verifications must report `Good signature`. An `unknown` trust-level notice does not itself mean verification failed, but the key fingerprints must meet your organization's supply-chain verification policy.
:::
:::{container} realtime-kernel-step
### Apply the patch and enable PREEMPT_RT

Use the running Ubuntu kernel configuration as the baseline, apply the patch, enable only `PREEMPT_RT`, then let `olddefconfig` provide defaults for new options.

```bash
tar xf linux-6.8.tar
cd linux-6.8
patch -p1 < ../patch-6.8-rt8.patch

cp -v /boot/config-$(uname -r) .config
scripts/config --disable DEBUG_INFO
scripts/config --disable DEBUG_INFO_DWARF_TOOLCHAIN_DEFAULT
scripts/config --disable DEBUG_KERNEL
scripts/config --disable SYSTEM_TRUSTED_KEYS
scripts/config --disable SYSTEM_REVOCATION_KEYS
scripts/config --disable PREEMPT_NONE
scripts/config --disable PREEMPT_VOLUNTARY
scripts/config --disable PREEMPT
scripts/config --disable PREEMPT_DYNAMIC
scripts/config --enable PREEMPT_RT
make olddefconfig

grep -E 'CONFIG_PREEMPT(_RT|_DYNAMIC|_NONE|_VOLUNTARY)?=' .config
grep -E 'CONFIG_SYSTEM_(TRUSTED_KEYS|REVOCATION_KEYS)' .config
make -s kernelrelease
```

Expect `CONFIG_PREEMPT_RT=y`, two `CONFIG_SYSTEM_*_KEYS=""` values, and `6.8.0-rt8`, respectively. If `patch` reports `FAILED`, `Reject`, or `Hunk ... FAILED`, stop and verify the source and patch versions.
:::
:::{container} realtime-kernel-step
### Build and install Debian packages

For a kernel.org tarball source tree, use `bindeb-pkg`, not `deb-pkg`; the latter also tries to create a source package that requires Git metadata. Select parallel jobs for the available CPU and memory; the example uses six jobs on an eight-logical-CPU machine.

```bash
make -j6 bindeb-pkg
ls -lh ../*.deb

cd ~/rt-kernel
sudo apt install \
  ./linux-image-6.8.0-rt8_6.8.0-2_amd64.deb \
  ./linux-headers-6.8.0-rt8_6.8.0-2_amd64.deb

ls -lh /boot/vmlinuz-6.8.0-rt8 /boot/initrd.img-6.8.0-rt8
grep -n '6.8.0-rt8' /boot/grub/grub.cfg
```

The build produces image and headers packages, plus optional `linux-libc-dev` and a very large debug package. Retain image and headers at minimum for deployment, and retain the original `generic` kernel during installation.
:::
:::{container} realtime-kernel-step
### Reboot, verify, archive, and retain a recovery path

If the GRUB menu is hidden by default, select the realtime kernel for the next boot only rather than changing the long-term default:

```bash
sudo grub-reboot 'Advanced options for Ubuntu>Ubuntu, with Linux 6.8.0-rt8'
sudo grub-editenv list
sudo reboot
```

After logging in, all three checks below must pass before the realtime kernel is considered active:

```bash
uname -r
cat /sys/kernel/realtime
grep CONFIG_PREEMPT_RT /boot/config-$(uname -r)
```

The required results are `6.8.0-rt8`, `1`, and `CONFIG_PREEMPT_RT=y`. After verification, archive `linux-image-6.8.0-rt8_6.8.0-2_amd64.deb` and `linux-headers-6.8.0-rt8_6.8.0-2_amd64.deb`; delete `~/rt-kernel` only after the system is stable and the packages are backed up.

If the realtime kernel does not boot or operates abnormally, boot the original `generic` kernel from GRUB's **Advanced options for Ubuntu**, then inspect build output, kernel configuration, and hardware-driver compatibility. Removing the work directory does not remove installed `/boot` files or `/lib/modules/6.8.0-rt8/`.
:::
::::
:::::
::::::

## Network Checks

Perform these checks in order. The commands assume a direct control-PC-to-controller link. If a switch is used, it must be a low-latency link dedicated to the robot; do not carry video, downloads, or high-volume logging on the same path.

Set the actual robot IP address and wired interface name in the current shell. `enp3s0` is only an example; obtain the real interface name in step 1:

```bash
export ROBOT_IP=192.168.10.75
export FCI_NIC=enp3s0
```

::::{container} network-checklist
:::{container} network-check-step
### Confirm the physical link and NIC name

```bash
ip -br link
```

**Pass condition:** The wired interface connected to the controller is `UP`, for example `enp3s0 UP ...`, and the link LEDs for the NIC and controller port are normal.

**If it fails:** Check the cable, the actual control-PC port, the controller port, and the NIC driver. Do not continue to FCI examples.

:::
:::{container} network-check-step
### Confirm the local IPv4 address and route to the controller

```bash
ip -4 addr show dev "$FCI_NIC"
ip route get "$ROBOT_IP"
```

**Pass condition:** The NIC has a unique IPv4 address in the same subnet as the controller. The route reports `$FCI_NIC` as `dev` and the NIC address as `src`. For example, when the robot is `192.168.10.75`, assign the control PC another unused address in that subnet.

**If it fails:** Configure a static IPv4 address and mask for the wired NIC in the operating-system network settings, then repeat this step. Never assign the controller IP to the control PC. If the route uses Wi-Fi, a VPN, or another NIC, disconnect it or correct the route.

:::
:::{container} network-check-step
### Check link errors, drops, and NIC power saving

```bash
ip -s link show dev "$FCI_NIC"
```

**Pass condition:** While observing the output, the `RX`/`TX` `errors`, `dropped`, and `overrun` counters do not increase. Use wired Ethernet and disable power saving, sleep, and automatic disconnect policies for this NIC in the operating-system network settings.

**If it fails:** Replace the cable or port and inspect switch negotiation and NIC drivers. Do not use a link with continuously increasing error counters for realtime control. Also rule out firewall or security-software interference with FCI traffic.

:::
:::{container} network-check-step
### Check basic IP reachability

```bash
ping -c 20 -i 0.2 "$ROBOT_IP"
```

**Pass condition:** The command completes without packet loss and round-trip times are stable without obvious long-tail spikes.

**If it fails:** Return to steps 1 and 2 to check physical connectivity, IP address, mask, route, and address conflicts. If site policy blocks ICMP, a failed `ping` alone does not prove that FCI is unavailable, but the read-only FCI checks below are still required.

:::
:::{container} network-check-step
### Establish one read-only FCI connection

```bash
./build/libfranka/examples/<model>/echo_robot_state "$ROBOT_IP"
```

**Pass condition:** The program creates `franka::Robot`, continuously reads and prints `RobotState`, then exits normally. This example sends no motion command.

**If it fails:** In addition to networking, verify that FCI is enabled on the controller, the controller software is compatible with `libfranka`, and firewall or security software is not blocking the connection. Success here proves only session establishment and one state read, not realtime readiness.

:::
:::{container} network-check-step
### Evaluate control communication only after site safety confirmation

`communication_test` first moves the robot and enters a zero-torque control session; it is not a read-only network test. Use it to evaluate control communication only after confirming personnel clearance, emergency stop, payload, collision thresholds, and an exit path.

:::
::::

```{warning}
Passing `ping` or state reading does not certify a realtime control system. Evaluate motion or torque-control examples only after the network checks and site safety confirmation both pass.
```

## Realtime Callback Principles

- Keep callback work deterministic.
- Do not print heavy logs or access disk inside callbacks.
- Avoid dynamic allocation, long mutex waits, and uncontrolled system calls.
- Limit velocity, torque, and command rate changes.

## Troubleshooting Directions

| Symptom | Possible Causes |
|---|---|
| Connection failure | IP address, cable, controller FCI state, or firewall |
| Control interruption | Cycle timeout, network jitter, target discontinuity, or a triggered limit |
| Unsmooth motion | Scheduling jitter, discontinuous targets, or insufficient limiting |
| Abnormal torque | Excessive gains, incorrect payload settings, or incorrect use of model terms |

```{note}
The values given in the examples are recommendations only; mandatory requirements follow the matching Diana FCI release notes, and final values should be tuned to the actual site conditions. This page documents engineering checks reflected by the current example source.
```

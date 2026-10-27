# 实时网络与系统配置

```{important}
使用任何 FCI 功能前，必须先在示教器上将机械臂切换到**协作模式**。机械臂处于其他模式时，无法通过 FCI 接口连接或控制。
```

```{attention}
FCI 的稳定性不仅取决于 API 调用，也取决于控制 PC、网络链路和应用线程。`franka::Robot` 默认要求实时优先级；开发者在普通开发环境中验证流程时，可显式使用 `franka::RealtimeConfig::kIgnore`。这不代表系统满足实时要求，仍可能出现加速度、加加速度或速度不连续等错误；正式实时应用应按现场要求配置系统实时性。
```

## Ubuntu PREEMPT_RT 实时内核

请根据控制 PC 的 Ubuntu 版本选择对应标签；两个流程使用不同的内核基线与 RT 补丁，命令不能混用。

```{important}
这是对控制 PC 的系统级修改，不要在机器人控制柜上执行。开始前请保留 Ubuntu 原有的普通内核，并确保可以进入 GRUB 的 **Advanced options for Ubuntu**；新内核无法启动时，应从这里切回原内核。启用 Secure Boot 的机器可能无法启动未签名的自编译内核，建议先确认其状态并按组织安全策略处理。
```

::::::{tab-set}
:class: realtime-kernel-tabs

:::::{tab-item} Ubuntu 20.04 · 5.9.1-rt20

在 Ubuntu 20.04 x86_64 控制 PC 上，使用 `Linux 5.9.1` 与 `PREEMPT_RT 5.9.1-rt20` 构建并验证实时内核。该版本必须使用与当前 `5.9.1` 基线匹配的补丁。

::::{container} realtime-kernel-steps
:::{container} realtime-kernel-step
### 检查环境并准备构建目录

确认 Ubuntu 版本、当前内核、x86_64 架构、Secure Boot 状态和根分区空间。源码和编译产物需要较多空间，建议预留数十 GB。

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
### 下载并验证源码和 RT 补丁

下载 `linux-5.9.1`、对应的 `patch-5.9.1-rt20` 及其签名文件。若首次验证提示没有公钥，请从终端输出中取得实际 Key ID，再导入该密钥。

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

导入公钥后的两次验证都必须包含 `Good signature`。`unknown` 信任级别提示不表示校验失败，但密钥来源仍应符合组织的供应链校验要求。
:::
:::{container} realtime-kernel-step
### 应用补丁并启用 PREEMPT_RT

当前系统内核为 `5.9.1` 时，可直接以它的配置作为基线。5.9 与 6.8 的 Kconfig 项不完全相同，个别不存在的关闭项不影响流程；最终以 `CONFIG_PREEMPT_RT=y` 为准。

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

期望看到 `CONFIG_PREEMPT_RT=y` 和 `5.9.1-rt20`。如 `patch` 出现 `FAILED`、`Reject` 或 `Hunk ... FAILED`，不要继续，应重新确认源码和补丁版本。
:::
:::{container} realtime-kernel-step
### 编译并安装 Debian 软件包

在 kernel.org 的压缩源码目录中使用 `bindeb-pkg`，不要使用需要 Git 元数据的 `deb-pkg`。并行数按实际 CPU、内存决定；下例为 8 个逻辑 CPU 使用 6 个任务。

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

至少保留 `linux-image-5.9.1-rt20_*.deb` 与 `linux-headers-5.9.1-rt20_*.deb`；`linux-libc-dev` 可选，体积很大的 debug 包通常无需分发。安装时保留原有普通内核。
:::
:::{container} realtime-kernel-step
### 重启验证、归档与回退

若 GRUB 菜单默认隐藏，先只指定下一次启动使用实时内核：

```bash
sudo grub-reboot 'Advanced options for Ubuntu>Ubuntu, with Linux 5.9.1-rt20'
sudo grub-editenv list
sudo reboot
```

登录后，以下三项都通过才表示实时内核真正生效：

```bash
uname -r
cat /sys/kernel/realtime
grep CONFIG_PREEMPT_RT /boot/config-$(uname -r)
```

期望输出依次为 `5.9.1-rt20`、`1`、`CONFIG_PREEMPT_RT=y`。验证后归档 image 与 headers 包；确认系统稳定且安装包已备份后，才可删除 `~/rt-kernel`。如新内核无法启动，在 GRUB 的 **Advanced options for Ubuntu** 选择原普通内核后，再检查构建日志、配置和硬件驱动兼容性。
:::
::::
:::::

:::::{tab-item} Ubuntu 22.04 · 6.8.0-rt8

在 Ubuntu 22.04 x86_64 控制 PC 上，使用 `Linux 6.8.0` 与 `PREEMPT_RT 6.8-rt8` 构建并验证实时内核。

::::{container} realtime-kernel-steps
:::{container} realtime-kernel-step
### 检查环境并准备构建目录

确认系统版本、当前内核、Secure Boot 状态和根分区空间。源码、编译中间文件和调试包会占用较多空间，建议预留数十 GB。`PREEMPT_DYNAMIC` 不等同于 `PREEMPT_RT`。

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
### 下载并验证源码和 RT 补丁

两个版本必须配套：`linux-6.8` 对应 `patch-6.8-rt8`。下载源码、补丁和签名文件：

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

两次验证结果都必须包含 `Good signature`。`unknown` 信任级别提示不表示校验失败，但公钥指纹应符合组织的供应链校验要求。
:::
:::{container} realtime-kernel-step
### 应用补丁并启用 PREEMPT_RT

以正在运行的 Ubuntu 内核配置作为基线，应用补丁后仅启用 `PREEMPT_RT`，再由 `olddefconfig` 补齐新版本选项。

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

期望依次看到 `CONFIG_PREEMPT_RT=y`、两个 `CONFIG_SYSTEM_*_KEYS=""`，以及 `6.8.0-rt8`。若 `patch` 出现 `FAILED`、`Reject` 或 `Hunk ... FAILED`，不要继续，应重新确认源码和补丁版本。
:::
:::{container} realtime-kernel-step
### 编译并安装 Debian 软件包

在 kernel.org 的压缩源码目录中使用 `bindeb-pkg`，不要使用 `deb-pkg`；后者还会尝试创建需要 Git 元数据的源码包。并行数按实际 CPU、内存决定；下例为 8 个逻辑 CPU 使用 6 个任务。

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

编译会生成 image、headers，以及可选的 `linux-libc-dev` 和体积很大的调试包。部署至少保留 image 和 headers；安装时保留原有 `generic` 内核。
:::
:::{container} realtime-kernel-step
### 重启验证、归档与回退

如果 GRUB 菜单默认隐藏，先仅指定下一次启动使用实时内核，避免直接改变长期默认启动项：

```bash
sudo grub-reboot 'Advanced options for Ubuntu>Ubuntu, with Linux 6.8.0-rt8'
sudo grub-editenv list
sudo reboot
```

重启并登录后，以下三项都通过才表示实时内核真正生效：

```bash
uname -r
cat /sys/kernel/realtime
grep CONFIG_PREEMPT_RT /boot/config-$(uname -r)
```

期望输出依次为 `6.8.0-rt8`、`1`、`CONFIG_PREEMPT_RT=y`。验证完成后，归档 `linux-image-6.8.0-rt8_6.8.0-2_amd64.deb` 与 `linux-headers-6.8.0-rt8_6.8.0-2_amd64.deb`；确认系统稳定且安装包已备份后，才可删除 `~/rt-kernel`。

如实时内核无法启动或运行异常，在 GRUB 的 **Advanced options for Ubuntu** 中选择原有 `generic` 内核启动，再检查构建日志、内核配置与硬件驱动兼容性。删除工作目录不会删除已安装的 `/boot` 文件或 `/lib/modules/6.8.0-rt8/`。
:::
::::
:::::
::::::

## 网络检查

以下检查按顺序执行。示例假定控制 PC 与控制柜直连；如使用交换机，应使用机器人专用、低延迟链路，且不要在同一链路上传输视频、下载或大规模日志。

先在当前终端设置实际的机器人 IP 和网卡名。`enp3s0` 仅为示例，请以步骤 1 的输出为准：

```bash
export ROBOT_IP=192.168.10.75
export FCI_NIC=enp3s0
```

::::{container} network-checklist
:::{container} network-check-step
### 确认物理链路与网卡名称

```bash
ip -br link
```

**通过条件：** 连接控制柜的有线网卡显示为 `UP`，例如 `enp3s0 UP ...`，且网卡与控制柜端口的链路指示灯正常。

**未通过时：** 先检查网线、控制 PC 实际使用的网口、控制柜端口和网卡驱动。不要继续执行后续 FCI 示例。

:::
:::{container} network-check-step
### 确认本机 IPv4 地址与到控制柜的路由

```bash
ip -4 addr show dev "$FCI_NIC"
ip route get "$ROBOT_IP"
```

**通过条件：** 网卡具有与控制柜同一网段、但不重复的 IPv4 地址；路由输出中的 `dev` 是 `$FCI_NIC`，`src` 是该网卡的地址。例如机器人为 `192.168.10.75` 时，控制 PC 可使用同网段内未被占用的其他地址。

**未通过时：** 在操作系统的网络设置中为该有线网卡配置静态 IPv4 地址和掩码，再重新执行本步骤。不要把控制柜 IP 配给控制 PC；若路由走向 Wi-Fi、VPN 或其他网卡，先断开或调整路由。

:::
:::{container} network-check-step
### 检查链路错误、丢包和网卡节能

```bash
ip -s link show dev "$FCI_NIC"
```

**通过条件：** 连续观察时 `RX`/`TX` 的 `errors`、`dropped` 和 `overrun` 不应增长。控制 PC 应使用有线网卡，并在系统网络设置中关闭该网卡的节能、自动休眠和自动断开策略。

**未通过时：** 更换网线或端口，检查交换机协商和网卡驱动；若错误计数持续增长，不要把该链路用于实时控制。防火墙或安全软件也应排除对 FCI 通信的拦截。

:::
:::{container} network-check-step
### 检查基础 IP 连通性

```bash
ping -c 20 -i 0.2 "$ROBOT_IP"
```

**通过条件：** 命令结束且无丢包；往返时间应稳定，没有明显的长尾尖峰。

**未通过时：** 回到步骤 1 和步骤 2 检查物理链路、IP、掩码、路由及地址冲突。ICMP 被现场策略禁止时，`ping` 失败不能单独证明 FCI 不可用，但仍必须完成后续只读 FCI 检查。

:::
:::{container} network-check-step
### 建立一次只读 FCI 连接

```bash
./build/libfranka/examples/<model>/echo_robot_state "$ROBOT_IP"
```

**通过条件：** 程序成功创建 `franka::Robot`、连续读取并打印 `RobotState` 后正常退出；该示例不下发运动命令。

**未通过时：** 除网络外，检查控制柜是否已启用 FCI、控制器软件与 `libfranka` 是否兼容，以及防火墙或安全软件是否拦截连接。此处成功只表示会话和一次读取可用，不代表链路已满足实时控制要求。

:::
:::{container} network-check-step
### 安全确认后再评估控制通信

`communication_test` 会先移动机器人并进入零力矩控制会话，不是只读网络测试。只有完成现场人员净空、急停、负载、碰撞阈值和退出路径确认后，才可使用它评估控制通信质量。

:::
::::

```{warning}
通过 `ping` 或状态读取不等于完成实时控制认证。只有网络检查和现场安全确认均通过后，才可评估运动或力矩示例。
```

## 实时线程原则

- 控制回调中只做确定性计算。
- 不在回调中打印大量日志或访问磁盘。
- 避免动态分配、长时间互斥锁和不可控系统调用。
- 对速度、力矩和目标变化率做限制。

## 故障方向

| 现象 | 可能原因 |
|---|---|
| 连接失败 | IP、网线、控制柜 FCI 状态、防火墙 |
| 控制中断 | 周期超时、网络抖动、目标跳变、限位触发 |
| 运动不平顺 | 系统调度抖动、目标不连续、限幅不足 |
| 力矩异常 | 增益过高、负载设置错误、模型项使用不当 |

```{note}
例程中给出的数值仅为推荐值；强制要求以对应的 Diana FCI 发布说明为准，最终取值应根据现场实际情况调整。本文只按当前示例源码给出工程侧检查思路。
```

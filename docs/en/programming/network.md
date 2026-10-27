# Network Setup

Network connectivity is a prerequisite for every SDK, FCI, and ROS 2 integration. Before writing software, complete the robot, controller, and teach-pendant connections described in the robot user manual and confirm that the robot is powered on.

```{figure} ../../_static/images/network-setup-en.png
:alt: Network connection between the control PC and robot controller
:width: 100%
```

```{attention}
Connect the control PC to port A on the robot controller over wired Ethernet.
```

## Connect the control PC to the controller

1. Connect the wired Ethernet port of the control PC to **port A** on the robot controller.
2. By default, the controller address on port A is `192.168.10.75`. After connecting the network port, check the actual address on the teach pendant's network information page.
3. Configure a static address for the control PC in the same subnet, for example:

   ```text
   Controller port A: 192.168.10.75
   Control PC:        192.168.10.100
   Subnet mask:       255.255.255.0
   ```

4. Verify the link before you start:

   ```bash
   ping 192.168.10.75
   ```

Prefer the supplied cable when one is provided. Otherwise use a Category 6 or higher Ethernet cable. Continue to the development preparation and connection initialization of the access method you use (SDK, FCI, or ROS 2) only after the network is reachable.

## Port roles and connection boundaries

| Port / interface | Purpose |
|---|---|
| Ethernet port A | SDK API communication with the control PC or a software teach pendant |
| Ethernet port D | TCP/IP or industrial communication such as Modbus-TCP; it does not replace the API port |
| Ethernet ports B and C | Reserved; do not use them as API ports |
| RS232/485 | May be used for other equipment communication; SDK API control still requires Ethernet |

## Network Requirements for FCI and ROS 2

The FCI examples and the ROS 2 launch argument `robot_ip` use the same controller address, `192.168.10.75` by default. Check the actual address on the teach pendant before connecting in the same way.

FCI and ROS 2 are real-time control and need a more stable link than ordinary SDK calls:

- Prefer a direct connection or a deterministic network between the control PC and the controller. A switch, an indirect path, or a cable or IP configuration problem is a common cause of FCI connection and real-time control failures.
- If a switch is unavoidable, use a low-latency link dedicated to the robot, and do not carry video, downloads, or large logs on the same link.
- For the steps to check kernel real-time behavior, the network adapter, and the link, see "Realtime Network and System Configuration" in the FCI chapter.

If a connection fails, first verify that the cable is in port A. Then check that the wired PC adapter is on the same subnet, that the controller responds to `ping`, and that another application is not occupying or repeatedly reconnecting the robot.

```{note}
IP addresses and port capabilities can vary with controller configuration. The device label, teach-pendant network configuration, and applicable controller manual take precedence over the example address on this page.
```

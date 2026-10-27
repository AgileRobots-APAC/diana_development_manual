# Safety Boundaries

```{danger}
API documentation does not replace the robot safety manual, risk assessment, emergency-stop/protective-device configuration, or functional-safety instructions.
```

This page covers the software safety boundary that API documentation can address; on-site operation must still follow the applicable model's user manual and safety procedures.

## First integration and redeployment checks

Before the first program run, after changing a tool or payload, or after redeployment, confirm at least the following:

- The robot base, tool, and cables are secured, and the workspace is clear of people and obstacles.
- Emergency stop, enabling device, external protective stop, and site interlocks have been verified under the safety procedure.
- Tool payload, center of gravity, TCP, and coordinate frames match the installed tooling.
- The control-PC network connection is correct and the controller has no pending error.
- The first motion uses conservative speed, acceleration, and range, with an operator able to reach emergency stop immediately.

```{note}
This is a minimum software-integration check, not a complete risk assessment or acceptance checklist. Installation strength, stopping distance, protective devices, and environmental requirements are governed by the applicable model manual and site safety plan.
```

Safety-related software entry points that can be found directly in the V3.4.0 API manual include:

- Collision detection and thresholds
- Rescue mode
- Joint / Cartesian motion limits
- Power-on / power-off interfaces
- Emergency-stop, STO, protective-stop, and safe-workspace errors in the error codes

When a safety-related stop or error occurs, first save the error code, robot state, and most recent command, then review [Error Codes](error_codes.md) and [Troubleshooting](troubleshooting.md). Do not recover a site simply by repeatedly clearing errors or sending another motion command.

# Troubleshooting

## Preserve the evidence first

Each SDK reports errors differently: through an error callback, an explicit query, an exception, logs, a ROS topic / service return value, or an FCI status code. Before investigating, record:

- the error code and the time it occurred;
- the robot state, active control mode, and IP connectivity;
- the most recent command and its key parameters;
- the SDK `version` file, the Examples version, and the documentation version.

Then look the code up in the [full error-code table](error_codes.md). Do not repeatedly restart or clear errors after this information is lost.

## Common directions

### Network / link

Focus on errors in the `-1001` to `-1015` range, which cover sockets, heartbeat, state feedback, and unregistered IP addresses.

Start at the physical layer and confirm in order: the control PC is connected to controller port A, the network adapter is on the same subnet, `ping` succeeds, controller initialization has completed, and no other application is holding the connection. Do not treat port D or a serial link as the SDK API link.

### Robot state / safety

Focus on errors from `-2201` onward, which cover call conflicts, collision, emergency stop, STO, protective stop, and soft/hard limits.

### Trajectory and kinematics

Errors from `-2301` onward cover planning, singularity, velocity/acceleration/jerk, inverse kinematics, and trajectory interpolation.

### Real-time / FCI

Errors from `-6001` onward describe position deviation, discontinuous velocity / acceleration, power, force thresholds, and motion stability.

For real-time issues, also record the actual and worst-case call period, CPU load, network jitter, whether the target points are continuous, and the stop strategy used after an interruption. First validate stability with reduced speed, acceleration, and update rate, then increase gradually toward the process parameters.

```{important}
The V3.4.0 manual gives special clearing procedures for `-2001` and `-2205` that differ from ordinary errors. When either occurs, first read the manual notes in the full [Error Codes](error_codes.md) entry instead of only clearing the error repeatedly.
```

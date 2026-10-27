# I/O and Mapping

This page describes only the I/O and mapping concepts shared by all SDKs. Look up specific function names, parameter types, module names, or topic / service names on the corresponding SDK page or in the separate interface reference.

| Type | Purpose | Typical use |
|---|---|---|
| Digital input (DI) | Read discrete input state | Sensors, gripper feedback, interlocks |
| Digital output (DO) | Control discrete output | Grippers, valves, indicator lamps |
| Analog input (AI) | Read continuous input | Pressure, displacement, external sensors |
| Analog output (AO) | Send continuous output | Speed, pressure, proportional valves |
| Address mapping | Map controller variables, I/O, or external data | PLC and process-device exchange |
| Mapping lock | Prevent mapping changes | Runtime stability |

Confirm terminal definitions, electrical ratings, PNP/NPN wiring, external power, and site safety logic before using I/O.

## Verify wiring and ranges

For controller configurations that support it, the COM wiring determines whether digital I/O uses PNP or NPN behavior. Analog I/O may also require selecting a voltage or current range. Before software reads or writes an I/O point:

1. Confirm the terminal number, COM wiring, input/output direction, and external power in the controller manual.
2. Verify the level and range with a meter or safe offline signal source before connecting a fixture or process device.
3. Include I/O failures, fixture-not-ready conditions, and safety interlocks in the application state machine; do not rely on a single read.
4. For mappings that must not change during operation, use controller-supported locking or prohibit changes in the application layer.

```{note}
Controller terminal definitions, electrical parameters, and PNP/NPN wiring are hardware information outside the main scope of this V3.4.0 API manual. The published site should bring them in separately from the controller user manual rather than mixing API semantics and hardware wiring on one page.
```

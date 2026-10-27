# Units and conventions

| Quantity | Unit |
|---|---|
| Force | N |
| Torque | Nm |
| Current | A |
| Length | m |
| Linear velocity | m/s |
| Linear acceleration | m/s² |
| Angle | rad |
| Angular velocity | rad/s |
| Angular acceleration | rad/s² |
| Time | s |

Unless a function page explicitly states otherwise, rotation values are interpreted as axis-angle. Array order, pose representation, and frame meaning for each interface still follow that function's description.

## Joint count

The documentation uses `JOINT_NUM` consistently:

- Diana: `JOINT_NUM = 7`
- Thor: `JOINT_NUM = 6`

```{important}
Examples, array lengths, and kinematics descriptions should use `JOINT_NUM` instead of hard-coding seven joints for every robot model.
```

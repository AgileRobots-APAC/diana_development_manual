# 03 print_joint_poses

```{important}
Before using any FCI feature, switch the robot to **Collaborative mode** on the teach pendant. FCI cannot be used to connect to or control the robot in another mode.
```

Source: `libfranka/examples/<model>/print_joint_poses.cpp`.

Reads the state once and uses the model to compute the pose matrices from the base to Joint1 … the end effector.

`<model>` is the selected patched robot directory: `diana3`, `diana7`, or `diana7G2`.

```bash
./build/libfranka/examples/<model>/print_joint_poses <robot-ip>
```

| Used API | Purpose in this example |
|---|---|
| `Robot::readOnce()` | Reads the current robot state. |
| `Robot::loadModel()` | Loads the kinematics model matching the current robot. |
| `Model::pose()` | Computes the pose matrix of the given joint or end-effector frame relative to the base. |
## Example flow

Robot::readOnce() → Robot::loadModel() → enumerate Frame::kJoint1 to Frame::kEndEffector → Model::pose().

### Key source excerpt

```cpp
franka::RobotState state = robot.readOnce();
franka::Model model(robot.loadModel());
for (franka::Frame frame = franka::Frame::kJoint1;
     frame <= franka::Frame::kEndEffector; frame++) {
  std::cout << model.pose(frame, state) << std::endl;
}
```

(fci-en-cpp-03_print_joint_poses-api)=
## API usage and call examples

(fci-en-cpp-03_print_joint_poses-api-132)=
### `franka::RobotState`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `franka::RobotState` | `struct RobotState` | The state structure itself has no function return value; it is provided by `Robot::readOnce()`, `Robot::read()` or the control callback. |

`RobotState` is a snapshot of the robot state, containing joint positions, velocities, torques, pose matrices, collision/contact flags and other fields. This example uses it as the input for the model computation and does not modify the object.

```{rubric} Call example
```

```cpp
franka::RobotState state = robot.readOnce();
std::cout << state.q << std::endl;
```


````

(fci-en-cpp-03_print_joint_poses-api-129)=
### `Robot::readOnce()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Robot::readOnce` | `virtual RobotState readOnce()` | Returns one `franka::RobotState` snapshot; throws an exception if a control loop is running, the network is interrupted or the robot reports an error. |

`readOnce()` reads only the current state frame. It is suitable for obtaining a start point, a model-computation input or a one-off diagnosis in the examples. The header recommends `Robot::read()` for reading state continuously.

```{rubric} Call example
```

```cpp
franka::RobotState state = robot.readOnce();
```


````

(fci-en-cpp-03_print_joint_poses-api-130)=
### `Robot::loadModel()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Robot::loadModel` | `Model loadModel()` | Returns the `franka::Model` matching the current robot; throws `ModelException` if the model library fails to load and `NetworkException` if the network is interrupted. |

`loadModel()` loads the robot dynamics/kinematics model. The examples use the returned `Model` to compute forward kinematics, the Jacobian, Coriolis and gravity terms.

```{rubric} Call example
```

```cpp
franka::Model model = robot.loadModel();
```


````

(fci-en-cpp-03_print_joint_poses-api-131)=
### `Model::pose()`

````{container} api-example-block

| Function | Prototype | Return value |
| --- | --- | --- |
| `Model::pose` | `std::array<double, 16> pose(Frame frame, const RobotState& robot_state) const` | Returns the 4x4 homogeneous matrix of the given frame relative to the base, flattened in column-major order. |

| Parameter | Direction/type | Meaning |
| --- | --- | --- |
| `frame` | Input, `Frame` | Frame to compute, such as `Frame::kJoint1` or `Frame::kEndEffector`. |
| `robot_state` | Input, `const RobotState&` | State snapshot used for the model computation. |

`pose()` computes the forward-kinematics pose of the given `Frame` from the given state. This example iterates from `Frame::kJoint1` to `Frame::kEndEffector` and prints each joint frame.

```{rubric} Call example
```

```cpp
auto O_T_frame = model.pose(frame, state);
std::cout << O_T_frame << std::endl;
```


````


```{warning}
Risk: Read-only. This example reads the robot state and sends no motion or torque commands; confirm the workspace, emergency stop and collision thresholds before running it.
```

```{note}
The code excerpts on this page are adapted from the libfranka examples (Copyright (c) 2023 Franka Robotics GmbH, Apache License 2.0) and modified for Diana robots; the adapted parts are Copyright (c) 2026 Agile Robots SE. See "License and Third-Party Notices" in the [Manual Overview](/about/overview.md).
```

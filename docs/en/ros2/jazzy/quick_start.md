# Quick Start

```{important}
This page starts from an already built workspace. If ROS 2, libfranka, the source, or the build are not ready yet, complete the [Development Setup](development.md) first. Steps that involve a real robot are collected in the last section, "Connect to a Real Robot"; all other steps work without a robot.
```

The goal is, in order: confirm that the packages are visible, view the robot model in RViz or Gazebo, run the first example controller on mock hardware, and connect to a real robot only after all prerequisites are met.

## Confirm the Packages Are Visible

In a new terminal, source ROS 2 and the workspace, then check the Diana packages:

```bash
source /opt/ros/jazzy/setup.bash
source ~/diana_ros2_ws/install/setup.bash
ros2 pkg list | grep -E 'diana|franka'
```

The output should include `diana_bringup`, `diana_description`, `diana_gazebo_bringup`, `diana_gazebo_hardware`, `diana_moveit_config`, `diana_selfcollision`, `franka_example_controllers`, `franka_hardware`, `franka_msgs`, `franka_robot_state_broadcaster`, and `franka_semantic_components`. See [Packages](packages/index.md) for what each package does.

## Model Visualization and Gazebo Simulation

All commands in this section run in simulation and do not connect to a real arm. `robot_type` is required and must be `diana3`, `diana7`, or `diana7g2`, matching your model; the commands below use `diana3` as an example.

### Model Visualization

```bash
ros2 launch diana_description diana.visualize.launch.py robot_type:=diana3
```

This starts `robot_state_publisher`, `joint_state_publisher_gui`, and RViz, so you can drag the joint sliders in RViz to inspect the model. It loads no controller, and the arm does not move by itself. See [diana_description](packages/diana_description.md) for the arguments and the Diana Duo usage.

### Simulation with an Example Controller

```bash
ros2 launch diana_gazebo_bringup diana.example_controller.launch.py \
  robot_type:=diana3 \
  controller:=joint_impedance_example_controller
```

`controller` must be a controller name configured in `config/controllers.yaml`. The launch file also offers `gz_args` (Gazebo arguments), `rviz` (whether to start RViz), and `namespace`; see [diana_gazebo_bringup](packages/diana_gazebo_bringup.md). The dependencies needed for the simulation are already installed by the `rosdep install` step of the [Development Setup](development.md).

Press `Ctrl+C` to stop the simulation.

```{tip}
To check MoveIt planning without a robot, run `ros2 launch diana_moveit_config moveit.launch.py robot_type:=diana3 robot_ip:=192.168.10.75 use_fake_hardware:=true`; see [diana_moveit_config](packages/diana_moveit_config.md).
```

## Run the First Example Controller on Mock Hardware

`diana.example_controllers.launch.py` reads a YAML robot configuration file. Do not edit the file in the install directory; copy it first:

```bash
cp "$(ros2 pkg prefix diana_bringup)/share/diana_bringup/config/diana.config.yaml" ~/my_fake.config.yaml
```

Open `~/my_fake.config.yaml` in an editor and check the following fields of the robot entry (`ROBOT1` by default):

- `robot_type`: set it to your own model (`diana3`, `diana7`, or `diana7g2`; the default in the file is only an example);
- `use_fake_hardware`: keep `"true"` (booleans need quotes); no real robot is connected;
- `namespace`: keep `""` so that no namespace is used.

See [diana_bringup](packages/diana_bringup.md) for the field descriptions.

### Start the Gravity Compensation Example

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
  robot_config_file:=$HOME/my_fake.config.yaml \
  controller_names:=gravity_compensation_example_controller
```

In another terminal, check the controller state:

```bash
ros2 control list_controllers
```

`joint_state_broadcaster` and `gravity_compensation_example_controller` should both be `active`. When `use_rviz` is `"true"` in the configuration file, RViz opens as well and shows the robot model. See [franka_example_controllers](packages/franka_example_controllers.md) for the prerequisites and limits of each example controller.

### Stop

Press `Ctrl+C` in the terminal running `diana.example_controllers.launch.py`. When `ros2_control_node` exits, the whole launch shuts down with it.

## Connect to a Real Robot

```{warning}
This section connects to a real robot, and the example controllers make it move or output torque. All of the following must hold before you start:

- The teach pendant has switched the arm to **Collaborative mode**, and the operating conditions in the [FCI Overview](../../fci/overview.md) are met;
- The control PC can reach the controller; see [Network Setup](../../programming/network.md);
- The workspace of the arm is free of people, workpieces, fixtures, and cables, and the emergency stop is within reach;
- You have read [Safety Boundaries](../../reference/safety.md), and you confirm the connection with commands that do not move the robot first.
```

Running on a real robot needs real-time permissions; see "Configure Real-Time Permissions" in the [Development Setup](development.md).

### Confirm the Connection First

Start only the control stack and the broadcasters, without loading a motion controller. Replace `<robot-ip>` with the actual controller address (the default address is `192.168.10.75`), set `robot_type` to your model, and turn mock hardware off explicitly:

```bash
ros2 launch diana_bringup diana.launch.py robot_type:=diana3 robot_ip:=<robot-ip> use_fake_hardware:=false
```

In another terminal, check:

```bash
ros2 control list_controllers
ros2 topic list
```

Now `joint_state_broadcaster` and `franka_robot_state_broadcaster` should be `active`. After you have confirmed that the robot state can be read, press `Ctrl+C` to stop.

### Run the Gravity Compensation Example

The gravity compensation example writes zero torque to all 7 joints. The arm hovers on its internal gravity compensation, can be pushed by hand, and does not actively hold its position. Copy and edit a configuration file first:

```bash
cp "$(ros2 pkg prefix diana_bringup)/share/diana_bringup/config/diana.config.yaml" ~/my_robot.config.yaml
```

In `~/my_robot.config.yaml`, set `robot_type` to your model, `robot_ip` to `<robot-ip>`, and `use_fake_hardware` to `"false"`. Then start:

```bash
ros2 launch diana_bringup diana.example_controllers.launch.py \
  robot_config_file:=$HOME/my_robot.config.yaml \
  controller_names:=gravity_compensation_example_controller
```

Check the controller state:

```bash
ros2 control list_controllers
```

If you set a value for `namespace` in the configuration file, specify the matching controller manager with `-c`, for example `ros2 control list_controllers -c /<namespace>/controller_manager`.

```{important}
For the first run, support the arm and the end payload, and keep a hand within reach of the emergency stop. Before running any other example that produces motion, read the matching section of [franka_example_controllers](packages/franka_example_controllers.md).
```

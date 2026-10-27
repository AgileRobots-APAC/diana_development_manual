# Quick Start

```{important}
This page starts from an already built workspace. If you have not yet installed ROS 2, obtained the source, or built it, complete [Development Setup](development.md) first. Steps that involve a real arm are collected in the final "Connecting to a Real Robot" section; every other step works without a robot.
```

The goal is to confirm that the packages are visible, view the robot model in RViz or Gazebo, run a first example controller on simulated hardware, and only then connect a real arm once all prerequisites are met.

## Confirming Packages Are Visible

In a new terminal, source ROS 2 and the workspace, then check for the Diana packages:

```bash
source /opt/ros/humble/setup.bash
source ~/diana_ros2_ws/install/setup.bash
ros2 pkg list | grep diana
```

The output should include `diana_bringup`, `diana_example_controllers`, `diana_gazebo_bringup`, `diana_hardware`, `diana_moveit_config`, `diana_msgs`, `diana_robot_state_broadcaster`, and `diana_semantic_components`. See [Packages](packages/index.md) for what each one does.

```{note}
The robot model comes from the external package `diana_description`, which is imported through `dependency.repos` in the source. If a launch command below reports that this package cannot be found, return to [Development Setup](development.md) and import the dependencies again.
```

## Model Visualization and Gazebo Simulation

All commands in this section run in simulation and do not connect to a real arm. `robot_type` is required and must be `diana3`, `diana7`, or `diana7g2`, matching your model; the commands below use `diana3` as an example. Simulation needs the Gazebo dependencies installed first; see "Install Gazebo Simulation Dependencies (Optional)" in the [Development Setup](development.md).

### Model Visualization

```bash
ros2 launch diana_gazebo_bringup visualize_diana_robot.launch.py robot_type:=diana3
```

This starts Gazebo with an empty world, `robot_state_publisher`, and RViz, spawns the robot into the world, and activates `joint_state_broadcaster`. It loads no motion controller, so the arm does not move on its own.

### Simulation with an Example Controller

```bash
ros2 launch diana_gazebo_bringup gazebo_diana_arm_example_controller.launch.py \
  robot_type:=diana3 \
  controller:=joint_impedance_example_controller
```

`controller` must be a controller name registered in `config/<robot_type>_gazebo_controllers.yaml` of `diana_gazebo_bringup`. The launch file also provides the `gz_args` (Gazebo arguments), `rviz` (whether to start RViz), and `namespace` arguments; see [diana_gazebo_bringup](packages/diana_gazebo_bringup.md).

```{figure} ../../../_static/images/ros2-humble-gazebo-example-controller.png
:alt: Simulation of diana3 in Gazebo and RViz
:width: 100%

`diana3` in Gazebo (left) and RViz (right). The Gazebo entity tree shows `ground_plane`, `sun`, and `diana3`.
```

Press `Ctrl+C` to end the simulation.

```{tip}
To verify MoveIt planning without a robot, run `ros2 launch diana_moveit_config moveit.launch.py robot_type:=diana3 robot_ip:=192.168.10.75 use_fake_hardware:=true`. See [diana_moveit_config](packages/diana_moveit_config.md).
```

## Running a First Example Controller on Simulated Hardware

`example.launch.py` reads a YAML configuration file in which `use_fake_hardware` defaults to `"false"`. To run without a robot it must be set to `"true"`. Do not edit the file in the install directory; copy it first:

```bash
cp "$(ros2 pkg prefix diana_bringup)/share/diana_bringup/config/diana.config.yaml" ~/my_fake.config.yaml
```

Open `~/my_fake.config.yaml` in an editor and change the following fields of the robot entry (`ROBOT1` by default):

- `robot_type`: set it to your own model (`diana3`, `diana7`, or `diana7g2`; the `"diana3"` in the file is only an example value);
- `use_fake_hardware`: set it to `"true"` (boolean values must be quoted);
- `namespace`: set it to `""` (optional); once cleared, the later commands need no namespace.

The fields are described in [diana_bringup](packages/diana_bringup.md).

### Starting the Gravity Compensation Example

```bash
ros2 launch diana_bringup example.launch.py \
  robot_config_file:=$HOME/my_fake.config.yaml \
  controller_names:=gravity_compensation_example_controller
```

In another terminal, check the controller state:

```bash
ros2 control list_controllers
```

Both `joint_state_broadcaster` and `gravity_compensation_example_controller` should be `active`. When `use_rviz` in the configuration file is `"true"`, RViz also opens and shows the robot model.

### Running the Joint Impedance Example

On simulated hardware only the two joint-level examples can run: `gravity_compensation_example_controller` and `joint_impedance_example_controller`. `example.launch.py` loads only the controllers named by `controller_names`; a controller that is not named is not loaded, so you cannot switch to it while the launch is running. To run a different example, press `Ctrl+C` in the terminal that runs the launch, then start it again with the other controller name:

```bash
ros2 launch diana_bringup example.launch.py \
  robot_config_file:=$HOME/my_fake.config.yaml \
  controller_names:=joint_impedance_example_controller
```

```{note}
The elbow and Cartesian examples call services and use interfaces such as `robot_time` and `elbow_state`, which are provided only by the real `diana_hardware`; they cannot run on simulated hardware. The prerequisites of each example are listed in [diana_example_controllers](packages/diana_example_controllers.md).
```

### Stopping

Press `Ctrl+C` in the terminal that runs `example.launch.py`. When `ros2_control_node` exits, the whole launch shuts down with it.

## Connecting to a Real Robot

```{warning}
This section connects to a real arm, and the example controllers move the arm or output torque. All of the following must be satisfied before you start:

- The pendant has switched the arm to **cooperative mode**, and the operating conditions in the [FCI overview](../../fci/overview.md) are met.
- The control PC and the control cabinet are connected over the network; see [Network Setup](../../programming/network.md).
- The arm workspace is free of people, workpieces, fixtures, cables, and other obstacles, and the emergency stop is within reach.
- You have read [Safety Boundaries](../../reference/safety.md) and have confirmed the connection with non-moving commands first.
```

Running on a real arm requires real-time permissions; see "Configure Realtime Permissions" in [Development Setup](development.md).

### Confirming the Connection First

Start only the control stack and the broadcasters, without loading a motion controller. Replace `<robot-ip>` with the actual controller address (the default address is `192.168.10.75`) and set `robot_type` to your model:

```bash
ros2 launch diana_bringup diana.launch.py robot_type:=diana3 robot_ip:=<robot-ip>
```

In another terminal, check:

```bash
ros2 control list_controllers
ros2 topic list
```

`joint_state_broadcaster` and `diana_robot_state_broadcaster` should now be `active`. Once you can read the robot state, press `Ctrl+C` to end the launch.

### Running the Gravity Compensation Example

The gravity compensation example writes zero torque to the 7 joints. The arm floats on its internal gravity compensation, can be pushed by hand, and does not actively hold its position. First copy and edit a configuration file:

```bash
cp "$(ros2 pkg prefix diana_bringup)/share/diana_bringup/config/diana.config.yaml" ~/my_robot.config.yaml
```

In `~/my_robot.config.yaml`, change `robot_type` to your model, set `robot_ip` to `<robot-ip>`, and make sure `use_fake_hardware` is `"false"`. Then launch:

```bash
ros2 launch diana_bringup example.launch.py \
  robot_config_file:=$HOME/my_robot.config.yaml \
  controller_names:=gravity_compensation_example_controller
```

The default configuration uses the namespace `NS_1`, so specify the controller manager when checking controllers:

```bash
ros2 control list_controllers -c /NS_1/controller_manager
```

```{important}
For the first run, support the arm and its end-effector load, and keep a hand within reach of the emergency stop. Before running any other example that produces motion, read the matching section of [diana_example_controllers](packages/diana_example_controllers.md).
```

## Run Flow

```text
Start launch (robot_state_publisher, ros2_control_node, broadcasters)
    → spawner loads and activates the controller → controller runs at a 1 kHz period
    → Ctrl+C shuts down the launch (to change the example, start it again with another controller name)
```

`diana.launch.py` starts only the broadcasters; `example.launch.py` builds on it and uses a `spawner` to load the controller named by `controller_names`; controllers that are not named are not loaded. While a controller runs, `diana_hardware` works in a single control mode only. See [diana_bringup](packages/diana_bringup.md).

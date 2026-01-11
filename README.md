> Files developed while following through with the **"ROS 2 For Begginers Level 2: URDF | Gazebo | Rviz | TF"** Udemy course. This only accounts for the final versions for each file, meaning some preliminar steps (such as the initial URDF before Xacro implementation) might not be present.

---

# File Structure

<pre><code>
├── build/
|   └── ...
├── install/
|   └── ...
├── log/
|   └── ...
└── <b>src/</b>
    ├── <b>robot_bringup</b>
    │   ├── CMakeLists.txt
    │   ├── config
    │   │   ├── gazebo_bridge.yaml
    │   │   └── urdf_cam.rviz
    │   ├── launch
    │   │   ├── absolute_description.launch.py
    │   │   ├── absolute_display.launch.py
    │   │   ├── display.launch.xml
    │   │   └── gazebo_robot.launch.py
    │   ├── package.xml
    │   └── worlds
    │       └── test_world.sdf
    └── <b>self_test_robot_description</b>
        ├── CMakeLists.txt
        ├── package.xml
        └── urdf
            ├── camera.xacro
            ├── common_properties.xacro
            ├── mobile_base_gazebo.xacro
            ├── mobile_base.xacro
            ├── robot.urdf
            └── robot.urdf.xacro
</code></pre>


As seen, this workspace includes **two ROS 2 packages**:
- <mark>robot_bringup</mark> -> launch and configuration files
- <mark>self_test_robot_description</mark> -> description (urdf and xacro) files

Executables will only be run from the bringup package, but both of them are necessary for anything to work, as the launch files commonly reference description files from the description package.

---
# Dependencies


This workspace was built for the following environment:
- Ubuntu 22.04
- ROS 2 humble
- Gazebo Harmonic

Attempting to run it with different versions for any of those items will likely result in failure and is not advised.

### Install ROS 2 Humble:
To install ROS 2 Humble, follow the procedures show in [this webpage](https://docs.ros.org/en/humble/Installation.html).

### Install Gazebo Harmonic with ROS Humble:
Remove the wrong version (Ingition Fortress):
```bash
$ sudo apt remove ros-humble-ros-gz
```
Install Gazebo Harmonic and its bridge:
```bash
$ sudo apt install ros-humble-ros-gzharmonic
$ sudo apt install ros-humble-ros-gzharmonic-bridge
```

---

# Executing 

The main, final launch file for the project is `gazebo_robot.launch.py` from the `robot_bringup` package. It includes the full launch from Gazebo, with the camera sensor and a pre-made world, as well as Rviz and JSP arguments to help with debuging if wished.

To execute it, run the following command.
```bash
ros2 launch robot_bringup gazebo_robot.launch.py
```

It includes the following launch arguments:
- **rviz_debug**
  - Type: pseudo-boolean (string)
  - Options: [True/False]
  - Default: False
  - Description: Choose between initializing, in addition to Gazebo, RViz for visual debug (True) or not (False)

- **use_camera**
  - Type: pseudo-boolean (string)
  - Options: [True/False]
  - Default: True
  - Description: Choose between showcasing the camera view in RViz (True) or not (False)

- **real_jsp**
  - Type: boolean
  - Options: [true/false]
  - Default: true
  - Description: Choose between using Gazebo, real Joint State Publisher (with gz_ros_bridge) or a placeholder, fake JSP. 

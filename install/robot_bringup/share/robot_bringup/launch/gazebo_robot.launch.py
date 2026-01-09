from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, PythonExpression

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    ld = LaunchDescription()

    # ==== Constantes ==== #    
    urdf_launch_package = FindPackageShare('urdf_launch')   # URDF relative launch package
    gz_sim_launch_package = FindPackageShare('ros_gz_sim')  # Pkg to launch gazebo sim
    base_rviz_config_path = PathJoinSubstitution([FindPackageShare('urdf_launch'),'config','urdf.rviz'])
    camera_rviz_config_path = PathJoinSubstitution([FindPackageShare('robot_bringup'), 'config', 'urdf_cam.rviz'])
    gazebo_config_file_path = PathJoinSubstitution([FindPackageShare('robot_bringup'), 'config', 'gazebo_bridge.yaml'])
    gazebo_world_file_path = PathJoinSubstitution([FindPackageShare('robot_bringup'), 'worlds', 'test_world.sdf'])

    # ==== Parameters ==== #
    ld.add_action(DeclareLaunchArgument(name='urdf_package',
                                        default_value='self_test_robot_description',
                                        description='Name of the package where urdf robot description is stored'))

    ld.add_action(DeclareLaunchArgument(name='robot_description_name',
                                        default_value='robot.urdf.xacro',
                                        description='File name of the .urdf robot description'))


    urdf_package = LaunchConfiguration('urdf_package')
    robot_description_file = LaunchConfiguration('robot_description_name')

    # ==== Boolean Conditional parameters ==== #
    # Enable/Disable RViz visual debug tool
    ld.add_action(DeclareLaunchArgument(name='real_jsp',
                                        default_value='true',
                                        choices=['true', 'false'],
                                        description='Allow choice between real jsp (with ros_gz_bridge) or fake placeholder jsp'))

    ld.add_action(DeclareLaunchArgument(name='rviz_debug',
                                        default_value='True',
                                        description='(OPTIONS ARE "True" or "False" ONLY!!!) Flag to enable RViz visual debug tool'))

    ld.add_action(DeclareLaunchArgument(name='use_camera',
                                        default_value='True',
                                        description='(OPTIONS ARE "True" or "False" ONLY!!!) Flag to choose whether to enable camera plugin view in RViz or not.'))


    #
    # ==== Generate Nodes ==== #
    robot_spawner_node = Node(package='ros_gz_sim',
                              executable='create',
                              arguments=['-topic', '/robot_description']
                              )

    # Rviz launcher without camera view
    rviz_launcher_node = Node(package='rviz2',
                              executable='rviz2',
                              output='screen',
                              arguments=['-d', base_rviz_config_path],
                              condition=IfCondition(
                                  PythonExpression([LaunchConfiguration('rviz_debug'), ' and not ',
                                                    LaunchConfiguration('use_camera')])))

    # Rviz launcher with camera view
    rviz_launcher_node_cam = Node(package='rviz2',
                              executable='rviz2',
                              output='screen',
                              arguments=['-d', camera_rviz_config_path],
                              condition=IfCondition(
                                  PythonExpression([LaunchConfiguration('rviz_debug'), ' and ',
                                                    LaunchConfiguration('use_camera')])))

    # Fake JSP
    fake_jsp_node = Node(package='joint_state_publisher',
                         executable='joint_state_publisher',
                         condition=UnlessCondition(LaunchConfiguration('real_jsp')))

    # Ros<->GZ bridge
    ros_gz_bridge_node = Node(package='ros_gz_bridge',
                              executable='parameter_bridge',
                              condition=IfCondition(LaunchConfiguration('real_jsp')),
                              parameters= [
                                {'config_file' : gazebo_config_file_path}
                              ]
                              )

    #
    # ==== Call Launch Files ==== #

    # Calls gazebo launcher
    ld.add_action(IncludeLaunchDescription(
        PathJoinSubstitution([gz_sim_launch_package, 'launch', 'gz_sim.launch.py']),
        launch_arguments={
            'gz_args' : [gazebo_world_file_path, " --render-engine ogre -r"]
        }.items()
    ))

    # robot_state_publisher launcher 
    ld.add_action(IncludeLaunchDescription(
        PathJoinSubstitution([urdf_launch_package, 'launch', 'description.launch.py']),
        launch_arguments={
            'urdf_package' : urdf_package,
            'urdf_package_path' : PathJoinSubstitution(['urdf', robot_description_file])
            # 'urdf_file_path' : PathJoinSubstitution([urdf_package, 'urdf', robot_description_file])
        }.items()
    ))

    #
    # ==== Call Nodes ==== #

    # Robot_Spawner_Node -> Spawns robot into gazebo
    ld.add_action(robot_spawner_node)
    ld.add_action(fake_jsp_node)
    ld.add_action(ros_gz_bridge_node)
    ld.add_action(rviz_launcher_node)
    ld.add_action(rviz_launcher_node_cam)

    return ld
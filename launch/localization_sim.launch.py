import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PythonExpression, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
  package_name = "localization"
  # Set the path to different files and folders.
  robot_localization_file_path = PathJoinSubstitution([FindPackageShare(package_name), 'config/ekf.yaml']) 
  
  camera_to_pose = Node(
    package=package_name,
    executable="camera_to_pose"
  )

  # Start robot localization using an Extended Kalman filter
  start_robot_localization_cmd = Node(
    package='robot_localization',
    executable='ekf_node',
    name='ekf_filter_node',
    output='screen',
    parameters=[robot_localization_file_path])
  
  # Create the launch description and populate
  ld = LaunchDescription()

  # Add any actions
  ld.add_action(start_robot_localization_cmd)
  # ld.add_action(camera_to_pose)
  return ld

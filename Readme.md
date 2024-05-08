# Localization

This package implements a EKF fliter for eirabot. It has a launch file for gazebo sim and physical robot implementation. This package also contains a file for converting TagData to a pose with covariance for the demo area downstairs based on the vertex locations in sample.xml

## EKF 

### What it does

The EKF fliter performs sensor fusion between the odometry data of the controller (motor encoders) and the tag readings to get a more accurate estimation of the robots location. The EKF implments the transform from odom to base_link with odom frame being based at 0,0. The EKF fuses the odometry data from motor and the pose data got from tag reading.

>:shit: Found Out this is bad practice and two seperate EKF should be used with one for fusing continuous position data and another for fusing global absolute position data

## Running localization

To add the EKF fliter nodes to a launch file add the following node to the file in as a launch description action

```python
robot_localization_file_path = PathJoinSubstitution([FindPackageShare(package_name), 'config/ekf.yaml']) 

start_robot_localization_cmd = Node(
    package='robot_localization',
    executable='ekf_node',
    name='ekf_filter_node',
    output='screen',
    parameters=[robot_localization_file_path])


```

To launch the ekf fliter and tagData to pose in terminal use the following commands

### on physical robot

```bash
ros2 launch localization localization.launch.py 
```

### in sim

```bash
ros2 launch localization localization_sim.launch.py
```

## Diagram

```mermaid
flowchart LR

/camera_convertor[ /camera_convertor ]:::main
/ekf_filter_node[ /ekf_filter_node ]:::main
/ekf_filter_node[ /ekf_filter_node ]:::node
/sim([ /sim<br>canopen_pgv150i_driver/msg/TagData ]):::bugged
/Tag_pose([ /Tag_pose<br>geometry_msgs/msg/PoseWithCovarianceStamped ]):::topic
/diffbot_base_controller/odom([ /diffbot_base_controller/odom<br>nav_msgs/msg/Odometry ]):::bugged
/set_pose([ /set_pose<br>geometry_msgs/msg/PoseWithCovarianceStamped ]):::bugged
/diagnostics([ /diagnostics<br>diagnostic_msgs/msg/DiagnosticArray ]):::bugged
/odometry/filtered([ /odometry/filtered<br>nav_msgs/msg/Odometry ]):::bugged
/enable[/ /enable<br>std_srvs/srv/Empty \]:::bugged
/set_pose[/ /set_pose<br>robot_localization/srv/SetPose \]:::bugged
/toggle[/ /toggle<br>robot_localization/srv/ToggleFilterProcessing \]:::bugged

/sim --> /camera_convertor
/Tag_pose --> /ekf_filter_node
/diffbot_base_controller/odom --> /ekf_filter_node
/set_pose --> /ekf_filter_node
/Tag_pose --> /ekf_filter_node
/camera_convertor --> /Tag_pose
/ekf_filter_node --> /diagnostics
/ekf_filter_node --> /odometry/filtered
/enable o-.-o /ekf_filter_node
/set_pose o-.-o /ekf_filter_node
/toggle o-.-o /ekf_filter_node



subgraph keys[<b>Keys<b/>]
subgraph nodes[<b><b/>]
topicb((No connected)):::bugged
main_node[main]:::main
end
subgraph connection[<b><b/>]
node1[node1]:::node
node2[node2]:::node
node1 o-.-o|to server| service[/Service<br>service/Type\]:::service
service <-.->|to client| node2
node1 -->|publish| topic([Topic<br>topic/Type]):::topic
topic -->|subscribe| node2
node1 o==o|to server| action{{/Action<br>action/Type/}}:::action
action <==>|to client| node2
end
end
classDef node opacity:0.9,fill:#2A0,stroke:#391,stroke-width:4px,color:#fff
classDef action opacity:0.9,fill:#66A,stroke:#225,stroke-width:2px,color:#fff
classDef service opacity:0.9,fill:#3B8062,stroke:#3B6062,stroke-width:2px,color:#fff
classDef topic opacity:0.9,fill:#852,stroke:#CCC,stroke-width:2px,color:#fff
classDef main opacity:0.9,fill:#059,stroke:#09F,stroke-width:4px,color:#fff
classDef bugged opacity:0.9,fill:#933,stroke:#800,stroke-width:2px,color:#fff
style keys opacity:0.15,fill:#FFF
style nodes opacity:0.15,fill:#FFF
style connection opacity:0.15,fill:#FFF

```

## To Do

- Make a second EKF so one for continuous position data and another for using global absolute position data
- Allow the EKF to take in IMU data
- Adjust the covariance matrices
- Allow tagData_to_pose node to take in different xml files

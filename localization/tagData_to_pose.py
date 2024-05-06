import rclpy
from geometry_msgs.msg import PoseArray
from rclpy.node import Node
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseWithCovarianceStamped
from canopen_pgv150i_driver.msg import TagData
import xml.etree.ElementTree as ET
import math
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

class camera_convertor(Node):
    def __init__(self):
        super().__init__('camera_convertor')
        self.subscriber=self.create_subscription(TagData,'sim',self.Tag_cb,10)
        self.pub= self.create_publisher(PoseWithCovarianceStamped, 'EKF_in_cam', 10)

        self.qr_array=PoseArray()
        tree = ET.parse("/home/brianwaters/workspaces/eirabot_ws/src/demo_area_mapping/demo_area_mapping/sample.xml")
        root = tree.getroot()
        self.VertexDictionary ={}
        for Vertex in root[4]:
            Position= {
                "Name":Vertex.attrib["Name"],
                "X":float(Vertex[4][0].text)/1000,
                "Y":float(Vertex[4][1].text)/1000,
                "Z":float(Vertex[4][2].text)/1000,
            }
            self.VertexDictionary[Vertex.attrib["Name"]]=Position
        print(self.VertexDictionary['612'])
    def Tag_cb(self,msg):
        #print(msg)
        if(msg.tag_present==False):
            return
        Tag_pose=self.VertexDictionary[str(msg.id)]
        pose_msg = PoseWithCovarianceStamped()
        pose_msg.header.stamp = self.get_clock().now().to_msg()
        pose_msg.header.frame_id = 'odom'
        pose_msg.pose.pose.position.x = Tag_pose["X"]+msg.x
        pose_msg.pose.pose.position.y = Tag_pose["Y"]+msg.y
        pose_msg.pose.pose.orientation.z = msg.angle
        self.pub.publish(pose_msg)

def main(args=None):
    rclpy.init(args=args)
    camera_con= camera_convertor()
    rclpy.spin(camera_con)

    # Destroy the node explicitly
    camera_con.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

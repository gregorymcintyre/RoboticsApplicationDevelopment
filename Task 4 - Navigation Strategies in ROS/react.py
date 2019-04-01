#!/usr/bin/env python
import rospy
from std_msgs.msg import Int8
from geometry_msgs.msg import Twist

rospy.init_node('scared_robot', anonymous=True)
pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard %d', data.data)
    if data.data > 4:
        vel_msg = Twist()
        vel_msg.linear.x = -2
        #Since we are moving just in x-axis
        vel_msg.linear.y = 0
        vel_msg.linear.z = 0
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        vel_msg.angular.z = 0
        pub.publish(vel_msg)

def listener():
    #rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('sensor', Int8, callback)
    #spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()

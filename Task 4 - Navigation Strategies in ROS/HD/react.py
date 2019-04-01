
 # HD Task
 #
 # Greg McIntyre
 # 1 APR 2018
 # 
 # Accurate wall avoidance using the Zumo’s full sensor array. Advanced solutions can also consider all IR emitters to each sensor
 #
 # the robot sucessfully avoids objects infront, to the left and right and moves away from the detected object
 #

#!/usr/bin/env python
import rospy
from std_msgs.msg import Int8
from geometry_msgs.msg import Twist

rospy.init_node('scared_robot', anonymous=True)
pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

def callback(data):
    #rospy.loginfo(rospy.get_caller_id() + ' I heard %d', data.data)
    if data.data > 4:
        rospy.loginfo(rospy.get_caller_id() + ' I heard %d from the front', data.data)
        vel_msg = Twist()
        vel_msg.linear.x = -2       #reverse
        #Since we are moving just in x-axis
        vel_msg.linear.y = 0
        vel_msg.linear.z = 0
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        vel_msg.angular.z = 0
        pub.publish(vel_msg)

def callleft(data):
    #rospy.loginfo(rospy.get_caller_id() + ' I heard %d', data.data)
    if data.data > 4:
        rospy.loginfo(rospy.get_caller_id() + ' I heard %d from the left', data.data)
        vel_msg = Twist()
        vel_msg.linear.x = 0
        #Since we are moving just in x-axis
        vel_msg.linear.y = 0
        vel_msg.linear.z = 0
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        vel_msg.angular.z = -2      #turn right
        pub.publish(vel_msg)

def callright(data):
    #rospy.loginfo(rospy.get_caller_id() + ' I heard %d', data.data)
    if data.data > 4:
        rospy.loginfo(rospy.get_caller_id() + ' I heard %d from the right', data.data)
        vel_msg = Twist()
        vel_msg.linear.x = 0
        #Since we are moving just in x-axis
        vel_msg.linear.y = 0
        vel_msg.linear.z = 0
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        vel_msg.angular.z = 2       #turn left
        pub.publish(vel_msg)



def listener():
    #rospy.init_node('listener', anonymous=True)
    #rospy.Subscriber('sensor', Int8, callback)
    rospy.Subscriber('proxLeftSensor', Int8, callleft)
    rospy.Subscriber('proxFrontSensor', Int8, callback)
    rospy.Subscriber('proxRightSensor', Int8, callright)

    #spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()

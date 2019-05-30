#
#	zumo_lane_change
#	(untested)	
#
#	Last Update 30/5/19
#
#	this script would require some creative implementation, it would be required to run only when other sensors are active, so if the zumo is turing right and it alterts to an object to the right it would immediately halt
#	in its current state it would immediately halt the vehicle, with any stimuli and thus would not be effective
#

#!/usr/bin/env python

import rospy
from std_msgs.msg import Int8
from geometry_msgs.msg import Twist
from std_msgs.msg import Int8

import time
import sys
import os

rospy.init_node('zumo_conflict_resolution', anonymous=True)
pub = rospy.Publisher('/zumo/4/cmd_vel', Twist, queue_size=10)
current_topic = 0
new_topic = 4


def stop():
	vel_msg = Twist()
	vel_msg.linear.x = 0
	vel_msg.linear.y = 0
	vel_msg.linear.z = 0
	vel_msg.angular.x = 0
	vel_msg.angular.y = 0
	vel_msg.angular.z = 0
	vel_msg.linear.x = 0
	pub.publish(vel_msg)
	
def handle_zumo_sensor(wall_msg):
	global current_topic

	if(wall_msg.data > 9):
		new_topic = 0
		stop()
	else:
		new_topic = 4

	if(current_topic ==0 and new_topic == 4):
		os.system("rosrun topic_tools mux_select mux_cmdvel /zumo/3/cmd_vel")
		current_topic = 4
	if(current_topic ==4 and new_topic == 0):
		os.system("rosrun topic_tools mux_select mux_cmdvel /zumo/2/cmd_vel")
		current_topic = 0

#	this is commented out because it would cause complications in its untested state	

rospy.Subscriber('/zumo/prox_left', Int8, handle_zumo_sensor)
rospy.Subscriber('/zumo/prox_right', Int8, handle_zumo_sensor)
rospy.Subscriber('/zumo/prox_frontleft', Int8, handle_zumo_sensor)
rospy.Subscriber('/zumo/prox_frontright', Int8, handle_zumo_sensor)


#take over
os.system("rosrun topic_tools mux_select mux_cmdvel /zumo/4/cmd_vel")
current_topic = 4
rospy.spin()
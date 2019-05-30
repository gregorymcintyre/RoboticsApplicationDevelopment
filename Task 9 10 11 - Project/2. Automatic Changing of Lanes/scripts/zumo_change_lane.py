#
#	zumo_lane_change
#	(untested)	
#
#	Last Update 30/5/19
#
#	this script is designed to have the zumo detect a close object infront and perform a manover to move into the next lane to the right
#	the subs should not interrupt each other so the manover into the right should be compelete before begining the return to original lane
#

#!/usr/bin/env python

import rospy
from std_msgs.msg import Int8
from geometry_msgs.msg import Twist
from std_msgs.msg import Int8

import time
import sys
import os

rospy.init_node('zumo_change_lane', anonymous=True)
pub = rospy.Publisher('/zumo/3/cmd_vel', Twist, queue_size=10)
current_topic = 0
new_topic = 3

def right():
	vel_msg = Twist()
	vel_msg.linear.x = 0
	vel_msg.linear.y = -1
	vel_msg.linear.z = 0
	vel_msg.angular.x = 0
	vel_msg.angular.y = 0
	vel_msg.angular.z = 0
	vel_msg.linear.x = 0
	pub.publish(vel_msg)

def left():
	vel_msg = Twist()
	vel_msg.linear.x = 0
	vel_msg.linear.y = 1
	vel_msg.linear.z = 0
	vel_msg.angular.x = 0
	vel_msg.angular.y = 0
	vel_msg.angular.z = 0
	vel_msg.linear.x = 0
	pub.publish(vel_msg)

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
	
def forward():
	vel_msg = Twist()
	vel_msg.linear.x = 0
	vel_msg.linear.y = 0
	vel_msg.linear.z = 0
	vel_msg.angular.x = 0
	vel_msg.angular.y = 0
	vel_msg.angular.z = 0
	vel_msg.linear.x = 1
	pub.publish(vel_msg)

def handle_zumo_sensor(wall_msg):
	global current_topic

	if(wall_msg.data > 9):
		new_topic = 2
		
		#
		#	move into the right, forward into position, left to correct within the lane
		#
		
		right()
		forward()
		rospy.sleep(1)
		left()
	else:
		new_topic = 3

	if(current_topic ==2 and new_topic == 3):
		os.system("rosrun topic_tools mux_select mux_cmdvel /zumo/3/cmd_vel")
		current_topic = 3
	if(current_topic ==3 and new_topic == 2):
		os.system("rosrun topic_tools mux_select mux_cmdvel /zumo/2/cmd_vel")
		current_topic = 2


def handle_zumo_sensor_right(wall_msg):
	global current_topic

	if(wall_msg.data > 9):
		new_topic = 2
		
		#
		#	if an unexpected object is in the right halt
		#
		
		stop()
	else:
		new_topic = 3

	#only change topics if we need to.
	if(current_topic ==2 and new_topic == 3):
		os.system("rosrun topic_tools mux_select mux_cmdvel /zumo/3/cmd_vel")
		current_topic = 3
	if(current_topic ==3 and new_topic == 2):
		os.system("rosrun topic_tools mux_select mux_cmdvel /zumo/2/cmd_vel")
		current_topic = 2

def handle_zumo_sensor_left(wall_msg):
	global current_topic

	if(wall_msg.data > 9):
		new_topic = 3
		
		#
		#	move into correct lane again, this is not currently enabled because i expect it to cause collisions, i would need to debug when to use this to have the action performed 
		#	only when the vehicle has passed the object but it would need to retain information about the object to accurately perform the manover.
		#
		
		left()
		forward()
		rospy.sleep(1)
		right()
	else:
		new_topic = 1

	if(current_topic ==2 and new_topic == 3):
		os.system("rosrun topic_tools mux_select mux_cmdvel /zumo/3/cmd_vel")
		current_topic = 3
	if(current_topic ==3 and new_topic == 2):
		os.system("rosrun topic_tools mux_select mux_cmdvel /zumo/2/cmd_vel")
		current_topic = 2

#	this is commented out because it would cause complications in its untested state	

#rospy.Subscriber('/zumo/prox_left', Int8, handle_zumo_sensor_right)
#rospy.Subscriber('/zumo/prox_right', Int8, handle_zumo_sensor_left)
rospy.Subscriber('/zumo/prox_frontleft', Int8, handle_zumo_sensor)
rospy.Subscriber('/zumo/prox_frontright', Int8, handle_zumo_sensor)


#take over
os.system("rosrun topic_tools mux_select mux_cmdvel /zumo/3/cmd_vel")
current_topic = 3
rospy.spin()
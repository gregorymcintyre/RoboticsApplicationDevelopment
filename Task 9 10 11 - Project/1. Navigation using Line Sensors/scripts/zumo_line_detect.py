#
#	zumo_line_detect
#	(untested)	
#
#	Last Update 30/5/19
#
#	this is the script to have the automated vehicle maintain position within two lines for ease of setup the surface of the road must be lighter in coulour than the lines
#	e.g. White table with black lines
#

#!/usr/bin/env python

import rospy
from std_msgs.msg import Int8
from geometry_msgs.msg import Twist
from std_msgs.msg import Int8

import time
import sys
import os

rospy.init_node('zumo_line_detect', anonymous=True)
pub = rospy.Publisher('/zumo/2/cmd_vel', Twist, queue_size=10)
current_topic = 0
new_topic = 1

def right():
	vel_msg = Twist()
	vel_msg.linear.x = 0
	vel_msg.linear.y = -0.5
	vel_msg.angular.x = 0
	vel_msg.angular.y = 0
	vel_msg.angular.z = 0
	#vel_msg.linear.x = 0
	pub.publish(vel_msg)

def left():
	vel_msg = Twist()
	vel_msg.linear.x = 0
	vel_msg.linear.y = 0.5
	vel_msg.linear.z = 0
	vel_msg.angular.x = 0
	vel_msg.angular.y = 0
	vel_msg.angular.z = 0
	#vel_msg.linear.x = 0
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

def handle_zumo_line_sensor_right(line_msg):

	#
	#	if a line is detected on the right perform left adjustment, turns are small to avoid over steering
	#

	global current_topic

	if(line_msg.data > 7):
		new_topic = 2
		left()
	else:
		new_topic = 1

	if(current_topic ==1 and new_topic == 2):
		os.system("rosrun topic_tools mux_select mux_cmdvel /zumo/2/cmd_vel")
		current_topic = 2
	if(current_topic ==2 and new_topic == 1):
		os.system("rosrun topic_tools mux_select mux_cmdvel /zumo/1/cmd_vel")
		current_topic = 1

def handle_zumo_line_sensor_left(line_msg):

	#
	#	if a line is detected on the left perform right adjustment, turns are small to avoid over steering
	#

	global current_topic

	if(line_msg.data > 7):
		new_topic = 2
		right()
	else:
		new_topic = 1

	if(current_topic ==1 and new_topic == 2):
		os.system("rosrun topic_tools mux_select mux_cmdvel /zumo/2/cmd_vel")
		current_topic = 2
	if(current_topic ==2 and new_topic == 1):
		os.system("rosrun topic_tools mux_select mux_cmdvel /zumo/1/cmd_vel")
		current_topic = 1

# only subscriber to required topics
rospy.Subscriber('/zumo/line_left', Int8, handle_zumo_line_sensor_right)			#left line turn right
rospy.Subscriber('/zumo/line_right', Int8, handle_zumo_line_sensor_left)			#right line turn left

#take over
os.system("rosrun topic_tools mux_select mux_cmdvel /zumo/1/cmd_vel")
current_topic = 1
rospy.spin()
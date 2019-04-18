#!/usr/bin/env python

import rospy
from std_msgs.msg import Int8
from geometry_msgs.msg import Twist
from std_msgs.msg import Int8

import time
import sys
import os

rospy.init_node('zumo_object_detect', anonymous=True)
pub = rospy.Publisher('/zumo/2/cmd_vel', Twist, queue_size=10)
current_topic = 0
new_topic = 1

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
		new_topic = 2
		stop() #actually publish a new message..
	else:
		new_topic = 1

	#only change topics if we need to.
	if(current_topic ==1 and new_topic == 2):
		os.system("rosrun topic_tools mux_select mux_cmdvel /zumo/2/cmd_vel")
		current_topic = 2
	if(current_topic ==2 and new_topic == 1):
		os.system("rosrun topic_tools mux_select mux_cmdvel /zumo/1/cmd_vel")
		current_topic = 1
	
rospy.Subscriber('/zumo/prox_frontleft', Int8, handle_zumo_sensor)
rospy.Subscriber('/zumo/prox_frontright', Int8, handle_zumo_sensor)

#take over
os.system("rosrun topic_tools mux_select mux_cmdvel /zumo/1/cmd_vel")
current_topic = 1
rospy.spin()
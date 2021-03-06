/*
 * LineSensor.ino
 * (Untested)
 * 
 * Greg McIntyre
 * Last Update: 30/05/19
 * 
 * This is a modified version of a promity senor program from the lab and the LineSensorTest from the Zumo examples
 * 
 * Due to some hardware problems this is untested code, it is designed to be a base for debugging to show and understanding
 * 
 */

#define USE_USBCON
#include <Wire.h>
#include <Zumo32U4.h>
#include <ros.h>
#include <geometry_msgs/Twist.h>
#include <std_msgs/Int8.h>

ros::NodeHandle nh;

Zumo32U4LineSensors lineSensors;
ZumoReflectanceSensorArray reflectanceSensors;

bool  lineLeftActive;
bool  lineRightActive;

unsigned int lineSensorValues[3];   //initthree

std_msgs::Int8 line_msg;

ros::Publisher pub_line_left("/zumo/line_left", &prox_msg);
ros::Publisher pub_line_right("/zumo/line_right", &prox_msg);

void ros_handler( const geometry_msgs::Twist& cmd_msg) {
  float x = cmd_msg.linear.x;
  float y = cmd_msg.linear.y;
  int speed = 100;
  
  if(x == 1.0) forward(speed);
  if(x == -1.0) backward(speed);
  if(y == 1.0) left(speed);
  if(y == -1.0) right(speed);
  stop();
}

ros::Subscriber<geometry_msgs::Twist> sub("/zumo/cmd_vel", ros_handler);

Zumo32U4Motors motors;

void setup()
{
  nh.initNode();
  nh.subscribe(sub);

  nh.advertise(pub_line_left);
  nh.advertise(pub_line_right);
  
  lineSensors.initThreeSensors();
  
  uint16_t defaultBrightnessLevels[] = {1,2,3,4,5,6,7,8,9,10};
}

void publishSensorData()
{
  line_msg.data = lineSensorValues[0]; //left
  pub_right.publish( &line_msg);
  ine_msg.data = lineSensorValues[2]; //right
  pub_right.publish( &line_msg);
  
}

void forward(int time)
{
  motors.setLeftSpeed(100);
  motors.setRightSpeed(100);
  delay(time);
}

void backward(int time)
{
  motors.setLeftSpeed(-100);
  motors.setRightSpeed(-100);
  delay(time);
}

void left(int time)
{
  motors.setLeftSpeed(-100);
  motors.setRightSpeed(100);
  delay(time);
}

void right(int time)
{
  motors.setLeftSpeed(100);
  motors.setRightSpeed(-100);
  delay(time);
}

void stop()
{
  motors.setLeftSpeed(0);
  motors.setRightSpeed(0);
}

void loop()
{
  static uint16_t lastSampleTime = 0;
  if ((uint16_t)(millis() - lastSampleTime) >= 100)
  {
    lastSampleTime = millis();
    lineSensors.read(lineSensorValues,QTR_EMITTERS_ON);
    publishSensorData();
  }
  nh.spinOnce();
  delay(1);
}


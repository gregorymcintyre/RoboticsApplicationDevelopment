/*
 * HD Task
 *
 * Greg McIntyre
 * 1 APR 2018
 * 
 * Accurate wall avoidance using the Zumo’s full sensor array. Advanced solutions can also consider all IR emitters to each sensor
 *
 * the robot sucessfully avoids objects infront, to the left and right and moves away from the detected object
 *
 */

#define USE_USBCON
#include <Wire.h>
#include <Zumo32U4.h>
#include <ros.h>
#include <geometry_msgs/Twist.h>
#include <std_msgs/Int8.h>

ros::NodeHandle nh;
std_msgs::Int8 msg;
ros::Publisher pub("sensor", &msg);

ros::Publisher pl_pub("proxLeftSensor", &msg);
ros::Publisher pf_pub("proxFrontSensor", &msg);
ros::Publisher pr_pub("proxRightSensor", &msg);

void ros_handler( const geometry_msgs::Twist& cmd_msg) 
{
  float x = cmd_msg.linear.x;
  float z = cmd_msg.angular.z;
  
  if(x == -2.0) backward(100);
  if(x == 2.0) forward(100);
  if(z == -2.0) right(100);
  if(z == 2.0) left(100);

  stop();
}

ros::Subscriber<geometry_msgs::Twist> sub("/turtle1/cmd_vel", ros_handler);

Zumo32U4ProximitySensors proxSensors;
bool proxLeftActive;
bool proxFrontActive;
bool proxRightActive;

Zumo32U4Motors motors;

void setup()
{
  // Uncomment if necessary to correct motor directions:
  //motors.flipLeftMotor(true);
  //motors.flipRightMotor(true);
  nh.initNode();
  nh.subscribe(sub);
  proxSensors.initThreeSensors();
  nh.initNode();
  nh.advertise(pub);
  
  nh.advertise(pl_pub);
  nh.advertise(pf_pub);
  nh.advertise(pr_pub);
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

void right(int time)
{
  motors.setLeftSpeed(100);
  motors.setRightSpeed(-100);
  delay(time);
}

void left(int time)
{
  motors.setLeftSpeed(-100);
  motors.setRightSpeed(100);
  delay(time);
}

void stop()
{
  motors.setLeftSpeed(0);
  motors.setRightSpeed(0);
}

void publishReadings()
{
  msg.data = proxSensors.countsLeftWithLeftLeds();
  pub.publish( &msg);
  
  msg.data = proxSensors.countsLeftWithLeftLeds();
  pl_pub.publish( &msg);
  
  msg.data = proxSensors.countsFrontWithLeftLeds();
  pf_pub.publish( &msg);
  
  msg.data = proxSensors.countsRightWithRightLeds();
  pr_pub.publish( &msg);
  
  nh.spinOnce();
  delay(100);
}

void loop()
{
  static uint16_t lastSampleTime = 0;
  if ((uint16_t)(millis() - lastSampleTime) >= 100)
  {
    lastSampleTime = millis();
    // Send IR pulses and read the proximity sensors.
    proxSensors.read();
    // Just read the proximity sensors without sending pulses.
    proxLeftActive = proxSensors.readBasicLeft();
    proxFrontActive = proxSensors.readBasicFront();
    proxRightActive = proxSensors.readBasicRight();
    publishReadings();
  }
  
  nh.spinOnce();
  delay(1);
}

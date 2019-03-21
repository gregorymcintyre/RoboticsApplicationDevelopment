#define USE_USBCON

#include <Wire.h>
#include <Zumo32U4.h>
#include <ros.h>
#include <std_msgs/UInt16.h>

Zumo32U4Motors motors;
Zumo32U4LCD lcd;

ros::NodeHandle nh;
void ros_handler( const std_msgs::UInt16& cmd_msg){
  if(cmd_msg.data == 0) stop();
  if(cmd_msg.data == 1) forward(1000);
  if(cmd_msg.data == 2) backward(1000);
  lcd.clear();
  lcd.print(cmd_msg.data);
}

ros::Subscriber<std_msgs::UInt16> sub("control", ros_handler);

void setup()
{
// Uncomment if necessary to correct motor directions:
//motors.flipLeftMotor(true);
//motors.flipRightMotor(true);
  nh.initNode();
  nh.subscribe(sub);
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

void stop()
{
  motors.setLeftSpeed(0);
  motors.setRightSpeed(0);
}

void loop()
{
  nh.spinOnce();
  delay(1);
}

#define USE_USBCON
#include <ros.h>
#include <std_msgs/Int8.h>
ros::NodeHandle nh;
std_msgs::Int8 msg;
ros::Publisher pub("sensor", &msg);

#include <Wire.h>
#include <Zumo32U4.h>
Zumo32U4ProximitySensors proxSensors;
bool proxLeftActive;
bool proxFrontActive;
bool proxRightActive;
void setup()
{
/* Configuration:
* - 3 proximity sensors (left, front, right)
*
*/
proxSensors.initThreeSensors();
nh.initNode();
nh.advertise(pub);
}
// Prints a line with all the sensor readings to the serial
// monitor.
void printReadingsToSerial()
{
msg.data = proxSensors.countsLeftWithLeftLeds();
pub.publish( &msg);
nh.spinOnce();
delay(100);
}
void loop()
{
static uint16_t lastSampleTime = 10;
if ((uint16_t)(millis() - lastSampleTime) >= 100)
{
lastSampleTime = millis();
// Send IR pulses and read the proximity sensors.
proxSensors.read();
// Just read the proximity sensors without sending pulses.
proxLeftActive = proxSensors.readBasicLeft();
proxFrontActive = proxSensors.readBasicFront();

proxRightActive = proxSensors.readBasicRight();
printReadingsToSerial();
}
}

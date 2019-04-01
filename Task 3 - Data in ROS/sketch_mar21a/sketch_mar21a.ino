/*
 * 
 * 
 */
#include <Wire.h>
#include <Zumo32U4.h>
Zumo32U4ProximitySensors proxSensors;
//uint16_t lineSensorValues[5] = { 0, 0, 0, 0, 0 };
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
}

// Prints a line with all the sensor readings to the serial
// monitor.
void printReadingsToSerial()
{
static char buffer[80];
sprintf(buffer, "%d %d %d %d\n",
proxSensors.countsLeftWithLeftLeds(),
proxSensors.countsFrontWithLeftLeds(),
proxSensors.countsFrontWithRightLeds(),
proxSensors.countsRightWithRightLeds()
);
Serial.print(buffer);
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
printReadingsToSerial();
}
}

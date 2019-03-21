#include <Wire.h>
#include <Zumo32U4.h>
Zumo32U4Motors motors;
Zumo32U4ButtonA buttonA;
void setup()
{
// Uncomment if necessary to correct motor directions:
//motors.flipLeftMotor(true);
//motors.flipRightMotor(true);
// Wait for the user to press button A.
buttonA.waitForButton();
// Delay so that the robot does not move away while the user is
// still touching it.
delay(1000);
}
void loop()
{
// Run robot forward for 1 second.
motors.setLeftSpeed(100);
motors.setRightSpeed(100);
delay(1000);
// Wait robot for 1 second.
motors.setLeftSpeed(0);
motors.setRightSpeed(0);
delay(1000);
// Run robot forward for 1 second.
motors.setLeftSpeed(-100);
motors.setRightSpeed(-100);
delay(1000);

// Wait robot for 1 second.
motors.setLeftSpeed(0);
motors.setRightSpeed(0);
delay(1000);
}

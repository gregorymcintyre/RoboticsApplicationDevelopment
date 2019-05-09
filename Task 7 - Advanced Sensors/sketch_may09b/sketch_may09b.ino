#include <Wire.h>
#include <Zumo32U4.h>

LSM303 compass;
void setup()
{
  Wire.begin();
  if (!compass.init())
  {
    // Failed to detect the compass.
    ledRed(1);
    while(1)
    {
      Serial.println(F("Failed to detect the compass."));
      delay(100);
    }
  }
  //replace your calibration values
  compass.enableDefault();
  compass.m_min.x=-7788;
  compass.m_min.y=142;
  compass.m_min.z=-461;
  compass.m_max.x=-2905;
  compass.m_max.y=3639;
  compass.m_max.z=2446;
}
void loop()
{
  compass.read();
  Serial.println(compass.heading());
  delay(100);
}

#include <Wire.h>
#include <Zumo32U4.h>

LSM303 compass;

char report[120];

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

  compass.enableDefault();
}

int minx=32767, miny=32767, minz=32767, maxx=-32767, maxy=-32767, maxz=-32767;

void loop()
{
  
  compass.read();
  if(compass.m.x<minx)  minx=compass.m.x;
  if(compass.m.y<miny)  miny=compass.m.y;
  if(compass.m.z<minz)  minz=compass.m.z;
  if(compass.m.x>maxx)  maxx=compass.m.x;
  if(compass.m.y>maxy)  maxy=compass.m.y;
  if(compass.m.z>maxz)  maxz=compass.m.z;
  
  snprintf_P(report, sizeof(report),
  PSTR("Current: %6d %6d %6d  MAX: %6d %6d %6d"),
  compass.m.x, compass.m.y, compass.m.z,
  compass.m.x, compass.m.y, compass.m.z);
  Serial.println(report);
  
  snprintf_P(report, sizeof(report),
  PSTR("MIN: %6d %6d %6d  MAX: %6d %6d %6d"),
  minx, miny, minz,
  maxx, maxy, maxz);
  Serial.println(report);
  
  Serial.println();
  delay(100);
}

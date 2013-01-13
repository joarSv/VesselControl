/*
	VesselControlArduino
		Created 2012-10-09
		Rasmus Jansson and Joar Svensson
		Version 0.2
*/

#include <Servo.h>
#include "DualVNH5019MotorShield.h"

// Initialize servos
Servo servoX;
Servo servoY;

// Initialize motorshield
DualVNH5019MotorShield md;

void setup() 
{
  servoX.attach(9);
  servoY.attach(10);
  md.init();
  
  Serial.begin(9600);
  Serial.println("Arduino Uno available");
}

void loop() 
{ 
    if(Serial.available() >= 3)
    {
      int id = 0;
      id = Serial.read(); 
      if(id >=1 && id <=6)   {
        int value = Serial.read();
        int dir = Serial.read();
        moveServo(id, value, dir);
        
        // Motor 1, -400 to 400. Zero is full throttle.
        md.setM1Speed(value);
        stopIfFault();
        
        // Motor 2
        md.setM2Speed(value);
        stopIfFault();
      }
    }
}

// Stop motors if fault arise
void stopIfFault()
{
  if (md.getM1Fault())
  {
    Serial.println("M1 fault");
    while(1);
  }
  if (md.getM2Fault())
  {
    Serial.println("M2 fault");
    while(1);
  }
}

// Method for moving servo
void moveServo(int id, int value, int dir) 
{
  switch(id)
  {
    case 1:
      servoX.write(value);
      break;
    case 2:
      servoY.write(value);
        break;
     case 4:
       if(dir == 1) 
       {
          motor4.run(FORWARD);
       }
       else if(dir == 2) 
       {
          motor4.run(BACKWARD);
       }
       else if(dir == 0)
       {
          motor4.run(RELEASE); 
       }
       motor4.setSpeed(value);
       break;
    default:
      break;
  }  
}

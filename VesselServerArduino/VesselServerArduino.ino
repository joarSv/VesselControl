/*
	VesselControlArduino
		Created 2012-10-09
		Rasmus Jansson and Joar Svensson
		Version 0.1
		
*/

#include <Servo.h> 

// Initialize servos
Servo servoX;
Servo servoY;

void setup() 
{
  servoX.attach(9);
  servoY.attach(10);
  Serial.begin(9600);
  Serial.println("Arduino available");
}

void loop() 
{ 
    if(Serial.available() >= 3)
    {
      int data = 0;
      data = Serial.read(); 
      if(data == 255)
      {
        int servo = Serial.read();
        int angle = Serial.read();  
        moveServo(servo, angle);
        Serial.println("Arduino response");   
      }
    }
}

// Method for moving servo
void moveServo(int servo, int angle) 
{
  switch(servo)
  {
    case 1:
      servoX.write(angle);
      break;
    case 2:
      servoY.write(angle);
      break;
    default:
      break;
  }  
}

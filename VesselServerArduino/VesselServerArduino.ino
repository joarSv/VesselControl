/*
	VesselControlArduino
		Created 2012-10-09
		Rasmus Jansson and Joar Svensson
		Version 0.2
*/

#include <Servo.h>

// Initialize voltmeter variables
int analogInput = 0;
float value = 0.0;
float vOut = 0.0;
float vIn = 0.0;
// Value of resistors
float r1 = 47400.0;
float r2 = 3840.0;

// Initialize servos
Servo servoX;
Servo servoY;

void setup() 
{
  pinMode(analogInput, INPUT);
  
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
        
        value = analogRead(analogInput);
        vOut = (value * 5.0) / 1024.0;
        vIn = vOut / (r2/(r1+r2));
        Serial.println(vIn);   
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

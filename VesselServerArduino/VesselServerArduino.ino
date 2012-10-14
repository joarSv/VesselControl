/*
	VesselControlArduino
		Created 2012-10-09
		Rasmus Jansson and Joar Svensson
		Version 0.2
*/

#include <Servo.h>
#include <AFMotor.h>

// Initialize servos and motors
Servo servoX;
Servo servoY;
//AF_DCMotor motor1(1);
//AF_DCMotor motor2(2);
//AF_DCMotor motor3(3);
//AF_DCMotor motor4(4);

void setup() 
{
  servoX.attach(9);
  servoY.attach(10);
  
  //mainMotor1.run(RELEASE);
  //mainMotor2.run(RELEASE);
  //bowThruster.run(RELEASE);
  //sternThruster.run(RELEASE);
  
  Serial.begin(9600);
  Serial.println("Arduino Uno available");
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
      //if (angle >= 90)
        //mainMotor1.run(FORWARD);
        //mainMotor1.setSpeed(angle);
      //else if (angle <= 89)
        //mainMotor1.run(REVERSE);
        //mainMotor1.setSpeed(angle);
      break;
    case 2:
      servoY.write(angle);
      //if (angle >= 90)
        //mainMotor2.run(FORWARD);
        //mainMotor2.setSpeed(angle);
      //else if (angle <= 89)
        //mainMotor2.run(REVERSE);
        //mainMotor2.setSpeed(angle);
        break;
    default:
      break;
  }  
}

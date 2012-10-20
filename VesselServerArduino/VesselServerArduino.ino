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
AF_DCMotor motor4(4);

void setup() 
{
  servoX.attach(9);
  servoY.attach(10);
  
  motor4.run(RELEASE);
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
      int id = 0;
      id = Serial.read(); 
      if(id >=1 && id <=6)   {
        int value = Serial.read();
        int dir = Serial.read();
        moveServo(id, value, dir); 
      }
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

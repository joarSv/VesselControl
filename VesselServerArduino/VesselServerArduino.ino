#include <Servo.h> 
/*
  byte = 1 byte
  char = 1 byte
  word = 2 bytes
  int = 2 bytes
  long = 4 bytes
*/
Servo servoX;
Servo servoY;

void setup() 
{
  servoX.attach(9);
  servoY.attach(10);
  Serial.begin(9600);
}

void loop() 
{ 
   int data = 0;
    if(Serial.available() >= 3)
    {
      data = Serial.read(); 
      if(data == 255)
      {
        int servo = Serial.read();
        int angle = Serial.read();  
        moveServo(servo, angle);     
      }
    }
}

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
    /*case 3:
      servoZ.write(angle);
      break;*/
    default:
      break;
  }  
}

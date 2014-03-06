/*
	VesselControlArduino
		Created 2012-10-09
		Rasmus Jansson and Joar Svensson
		Version 0.3
*/

// This line specifies what pin we will use for sending the
// signal to the servo.  You can change this.
#define SERVO_PIN 11
 
// This is the time since the last rising edge in units of 0.5us.
uint16_t volatile servoTime = 0;
 
// This is the pulse width we want in units of 0.5us.
uint16_t volatile servoHighTime = 3000;
 
// This is true if the servo pin is currently high.
boolean volatile servoHigh = false;

int outputValue;

//#include <Servo.h>
#include "DualVNH5019MotorShield.h"

// Initialize motorshield
DualVNH5019MotorShield md;

void setup() 
{
	md.init();
  servoInit();
  
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

ISR(TIMER2_COMPA_vect)
{
  // The time that passed since the last interrupt is OCR2A + 1
  // because the timer value will equal OCR2A before going to 0.
  servoTime += OCR2A + 1;
   
  static uint16_t highTimeCopy = 3000;
  static uint8_t interruptCount = 0;
   
  if(servoHigh)
  {
    if(++interruptCount == 2)
    {
      OCR2A = 255;
    }
 
    // The servo pin is currently high.
    // Check to see if is time for a falling edge.
    // Note: We could == instead of >=.
    if(servoTime >= highTimeCopy)
    {
      // The pin has been high enough, so do a falling edge.
      digitalWrite(SERVO_PIN, LOW);
      servoHigh = false;
      interruptCount = 0;
    }
  } 
  else
  {
    // The servo pin is currently low.
     
    if(servoTime >= 40000)
    {
      // We've hit the end of the period (20 ms),
      // so do a rising edge.
      highTimeCopy = servoHighTime;
      digitalWrite(SERVO_PIN, HIGH);
      servoHigh = true;
      servoTime = 0;
      interruptCount = 0;
      OCR2A = ((highTimeCopy % 256) + 256)/2 - 1;
    }
  }
}
 
void servoInit()
{
  digitalWrite(SERVO_PIN, LOW);
  pinMode(SERVO_PIN, OUTPUT);
   
  // Turn on CTC mode.  Timer 2 will count up to OCR2A, then
  // reset to 0 and cause an interrupt.
  TCCR2A = (1 << WGM21);
  // Set a 1:8 prescaler.  This gives us 0.5us resolution.
  TCCR2B = (1 << CS21);
   
  // Put the timer in a good default state.
  TCNT2 = 0;
  OCR2A = 255;
   
  TIMSK2 |= (1 << OCIE2A);  // Enable timer compare interrupt.
  sei();   // Enable interrupts.
}
 
void servoSetPosition(uint16_t highTimeMicroseconds)
{
  TIMSK2 &= ~(1 << OCIE2A); // disable timer compare interrupt
  servoHighTime = highTimeMicroseconds * 2;
  TIMSK2 |= (1 << OCIE2A); // enable timer compare interrupt
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
    	outputValue = map(value, 0, 180, 1000, 2000); 
      servoSetPosition(outputValue);
      break;
    case 2:
    //  servoY.write(value);
        break;
    case 3:
       //motor4.run(FORWARD);
       // Motor 2, -400 to 400. Zero is full throttle. 
       value = (value-100)*4; //(-400 400)
       md.setM1Speed(value);
       stopIfFault();
       break;
    case 4:
       //motor4.run(FORWARD);
       // Motor 1, -400 to 400. Zero is full throttle. 
       value = (value-100)*4; //(-400 400)
       md.setM2Speed(value);
       stopIfFault();
       break;
  }
}

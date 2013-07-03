/*
	VesselControlArduino
		Created 2012-10-09
		Rasmus Jansson and Joar Svensson
		Version 0.1
*/

// Initialize voltmeter variables
int analogInput = 0;
float value = 0.0;
float vOut = 0.0;
float vIn = 0.0;
// Value of resistors
float r1 = 47400.0;
float r2 = 3840.0;

void setup() 
{
  pinMode(analogInput, INPUT);
  
  Serial.begin(9600);
  Serial.println("Arduino Nano available");
}

void loop() 
{ 
  value = analogRead(analogInput);
  vOut = (value * 5.0) / 1024.0;
  vIn = vOut / (r2/(r1+r2));
  Serial.println(vIn);
  delay(2000);  
}

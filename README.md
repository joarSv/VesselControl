<h1>VesselControll</h1>

VesselControl is a project aiming to remotely control and operate a model vessel. Equipment used is an Android smartphone, a Raspberry Pi with usb wifi-dongle and an Arduino Uno.

The Raspberry Pi acts as a combined server and access point through a connected usb wifi-dongle. 
The Pi is running python software connecting an Android smartphone with a Arduino enabling control of DC motors and servos.

The whole setup is currently powered by a two 6 volt lead-acid batteries often found in larger torches and small motorbikes. One battery is powering the motors and servos, while the other one is solely powering the Pi.

We are currently using Samsung S3 smartphones to operate the vessel. The Android application is using accelerometer readings mapped to suit the servo and motor operations.
The wifi connection enables the raspberry to stream a webcam feed back to the operator, this is currently achived by using the Linux software Motion together with a HD webcam.

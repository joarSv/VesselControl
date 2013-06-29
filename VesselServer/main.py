#
#    VesselServer
#        Created 2012-10-09
#        Rasmus Jansson and Joar Svensson
#        Version 0.2
#	 https://github.com/JoarSvensson/VesselControl.git
#        

from serial import Serial
import SocketServer, os, time, logging
#import RPi.GPIO as GPIO

#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(11, GPIO.OUT)
        
# This class contains the socket server
class VesselTCPHandler(SocketServer.BaseRequestHandler):
    
    # Function to handle connections and sending instructions to the Arduino
    def handle(self):       
	connected = True
	printLog(str(time.time()) + ': Client connected')
        
	while(connected):
            self.data = self.request.recv(3)
            if(self.data == ""):		
		printLog(str(time.time()) + ': Client disconnected')
                break
            if(len(self.data) == 3):
                number = ord(self.data[0])
                value = ord(self.data[1])
                direction = ord(self.data[2])
                if(number > 0 and number < 7):
                    move(number, value, direction)
                    
        connected = False
        # Stop motors when client disconnect
	printLog(str(time.time()) + ': Motors de-attached')
        move(1,90,0)
        move(3,100,0)
        move(4,100,0)
        
# This function sends instructions to the Arduino Uno
def move(number, value, direction):
        ser.write(chr(number))
        ser.write(chr(value))
        ser.write(chr(direction))
        ser.flush()	
	printLog(str(time.time()) + ': Moving ' + str(number) + ' to ' + str(value))

# This function writes messages to log file
def printLog(message):
	f.write(message + '\n')
	f.flush()
        
#def shutDown():
#    if GPIO.input(11): 
#        os.system("poweroff")

# Initiate log file    
f = open('VesselServer.log','w')

# Socket server settings
socketAddress = '0.0.0.0'
socketPort = 10000
        
# Serial settings for Arduino Uno
# Linux: /dev/ttyACM0
# Windows: COM1
port = '/dev/ttyACM0'#'COM4'
baudrate = 9600
connected = False

# Initiate serial connections
try:
    ser = Serial(port, baudrate, timeout=1)
    printLog(str(time.time()) + ': Server connected to:' + str(ser.portstr))
    
except Exception, error:
    printLog(str(time.time()) + ': Error, connection with Arduino failed: ' + str(error))
    

# Initiate socket server
server = SocketServer.TCPServer((socketAddress, socketPort), VesselTCPHandler)
server.serve_forever()

# Close serial connections
ser.close()
#serNano.close()

# Close socket connection
server.close_request(VesselTCPHandler)

# Print to log
printLog(str(time.time()) + ': Connection closed\n-----------------------------------------------------------')
f.close()

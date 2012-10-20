#
#    VesselServer
#        Created 2012-10-09
#        Rasmus Jansson and Joar Svensson
#        Version 0.1
#        

from serial import Serial
import SocketServer
from threading import Thread

# Serial settings for Arduino Uno
# Linux: /dev/ttyACM0
# Windows: COM1
port = '/dev/ttyACM0'#'COM4'
baudrate = 9600
connected = False

# Serial settings for Arduino Nano
#portNano = '/dev/ttyACM1'#'COM5'
baudrateNano = 9600

# Initiate serial connections
try:
    ser = Serial(port, baudrate, timeout=1)
#    serNano = Serial(portNano, baudrateNano, timeout=1)
except Exception, error:
    print error
    
print("Server connected to: " + ser.portstr)
#print("Server connected to: " + serNano.portstr)

# This function sends instructions to the Arduino Uno
def move(servo, angle):
    if (0 <= angle <= 180):
        ser.write(chr(servo))
        ser.write(chr(angle))
        ser.flush()
        print("Command sent to servo "  + str(servo) + " angle = " +str(angle))
    else:
        print "Servo angle must be a number between 0 and 180. Now it's " + str(angle)+ "\n"
        
# Function to read sensor data from Arduino Nano
#def readSerial(serNano):
#    while True:
#        line = serNano.readline()
#        print (line)
        
# This class contains the socket server
class MyTCPHandler(SocketServer.BaseRequestHandler):
    
    # Function to handle connections and sending instructions to the Arduino
    def handle(self):        
        connected = True
        print("Client connected")
        while(connected):
            self.data = self.request.recv(2)
            if(self.data == ""):
                print("Client disconnected")
                break
            if(len(self.data) == 2):
                servo = ord(self.data[0])
                angle = ord(self.data[1])
                if(servo > 0 and servo< 4):
                    move(servo, angle)
                    
        connected = False
        
#try:
#    Thread(target=readSerial, args=(serNano,)).start()
#except Exception, error:
#    print error

# Define socket server settings
socketAddress = '0.0.0.0'
socketPort = 10000

# Initiate socket server
server = SocketServer.TCPServer((socketAddress, socketPort), MyTCPHandler)
server.serve_forever()

# Close serial connections
ser.close()
#serNano.close()

# Close socket connection
server.close_request(MyTCPHandler)
print("Connection closed")
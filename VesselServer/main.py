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
#baudrateNano = 9600

# Initiate serial connections
try:
    ser = Serial(port, baudrate, timeout=1)
#    serNano = Serial(portNano, baudrateNano, timeout=1)
except Exception, error:
    print error
    
print("Server connected to: " + ser.portstr)
#print("Server connected to: " + serNano.portstr)

# This function sends instructions to the Arduino Uno
def move(id, value, direction):
        ser.write(chr(id))
        ser.write(chr(value))
        ser.write(chr(direction))
        ser.flush()
        print("Command sent to unit "  + str(id) + " value = " +str(value))
        
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
            self.data = self.request.recv(3)
            if(self.data == ""):
                print("Client disconnected")
                break
            if(len(self.data) == 3):
                id = ord(self.data[0])
                value = ord(self.data[1])
                direction = ord(self.data[2])
                if(id > 0 and id < 7):
                    move(id, value, direction)
                    
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
#
#    VesselServer
#        Created 2012-10-09
#        Rasmus Jansson and Joar Svensson
#        Version 0.1
#        


from serial import Serial
import SocketServer

# Define serial settings
port = 'COM4'
baudrate = 9600

# Initiate serial connection
ser = Serial(port, baudrate, timeout=1)

print("Server connected to: " + ser.portstr)

# This function sends instructions to the Arduino
def move(servo, angle):
    if (0 <= angle <= 180):
        ser.write(chr(255))
        ser.write(chr(servo))
        ser.write(chr(angle))
        ser.flush()
        print("Command sent to servo "  + str(servo) + " angle = " +str(angle))
    else:
        print "Servo angle must be an integer between 0 and 180. Now it's " + str(angle)+ "\n"
        

# This class contains the socket server
class MyTCPHandler(SocketServer.BaseRequestHandler):
    
    # Function to handle connections and sending instructions to the Arduino
    def handle(self):        
        print("Client connected")
        while(True):
            self.data = self.request.recv(2)
            if(self.data == ""):
                print("Client disconnected")
                break
            if(len(self.data) == 2):
                servo = ord(self.data[0])
                angle = ord(self.data[1])
                if(servo > 0 and servo< 4):
                    move(servo, angle)

# Define socket server settings
socketAddress = '0.0.0.0'
socketPort = 10000

# Initiate socket server
server = SocketServer.TCPServer((socketAddress, socketPort), MyTCPHandler)
server.serve_forever()

# Closing serial connection
ser.close()

# Closing socket connection
server.close_request(MyTCPHandler)
print("Connection closed")
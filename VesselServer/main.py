#!/usr/bin/python3

from serial import Serial
import SocketServer

ser = Serial('COM4', 9600, timeout=1)

print("Connected to: " + ser.portstr)
def move(servo, angle):
    if (0 <= angle <= 180):
        ser.write(chr(255))
        ser.write(chr(servo))
        ser.write(chr(angle))
        ser.flush()
        print("Command sent to servo "  + str(servo) + " angle = " +str(angle))
    else:
        print "Servo angle must be an integer between 0 and 180. now it's " + str(angle)+ "\n"

class MyTCPHandler(SocketServer.BaseRequestHandler):
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

server = SocketServer.TCPServer(("0.0.0.0", 1000), MyTCPHandler)
server.serve_forever()

ser.close()
server.close_request(MyTCPHandler)
print("Connection closed")
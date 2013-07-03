#
#    VesselServer threaded
#        Created 2013-06-29
#        Rasmus Jansson and Joar Svensson
#        Version 0.2
#	 https://github.com/JoarSvensson/VesselControl.git
#       

import SocketServer, os, time, threading, thread
from serial import Serial
from socket import *

# This function handles connections
def handler(clientsock,addr):	
	connected = True

	while(connected):
	    data = clientsock.recv(3)
	    if(data == ""):		
		printLog(str(time.time()) + ': Client disconnected')
		break
	    if(len(data) == 3):
		number = ord(data[0])
		value = ord(data[1])
		direction = ord(data[2])
		if(number > 0 and number < 7):
		    move(number, value, direction)
		    
	connected = False
	# Stop motors when client disconnect
	printLog(str(time.time()) + ': Motors de-attached')
	move(1,90,0)
	move(3,100,0)
	move(4,100,0)
	clientsock.close()

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

if __name__=='__main__':
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
	    printLog(str(time.time()) + ': Server connected to Arduino on: ' + str(ser.portstr))
	    
	except Exception, error:
	    printLog(str(time.time()) + ': Error, connection with Arduino failed: ' + str(error))

	ADDR = (socketAddress, socketPort)
	serversock = socket(AF_INET, SOCK_STREAM)
	serversock.bind(ADDR)
	serversock.listen(2)

	# Run server and listen for connections
	while True:
		print 'Server started!\nWaiting for connections...'
		clientsock, addr = serversock.accept()
		printLog(str(time.time()) + ': Client connected from: ' + str(addr))		
		print 'Client connected from: ', addr
		thread.start_new_thread(handler, (clientsock, addr))


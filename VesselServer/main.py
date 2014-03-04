#
#    VesselServer
#    	Created 2013-06-29
#     Rasmus Jansson and Joar Svensson
#     Version 0.2
#	 		https://github.com/JoarSvensson/VesselControl.git
#       

import SocketServer, os, time, threading, thread, logging
from serial import Serial
from socket import *

''' This function handles connections '''
def handler(clientsock,addr):	
	connected = True

	while(connected):
		data = clientsock.recv(3)
		if(data == ""):
			print 'Client disconnected from ' + str(addr)
			logging.info('Client disconnected from '+ str(addr))
			break
			
		if(len(data) == 3):
			number = ord(data[0])
			value = ord(data[1])
			direction = ord(data[2])
			if(number > 0 and number < 7):
				move(number, value, direction)
			
	connected = False
	# Stop motors when client disconnect
	logging.info('Motors de-attached and stopped')
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
	logging.info('Moving ' + str(number) + ' to ' + str(value))


''' Run server and listen for incoming client connections'''
if __name__=='__main__':
	# Initiate logging
	logging.basicConfig(format='%(asctime)s %(message)s',filename='VesselServer.log',level=logging.DEBUG)
	
	# Settings variables
	socketAddress = '0.0.0.0'
	socketPort = 10000
	port = '/dev/ttyACM0'
	baudrate = 9600
	connected = False

	# Initiate serial connections
	try:
		ser = Serial(port, baudrate, timeout=1)
		logging.info('Server connected to Arduino on: ' + str(ser.portstr))
	    
	except Exception, error:
		logging.warning('Connection with Arduino failed: ' + str(error))

	ADDR = (socketAddress, socketPort)
	serversock = socket(AF_INET, SOCK_STREAM)
	serversock.bind(ADDR)
	serversock.listen(2)
	
	print 'Server started on port '+ str(socketPort) +', waiting for connections...'
	logging.info('Server started on port '+ str(socketPort) +', waiting for connections...')

	# Run server and listen for connections
	while True:
		clientsock, addr = serversock.accept()		
		print 'Client connected from: ', addr
		logging.info('Client connected from: ' + str(addr))
		thread.start_new_thread(handler, (clientsock, addr))


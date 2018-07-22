#!/usr/bin/
#This code was written by Caleb G. Teague in 2017

import socket
import time

HOST = "localhost"
PORT = 8080

def main():
	
	 
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	connected = False
	while not connected:
		try:
			sock.connect((HOST, PORT))
			connected = True
		except:
			connected = False
			print "No connection availible"
			time.sleep(0.1)
	i = 0
	y = 3
	while (i < 100):
		y = i+50
		sock.sendall(str(i) + "," + str(y) + "\n")
		print "Sent" + str(i) + "," + str(y) + "\n"
		data = sock.recv(1024)
		print str(i) + ")", data
		i = i + 1

	sock.close()

				
if __name__ == "__main__":
		print "Socket is main"
		main()



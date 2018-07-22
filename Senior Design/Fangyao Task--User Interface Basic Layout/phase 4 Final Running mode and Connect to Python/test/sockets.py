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
	 
	sock.sendall("Hello\n")
	data = sock.recv(1024)
	print "1)", data
	 
	if ( data == "olleH\n" ):
		sock.sendall("Bye\n")
		data = sock.recv(1024)
		print "2)", data
	 
		if (data == "eyB}\n"):
			sock.close()
			print "Socket closed"
                
if __name__ == "__main__":
        print "Socket is main"
        main()



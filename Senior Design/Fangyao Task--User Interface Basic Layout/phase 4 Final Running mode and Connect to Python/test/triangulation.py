#!/usr/bin/
#This code was written by Caleb G. Teague in 2017

"""To do:
	Need to factor filtered value from gyro/mag into the angle calculation.
	Need to get and process info from FM receiver.
	Need to output myPos to user.
"""	

import numpy as np
import math
import time

from MinIMU_v5_pi import MinIMU_v5_pi
from encoder import encoder

import RFM69
from RFM69registers import RF69_915MHZ
import RPi.GPIO as GPIO

transponders = {0x00:[15, 5], 0x01:[5, 5], 0x02:[10, -5]} #Dictionary with keys, you access each item by the key instead of the index.
inRange = {} #Holds the transponders which are in range and their a and b values
myPos = [0,0]
lines = [] #List version of inRange
keepTime = 1

"""Adds the a and b values of the new transponder to inRange and calls findPos()."""
def addTransponder(key, angle):
	angle = normalizeAngle(angle)
	a = math.tan(angle)
	b = transponders[key][1] - a*transponders[key][0] #y_value - a*x_value
	inRange[key] = [a, b, time.time()]
	
	keys = inRange.keys()
	i=0
	#Removes a transponder if it hasn't been pinged in longer than keepTime
	#and makes sure we can still return a position (have two transponders).
	while i < len(keys) and len(inRange) > 2:  
		if inRange[keys[i]][2] + keepTime < time.time():
			del inRange[keys[i]]
		i += 1
	del lines[:] #Clears the list
	for value in inRange.itervalues(): #Updates the global list variable from inRange
		lines.append(value)

"""Takes in an angle in degrees and returns one from 0 to pi radians"""
def normalizeAngle(angle):
	angle = angle % 180 # % always returns a positive number
	return math.radians(angle)
		

"""Finds the intersection for each pair of lines (if they exist)
and updates myPos."""
def findPos():
	i = 0
	intersections = [] #contains 1x2 matrices of (x,y) intersects	
	while (i < len(lines) - 1):
		j = i + 1
		while (j < len(lines)):
			#lines[i][0] is a, and lines[i][1] is b
			if (lines[i][0] != lines[j][0]): #Making sure they aren't parralel
				A = np.matrix([[lines[i][0], -1], [lines[j][0], -1]])
				B = np.matrix([[-1*lines[i][1]], [-1*lines[j][1]]])
				X = A.getI()*B
				intersections.append(X.transpose().tolist()[0]) #X.transpose().tolist()[0] just returns the x,y values in a list [x,y].
			j += 1
		i += 1
#This is just averaging the intersections found, another method may be better but this works for now.
	if(len(intersections) > 0):
		x_sum = 0
		y_sum = 0
		for point in intersections:
			x_sum += point[0]
			y_sum += point[1]
		myPos[0] = x_sum / len(intersections)
		myPos[1] = y_sum / len(intersections)


def main():
	#Setup for motor
	motor = encoder(23, 24)

	#Setup for MinIMU_v5_pi
	IMU = MinIMU_v5_pi()
	IMU.trackYaw()

	#Setup for radio
	radio = RFM69.RFM69(RF69_915MHZ, 1, 1, True)
	radio.rcCalibration()
	radio.setHighPower(True)

	while True: #Main loop             
		while not radio.receiveDone():
			time.sleep(0.03)
				
		if radio.ACKRequested():
			radio.sendACK()                               

		transponderID = int("".join([chr(letter) for letter in radio.DATA]))
		angle = motor.getAngle() + IMU.prevYaw[0]
		addTransponder(transponderID, angle)
		findPos()
		print myPos
			
	print "shutting down"
	radio.shutdown()


	#Speed test and constant error test
	addTransponder(0x00, 45)
	addTransponder(0x01, 135)
	addTransponder(0x02, 270)
	"""
	addTransponder(0x00, 65)
	addTransponder(0x01, 155)
	addTransponder(0x02, 290)
	"""

	t0 = time.time()
	for x in range(1000): findPos()
	t1 = time.time()
	print t1 - t0

if __name__ == "__main__":
	main()



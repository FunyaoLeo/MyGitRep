#!/usr/bin/
#This code was written by Caleb G. Teague in 2017

"""To do:

"""

import RPi.GPIO as GPIO
import time

"""Takes the two encoder pins (order doesn't matter) and configures them for input.
Assumes BCM pin numbers are used."""
class encoder():
	
	def __init__(self, pin1, pin2):
		self.count = [0]
		self.pin1 = pin1
		self.pin2 = pin2
		self.setup()

	"""Setup two pins for encoder input."""
	def setup(self):
		GPIO.setmode(GPIO.BOARD) #Use the BCM numbering sytem for the pi
		GPIO.setup([self.pin1, self.pin2], GPIO.IN) #Setup pins for input
		GPIO.add_event_detect(self.pin1, GPIO.BOTH, callback=self.interupt) #Add rising and falling edge detection on pin1
		GPIO.add_event_detect(self.pin2, GPIO.BOTH, callback=self.interupt) #Add rising and falling edge detection on pin2

	"""Keeps track of the number of 'ticks' the encoder has had."""
	def interupt(self, channel):
		self.count[0] = (self.count[0] + 1) % 3200 #50 * 16 * 2 * 2 edges per revolution

	"""Returns the current angle of the encoder relative to the starting position."""
	def getAngle(self):
		return self.count[0] / 3200.0 * 360
		
	"""Free used pins on object destruction"""
	def __del__(self):
		GPIO.cleanup([self.pin1, self.pin2])

	


def main():
	try:
		motor = encoder(16, 18)
		while True:
			time.sleep(0.001)
			print motor.getAngle()
	except:
		GPIO.cleanup()


			
if __name__ == "__main__":
	main()
	print "Encoder is main"

#!/usr/bin/
#This code was written by Caleb G. Teague in 2017

"""To do:
	Comments!!!
	Turn into easy to use module
	Cleaning
"""

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup([23, 24], GPIO.IN)

global pos

count = [0]

def aRise(channel):
    count[0] = count[0] + 1
    #print 'rise'

def aFall(channel):
    pos +=1

"""
def bRise(channel):
    #pos +=1
    print 'riseB'

def bFall(channel):
    pos +=1
"""



GPIO.add_event_detect(23, GPIO.BOTH, callback=aRise)  # add rising edge detection on a channel
#GPIO.add_event_detect(23, GPIO.FALLING, callback=aFall)  # add falling edge detection on a channel
#GPIO.add_event_detect(24, GPIO.RISING, callback=bRise)  # add rising edge detection on a channel
#GPIO.add_event_detect(24, GPIO.FALLING, callback=bFall)  # add falling edge detection on a channel




try:
    while True:
        time.sleep(0.01)
        count[0] = count[0] % 1600 #50 * 16 * 2 edges per revolution
        print count[0] / 1600.0 * 360
    GPIO.cleanup()
except:
    GPIO.cleanup()

#!/usr/bin/
#This code was written by Caleb G. Teague in 2017

"""To do:
	
"""	

import RFM69
from RFM69registers import *
import RPi.GPIO as GPIO
import datetime
import time


def exampleRFM69():
        radio = RFM69.RFM69(RF69_915MHZ, 2, 1, True)
        print "class initialized"
        print "Performing rcCalibration"
        radio.rcCalibration()
        print "setting high power"
        radio.setHighPower(True)
        print "reading"
        while True:
                while not radio.receiveDone():
                        time.sleep(0.03)
                #if radio.receiveDone():
                t0 = time.time()
                if radio.ACKRequested():
                        radio.sendACK()
                        t1 = time.time()
                        print "Ack sent in " + str(t1 - t0) + " seconds."                               

                message = "".join([chr(letter) for letter in radio.DATA])
                print message + " received from node " + str(radio.SENDERID) + " RSSI: " + str(radio.RSSI)
                print ""
                """if radio.RSSI == 0:
                        print "Performing rcCalibration"
                        radio.rcCalibration()
                        print "setting high power"
                        radio.setHighPower(True)"""
                #print "".join([chr(letter) for letter in radio.DATA])
                                             
                                        
        print "shutting down"
        radio.shutdown()


def main():
        #print "spi_test is main"
        try:
                exampleRFM69()
        except KeyboardInterrupt:
                GPIO.cleanup()


if __name__ == "__main__":
	main()

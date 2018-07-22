#!/usr/bin/
#This code was written by Caleb G. Teague in 2017

"""To do:
	
"""	


import RFM69
from RFM69registers import *
import RPi.GPIO as GPIO
import time


def exampleRFM69():
        radio = RFM69.RFM69(RF69_915MHZ, 1, 1, True)
        print "class initialized"
        #print "reading all registers"
        #results = radio.readAllRegs()
        #for result in results:
        #        print result
        print "Performing rcCalibration"
        radio.rcCalibration()
        print "setting high power"
        radio.setHighPower(True)
        #print "Checking temperature"
        #print radio.readTemperature(0)
        #print "setting encryption"
        #radio.encrypt("12345678" + "91011121")
        i=0
        while True:                
                print "Sending text to node 2, try " + str(i)
                message = "Try " + str(i) + "."
                if radio.sendWithRetry(2, message, 1, 100): #Node, message, #tries (not retries), retry wait time
                        print "Got ack, rssi: " + str(radio.RSSI)
                time.sleep(2)
                i +=1
        
        print "shutting down" #put radio in RX mode
        radio.shutdown()


def main():
        try:
                exampleRFM69()
        except KeyboardInterrupt:
                GPIO.cleanup()

if __name__ == "__main__":
	main()

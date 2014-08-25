#!/usr/bin/env python

#import time
#import sys

#card = ['0007181175']

#def main():
#    with open('/dev/tty1', 'r') as tty:
#        while True:
#            RFID_input = tty.readline().rstrip()
            
#            if RFID_input in card:
#                print "Access Granted: {0}".format(RFID_input)
#            else:
#                print "Access Denied: {0}".format(RFID_input)
            
#main()

#! /usr/bin/python
import serial
import time

ser = serial.Serial('/dev/tty1', 2400, timeout=1) 

while True:
    try:
        response = ser.readline).rstrip()
    except:
        print "Erro"
        response = ""
    
    if response <> "":
        print str(response)

ser.close()

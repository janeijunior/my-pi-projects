#import serial
#serial = serial.Serial("/dev/ttyUSB0", baudrate=9600)
#
#code = ''

#while True:
#        data = serial.read()
#        if data == '\r':
#                print(code)
#                code = ''
#        else:
#                code = code + data

import time
import sys

card = '0019171125'

def main():
    with open('/dev/tty0', 'r') as tty:
        while True:
            RFID_input = tty.readline()
            if RFID_input == card:
                print "Access Granted" 
                print "Read code from RFID reader:{0}".format(RFID_input)
            else:
                print "Access Denied"
                
main()
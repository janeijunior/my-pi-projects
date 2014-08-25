#!/usr/bin/env python

import time
import sys

card = ['0007181175']

def main():
    while True:
        with open('/dev/tty0', 'r') as tty:
            RFID_input = tty.readline().rstrip()
            
            if RFID_input in card:
                print "Access Granted: {0}".format(RFID_input)
            else:
                print "Access Denied: {0}".format(RFID_input)
                        
main()
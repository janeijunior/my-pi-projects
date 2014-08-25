#!/usr/bin/env python

import time
import sys

card = '0007181175'

def main():
    with open('/dev/tty0', 'r') as tty:
        while True:
            RFID_input = tty.readline()
            
            if RFID_input == card:
                print "Access Granted: {0}".format(RFID_input)
            else:
                print "Access Denied: {0}".format(RFID_input)
main()
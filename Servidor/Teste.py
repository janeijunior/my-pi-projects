#!/usr/bin/env python

import time
import sys

card = ['0007181175']

def main():
    while True:
        sys.stdin = open('/dev/tty0', 'r')
        
        RFID_input = str(input())
        
        if RFID_input == card:
            print "Access Granted"
            print "Read code from RFID reader:{0}".format(RFID_input)
        else:
            print "Access Denied"
            tty.close()
            
main()
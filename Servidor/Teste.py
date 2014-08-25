#!/usr/bin/env python

import sys
import thread
import threading
import RFID

def main():
    RFID = RFID.RFID(None)
    RFID.start() 

main()


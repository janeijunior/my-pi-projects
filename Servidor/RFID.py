#!/usr/bin/python
#-*- coding: utf-8 -*-

import thread
import threading
import time
import sys

card1 = '0007181175'
card2 = '0008056554'

class RFID(threading.Thread):
    def __init__(self, alarme):
        threading.Thread.__init__(self)
        self.name = 'ThreadRFID'
        self.__stop_thread_event = threading.Event()
        
        #atributos
        self.alarme = alarme
                
    def stop(self):
        self.__stop_thread_event.set()
        
    def run(self):
        with open('/dev/tty4', 'r') as tty:
            while True:
                RFID_input = tty.readline()
                if (RFID_input == card1) :
                    print "Access Granted" 
                    print "Read code from RFID reader:{0}".format(RFID_input)
                else:
                    print "Access Denied"

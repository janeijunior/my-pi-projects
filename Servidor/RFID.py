#!/usr/bin/python
#-*- coding: utf-8 -*-

import thread
import threading
import time
import sys
import serial

card = ['0007181175', '0008056554']

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
        self.lerRFID()
    
    def ler(self):
        
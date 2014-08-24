#!/usr/bin/python
#-*- coding: utf-8 -*-

#import thread
#import threading
#import time
#import sys
#import serial
#
#card1 = '0007181175'
#card2 = '0008056554'
#
#class RFID(threading.Thread):
#    def __init__(self, alarme):
#        threading.Thread.__init__(self)
#        self.name = 'ThreadRFID'
#        self.__stop_thread_event = threading.Event()
#        
#        #atributos
#        self.alarme = alarme
#                
#    def stop(self):
#        self.__stop_thread_event.set()
#        
#    def run(self):
#        while True:
#            dados = raw_input()
#            
#            if dados <> '':
#                print dados
#                
#                if (dados == card1) or (dados == card2):
#                    print "Acesso Permitido."
#                    
#                    if self.alarme.alarmeLigado:
#                        self.alarme.ligarAlarme()
#                    else:
#                        self.alarme.desligarAlarme()
#                else:
#                    print "Acesso Negado."
#                
#                time.sleep(1.5)

#import serial

#serial = serial.Serial("/dev/tty0", baudrate=2400)

#code = ''

#while True:
#        print 'lendo...'

#        data = serial.read()
                
#        if data == '\r':
#                print(code)
#                code = ''
#        else:
#                code = code + data

import serial
import time
 
ser = serial.Serial('/dev/tty0', 2400, timeout=1) # replace '/dev/ttyUSB0' with your port
 
while True:
    response = ser.read(12)
    if response <> "":
        print "raw: " + str(response)
        print "hex: " + str(response[-8:])
        print "dec: " + str(int(response[-8:], 16))
    time.sleep(1)
 
ser.close()

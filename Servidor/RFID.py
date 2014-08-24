#!/usr/bin/python
#-*- coding: utf-8 -*-

import thread
import threading
import time
import serial

card = ['007181175', '008056554']

class RFID(threading.Thread):
    def __init__(self, alarme):
        threading.Thread.__init__(self)
        self.name = 'ThreadRFID'
        self.__stop_thread_event = threading.Event()
        
        #atributos
        self.alarme = alarme
        self.serial = serial.Serial('/dev/tty0', 2400, timeout=1)
                
    def stop(self):
        self.serial.close()
        self.__stop_thread_event.set()
        
    def run(self):
        while True:
            resposta = self.serial.read(12)
            
            if resposta <> '':
                print resposta
                
                if resposta in card:
                    print "Acesso Permitido."
                    
                    if self.alarme.alarmeLigado:
                        self.alarme.ligarAlarme()
                    else:
                        self.alarme.desligarAlarme()
                else:
                    print "Acesso Negado."
                
            time.sleep(1)

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
        while True:
            dados = raw_input()
            
            if dados <> '':
                print dados
                
                if (dados == card1) or (dados == card2):
                    print "Acesso Permitido."
                    
                    if self.alarme.alarmeLigado:
                        self.alarme.ligarAlarme()
                    else:
                        self.alarme.desligarAlarme()
                else:
                    print "Acesso Negado."
                
                time.sleep(1.5)

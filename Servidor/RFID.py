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
        serial = serial.Serial("/dev/tty0", baudrate=9600)
        
        while True:
                try:
                    resposta = serial.read()
                    resposta = resposta.strip()
                except:
                    print 'Erro na leitura.'
                    resposta = ''
                
                if resposta <> '':
                    print resposta
                    
                    if resposta in card:
                        print "Acesso Permitido."
                        
                        if self.alarme.alarmeLigado:
                            self.alarme.desligarAlarme()
                        else:
                            self.alarme.ligarAlarme()
                    else:
                        print "Acesso Negado."
                
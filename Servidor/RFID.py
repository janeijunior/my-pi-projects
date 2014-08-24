#!/usr/bin/python
#-*- coding: utf-8 -*-

import thread
import threading
import time
import sys

card = ['0007181175', '0008056554']

class RFID(threading.Thread):
    def __init__(self, alarme):
        threading.Thread.__init__(self)
        self.name = 'ThreadRFID'
        self.__stop_thread_event = threading.Event()
        
        #atributos
        self.alarme = alarme
                
    def stop(self):
        self.serial.close()
        self.__stop_thread_event.set()
        
    def run(self):
        with open('/dev/tty0', 'r') as tty:
            while True:
                try:
                    resposta = tty.readline()
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
                    
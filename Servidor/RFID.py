#!/usr/bin/python
#-*- coding: utf-8 -*-

import thread
import threading
import sys

class RFID(threading.Thread):
    def __init__(self, alarme, tag):
        threading.Thread.__init__(self)
        self.name = 'ThreadRFID'
        self.__stop_thread_event = threading.Event()
        
        #atributos
        self.alarme = alarme
        self.tag = tag
                
    def stop(self):
        self.__stop_thread_event.set()
        
    def run(self):
        self.lerDadosTeclado()
        #self.lerDadosTTY()
    
    def lerDadosTeclado(self):
        while not self.__stop_thread_event.isSet():
            RFID_input = raw_input('RFID:')
                    
            if RFID_input in self.tag:
                print "Acesso Permitido: {0}".format(RFID_input)
                    
                if self.alarme.alarmeLigado:
                    self.alarme.desligarAlarme()
                else:
                    self.alarme.ligarAlarme()
            else:
                print "Acesso Negado: {0}".format(RFID_input)
                        
    def lerDadosTTY(self):
        while not self.__stop_thread_event.isSet():
            try:
                with open('/dev/tty1', 'r') as tty:
                    RFID_input = tty.readline().rstrip()
                    
                    if RFID_input in self.tag:
                        print "Acesso Permitido: {0}".format(RFID_input)
                        
                        if self.alarme.alarmeLigado:
                            self.alarme.desligarAlarme()
                        else:
                            self.alarme.ligarAlarme()
                    else:
                        print "Acesso Negado: {0}".format(RFID_input)
                    
                    tty.close()
            except:
                print "Erro ao abrir o arquivo."
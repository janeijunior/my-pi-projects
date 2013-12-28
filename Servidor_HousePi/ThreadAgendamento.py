#!/usr/bin/python

import thread
import threading
import time
import MySQLdb
import Funcoes

ATIVO = 1
DESATIVADO = 0

class ThreadAgendamento(threading.Thread):
    def __init__(self, sirene):
        threading.Thread.__init__(self)
        self.name = 'ThreadAgendamento'
        self.__stop_thread_event = threading.Event()
        
                
    def stop(self):
        self.__stop_thread_event.set()
        
        
    def run(self):
        
        #executa enquanto nao setar o evento
        while not self.__stop_thread_event.isSet(): 
                        
            time.sleep(0.05)

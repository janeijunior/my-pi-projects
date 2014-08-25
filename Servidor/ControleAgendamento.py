#!/usr/bin/python
#-*- coding: utf-8 -*-

from datetime import date, datetime
import thread
import threading
import time

ATIVO = 1
DESATIVADO = 0

class ControleAgendamento(threading.Thread):
    def __init__(self, agendamentos):
        threading.Thread.__init__(self)
        self.name = 'ThreadAgendamento'
        self.__stop_thread_event = threading.Event()
        
        #atributos
        self.listaAgendamento = agendamentos
                
    def stop(self):
        self.__stop_thread_event.set()
        
    def run(self):
        
        
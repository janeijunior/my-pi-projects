#!/usr/bin/python

import thread
import threading
import time
import MySQLdb
import Funcoes
import datetime
from dateutil import parser

ATIVO = 1
DESATIVADO = 0

class ThreadAgendamento(threading.Thread):
    def __init__(self, listaAgendamento):
        threading.Thread.__init__(self)
        self.name = 'ThreadAgendamento'
        self.__stop_thread_event = threading.Event()
        
        #atributos
        self.listaAgendamento = listaAgendamento
                
    def stop(self):
        self.__stop_thread_event.set()
        
        
    def run(self):
        
        #executa enquanto nao setar o evento
        while not self.__stop_thread_event.isSet(): 
            
            #data e hora atual
            atual = datetime.now().toordinal()
            
            for agendamento in self.listaAgendamento
                
                #data e hora para ligar
                dtLigar = parser.parse(agendamento.dataHoraInicial)
                ligar = dtLigar.toordinal()
                
                #data e hora para desligar
                dtDesligar = parser.parse(agendamento.dataHoraFinal)
                desligar = dtDesligar.toordinal()
                
                if (atual = ligar) and (atual < desligar):
                    if agendamento.alarme == None:
                        agendamento.rele.ligar()    
                    else
                        agendamento.rele.desligar()
                elif (atual = desligar) and (atual > ligar):
                    
                        
            time.sleep(0.05)

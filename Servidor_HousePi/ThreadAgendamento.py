#!/usr/bin/python

from datetime import date, datetime
import thread
import threading
import time
import MySQLdb
import Funcoes

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
            atual = date.today().toordinal()
            
            for agendamento in self.listaAgendamento:
                #data e hora para ligar
                dtLigar = datetime.strptime(str(agendamento.dataHoraInicial), '%Y-%m-%d %H:%M:%S')
                ligar = dtLigar.toordinal()
                
                #data e hora para desligar
                dtDesligar = datetime.strptime(str(agendamento.dataHoraFinal), '%Y-%m-%d %H:%M:%S')
                desligar = dtDesligar.toordinal()
                
                print "Data atual: ", str(atual)
                print "Data ligar: ", str(ligar)
                print "Data desligar: ", str(desligar)
                
                if (atual == ligar) and (atual < desligar):
                    if agendamento.alarme == None:
                        agendamento.rele.ligar()    
                    else:
                        agendamento.alarme.ligarAlarme()
                elif (atual == desligar) and (atual > ligar):
                    if agendamento.alarme == None:
                        agendamento.rele.desligar()    
                    else:
                        agendamento.alarme.desligarAlarme()
                                        
            time.sleep(0.2)

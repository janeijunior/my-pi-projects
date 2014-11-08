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
        #executa enquanto nao setar o evento
        while not self.__stop_thread_event.isSet(): 
            #data e hora atual
            atual     = datetime.now().strftime("%Y%m%d%H%M%S")
            diaAtual  = datetime.now().strftime("%Y%m%d") 
            horaAtual = datetime.now().strftime("%H%M%S")
            dthoje    = datetime.today()
            hoje      = dthoje.strftime("%w")
            
            for agendamento in self.listaAgendamento:
                if agendamento.ativo == 1:
                    #data e hora para ligar
                    dtLigar   = datetime.strptime(str(agendamento.dataHoraInicial), "%Y-%m-%d %H:%M:%S")
                    ligar     = dtLigar.strftime("%Y%m%d%H%M%S")
                    diaLigar  = dtLigar.strftime("%Y%m%d")
                    horaLigar = dtLigar.strftime("%H%M%S")
                    
                    #data e hora para desligar
                    dtDesligar   = datetime.strptime(str(agendamento.dataHoraFinal), "%Y-%m-%d %H:%M:%S")
                    desligar     = dtDesligar.strftime("%Y%m%d%H%M%S")
                    diaDesligar  = dtDesligar.strftime("%Y%m%d")
                    horaDesligar = dtDesligar.strftime("%H%M%S")
                    
                    #print "Data atual: ", str(atual)
                    #print "Data ligar: ", str(ligar)
                    #print "Data desligar: ", str(desligar)
                    
                    if len(agendamento.listaDias) > 0:
                        if (diaAtual >= diaLigar) and (diaAtual <= diaDesligar):
                            for dia in agendamento.listaDias:
                                if dia == hoje:
                                    if (horaAtual == horaLigar) and (horaAtual < horaDesligar):
                                        for rele in agendamento.reles:                        
                                            if rele.status == 0:
                                                rele.ligar()    
                                        
                                        if (agendamento.alarme <> None) and (agendamento.alarme.alarmeLigado == False):
                                            agendamento.alarme.ligarAlarme()
               
                                    elif (horaAtual == horaDesligar) and (horaAtual > horaLigar):
                                        for rele in agendamento.reles:                        
                                            if rele.status == 1:
                                                rele.desligar()
                                                rele.atualizarStatusBanco()
                                    
                                        if (agendamento.alarme <> None) and (agendamento.alarme.alarmeLigado == True):
                                            agendamento.alarme.desligarAlarme()    
                        
                        if (diaAtual > diaDesligar) or ((diaAtual >= diaDesligar) and (horaAtual > horaDesligar)):
                            agendamento.desativarRegistroBanco()
                        
                    else:
                        if (atual == ligar) and (atual < desligar):
                            for rele in agendamento.reles:                        
                                if rele.status == 0:
                                    rele.ligar()    
                            
                            if (agendamento.alarme <> None) and (agendamento.alarme.alarmeLigado == False):
                                agendamento.alarme.ligarAlarme()
                        
                        elif (atual == desligar) and (atual > ligar):
                            for rele in agendamento.reles:                        
                                if rele.status == 1:
                                    rele.desligar()
                                    rele.atualizarStatusBanco()
                        
                            if (agendamento.alarme <> None) and (agendamento.alarme.alarmeLigado == True):
                                agendamento.alarme.desligarAlarme()
                                
                            agendamento.desativarRegistroBanco()
                    
            time.sleep(0.15) 
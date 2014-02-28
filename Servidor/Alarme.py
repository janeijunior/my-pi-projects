#!/usr/bin/python
#-*- coding: utf-8 -*-

import ThreadAlarme
import Funcoes

class Alarme(object):
    
    #construtor
    def __init__(self, sirene):
        
        #atributos publicos da classe
        self.alarmeLigado = False
        self.panicoAlarmeLigado = False    
        self.sirene = sirene
        
        #pega os status do banco e se necessario liga o alarme/panico
        row = Funcoes.consultarRegistro("select StatusAlarme, StatusPanico from ConfiguracaoAlarme")
        
        if row['StatusAlarme'] == 1:
            self.ligarAlarme()
        
        if row['StatusPanico'] == 1:
            self.ligarPanicoAlarme()     
        
    #funcoes
    #funcao para ligar o alarme
    def ligarAlarme(self):
        self.threadAlarme = ThreadAlarme.ThreadAlarme(sirene=self.sirene)
        self.threadAlarme.start() 
        self.alarmeLigado = True
        self.atualizarStatusBanco()
        
    #funcao para desligar o alarme
    def desligarAlarme(self):
        self.threadAlarme.stop()
        self.alarmeLigado = False
        self.atualizarStatusBanco()
    
    #funcao para ler o status do alarme
    def getStatusAlarme(self):
        try:
            return self.threadAlarme.status
        except:
            return -1
        
    #funcao para ligar o panico do alarme
    def ligarPanicoAlarme(self):
        self.sirene.ligar()
        self.panicoAlarmeLigado = True
        self.atualizarStatusBanco()
        
    #funcao para desligar o panico do alarme
    def desligarPanicoAlarme(self):
        if self.getStatusAlarme() <> 1:
            self.sirene.desligar()
        
        self.panicoAlarmeLigado = False
        self.atualizarStatusBanco()
    
    #funcao para atualizar os status no banco
    def atualizarStatusBanco(self):
       sql = "update Configuracao set StatusAlarme = {statusAlarme}, StatusPanico = {statusPanico}"
       sql = sql.format(statusAlarme = int(self.alarmeLigado), statusPanico = int(self.panicoAlarmeLigado))
       
       return Funcoes.executarComando(sql)
       
    #destrutor
    def __done__(self):
        self.desligarPanicoAlarme()
        self.desligarAlarme()
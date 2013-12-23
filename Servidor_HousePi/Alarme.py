#!/usr/bin/python

import ThreadAlarme

class Alarme(object):
    
    #construtor
    def __init__(self, sirene, conBanco):
        
        #atributos publicos da classe
        self.alarmeLigado = False
        self.panicoAlarmeLigado = False    
        self.sirene = sirene
        self.conBanco = conBanco
        
    #funcoes
    #funcao para ligar o alarme
    def ligarAlarme(self):
        self.threadAlarme = ThreadAlarme.ThreadAlarme(conBanco=self.conBanco, sirene=self.sirene)
        self.threadAlarme.start() 
        self.alarmeLigado = True
        
    #funcao para desligar o alarme
    def desligarAlarme(self):
        self.threadAlarme.stop()
        self.alarmeLigado = False
    
    #funcao para ler o status do alarme
    def getStatusAlarme(self):
        try:
            return self.threadAlarme.status
        except:
            return 0
            print "Erro ao ler status"
        
    #funcao para ligar o panico do alarme
    def ligarPanicoAlarme(self):
        self.sirene.ligar()
        self.panicoAlarmeLigado = True
        
    #funcao para desligar o panico do alarme
    def desligarPanicoAlarme(self):
        if self.getStatusAlarme() <> 1
            self.sirene.desligar()
        
        self.panicoAlarmeLigado = False
        
    #destrutor
    def __done__(self):
        self.desligarPanicoAlarme()
        self.desligarAlarme()
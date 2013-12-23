#!/usr/bin/python

import ThreadAlarme

class Alarme(object):
    
    #construtor
    def __init__(self, sirene):
        
        #atributos publicos da classe
        self.alarmeLigado = False
        self.panicoAlarmeLigado = False    
        self.sirene = sirene
        
    #funcoes
    #funcao para ligar o alarme
    def ligarAlarme(self):
        self.threadAlarme = ThreadAlarme.ThreadAlarme(self.sirene)
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
        self.panicoLigado = True
        
    #funcao para desligar o panico do alarme
    def desligarPanicoAlarme(self):
        self.sirene.desligar()
        self.panicoLigado = False
        
    #destrutor
    def __done__(self):
        self.desligarPanicoAlarme()
        self.desligarAlarme()
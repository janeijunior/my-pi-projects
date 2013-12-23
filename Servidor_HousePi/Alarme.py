#!/usr/bin/python

import ThreadAlarme

NORMAL = 0
DISPARADO = 1

class Alarme(object):
    
    #construtor
    def __init__(self, sirene):
        
        #atributos publicos da classe
        self.status = 
        self.alarmeLigado = False
        self.panicoLigado = False    
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
        
    #funcao para ligar o panico do alarme
    def ligarPanicoAlarme(self):
        self.panicoLigado = True
        self.sirene.ligar()
        
    #funcao para desligar o panico do alarme
    def desligarPanicoAlarme(self):
        self.panicoLigado = False
    
    #destrutor
    def __done__(self):
        self.desligarPanicoAlarme()
        self.desligarAlarme()
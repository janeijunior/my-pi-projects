#!/usr/bin/python

import ThreadAlarme

SIRENE = 10
NORMAL = 0
DISPARADO = 1

class Alarme(object):
    
    #construtor
    def __init__(self):
        
        #atributos publicos da classe
        self.status = 
        self.alarmeLigado = False
        self.panicoLigado = False
        self.threadAlarme = ThreadAlarme.ThreadAlarme(sirene = listaReles[SIRENE]) 
            
    #funcoes
    #funcao para ligar o alarme
    def ligarAlarme(self):
        self.alarmeLigado = True
        self.threadAlarme = ThreadAlarme.ThreadAlarme(sirene = listaReles[SIRENE])
        self.threadAlarme.start() 
    else:
        threadAlarme.stop()
        print "Alarme desativado."
    
        
    #funcao para desligar o alarme
    def desligarAlarme(self):
        self.alarmeLigado = False
        
    #funcao para ligar o panico do alarme
    def ligarPanicoAlarme(self):
        self.panicoLigado = True
        
    #funcao para desligar o panico do alarme
    def desligarPanicoAlarme(self):
        self.panicoLigado = False
    
    #destrutor
    def __done__(self):
        self.desligarPanicoAlarme()
        self.desligarAlarme()
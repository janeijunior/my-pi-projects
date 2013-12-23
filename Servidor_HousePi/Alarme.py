#!/usr/bin/python

class Rele(object):
    
    #construtor
    def __init__(self, id, numeroGPIO, status, nome):
        
        #atributos publicos da classe
        self.status = 
        self.alarmeLigado = False
        self.panicoLigado = False    
            
    #funcoes
    #funcao para ligar o alarme
    def ligarAlarme(self):
        self.alarmeLigado = True
        
    #funcao para desligar o alarme
    def desligarAlarme(self):
        self.alarmeLigado = True
        
    #funcao para ligar o panico do alarme
    def ligarPanicoAlarme(self):
        
    #funcao para desligar o panico do alarme
    def desligarPanicoAlarme(self):
    
    #destrutor
    def __done__(self):
        self.desligarPanicoAlarme()
        self.desligarAlarme()
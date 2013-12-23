#!/usr/bin/python

class Rele(object):
    
    #construtor
    def __init__(self, id, numeroGPIO, status, nome):
        
        #atributos publicos da classe
        self.status = 
        self.ligado = False
            
    #funcoes
    #funcao para ligar o alarme
    def ligarAlarme(self):
        mcp.config(self.numeroGPIO, mcp.OUTPUT)
    
    #funcao para ligar o rele
    def ligar(self):
        mcp.output(self.numeroGPIO, LIGAR)
        self.status = STATUS_LIGADO
    
    #funcao para desligar o rele
    def desligar(self):
        mcp.output(self.numeroGPIO, DESLIGAR)
        self.status = STATUS_DESLIGADO
    
    #destrutor
    #def __done__(self):
    #    self.desligar()
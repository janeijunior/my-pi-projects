#!/usr/bin/python

import Adafruit_MCP230xx

#Variavel para controle dos pinos GPIO (reles)
mcp = Adafruit_MCP230xx.Adafruit_MCP230XX(address=0x20, num_gpios=16)

class Rele(object):
    
    #construtor
    def __init__(self, numero, status, nome):
        self._numero = numero
        self._status = status
        self._nome = nome
        
        self.configurar()
        
    #propriedades
    def getNumero(self):
        return self._numero
        
    def getStatus(self):
        return self._status
    
    def getNome(self):
        return self._nome
    
    def setNumero(self, numero):
        self._numero = numero
    
    def setStatus(self, status):
        self._status = status
    
    def setNome(self, nome):
        self._nome = nome
    
    numero  = property(fget = getNumero, fset = setNumero)
    status  = property(fget = getStatus, fset = setStatus)
    nome    = property(fget = getNome, fset = setNome)
    
    #funcoes
    def configurar(self):
        mcp.config(self.getNumero, mcp.OUTPUT)
    
    def ligar(self):
        mcp.output(self.getNumero, 1)
        self.setStatus(1)
    
    def desligar(self):
        mcp.output(self.getNumero, 0)
        self.setStatus(0)
    
    #destrutor
    #def __done__(self):
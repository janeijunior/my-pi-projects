#!/usr/bin/python

import Adafruit_MCP230xx

#Variavel para controle dos pinos GPIO (reles)
mcp = Adafruit_MCP230xx.Adafruit_MCP230XX(address=0x20, num_gpios=16)

class Rele(object):
    
    #construtor
    def __init__(self, numero, status, nome):
        self.numero = numero
        self.status = status
        self.nome = nome
        self.configurar()
        
    #propriedades
    @property
    def getNumero(self):
        return self.numero
        
    @property
    def getStatus(self):
        return self.status
    
    @property
    def getNome(self):
        return self.nome
    
    @property
    def setNumero(self, numero):
        self.numero = numero
    
    @property
    def setStatus(self, status):
        self.status = status
    
    @property
    def setNome(self, nome):
        self.nome = nome
    
    #funcoes
    def configurar(self):
        mcp.config(self.numero, mcp.OUTPUT)
    
    def ligar(self):
        mcp.output(self.numero, 1)
        self.status = 1
    
    def desligar(self):
        mcp.output(self.numero, 0)
        self.status = 0
    
    #destrutor
    #def __done__(self):
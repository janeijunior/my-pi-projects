#!/usr/bin/python

import Adafruit_MCP230xx

#variavel para controle dos pinos GPIO (reles)
mcp = Adafruit_MCP230xx.Adafruit_MCP230XX(address=0x20, num_gpios=16)

class Rele(object):
    
    #construtor
    def __init__(self, numero, status, nome):
        
        #atributos publicos da classe
        self.numero = numero
        self.status = status
        self.nome   = nome
        
        self.configurar()
            
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
    def __done__(self):
        self.desligar()
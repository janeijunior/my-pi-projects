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
        mcp.config(self.numero, mcp.OUTPUT)
    
    def ligar(self):
        mcp.output(self.numero, 1)
        self.status = 1
    
    def desligar(self):
        mcp.output(self.numero, 0)
        self.status = 0
    
    #destrutor
    def __done__(self):
        self.desligar()
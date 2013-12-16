#!/usr/bin/python

import Adafruit_MCP230xx

#variavel para controle dos pinos GPIO (reles)
mcp = Adafruit_MCP230xx.Adafruit_MCP230XX(address=0x20, num_gpios=16)

#constantes
LIGAR    = 1
DESLIGAR = 0
STATUS_LIGADO = 1
STATUS_DESLIGADO = 0

class Rele(object):
    
    #construtor
    def __init__(self, id, numeroGPIO, status, nome):
        
        #atributos publicos da classe
        self.id         = id
        self.numeroGPIO = numeroGPIO
        self.status     = status
        self.nome       = nome
        
        self.configurar()
            
    #funcoes
    #funcao para configurar o rele para uso
    def configurar(self):
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
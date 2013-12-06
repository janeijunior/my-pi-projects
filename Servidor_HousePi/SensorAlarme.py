#!/usr/bin/python

import RPi.GPIO as GPIO 

class SensorAlarme(object):
    
    #construtor
    def __init__(self, numero, ativo, nome):
        self.numero = numero
        self.ativo = ativo
        self.nome = nome
        self.configurar()
            
    #propriedades
    @property
    def getNumero(self):
        return self.numero
    
    @property
    def getAtivo(self):
        return self.ativo
    
    @property
    def getNome(self):
        return self.nome
        
    @property
    def setNumero(self, numero):
        self.numero = numero

    @property
    def setAtivo(self, ativo):
        self.ativo = ativo 
    
    @property
    def setNome(self, nome):
        self.nome = nome
    
    #funcoes
    def configurar(self):
        GPIO.setmode(GPIO.BCM) 
        GPIO.setup(self.numero, GPIO.IN)
        
    def lerStatus(self):
        GPIO.input(numero)
    
    def verificaDisparo(self):
        if (self.ativo == 1) and (self.lerStatus == 1):
            return True
        else:
            return False
            
    #destrutor
    #def __done__(self):
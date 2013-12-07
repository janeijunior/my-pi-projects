#!/usr/bin/python

import RPi.GPIO as GPIO 

class SensorAlarme(object):
    
    #construtor
    def __init__(self, numero, ativo, nome):
        
        #atributos publicos da classe
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
        return GPIO.input(self.numero)
    
            
    #destrutor
    #def __done__(self):
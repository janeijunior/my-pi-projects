#!/usr/bin/python

import RPi.GPIO as GPIO 

class SensorAlarme(object):
    
    #construtor
    def __init__(self, numero, ativo, nome):
        
        #atributos publicos da classe
        self.numero = numero
        self.ativo  = ativo
        self.nome   = nome
        
        self.configurar()
            
    #funcoes
    def configurar(self):
        GPIO.setmode(GPIO.BCM) 
        GPIO.setup(self.numero, GPIO.IN)
        
    def lerStatus(self):
        return GPIO.input(self.numero)
    
            
    #destrutor
    #def __done__(self):
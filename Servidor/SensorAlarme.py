#!/usr/bin/python
#-*- coding: utf-8 -*-

import RPi.GPIO as GPIO 

class SensorAlarme(object):
    
    #construtor
    def __init__(self, id, numeroGPIO, ativo, nome):
        
        #atributos publicos da classe
        self.id         = id
        self.numeroGPIO = numeroGPIO
        self.ativo      = ativo
        self.nome       = nome
        
        self.configurar()
            
    #funcoes
    #funcao para configurar o sensor
    def configurar(self):
        GPIO.setmode(GPIO.BCM) 
        GPIO.setup(self.numeroGPIO, GPIO.IN)
    
    #funcao para ler o status do sensor (1 = normal e 0 = violado)
    def lerStatus(self):
        return GPIO.input(self.numeroGPIO)
    
    #destrutor
    #def __done__(self):
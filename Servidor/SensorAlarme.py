#!/usr/bin/python
#-*- coding: utf-8 -*-

import RPi.GPIO as GPIO 
import Base

class SensorAlarme(Base.Base):
    
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
        #GPIO.setmode(GPIO.BCM) 
        GPIO.setup(self.numeroGPIO, GPIO.IN)
    
    #funcao para ler o status do sensor (1 = normal e 0 = violado)
    def lerStatus(self):
        return GPIO.input(self.numeroGPIO)
    
    #funcao para gravar o novo nome do sensor e se esta ativo
    def gravarRegistroBanco(self):
        sql = "update SensorAlarme set Nome = '{nomeSensor}', Ativo = {ativo} where Id = {idSensor}"
        sql = sql.format(nomeSensor = self.nome, ativo = self.ativo, idSensor = self.id)
        
        return self.executarComando(sql)
    
    #destrutor
    #def __done__(self):
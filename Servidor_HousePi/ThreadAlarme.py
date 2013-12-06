#!/usr/bin/python

import thread
import threading
import time
import RPi.GPIO as GPIO 
import EnviaEmail
import Adafruit_MCP230xx

mcp = Adafruit_MCP230xx.Adafruit_MCP230XX(address=0x20, num_gpios=16)

class ThreadAlarme(threading.Thread):
    def __init__(self, threadID, name, counter, tempoDisparo):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.__stop_thread_event = threading.Event()
    def stop(self):
        mcp.output(10, 0)
        self.__stop_thread_event.set()
    def run(self):
        
        listaSensores = [];
        
        listaSensores.insert(0, SensorAlarme.SensorAlarme(numero = 17, ativo = 1, nome = "Casa 0")) #GPIO 0 
        listaSensores.insert(1, SensorAlarme.SensorAlarme(numero = 18, ativo = 0, nome = "Casa 1")) #GPIO 1
        listaSensores.insert(2, SensorAlarme.SensorAlarme(numero = 27, ativo = 0, nome = "Casa 2")) #GPIO 2
        listaSensores.insert(3, SensorAlarme.SensorAlarme(numero = 22, ativo = 0, nome = "Casa 3")) #GPIO 3
        listaSensores.insert(4, SensorAlarme.SensorAlarme(numero = 23, ativo = 0, nome = "Casa 4")) #GPIO 4
        listaSensores.insert(5, SensorAlarme.SensorAlarme(numero = 24, ativo = 0, nome = "Casa 5")) #GPIO 5
        listaSensores.insert(6, SensorAlarme.SensorAlarme(numero = 25, ativo = 0, nome = "Casa 6")) #GPIO 6
        listaSensores.insert(7, SensorAlarme.SensorAlarme(numero =  5, ativo = 0, nome = "Casa 7"))  #GPIO 7
                
        rele = Rele.Rele(numero = 10, status = 0, nome = 'Sirene')
        
        while not self.__stop_thread_event.isSet(): 

            for i in range(0, 7): 
                if listaSensores[i].verificaDisparo():
                    print("Sensor " + str(i) + "/" + listaSensores[i].numero + " violado!")
                    rele.ligar()
                    EnviaEmail.EnviarEmail()
                    time.sleep(5)
                    rele.desligar() 
                    
            time.sleep(0.05)

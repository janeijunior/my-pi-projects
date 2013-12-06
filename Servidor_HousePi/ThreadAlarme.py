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
        
        listaSensores.insert( , SensorAlarme.SensorAlarme(numero = 17, ativo = 1)) #GPIO 0 
        listaSensores.insert( , SensorAlarme.SensorAlarme(numero = 18, ativo = 0)) #GPIO 1
        listaSensores.insert( , SensorAlarme.SensorAlarme(numero = 27, ativo = 0)) #GPIO 2
        listaSensores.insert( , SensorAlarme.SensorAlarme(numero = 22, ativo = 0)) #GPIO 3
        listaSensores.insert( , SensorAlarme.SensorAlarme(numero = 23, ativo = 0)) #GPIO 4
        listaSensores.insert( , SensorAlarme.SensorAlarme(numero = 24, ativo = 0)) #GPIO 5
        listaSensores.insert( , SensorAlarme.SensorAlarme(numero = 25, ativo = 0)) #GPIO 6
        listaSensores.insert( , SensorAlarme.SensorAlarme(numero =  5, ativo = 0))  #GPIO 7
                
        
        while not self.__stop_thread_event.isSet(): 

            for i in range(0, 15): 
            
            if (input0 == 1): 
                print("sensor 0 Normal")
            else:
                print("Sendor 0 Violado!")
                #mcp.output(10, 1)
                #time.sleep(5) 
                #mcp.output(10, 0)
                EnviaEmail.EnviarEmail()
                
            if (input1 == 1): 
                print("sensor1") 
            if (input2 == 1): 
                print("sensor2") 
            if (input3 == 1): 
                print("sensor3") 
            if (input4 == 1):
                print("sensor4") 
            if (input5 == 1): 
                print("sensor5") 
            if (input6 == 1): 
                print("sensor6") 
            if (input7 == 1): 
                print("sensor7")
            
            time.sleep(0.05)

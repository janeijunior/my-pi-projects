#!/usr/bin/python
#-*- coding: utf-8 -*-

import time 
import Adafruit_MCP230xx #usado para os reles
import RPi.GPIO as GPIO  # usado para o alarme
 
OUTPUT = 0 
INPUT = 1 
 
if __name__ == '__main__': 
  
  #exemplo de uso dos reles
  
  mcp = Adafruit_MCP230xx.Adafruit_MCP230XX(address=0x20, num_gpios=16)
 
  # configura os pinos para uso
  mcp.config(0, OUTPUT) 
  mcp.config(1, OUTPUT) 
  mcp.config(2, OUTPUT) 
  mcp.config(3, OUTPUT) 
  mcp.config(4, OUTPUT) 
  mcp.config(5, OUTPUT) 
  mcp.config(6, OUTPUT) 
  mcp.config(7, OUTPUT) 
  mcp.config(8, OUTPUT) 
  mcp.config(9, OUTPUT) 
 
 
  #mcp.output(Pino, Status) 
  #liga os 10 reles
  mcp.output(0, 1)  
  mcp.output(1, 1) 
  mcp.output(2, 1) 
  mcp.output(3, 1)  
  mcp.output(4, 1)  
  mcp.output(5, 1) 
  mcp.output(6, 1) 
  mcp.output(7, 1) 
  mcp.output(8, 1) 
  mcp.output(9, 1) 
  
  # espera 10 segundos
  time.sleep(10) 
 
  #desliga os 10 reles
  mcp.output(0, 0)  
  mcp.output(1, 0)   
  mcp.output(2, 0) 
  mcp.output(3, 0) 
  mcp.output(4, 0)  
  mcp.output(5, 0) 
  mcp.output(6, 0) 
  mcp.output(7, 0) 
  mcp.output(8, 0) 
  mcp.output(9, 0) 
  
  #exemplo de uso do alarme
  
  GPIO.setmode(GPIO.BCM) 
  GPIO.setup(17,GPIO.IN) #GPIO0 
  GPIO.setup(18,GPIO.IN) #GPIO1 
  GPIO.setup(27,GPIO.IN) #GPIO2 
  GPIO.setup(22,GPIO.IN) #GPIO3 
  GPIO.setup(23,GPIO.IN) #gpio4 
  GPIO.setup(24,GPIO.IN) #GPIO5 
  GPIO.setup(25,GPIO.IN) #GPIO6 
  GPIO.setup(4,GPIO.IN)  #GPIO7 
  
  #obs: sensores de alarme nao conectados retorna como disparado
  #por isso implemente no exemplo a leitura apenas do q possuo conectado a placa...
  #retorno 1 = normal e 0 = disparado
  
  #configura a saida 12v para uso da sirene
  mcp.config(11, OUTPUT) 
  
  while True:
      if GPIO.input(17) == 0:
        print "Sensor 0 Violado!"
        mcp.output(11, 1)
        time.sleep(10) 
        mcp.output(11, 0)
        break;
      #elif GPIO.input(18) == 0:
      #  print "Sensor 1 Violado!"
      #  mcp.output(11, 1)
      #  time.sleep(10) 
      #  mcp.output(11, 0)
      #  break;
      
      # e assim por diante..
      
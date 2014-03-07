#!/usr/bin/python
#-*- coding: utf-8 -*-

import time 
import Adafruit_MCP230xx
 
OUTPUT = 0 
INPUT = 1 
 
if __name__ == '__main__': 
  #  Use busnum = 0 for older Raspberry Pi's (pre 512MB) 
  mcp = Adafruit_MCP230XX(busnum = 1, address = 0x20, num_gpios = 16) 
  # Use busnum = 1 for new Raspberry Pi's (512MB) 
 
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
  
  
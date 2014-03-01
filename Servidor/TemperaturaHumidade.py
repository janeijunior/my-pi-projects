#!/usr/bin/python
#-*- coding: utf-8 -*-

import subprocess
import re
import sys
import time
import datetime
import Funcoes

class TemperaturaHumidade(object):

    def __lerSensor():
        return subprocess.check_output([Funcoes.lerConfiguracaoIni("CaminhoDHT"), Funcoes.lerConfiguracaoIni("TipoDHT"), Funcoes.lerConfiguracaoIni("GPIODHT")]);
    
    
    def getTemperaturaHumidade():
        output  = __lerSensor(); 
        matches = re.search("Temp =\s+([0-9.]+)", output)
        
        if (not matches):
          time.sleep(3)
          output  = __lerSensor();
          matches = re.search("Temp =\s+([0-9.]+)", output)
          
        temp = float(matches.group(1))
        
        matches = re.search("Hum =\s+([0-9.]+)", output)
        
        if (not matches):
          time.sleep(3)
          output  = __lerSensor();     
          matches = re.search("Hum =\s+([0-9.]+)", output)  
          
        hum = float(matches.group(1))
        
        lista = []
        lista.insert(0, "%.1f" % temp)
        lista.insert(1, "%.1f" % hum)
    
        return lista

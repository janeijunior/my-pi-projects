#!/usr/bin/python

import subprocess
import re
import sys
import time
import datetime

def lerSensor():
    return subprocess.check_output([" ./Adafruit_DHT", "2302", "4"]);


def lerTemperaturaHumidade():
    output  = lerSensor(); 
    matches = re.search("Temp =\s+([0-9.]+)", output)
    
    if (not matches):
      time.sleep(3)
      output  = lerSensor();
      matches = re.search("Temp =\s+([0-9.]+)", output)
      
    temp = float(matches.group(1))
    
    matches = re.search("Hum =\s+([0-9.]+)", output)
    
    if (not matches):
      time.sleep(3)
      output  = lerSensor();     
      matches = re.search("Hum =\s+([0-9.]+)", output)  
      
    hum = float(matches.group(1))
    
    lista = []
    lista.insert(0, "%.1f" % temp)
    lista.insert(1, "%.1f" % hum)

    return lista

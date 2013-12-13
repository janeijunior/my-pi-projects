#!/usr/bin/python

import subprocess
import re
import sys
import time
import datetime

def lerSensor():
    return = subprocess.check_output(["./Adafruit_DHT", "2302", "4"]);

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
  
humidity = float(matches.group(1))

print "Temperatura: %.1f C" % temp
print "Humidade:    %.1f %%" % humidity


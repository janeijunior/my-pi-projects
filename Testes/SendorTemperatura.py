import httplib
import json as simplejson
from random import randint
import time
import os
import glob

# Pass os commands to set up I2C bus 
os.system('modprobe w1-gpio')  
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

run_number = 0

SENSE_API_KEY = "long sen.se passphase here. note that it is in quotes"
FEED_ID1 = 12345  # five digit sen.se channel code.  note it is NOT in quotes

def read_temp_raw():  #read the DS18B20 function
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(): #process the raw temp file output and convert to F
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(1)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        ambC = float(temp_string) / 1000.0
        ambF = ambC * 9.0 / 5.0 + 32.0
        return ambF

def send_to_opensense(data):
#    print  >> fout, "\t=> Sending to OpenSense: %s" % data
 try:
  # prepare data 
  datalist = [{"feed_id" : FEED_ID1, "value" :data['F']},]
  headers = {"sense_key": SENSE_API_KEY,"content-type": "application/json"}
  conn = httplib.HTTPConnection("api.sen.se")
  # format a POST request with JSON content
  conn.request("POST", "/events/", simplejson.dumps(datalist), headers)
  response = conn.getresponse()
  # you may get interesting information here in case it fails
  #   print >> fout, response.status, response.reason
  #   print >> fout, response.read()
  conn.close()
 except:
  pass

while(True):
 try: 
  run_number = run_number + 1
  ambF = read_temp()
  print "RasPI(2) Ambient Run:", run_number, "    ambF:",ambF  
  data = { 'F' : ambF}
  send_to_opensense(data)
  time.sleep(300)
 except:
  pass
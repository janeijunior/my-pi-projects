# Notes
# Find the RFID reader within Raspberry Pi 
# $ ls /dev/tty*

import time
import serial

delay  = 0
port   = 2400
tag_death = "440033886D"
serial = serial.Serial('/dev/tty0', port, timeout=1)

def check():
  #The tag is a 12-byte string starting with a carriage
  #return and ending with a newline return EM4001 tags will
  #never contain anything but ASCII digits 0-9A-F
  unique_id = serial.read(12)
  unique_id = unique_id[2:][:-2]
  if unique_id == tag_death:
    print("You found the death key")
    exit()
  else:
      print("Sandy's Super Access Code:", unique_id)

try:
  while True:
    time.sleep(delay)
    check()
except KeyboardInterrupt:
  exit()

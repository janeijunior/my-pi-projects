#! /usr/bin/python
import serial
import time

ser = serial.Serial('/dev/tty0', 2400, timeout=1) # replace '/dev/ttyUSB0' with your port

while True:
    response = ser.readline()
    if response <> "":
        print str(response)
    time.sleep(1)

ser.close()

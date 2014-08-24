#! /usr/bin/python
import serial
import time

ser = serial.Serial('/dev/tty0', 2400, timeout=1) # replace '/dev/ttyUSB0' with your port

while True:
    response = ser.read(12)
    if response <> "":
        print "raw: " + str(response)
        print "hex: " + str(response[-8:])
        print "dec: " + str(int(response[-8:], 16))
    time.sleep(1)

ser.close()

#!/usr/bin/python

maxcount = 200

import RPi.GPIO as GPIO, time, sys
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

GPIO.setup(21, GPIO.IN)

while True:
  pin = GPIO.input(21)
  if pin:
    count = 0
    while (count < maxcount):
      pin = GPIO.input(21)
      sys.stdout.write(str(int(pin)))
      pin = 0
      count = count + 1
      if count == maxcount:
        print("---")
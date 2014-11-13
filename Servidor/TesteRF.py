#!/usr/bin/python

import RPi.GPIO as GPIO, time, sys
GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.IN)

while True:
    input_value = GPIO.input(4)
    sys.stdout.write(str(int(input_value)))
    input_value = 0
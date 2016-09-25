#!/usr/bin/python
import time
from RPi import GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)
 
while True:
    inputval1 = GPIO.output(32, False)
    time.sleep(1)
    inputval1 = GPIO.output(32, True)
    time.sleep(1)
 
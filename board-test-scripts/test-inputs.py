#!/usr/bin/python
import time
from RPi import GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
 
while True:
    inputval1 = GPIO.input(18)
    inputval2 = GPIO.input(22)
    inputval3 = GPIO.input(37)
    inputval4 = GPIO.input(13)
    print "INPUT1="+str(inputval1) +  ",INPUT2="+str(inputval2) + ",INPUT3="+str(inputval3) +   ",INPUT4="+str(inputval4)
 
    time.sleep(1)

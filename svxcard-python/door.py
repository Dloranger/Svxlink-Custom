
#!/usr/bin/python
import time
import os  

doorstatus = 0
 
from RPi import GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
 
while True:
    inputval1 = GPIO.input(18)
#    inputval2 = GPIO.input(22)
#    inputval3 = GPIO.input(37)
#    inputval4 = GPIO.input(13)
    print "INPUT1="+str(inputval1)
    print str(doorstatus)
  
    if (inputval1 == 0 and doorstatus == 0):
      os.system ("sudo echo 123 \# | nc 127.0.0.1 10000")
      doorstatus = 1
      os.system ("echo 1 > /sys/class/gpio/gpio23/value") 
      doorstatus = 1
    if (inputval1 == 1 and doorstatus == 1):
      doorstatus = 0   
      os.system ("echo 0 > /sys/class/gpio/gpio23/value")
    time.sleep(1)

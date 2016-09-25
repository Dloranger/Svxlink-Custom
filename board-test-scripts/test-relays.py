#!/usr/bin/python
import os
import time
 
os.system("gpio -g write 20 1")
time.sleep(1)
os.system("gpio -g write 21 1")
time.sleep(1)
os.system("gpio -g write 22 1")
time.sleep(1)
os.system("gpio -g write 23 1")
time.sleep(1)
os.system("gpio -g write 20 0")
time.sleep(1)
os.system("gpio -g write 21 0")
time.sleep(1)
os.system("gpio -g write 22 0")
time.sleep(1)
os.system("gpio -g write 23 0")
time.sleep(1)
os.system("for i in 20 21 22 23 ; do gpio -g write $i 1; done")
time.sleep(1)
os.system("for i in 20 21 22 23 ; do gpio -g write $i 0; done")
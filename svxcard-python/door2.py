
#!/usr/bin/python
import time
import os  


doorstatus = 0

cwd = os.system ("cat /sys/class/gpio/gpio24/value")
  
while True: 
    cwd =os.system ("cat /sys/class/gpio/gpio24/value")
    print "Etat porte 0=fermee 1=ouverte : "+str(doorstatus)
    print str(cwd)    
    if (str(cwd) == 0 and doorstatus == 0):
     os.system ("sudo echo 123 \# | nc 127.0.0.1 10000")
     doorstatus = 1
    if (str(cwd) == 1 and doorstatus == 1):
     doorstatus = 0      
   
time.sleep(1)

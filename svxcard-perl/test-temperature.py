#!/usr/bin/env python
# -*- coding: utf-8 -*-

""""
"  SVXLINK ONBOARD TEMPERATURE
"  SVXLink Card on http://svxcard.f5uii.net
"
"  This Python software generate a status file, in which the temperature given by the DS18B20 is written 
"  08.02.2016 (b)- Christian, F5UII
"  version 0.1 - Under Creative Commons licence [by-nc-sa] http://creativecommons.org/licenses/by-nc-sa/4.0/
"
"""
import time

svxtempfile="/usr/share/svxlink/events.d/local/SVXCard/svx_temp.conf" # Generated file by this software
delay = 15 #delay of update of temperature in the 'svxtempfile' file

sensorids = ["28-0000067b9b8a"]  #Indiquer ici le numéro de série de votre 18b20 : ls /sys/bus/w1/devices/
for sensor in range(len(sensorids)):
        temperatures = []
        while True:
                text = '';
                while text.split("\n")[0].find("YES") == -1:
                                tfile = open("/sys/bus/w1/devices/"+ sensorids[sensor] +"/w1_slave")
                                text = tfile.read()                                       
                                tfile.close()
             
                secondline = text.split("\n")[1]
                temperaturedata = secondline.split(" ")[9]
                temperature = float(temperaturedata[2:])/1000
                temperature = ("%.1f" % temperature)
                print temperature
                fo = open(svxtempfile, "w")
                lin = fo.writelines( "\n###  SVXLINK CARD - Onboard temperature  ###\n\n\n" )
                lin = fo.writelines( "\n[STATUS]          # Section with dynamic informations \n\n")
                lin = fo.writelines( "SVX_TEMP="+str(temperature)+"\n")
                fo.close()
                time.sleep (5)



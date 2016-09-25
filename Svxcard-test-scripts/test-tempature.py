#!/usr/bin/python
# - * - coding: utf-8 - * -
import time

sensorids = ["28-041600ff7aff"]
avgtemperatures = []
for sensor in range(len(sensorids)):
        temperatures = []
        for polltime in range(0,3):
                        text = '';
                        while text.split("\n")[0].find("YES") == -1:
                                        tfile = open("/sys/bus/w1/devices/"+ sensorids[sensor] +"/w1_slave")
                                        text = tfile.read()
                                        #print text
                                        tfile.close()
                                        time.sleep(1)

                        secondline = text.split ("\n") [1]
                        temperaturedata = secondline.split (" ") [9]
                        temperature =  float (temperaturedata [2:]) / 1000
                        print ( "temperature =% .3f ° C" % temperature )

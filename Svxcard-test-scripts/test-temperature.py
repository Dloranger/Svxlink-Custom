#!/usr/bin/python
# - * - coding: utf-8 - * -
sensorids = ["10-00080109d8c4"]  #Indicate the serial number of your 18b20 here : ls /sys/bus/w1/devices/
for sensor in range(len(sensorids)):
        temperatures = []
        while True:
                        text = '';
                        while text.split("\n")[0].find("YES") == -1:
                                        tfile = open("/sys/bus/w1/devices/"+ sensorids[sensor] +"/w1_slave"                                       )
                                        text = tfile.read()
                                        tfile.close()
 
                        secondline = text.split("\n")[1]
                        temperaturedata = secondline.split(" ")[9]
                        temperature = float(temperaturedata[2:])/1000
                        print("temperature = %.3f °C" % temperature)
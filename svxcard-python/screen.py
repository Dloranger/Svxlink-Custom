#!/usr/bin/python                                                                
import serial                                                                   
import time                                                                     
import select                                                                   
import sys                                                                      
import ConfigParser, os
import random


#port = '/dev/hidraw1'
port = '/dev/ttyAMA0'
baud = 9600

svxstatusfile="/usr/share/svxlink/events.d/local/SVXCard/svx_status.conf"   #File of live status of SVXLink Repeater
svxtempfile="/usr/share/svxlink/events.d/local/SVXCard/svx_temp.conf" # File with aboard temperature of SVXLink Card
svxlog = "/var/log/svxlink"   #SVXLink log file 

serial_port = serial.Serial(port, baud, 8, 'N', 1, timeout=.1)
serial_port.close()
serial_port.open()                                                                                                   
                      


   

callsign = 'F1ZBV'
cmd=''
tx=''
rx=''
svxrun=''
cpu_temp=''
def read_status ():
  global callsign,svxstatusfile,rx, tx,svxrun,tone,longb,shortb,cpu_temp,svx_temp
  config = ConfigParser.ConfigParser()
  try:
    config.read(svxstatusfile)
    svxrun = config.get('STATUS', 'SVXLINK_RUN')
    callsign = config.get('CONFIG', 'REP_CALLSIGN')
    tx = config.get('STATUS', 'TX')
    rx = config.get('STATUS', 'RX')
    tone = config.get('STATUS', 'TONE')
    longb = config.get('STATUS', 'LONGBEACON')
    shortb = config.get('STATUS', 'SHORTBEACON')
    cpu_temp = config.get('STATUS', 'CPU_TEMP')
  except: #catch all error
    print 'Access file Error ...'  
  
  config_temp = ConfigParser.ConfigParser()
  try:
    config.read(svxtempfile)
    svx_temp = config.get('STATUS', 'SVX_TEMP')
  except: #catch all error
    print 'Access file Error ...'  

while True:                                                                     
    # Check whether the user has typed anything (timeout of .2 sec):            
    inp, outp, err = select.select([sys.stdin, serial_port], [], [], .1)         
    time.sleep(0.5)

    cmd = cmd + 'sendme'+'\xFF\xFF\xFF'  # Send current page ID
                                                                            
    if serial_port in inp :                                                      
        line = serial_port.readline().strip()                                    
        #print "rx:", line
        trame = line.encode("hex")
        #print line 
        if "6603ffffff" in trame:  #page 3 Reboot/restart window
            last_line = file(svxlog, "r").readlines()[-1]
            cmd= cmd + 'page3.log1.txt="'+last_line+'"'+'\xFF\xFF\xFF'
            last_line = file(svxlog, "r").readlines()[-2]
            cmd= cmd + 'page3.log2.txt="'+last_line+'"'+'\xFF\xFF\xFF'
            last_line = file(svxlog, "r").readlines()[-3]
            cmd= cmd + 'page3.log3.txt="'+last_line+'"'+'\xFF\xFF\xFF'
            last_line = file(svxlog, "r").readlines()[-4]
            cmd= cmd + 'page3.log4.txt="'+last_line+'"'+'\xFF\xFF\xFF'
            last_line = file(svxlog, "r").readlines()[-5]
            cmd= cmd + 'page3.log5.txt="'+last_line+'"'+'\xFF\xFF\xFF'
            last_line = file(svxlog, "r").readlines()[-6]
            cmd= cmd + 'page3.log6.txt="'+last_line+'"'+'\xFF\xFF\xFF'    
            last_line = file(svxlog, "r").readlines()[-7]
            cmd= cmd + 'page3.log7.txt="'+last_line+'"'+'\xFF\xFF\xFF'
            last_line = file(svxlog, "r").readlines()[-8]
            cmd= cmd + 'page3.log8.txt="'+last_line+'"'+'\xFF\xFF\xFF' 
        if "***screen-cmd=restart***" in line:
            os.system ("sudo sh /usr/share/svxlink/events.d/local/restart-svxlink.sh")
        if "***screen-cmd=reboot***" in line:
            os.system ("sudo reboot -f")        
        if "***cmd=K4CLOSE***" in line: 
            os.system("sudo echo '0'>  /sys/class/gpio/gpio23/value")  
        if "***cmd=K4OPEN***" in line: 
            os.system("sudo echo '1'>  /sys/class/gpio/gpio23/value")
        if "***cmd=K3CLOSE***" in line: 
            os.system("sudo echo '0'>  /sys/class/gpio/gpio22/value")  
        if "***cmd=K3OPEN***" in line: 
            os.system("sudo echo '1'>  /sys/class/gpio/gpio22/value")
        if "***cmd=K2CLOSE***" in line: 
            os.system("sudo echo '0'>  /sys/class/gpio/gpio21/value")  
        if "***cmd=K2OPEN***" in line: 
            os.system("sudo echo '1'>  /sys/class/gpio/gpio21/value")
        if "***cmd=K1CLOSE***" in line: 
            os.system("sudo echo '0'>  /sys/class/gpio/gpio20/value")  
        if "***cmd=K1OPEN***" in line: 
            os.system("sudo echo '1'>  /sys/class/gpio/gpio20/value")            
        if "***cmd=RELAYSEQUENCE***" in line: 
            os.system("sudo echo '0'>  /sys/class/gpio/gpio20/value && sudo echo '0'>  /sys/class/gpio/gpio21/value && sudo echo '0'>  /sys/class/gpio/gpio22/value && sudo echo '0'>  /sys/class/gpio/gpio23/value")        
            time.sleep(0.5)
            os.system("sudo echo '1'>  /sys/class/gpio/gpio20/value && sudo echo '1'>  /sys/class/gpio/gpio21/value && sudo echo '1'>  /sys/class/gpio/gpio22/value && sudo echo '1'>  /sys/class/gpio/gpio23/value")        
            time.sleep(0.5)
            os.system("sudo echo '0'>  /sys/class/gpio/gpio20/value && sudo echo '0'>  /sys/class/gpio/gpio21/value && sudo echo '0'>  /sys/class/gpio/gpio22/value && sudo echo '0'>  /sys/class/gpio/gpio23/value")        
            time.sleep(0.5)
            os.system("sudo echo '1'>  /sys/class/gpio/gpio20/value && sudo echo '1'>  /sys/class/gpio/gpio21/value && sudo echo '1'>  /sys/class/gpio/gpio22/value && sudo echo '1'>  /sys/class/gpio/gpio23/value")        
    read_status()    
    
   
    cmd = cmd + 'page1.callsign.txt="'+callsign+'"'+'\xFF\xFF\xFF'
    if tx=='1' :
      cmd= cmd +'page1.screen_tx.pic=3'+'\xFF\xFF\xFF'
    else:
      cmd= cmd +'page1.screen_tx.pic=4'+'\xFF\xFF\xFF'
    if rx=='1' :
      cmd= cmd +'page1.screen_rx.pic=2'+'\xFF\xFF\xFF'
    else:
      cmd= cmd +'page1.screen_rx.pic=1'+'\xFF\xFF\xFF'
    if rx=='1' :
      cmd= cmd +'page1.screen_rx.pic=2'+'\xFF\xFF\xFF'
    else:
      cmd= cmd +'page1.screen_rx.pic=1'+'\xFF\xFF\xFF'
    if svxrun=='1' :
      cmd= cmd +'page1.information.txt="SVXLINK is running"'+'\xFF\xFF\xFF'
    else:
      cmd= cmd +'page1.information.txt="SVXLINK is STOPPED !"'+'\xFF\xFF\xFF'
    cmd= cmd +'CPU_temp.txt="'+cpu_temp+' C"\xFF\xFF\xFF'
    cmd= cmd +'svx_temp.txt="'+svx_temp+' C"\xFF\xFF\xFF' 

    cmd= cmd +'testcom.txt="'+str(random.randint(1, 9000))+'"\xFF\xFF\xFF'  #diagnose of communication status on the screen
    cmd= cmd +'heure.txt="'+str(time.strftime("%H:%M:%S" ))+'"\xFF\xFF\xFF'  #diagnose of communication status on the screen
    serial_port.write(cmd)
    cmd= ''

serial_port.close()

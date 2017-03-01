#!/usr/bin/python
""""
"  SVXLINK REALTIME STATUS OF SVXLINK
"  SVXLink Card on http://svxcard.f5uii.net
"
"  This Python software generate a status configuration file, in which the status of activities of SVXlink is detailed
"  08.02.2016 (b)- Christian, F5UII
"  version 0.2 - Under Creative Commons licence [by-nc-sa] http://creativecommons.org/licenses/by-nc-sa/4.0/
"
"""
import ConfigParser, os
import time # used by follow function
import sys
 
svxlogfile="/var/log/svxlink"         # Real time log which is analysed by this software
#svxlogfile="/home/pi/svxlink.log"         # Real time log which is analysed by this software
svxconfigfile="/etc/svxlink/svxlink.conf" # Configuration File of SVXLink
svxstatusfile="/usr/share/svxlink/events.d/local/SVXCard/svx_status.conf" # Generated file by this software
sensorids = ["28-0000067b9b8a"]          # Here the serial number of the 18b20 : ls /sys/bus/w1/devices/


#LOGICS NAMES
StrSimplex = "SimplexLogic"                 # Identification of a Simplex Logic in Svxlink, by default = "SimplexLogic"
StrRepeater = "RepeaterLogic"               # Identification of a Repeater Logic in Svxlink, by default = "RepeaterLogic"
#MODULES NAMES
StrHelp = "Help"                      # Identification of a Help Module in Svxlink, by default = "Help"
StrParrot = "Parrot"                  # Identification of a Parrot Module in Svxlink, by default = "Parrot"
StrEcholink = "EchoLink"              # Identification of a Echolink Module in Svxlink, by default = "EchoLink"
StrVoicemail = "TclVoiceMail"         # Identification of a Voicemail Module in Svxlink, by default = "TclVoiceMail"
StrMetarinfo = "MetarInfo"            # Identification of a Metar informations Module in Svxlink, by default = "MetarInfo"
StrDtmfrepeater = "DtmfRepeater"      # Identification of a DTMF Repeater Module in Svxlink, by default = "DtmfRepeater"
StrSelcallenc = "SelCallEnc"          # Identification of a Selective Call Encoder Module in Svxlink, by default = "SelCallEnc"
StrPropagation = "PropagationMonitor" # Identification of a Propagation information Module in Svxlink, by default = "PropagationMonitor"
 
# Variables initialisation
tx=0
rx=0
tone=0
svxrun=0
longbeacon=0
shortbeacon=0
module_echolink=0
echolinkstat_count=0
process = 0
rep_mod_help=0
rep_mod_parrot=0
rep_mod_echolink=0
rep_mod_metar=0
rep_mod_voicemail=0
rep_mod_dtmf=0
rep_mod_selcall=0
rep_mod_propag=0
rep_recoder=0   #QSO recorder , by default be activated by DTMF = 81#, desactivated by DTMF = 80#
sim_mod_help=0
sim_mod_parrot=0
sim_mod_echolink=0
sim_mod_metar=0
sim_mod_voicemail=0
sim_mod_dtmf=0
sim_mod_selcall=0
sim_mod_propag=0
sim_recoder=0   #QSO recorder , by default be activated by DTMF = 81#, desactivated by DTMF = 80#
Last_Echolink_station = ""   #Callsign of the last Echolink station
Echok_Station_conn = 0      # 1 = Echolink Station connected on repeater 

# Return CPU temperature as a character string                                      
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))
# Return RAM information (unit=kb) in a list                                        
# Index 0: total RAM                                                                
# Index 1: used RAM                                                                 
# Index 2: free RAM                                                                 
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])
# Return % of CPU used by user as a character string                                
def getCPUuse():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip(\
)))
# Return information about disk space as a list (unit included)                     
# Index 0: total disk space                                                         
# Index 1: used disk space                                                          
# Index 2: remaining disk space                                                     
# Index 3: percentage of disk used                                                  
def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            return(line.split()[1:5])
def check_svxlink( *args ):
    p=os.popen('pidof svxlink |wc -w' ).readline()
    return int(p)
        
# Writing the file of current status
def writeconf():
   
    fo = open(svxstatusfile, "w")
    lin = fo.writelines( "\n###  SVXLINK STATUS  ###\n\n\n" )
    lin = fo.writelines( "[CONFIG]          # Section with static informations, provided by configuration files\n\n")
    lin = fo.writelines( "STATION_INFO="+ Station_info +"\n")
    lin = fo.writelines( "# Simplex Logic\n")
    lin = fo.writelines( "SIM_CALLSIGN=" + Sim_callsign + "\n" )
    lin = fo.writelines( "SIM_MODULES=" + Sim_modules + "\n" )
    lin = fo.writelines( "\n# Repeater Logic\n")
    lin = fo.writelines( "REP_CALLSIGN=" + Rep_callsign + "\n" )
    lin = fo.writelines( "REP_MODULES=" + Rep_modules + "\n" )
    lin = fo.writelines( "\n[STATUS]          # Section with dynamic informations, provided by log files and shell commands\n\n")
    lin = fo.writelines( "SVXLINK_RUN="+str(svxrun)+"\n")
    lin = fo.writelines( "TX="+str(tx)+"\n")
    lin = fo.writelines( "RX="+str(rx)+"\n")
    lin = fo.writelines( "TONE="+str(tone)+"\n")
    lin = fo.writelines( "LONGBEACON="+str(longbeacon)+"\n")
    lin = fo.writelines( "SHORTBEACON="+str(shortbeacon)+"\n")
    lin = fo.writelines( "REP_MOD_HELP="+str(rep_mod_help)+"\n")
    lin = fo.writelines( "REP_MOD_PARROT="+str(rep_mod_parrot)+"\n")
    lin = fo.writelines( "REP_MOD_ECHOLINK="+str(rep_mod_echolink)+"\n")
    lin = fo.writelines( "REP_MOD_METAR="+str(rep_mod_metar)+"\n")
    lin = fo.writelines( "REP_MOD_VOICEMAIL="+str(rep_mod_voicemail)+"\n")
    lin = fo.writelines( "REP_MOD_DTMF="+str(rep_mod_dtmf)+"\n")
    lin = fo.writelines( "REP_MOD_SELCALL="+str(rep_mod_selcall)+"\n")
    lin = fo.writelines( "REP_MOD_PROPAGATION="+str(rep_mod_propag)+"\n")
    lin = fo.writelines( "REP_RECORDER="+str(rep_recoder)+"\n")
    lin = fo.writelines( "SIM_MOD_HELP="+str(sim_mod_help)+"\n")
    lin = fo.writelines( "SIM_MOD_PARROT="+str(sim_mod_parrot)+"\n")
    lin = fo.writelines( "SIM_MOD_ECHOLINK="+str(sim_mod_echolink)+"\n")
    lin = fo.writelines( "SIM_MOD_METAR="+str(sim_mod_metar)+"\n")
    lin = fo.writelines( "SIM_MOD_VOICEMAIL="+str(sim_mod_voicemail)+"\n")
    lin = fo.writelines( "SIM_MOD_DTMF="+str(sim_mod_dtmf)+"\n")
    lin = fo.writelines( "SIM_MOD_SELCALL="+str(sim_mod_selcall)+"\n")
    lin = fo.writelines( "SIM_MOD_PROPAGATION="+str(sim_mod_propag)+"\n")
    lin = fo.writelines( "SIM_RECORDER="+str(sim_recoder)+"\n")
    lin = fo.writelines( "CPU_TEMP="+str(getCPUtemperature())+"\n")
    lin = fo.writelines( "CPU_USE="+str(getCPUuse())+"\n")
    lin = fo.writelines( "RAM_USE="+str(getRAMinfo())+"\n")
    lin = fo.writelines( "DISK_USE="+str(getDiskSpace())+"\n")    
    fo.close()
def follow(thefile):
    thefile.seek(0,2)      # Go to the end of the file
    while True:
         line = thefile.readline()
         if not line:
             time.sleep(0.1)    # Sleep briefly
             continue
         yield line
 
# Checking of the configuration file 
config = ConfigParser.ConfigParser()
config.read(svxconfigfile)
Logics = config.get('GLOBAL', 'LOGICS')
Sim_modules = ""
Rep_modules = ""
Sim_callsign = ""
Rep_callsign = ""
if  StrRepeater in Logics :
        Rep_callsign = config.get(StrRepeater, 'CALLSIGN')
        print "Repeater logic detected in SvxConfig"
        print "Repeater Callsign "+Rep_callsign;
        Rep_modules = config.get(StrRepeater, 'MODULES')
if  StrSimplex in Logics :
        Sim_callsign = config.get(StrSimplex, 'CALLSIGN')
        print "Simplex logic detected in SvxConfig"
        print "Simplex Callsign "+Sim_callsign;
        Sim_modules = config.get(StrSimplex, 'MODULES')

Station_info=""
Freq=""
Ant_h=""
Ant_gain=""
try: 
    Freq = config.get('LocationInfo', 'FREQUENCY')
except ConfigParser.NoOptionError, err: print "Info : "+str(err)
try:
    Power = config.get('LocationInfo', 'TX_POWER')
except ConfigParser.NoOptionError, err: print "Info : "+str(err)
try:
    Ant_gain = config.get('LocationInfo', 'ANTENNA_GAIN')
except ConfigParser.NoOptionError, err: print ("Info : "+str(err))
try:
    Ant_h = config.get('LocationInfo', 'ANTENNA_HEIGHT')
except ConfigParser.NoOptionError, err: print "Info : "+str(err)
if Freq :
    Station_info = "Frequency is set to " + Freq + ". "
if Ant_h :
    Station_info =  Station_info + "The antenna is installed on "+ Ant_h + " height. "
if Ant_gain :
    Station_info = Station_info + "Antenna gain is " + Ant_gain +". "
print Station_info
         

writeconf()  # Write the status file on disk
#Checking the real time status with Log file
i=0
logfile = open(svxlogfile)
loglines = follow(logfile)
for line in loglines:
        #print line
        if "transmitter ON" in line:
                print "TX ON"
                tx = 1
        elif "transmitter OFF" in line:
                print "TX OFF"
                tx = 0
                tone=0
                longbeacon=0
                shortbeacon=0
        elif "Shutting down application" in line:
                print "SHUTTING DOWN SVX"
                svxrun = 0
        elif "tone call detected" in line:
                print "TONE DETECTED"
                tone = 1
        elif "Sending long identification" in line:
                print "LONG BEACON"
                longbeacon = 1
        elif "Sending short identification." in line:
                print "SHORT BEACON"
                shortbeacon=1
        elif "The squelch is OPEN"  in line:
                print "SQUELCH OPEN"
                rx = 1
        elif "The squelch is CLOSED" in line:
                print "SQUELCH CLOSED"
                rx = 0
        elif StrRepeater+": Activating module " + StrParrot  in line:
                print StrParrot+ " module activated on "+StrRepeater
                rep_mod_parrot = 1    
        elif StrRepeater+": Deactivating module " + StrParrot  in line:
                print StrParrot+" module desactivated on "+StrRepeater
                rep_mod_parrot = 0
        elif StrRepeater+": Activating module " + StrHelp  in line:
                print StrHelp+" module activated on "+StrRepeater
                rep_mod_help = 1    
        elif StrRepeater+": Deactivating module " + StrHelp  in line:
                print StrHelp+" module desactivated on "+StrRepeater
                rep_mod_help = 0
        elif StrRepeater+": Activating module " + StrEcholink  in line:
                print StrEcholink+" module activated on "+StrRepeater
                rep_mod_echolink = 1    
        elif StrRepeater+": Deactivating module " + StrEcholink in line:
                print StrEcholink+" module desactivated on "+StrRepeater
                rep_mod_echolink = 0                
        elif StrRepeater+": Activating module " + StrMetarinfo  in line:
                print StrMetarinfo+" module activated on "+StrRepeater
                rep_mod_metar = 1    
        elif StrRepeater+": Deactivating module " + StrMetarinfo in line:
                print StrMetarinfo+" module desactivated on "+StrRepeater
                rep_mod_metar = 0     
        elif StrRepeater+": Activating module " + StrVoicemail  in line:
                print StrVoicemail+" module activated on "+StrRepeater
                rep_mod_voicemail = 1    
        elif StrRepeater+": Deactivating module " + StrVoicemail in line:
                print StrVoicemail+" module desactivated on "+StrRepeater
                rep_mod_voicemail = 0         
        elif StrRepeater+": Activating module " + StrDtmfrepeater  in line:
                print StrDtmfrepeater+" module activated on "+StrRepeater
                rep_mod_dtmf = 1    
        elif StrRepeater+": Deactivating module " + StrDtmfrepeater in line:
                print StrDtmfrepeater+" module desactivated on "+StrRepeater
                rep_mod_dtmf = 0    
        elif StrRepeater+": Activating module " + StrSelcallenc in line:
                print StrSelcallenc+" module activated on "+StrRepeater
                rep_mod_selcall= 1    
        elif StrRepeater+": Deactivating module " + StrSelcallenc in line:
                print StrSelcallenc+" module desactivated on "+StrRepeater
                rep_mod_selcall = 0    
        elif StrRepeater+": Activating module " + StrPropagation in line:
                print StrPropagation+" module activated on "+StrRepeater
                rep_mod_propag= 1    
        elif StrRepeater+": Deactivating module " + StrPropagation in line:
                print StrPropagation+" module desactivated on "+StrRepeater
                rep_recoder = 0    
        elif StrRepeater+": Activating QSO recorder" in line:
                print "QSO recorder activated on "+StrRepeater
                rep_recoder= 1    
        elif StrRepeater+": Deactivating QSO recorder" in line:
                print "QSO recorder module desactivated on "+StrRepeater
                rep_mod_propag = 0    
        elif StrSimplex+": Activating module " + StrParrot  in line:
                print StrParrot+ " module activated on "+StrSimplex
                sim_mod_parrot = 1    
        elif StrSimplex+": Deactivating module " + StrParrot  in line:
                print StrParrot+" module desactivated on "+StrSimplex
                sim_mod_parrot = 0
        elif StrSimplex+": Activating module " + StrHelp  in line:
                print StrHelp+" module activated on "+StrSimplex
                sim_mod_help = 1    
        elif StrSimplex+": Deactivating module " + StrHelp  in line:
                print StrHelp+" module desactivated on "+StrSimplex
                sim_mod_help = 0
        elif StrSimplex+": Activating module " + StrEcholink  in line:
                print StrEcholink+" module activated on "+StrSimplex
                sim_mod_echolink = 1    
        elif StrSimplex+": Deactivating module " + StrEcholink in line:
                print StrEcholink+" module desactivated on "+StrSimplex
                sim_mod_echolink = 0                
        elif StrSimplex+": Activating module " + StrMetarinfo  in line:
                print StrMetarinfo+" module activated on "+StrSimplex
                sim_mod_metar = 1    
        elif StrSimplex+": Deactivating module " + StrMetarinfo in line:
                print StrMetarinfo+" module desactivated on "+StrSimplex
                sim_mod_metar = 0     
        elif StrSimplex+": Activating module " + StrVoicemail  in line:
                print StrVoicemail+" module activated on "+StrSimplex
                sim_mod_voicemail = 1    
        elif StrSimplex+": Deactivating module " + StrVoicemail in line:
                print StrVoicemail+" module desactivated on "+StrSimplex
                sim_mod_voicemail = 0         
        elif StrSimplex+": Activating module " + StrDtmfrepeater  in line:
                print StrDtmfrepeater+" module activated on "+StrSimplex
                sim_mod_dtmf = 1    
        elif StrSimplex+": Deactivating module " + StrDtmfrepeater in line:
                print StrDtmfrepeater+" module desactivated on "+StrSimplex
                sim_mod_dtmf = 0    
        elif StrSimplex+": Activating module " + StrSelcallenc in line:
                print StrSelcallenc+" module activated on "+StrSimplex
                sim_mod_selcall= 1    
        elif StrSimplex+": Deactivating module " + StrSelcallenc in line:
                print StrSelcallenc+" module desactivated on "+StrSimplex
                sim_mod_selcall = 0    
        elif StrSimplex+": Activating module " + StrPropagation in line:
                print StrPropagation+" module activated on "+StrSimplex
                sim_mod_propag= 1    
        elif StrSimplex+": Deactivating module " + StrPropagation in line:
                print StrPropagation+" module desactivated on "+StrSimplex
                sim_mod_propag = 0    
        elif StrSimplex+": Activating QSO recorder" in line:
                print "QSO recorder activated on "+StrSimplex
                sim_recoder= 1    
        elif StrSimplex+": Deactivating QSO recorder" in line:
                print "QSO recorder module desactivated on "+StrSimplex
                sim_recoder = 0    
                
        elif "EchoLink QSO state changed to CONNECTED" in line:
            ch =  line.split(':')
            Last_Echolink_station = ch[0]
            Echok_Station_conn = 1
            print "ECHOLINK STATION CONNECTED"
        elif "EchoLink QSO state changed to BYE_RECEIVED" in line:
            Echok_Station_conn = 0
            print "ECHOLINK STATION DISCONNECTED"
              
        # Check if process svxlink is running
        if check_svxlink() == 1 :
            svxrun = 1
        else :
            svxrun = 0
        writeconf()  # Write the status file on disk
       
        

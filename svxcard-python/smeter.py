#!/usr/bin/python
#
# MCP3204/MCP3208 sample program for Raspberry Pi
#
# how to setup /dev/spidev?.?
# $ sudo modprobe spi_bcm2708
#
# how to setup spidev
# $ sudo apt-get install python-dev python-pip
# $ sudo pip install spidev
#
import spidev
import time
from collections import deque
 
class MCP3208:
	def __init__(self, spi_channel=0):
		self.spi_channel = spi_channel
		self.conn = spidev.SpiDev(0, spi_channel)
		self.conn.max_speed_hz = 1000000 # 1MHz
 
	def __del__( self ):
		self.close
 
	def close(self):
		if self.conn != None:
			self.conn.close
			self.conn = None
 
	def bitstring(self, n):
		s = bin(n)[2:]
		return '0'*(8-len(s)) + s
 
	def read(self, adc_channel=0):
		# build command
		cmd = 128 # start bit
		cmd += 64 # single end / diff
		if adc_channel % 2 == 1:
			cmd += 8
		if (adc_channel/2) % 2 == 1:
			cmd += 16
		if (adc_channel/4) % 2 == 1:
			cmd += 32
 
		# send & receive data
		reply_bytes = self.conn.xfer2([cmd, 0, 0, 0])
 
		#
		reply_bitstring = ''.join(self.bitstring(n) for n in reply_bytes)
		# print reply_bitstring
 
		# see also... http://akizukidenshi.com/download/MCP3204.pdf (page.20)
		reply = reply_bitstring[5:19]
		return int(reply, 2)
 
if __name__ == '__main__':
		spi = MCP3208(0)
 
		count = 0
		nb=4  #number of aquiring signal
		t = 0.25 #time between two acquiring in seconds. Can be a float value. If nb=3 and t= 2, the qualified value will be given after 6 seconds of continuous signal over 'level'
		level=1500 #under this value, signal is not considered
 		stack = deque([],maxlen=nb)
		
 		sig=-1
		sig_old= -1
		#while count <= 11:
		while True:
			
			val = spi.read(0)
			time.sleep(t)
			#print val
			#print stack
			if val>	level :    # software Squelch
 				stack.append(val)
													
			else :  # Reset counting
				stack = deque([],maxlen=nb)
				sig = -1
			

			
			if len(stack)==nb :
				v=0
				for i in range(0,nb) :
					v+= stack [i]
    					i = i+1
			        meanv= (v/nb)		
			#print len(stack)
			#print stack
				#print meanv
				if 0 <= meanv < 650 : sig=-1
				elif 650 <= meanv < 1950 : sig=0
				elif 1950 <= meanv < 2010 : sig=1
				elif 2010 <= meanv < 2070 : sig=2
				elif 2070 <= meanv < 2130 : sig=3
				elif 2130 <= meanv < 2220 : sig=4
				elif 2150 <= meanv < 2250 : sig=5
				elif 2250 <= meanv < 2310 : sig=6
				elif 2310 <= meanv < 2370 : sig=7
				elif 2370 <= meanv < 2430 : sig=8
				elif 2430 <= meanv < 2550 : sig=9
				elif meanv>=2550 : sig=24
				else : sig=-1


			#print "%d" % sig
			if sig != sig_old :
				print "Changement de niveau de signal =  %d" % sig
				file = open("/etc/svxlink/smeter/smeter.tcl", "w")
				file.write( "set signal " + str(sig) + ";")
				file.close()
				sig_old=sig

				

			


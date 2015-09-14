#!/usr/bin/env python
#------------------------------------------------------
#	This is a module for Plus DS18B20
#		Import this module by 
#			import DS18B20 as Temp
#		Setup by:
#			Temp.setup()
#		Read temperature by:
#			temperature = Temp.read()
#
# 	History: V1.0
#	Release 2015/08/21		Cavon
#------------------------------------------------------
import os

ds18b20 = ''

def setup():
	global ds18b20
	for i in os.listdir('/sys/bus/w1/devices'):
		if i != 'w1-bus-master1':
			ds18b20 = i

def read():
#	global ds18b20
	location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
	tfile = open(location)
	text = tfile.read()
	tfile.close()
	secondline = text.split("\n")[1]
	temperaturedata = secondline.split(" ")[9]
	temperature = float(temperaturedata[2:])
	temperature = temperature / 1000
	return temperature
	
def loop():
	while True:
		if read() != None:
			print "Current temperature : %0.3f C" % read()

def destroy():
	pass

if __name__ == '__main__':
	try:
		setup()
		loop()
	except KeyboardInterrupt:
		destroy()


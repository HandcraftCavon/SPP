#!/usr/bin/env python
from PiPlus import *

def setup():
	global TEMP
	'''
	initial the DS18B20 module with PiPlus.DS18B20()
	'''
	TEMP = DS18B20()

def main():
	while True:
		'''
		DS18B20.read(unit)
		This Function reads the temperature from DS18B20.
		set unit to DS18B20.C for celsius degree
		set unit to DS18B20.F for fahrenheit degree
		'''
		temp_c = TEMP.read()	# Leave empty for default setting TEMP.C
		temp_f = TEMP.read(TEMP.F)
		print 'temperature =', temp_f, 'F'
		print 'temperature =', temp_c, 'C'
		time.sleep(0.2)

def destroy():
	TEMP.destroy()
	GPIO.cleanup()
	
if __name__ == "__main__":
	try:
		setup()
		main()
	except KeyboardInterrupt:
		destroy()
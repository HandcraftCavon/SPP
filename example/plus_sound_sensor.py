#!/usr/bin/env python
from PiPlus import *

def setup():
	global MIC
	'''
	initial the Sound Sensor module with PiPlus.Sound_Sensor()
	'''
	MIC = Sound_Sensor()

def main():
	while True:
		print MIC.read_max()

def destroy():
	MIC.destroy()
	GPIO.cleanup()
	
if __name__ == "__main__":
	try:
		setup()
		main()
	except KeyboardInterrupt:
		destroy()

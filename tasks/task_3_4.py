#!/usr/bin/env python
from PiPlus import *

def setup():
	global MIC, Buzzer
	MIC = Sound_Sensor()
	Buzzer = Buzzer(port='B')

def main():
	while True:
		tmp = abs(MIC.read())
		if tmp > 200:
			Buzzer.on()
		else:
			Buzzer.off()

def destroy():
	MIC.destroy()
	Buzzer.destroy()
	GPIO.cleanup()
	
if __name__ == "__main__":
	try:
		setup()
		main()
	except KeyboardInterrupt:
		destroy()

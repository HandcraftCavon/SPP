#!/usr/bin/env python
from PiPlus import *

def setup():
	ADC.setup()

def loop():
	while True:
		print "Current illumination: ", ADC.read(3)
		time.sleep(0.1)

def destroy():
	ADC.write(0)

if __name__ == "__main__":
	try:
		setup()
		loop()
	except KeyboardInterrupt:
		destroy()

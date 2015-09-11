#!/usr/bin/env python
import PCF8591 as ADC
import time

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

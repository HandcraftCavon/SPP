#!/usr/bin/env python
from PiPlus import *

def setup():
	ADC.setup()

def loop():
	tmpa = 0
	tmpb = 0
	tmpc = 0
	while True:
		a = ADC.read(0)
		b = ADC.read(1)
		c = ADC.read(2)
		if a != tmpa:
			print 'A =', a
			tmpa = a
		if b != tmpb:
			print 'B =', b
			tmpb = b
		if c != tmpc:
			print 'C =', c
			tmpc = c

def destroy():
	ADC.write(0)

if __name__ == "__main__":
	try:
		setup()
		loop()
	except KeyboardInterrupt:
		destroy()

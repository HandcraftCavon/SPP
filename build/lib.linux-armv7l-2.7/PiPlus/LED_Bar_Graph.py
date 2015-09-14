#!/usr/bin/env python
from PiPlus import *

LED = [CE0, D9, D10, D11, D12, D13, D14, D15, D16, CE1]

def setup():
	for i in LED:
		GPIO.setup(i, GPIO.OUT, initial=GPIO.HIGH)

def off():
	for i in LED:
		GPIO.output(i, 1)

def LEDBarGraph(value):
	off()
	for i in range(10):
		if value < 25.5*(i):
			break
		GPIO.output(LED[i], 0)

def destroy():
	GPIO.cleanup()

def loop():
	for value in range(256):
		LEDBarGraph(value)
		print value
		time.sleep(0.1)

if __name__ == "__main__":
	try:
		setup()
		while True:
			loop()
	except KeyboardInterrupt:
		destroy()

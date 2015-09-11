#!/usr/bin/env python

from PiPlus import *

# Pin define (If you plug the Buzzerin Digital Port B, Change D3 to D11)
Buzzer = D4

def setup():
	GPIO.setup(Buzzer, GPIO.OUT, initial=0)

def on():
	GPIO.output(Buzzer, 1)

def off():
	GPIO.output(Buzzer, 0)

def beep(x, times):	# x for dalay time.
	for i in range(times):
		on()
		time.sleep(x)
		off()
		time.sleep(x)

def main():
	time.sleep(1)
	beep(0.5, 4)
	beep(0.25, 8)
	beep(0.125, 16)
	on()
	time.sleep(1)
	destroy()

def destroy():
	GPIO.output(Buzzer, 0)		
	time.sleep(0.5)
	GPIO.cleanup()

if __name__ == "__main__":
	try:
		setup()
		main()
	except KeyboardInterrupt:
		destroy()

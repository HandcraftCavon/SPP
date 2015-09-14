#!/usr/bin/env python
from PiPlus import *

def setup(port='A'):
	global _Buzzer
	if port == 'A':
		_Buzzer = DA4
	if port == 'B':
		_Buzzer = DB4
	GPIO.setup(_Buzzer, GPIO.OUT, initial=0)

def on():
	global _Buzzer
	GPIO.output(_Buzzer, 1)

def off():
	GPIO.output(_Buzzer, 0)

def beep(x, times=1):	# x for dalay time.
	for i in range(times):
		on()
		time.sleep(x)
		off()
		time.sleep(x)

def _test():
	time.sleep(1)
	beep(0.5, 4)
	beep(0.25, 8)
	beep(0.125, 16)
	on()
	time.sleep(1)
	destroy()

def destroy():
	off()
	GPIO.cleanup()

if __name__ == "__main__":
	try:
		setup()
		_test()
	except KeyboardInterrupt:
		destroy()

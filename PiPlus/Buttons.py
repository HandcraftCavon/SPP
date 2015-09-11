#!/usr/bin/env python
from __init__ import *

def setup(port='A'):
	if port == 'A':
		Btn = [D1, D2, D3, D4]
	if port == 'B':
		Btn = [D9, D10, D11, D12]
	GPIO.setup(Btn[0], GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(Btn[1], GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(Btn[2], GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(Btn[3], GPIO.IN, pull_up_down=GPIO.PUD_UP)

	GPIO.add_event_detect(Btn[0], GPIO.FALLING, callback=_button1, bouncetime=20)
	GPIO.add_event_detect(Btn[1], GPIO.FALLING, callback=_button2, bouncetime=20)
	GPIO.add_event_detect(Btn[2], GPIO.FALLING, callback=_button3, bouncetime=20)
	GPIO.add_event_detect(Btn[3], GPIO.FALLING, callback=_button4, bouncetime=20)

def _button1(chn):
	print 'button 1'
def _button2(chn):
	print 'button 2'
def _button3(chn):
	print 'button 3'
def _button4(chn):
	print 'button 4'

def loop():
	pass

def destroy():
	GPIO.cleanup()

if __name__ == '__main__':
	try:
		setup()
		while True:
			loop()
	except KeyboardInterrupt:
		destroy()


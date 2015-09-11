#!/usr/bin/env python
import RPi.GPIO as GPIO
from PiPlus import *

Btn = [D9, D10, D11, D12]

def setup():
	# Set BtnPin's mode is input,
	# and pull up to high lev    el(3.3V)
	GPIO.setup(Btn[0], GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(Btn[1], GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(Btn[2], GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(Btn[3], GPIO.IN, pull_up_down=GPIO.PUD_UP)

	GPIO.add_event_detect(Btn[0], GPIO.FALLING, callback=button1, bouncetime=20)
	GPIO.add_event_detect(Btn[1], GPIO.FALLING, callback=button2, bouncetime=20)
	GPIO.add_event_detect(Btn[2], GPIO.FALLING, callback=button3, bouncetime=20)
	GPIO.add_event_detect(Btn[3], GPIO.FALLING, callback=button4, bouncetime=20)

def button1(chn):
	print 'button 1'
def button2(chn):
	print 'button 2'
def button3(chn):
	print 'button 3'
def button4(chn):
	print 'button 4'

def loop():
	while True:
		pass

def destroy():
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()


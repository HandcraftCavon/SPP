#!/usr/bin/env python
from PiPlus import *

def setup():
	global Buttons
	'''
	initial the Buttons module with PiPlus.Buttons(port='A')
	Set port to A or B, accoring to the port you plug the module in.
	Leave empty for default setting port='A'
	'''
	Buttons = Buttons(port='B')
	'''
	Set callbacks for falling, rising or both edge detect
	GPIO.add_event_detect(Pin, Rising/Falling, callback)
	Change Raise/Falling to 'GPIO.RISING' to detect rising, 
	Change Raise/Falling to 'GPIO.FALlING' to detect falling, 
	Change Raise/Falling to 'GPIO.BOTH' to detect both rising and falling,
	'''
	GPIO.add_event_detect(Buttons.btn1, GPIO.BOTH, callback=btn1)
	GPIO.add_event_detect(Buttons.btn2, GPIO.BOTH, callback=btn2)
	GPIO.add_event_detect(Buttons.btn3, GPIO.BOTH, callback=btn3)
	GPIO.add_event_detect(Buttons.btn4, GPIO.BOTH, callback=btn4)
	

def main():
	while True:
		pass


# Add callback function for each key
def btn1(chn):
	tmp = GPIO.input(Buttons.btn1)
	if tmp == 0:
		print 'Button 1 falling!'
	elif tmp == 1:
		print 'Button 1 rising'

def btn2(chn):
	tmp = GPIO.input(Buttons.btn2)
	if tmp == 0:
		print 'Button 2 falling!'
	elif tmp == 1:
		print 'Button 2 rising'

def btn3(chn):
	tmp = GPIO.input(Buttons.btn3)
	if tmp == 0:
		print 'Button 3 falling!'
	elif tmp == 1:
		print 'Button 3 rising'

def btn4(chn):
	tmp = GPIO.input(Buttons.btn4)
	if tmp == 0:
		print 'Button 4 falling!'
	elif tmp == 1:
		print 'Button 4 rising'

def destroy():
	Buttons.destroy()
	GPIO.cleanup()
	
if __name__ == "__main__":
	try:
		setup()
		main()
	except KeyboardInterrupt:
		destroy()

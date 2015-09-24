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
	Set callbacks for falling, rising or both edge detection
	add_event_detect(btn1_falling=None, btn2_falling=None, btn3_falling=None, btn4_falling=None, 
					 btn1_rising=None,	btn2_rising=None,  btn3_rising=None,  btn4_rising=None, 
					 btn1_both=None, 	btn2_both=None,    btn3_both=None,    btn4_both=None)
	Choose the Button you need, what kind of edge it would be and what callback
	function's name. if youdont need a button, leave it empty. 
	DO NOT DEFINED TWO EDGE DETECTION EVENT FOR ONE BUTTON
	Like this:
	'''
	Buttons.add_event_detect(btn1_falling=btn1, btn2_rising=btn2, btn3_both=btn3)
	

def main():
	while True:
		pass


# Add callback function for each button
def btn1(chn):
	print 'Button 1 falling!'
	
def btn2(chn):
	print 'Button 2 rising'

def btn3(chn):
	tmp = GPIO.input(Buttons.btn3)
	if tmp == 0:
		print 'Button 3 falling!'
	elif tmp == 1:
		print 'Button 3 rising'

def btn4(chn):
	pass

def destroy():
	Buttons.destroy()
	GPIO.cleanup()
	
if __name__ == "__main__":
	try:
		setup()
		main()
	except KeyboardInterrupt:
		destroy()

#!/usr/bin/env python
#------------------------------------------------------
#	This is a program for Plus Joystick Module.
#		This program depend on PCF8591 ADC chip. Plug 
#		this module on Analog Port on Plus Carrier.
#		Import the module by:
#			import Joystick as Joystick
#		Setup by:
#			Joystick.setup(X Pin, Y Pin, Button Pin)
#			# from 0 to 3 as AIN0 to AIN3, or leave it
#			# empty to use default settings.
#		Read status by:
#			a = Joystick.direction()
#			print a
#	History V1.0
#	Release 2015/08/21		Cavon
#------------------------------------------------------
import PCF8591 as ADC 
import time

def setup(xpin = 0, ypin = 1, btpin = 2):
	ADC.setup()					# Setup PCF8591
	global state, x, y, btn
	x = xpin
	y = ypin
	btn = btpin

def direction():	#get joystick result
	state = ['home', 'up', 'down', 'left', 'right', 'pressed']
	i = 0
	#print ADC.read(2)

	if ADC.read(y) >= 250:
		i = 1		#up
	if ADC.read(y) <= 5:
		i = 2		#down

	if ADC.read(x) >= 250:
		i = 3		#left
	if ADC.read(x) <= 5:
		i = 4		#right

	if ADC.read(btn) == 0:
		i = 5		# Button pressed

	if ADC.read(x) - 125 < 15 and ADC.read(x) - 125 > -15	and ADC.read(y) - 125 < 15 and ADC.read(y) - 125 > -15 and ADC.read(btn) == 255:
		i = 0
	
	return state[i]

def loop():
	status = ''
	while True:
		tmp = direction()
		if tmp != None and tmp != status:
			print tmp
			status = tmp

def destroy():
	pass

if __name__ == '__main__':		# Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  	# When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()

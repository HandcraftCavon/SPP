#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
from PiPlus import *
import PCF8591 as ADC

colors = [0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0xFF00FF, 0x00FFFF]
R = 11
G = 12
B = 13

def setup(Rpin, Gpin, Bpin):
	global pins
	global p_R, p_G, p_B
	pins = {'pin_R': Rpin, 'pin_G': Gpin, 'pin_B': Bpin}

	for i in pins:
		# Set pins' mode is output
		GPIO.setup(pins[i], GPIO.OUT)
		# Set pins to high(+3.3V) to off led
		GPIO.output(pins[i], GPIO.HIGH)

	# set Frequece to 2KHz
	p_R = GPIO.PWM(pins['pin_R'], 2000)
	p_G = GPIO.PWM(pins['pin_G'], 1999)
	p_B = GPIO.PWM(pins['pin_B'], 5000)

	# Initial duty Cycle = 0(leds off)
	p_R.start(100)
	p_G.start(100)
	p_B.start(100)

def map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# Turn off all leds
def off():
	for i in pins:
		GPIO.output(pins[i], GPIO.HIGH)

def setColor(col):   # For example : col = 0x11223
	R_val = (col & 0xff0000) >> 16
	G_val = (col & 0x00ff00) >> 8
	B_val = (col & 0x0000ff) >> 0
								
	R_val = map(R_val, 0, 255, 0, 100)
	G_val = map(G_val, 0, 255, 0, 100)
	B_val = map(B_val, 0, 255, 0, 100)
										
	# Change duty cycle
	p_R.ChangeDutyCycle(100-R_val)
	p_G.ChangeDutyCycle(100-G_val)
	p_B.ChangeDutyCycle(100-B_val)

def loop():
	while True:
		for col in colors:
			setColor(col)
			time.sleep(1)

def destroy():
	p_R.stop()
	p_G.stop()
	p_B.stop()
	off()
	GPIO.cleanup()

if __name__ == "__main__":
	try:
		setup(D5, D6, D7)
		loop()
	except KeyboardInterrupt:
		destroy()


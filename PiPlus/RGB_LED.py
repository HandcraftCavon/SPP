#!/usr/bin/env python
from __init__ import *

def setup(port='A'):
	global pins
	global p_R, p_G, p_B
	if port == 'A':
		pins = {'pin_R': D5, 'pin_G': D6, 'pin_B': D7}
	if port == 'B':
		pins = {'pin_R': D13, 'pin_G': D14, 'pin_B': D15}
	for i in pins:
		GPIO.setup(pins[i], GPIO.OUT)   # Set pins' mode is output
		GPIO.output(pins[i], GPIO.HIGH) # Set pins to high(+3.3V) to off led
	
	p_R = GPIO.PWM(pins['pin_R'], 100)  # set Frequece to 2KHz
	p_G = GPIO.PWM(pins['pin_G'], 100)
	p_B = GPIO.PWM(pins['pin_B'], 100)
	
	p_R.start(100)      # Initial duty Cycle = 0(leds off)
	p_G.start(100)
	p_B.start(100)

	ADC.setup()

def off():
	for i in pins:
		GPIO.output(pins[i], GPIO.HIGH)    # Turn off all leds

def setColor(R_val, G_val, B_val):
	R_val = map(R_val, 0, 255, 0, 100)
	G_val = map(G_val, 0, 255, 0, 100)
	B_val = map(B_val, 0, 255, 0, 100)
	
	p_R.ChangeDutyCycle(100-R_val)     # Change duty cycle
	p_G.ChangeDutyCycle(100-G_val)
	p_B.ChangeDutyCycle(100-B_val)

def loop():
	while True:
		R_val = ADC.read(0)
		G_val = ADC.read(1)
		B_val = ADC.read(2)
		setColor(R_val, G_val, B_val)

def destroy():
	p_R.stop()
	p_G.stop()
	p_B.stop()
	off()
	GPIO.cleanup()

if __name__ == "__main__":
	try:
		setup()
		loop()
	except KeyboardInterrupt:
		destroy()

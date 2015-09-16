#!/usr/bin/env python
from PiPlus import *

def setup():
	global RGB
	'''
	initial the RGB LED module with PiPlus.RGB_LED(port='A')
	Set port to A or B, accoring to the port you plug the module in.
	Leave empty for default setting port='A'
	'''
	RGB = RGB_LED(port='B')

def main():
	while True:
		'''
		off() to turn off the RGB.
		'''
		RGB.off()
		
		'''
		on(Red_value, Green_value, Blue_value) is to turn on the RGB 
		in specific RGB value, all value range from 0 to 255
		'''
		for R in range(256):
			RGB.on(R, 0, 0)
			time.sleep(0.01)
		for R in range(256):
			RGB.on(255-R, 0, 0)
			time.sleep(0.01)
			
		for G in range(256):
			RGB.on(0, G, 0)
			time.sleep(0.01)
		for G in range(256):
			RGB.on(0, 255-G, 0)
			time.sleep(0.01)
			
		for B in range(256):
			RGB.on(0, 0, B)
			time.sleep(0.01)
		for B in range(256):
			RGB.on(0, 0, 255-B)
			time.sleep(0.01)
			
		for i in range(768):
			R = abs(i-384)-128
			G = -abs(i-256)+256
			B = -abs(i-512)+256
			if R < 0:
				R = 0
			if G < 0:
				G = 0
			if B < 0:
				B = 0
			RGB.on(R, G, B)
			time.sleep(0.01)
	
def destroy():
	RGB.destroy()
	GPIO.cleanup()

if __name__ == "__main__":
	try:
		setup()
		main()
	except KeyboardInterrupt:
		destroy()

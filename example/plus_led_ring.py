#!/usr/bin/env python
import PiPlus
import time

def setup():
	global Ring
	'''
	initial the LED Ring module with PiPlus.LED_Ring(port='A')
	Set port to A or B, accoring to the port you plug the module in.
	Leave empty for default setting port='A'
	'''
	Ring = PiPlus.LED_Ring(port='b')
	
def main():
	while True:
		''' 
		Breathing light Function: LED_breath(dt=0.03), 
		dt for delta time, Leave empty for default setting 0.03
		'''
		for i in range(4):
			Ring.LED_breath(dt=0.01)
		
		'''
		Spin Function: LED_spin(ring, w=0, dt=0.2)
		w for wise, w=0: clockwise, w=1: anticlockwise
		dt for delta time. Leave w and dt, for default setting 0.03
		.SINGLE, .STAR, .TAIL are three pre set tuple.
		You can make your own tupleas: Mytuple = (0, 60, 0, 60, 60, 60, 0, 60)
		Tuple must be list() before using.
		'''
		ring = list(Ring.SINGLE)
		for i in range(8):
			Ring.LED_spin(ring, dt=0.1)
		
		ring = list(Ring.STAR)	
		for i in range(8):
			Ring.LED_spin(ring, dt=0.3)
			
		ring = list(Ring.TAIL)
		for i in range(8):
			Ring.LED_spin(ring, w=1)
		
		'''
		Meter Fuction: LED_meter(_value, brightness=40)
		_value must be in [0, 255].
		brightness effects all LED. Leave empty for default setting 40
		'''
		for i in range(256):
			Ring.LED_meter(i, brightness=10)
			print i
			time.sleep(0.05)
		for i in range(256):
			Ring.LED_meter(255-i, brightness = 80)
			print 255-i
			time.sleep(0.05)
		

def destroy():
	Ring.destroy()
	GPIO.cleanup()
	
if __name__ == "__main__":
	try:
		setup()
		main()
	except KeyboardInterrupt:
		destroy()

#!/usr/bin/env python

import PiPlus as Plus

ring=Plus.LED_Ring(port="A")

def setup():
	pass

def main():
	while True:
		ring.LED_breath()
		
def destroy():
	ring.destroy()
	GPIO.cleanup()

if __name__ == "__main__":
	try:
		setup()
		main()
	except KeyboardInterrupt:
		destroy()

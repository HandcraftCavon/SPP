#!/usr/bin/env python
import PiPlus
import PiPlus.LED_Ring as Ring

def setup():
	Ring.setup(port='b')
	
def main():
	while True:
		Ring.breath()

def destroy():
	Ring.destroy()
	
if __name__ == "__main__":
	try:
		setup()
		main()
	except KeyboardInterrupt:
		destroy()

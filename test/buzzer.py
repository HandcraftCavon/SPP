#!/usr/bin/env python

import PiPlus as Plus

buzzer=Plus.Buzzer(port="A")

def setup():
	pass

def main():
	while True:
		buzzer.beep(0.4, 4)
def destroy():
	buzzer.destroy()
	GPIO.cleanup()

if __name__ == "__main__":
	try:
		setup()
		main()
	except KeyboardInterrupt:
		destroy()

#!/usr/bin/env python
import PiPlus
import PiPlus.Buzzer as Buzzer
import time

def setup():
	Buzzer.setup()

def main():
	while True:
		print 'on'
		Buzzer.on()
		time.sleep(1)
		print 'off'
		Buzzer.off()
		time.sleep(1)
		print 'beep'
		Buzzer.beep(0.5, times=4)
	
def destroy():
	Buzzer.destroy()
	
if __name__ == "__main__":
	try:
		setup()
		main()
	except KeyboardInterrupt:
		destroy()

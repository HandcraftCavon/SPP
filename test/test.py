#!/usr/bin/env python
import PiPlus


state = 1 # 1 = Red, 2 = Green, 3 = Blue

def ChangeState(chn):
	global state
	state += 1
	if state > 3:
		state = 1

RE = PiPlus.RotaryEncoder(ChangeState, port='B')
RGB = PiPlus.RGBLED(port='A')

def loop():
	Red = 0
	Green = 0
	Blue = 0
	while True:
		if state == 1:
			Red = RE.rotaryDeal(Red)
			if Red > 255:
				Red = 255
			if Red < 0:
				Red = 0

		if state == 2:
			Green = RE.rotaryDeal(Green)
			if Green > 255:
				Green = 255
			if Green < 0:
				Green = 0

		if state == 3:
			Blue = RE.rotaryDeal(Blue)
			if Blue > 255:
				Blue =255
			if Blue < 0:
				Blue = 0
6
		RGB.on(Red, Green, Blue)
		
def destroy():
	RGB.destroy()
	RE.destroy()
	GPIO.cleanup()
	
if __name__ == "__main__":
	try:
		loop()
	except KeyboardInterrupt:
		destroy()

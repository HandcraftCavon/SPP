#!/usr/bin/env python
import PiPlus

RE = PiPlus.RotaryEncoder(port='B')
RGB = PiPlus.RGBLED(port='A')

state = 1 # 1 = Red, 2 = Green, 3 = Blue

def ChangeState(chn):
	global state
	state += 1
	if state == 4:
		state = 1

def loop():
	Red = 0
	Green = 0
	Blue = 0
	while True:
		if state == 1:
			Red = RE.rotaryDeal(Red)
			if Red > 255:
				Red = 255
		if state == 2:
			Green = RE.rotaryDeal(Green)
			if Green > 255:
				Green = 255
		if state == 3:
			Blue = RE.rotaryDeal(Blue)
			if Blue > 255:
				Blue =255
		RED.setColor(Red, Green, Blue)
		
def destroy():
	RGB.destroy()
	RE.destroy()
	GPIO.cleanup()
	
if __name__ == "__main__":
	try:
		loop()
	except KeyboardInterrupt:
		destroy()

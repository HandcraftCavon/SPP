#!/usr/bin/env python
import PiPlus
import time

LCD1602 = PiPlus.LCD1602()

def setup():
	LCD1602.write(0, 0, 'Greetings!!')
	LCD1602.write(1, 1, 'from SunFounder')
	time.sleep(2)

def loop():
	space = '                '
	greetings = 'Thank you for buying SunFounder Sensor Kit for Raspberry! ^_^'
	greetings = space + greetings
	while True:
		tmp = greetings
		for i in range(0, len(greetings)):
			LCD1602.write(0, 0, tmp)
			tmp = tmp[1:]
			time.sleep(0.8)
			LCD1602.clear()

def destroy():
	pass	

if __name__ == "__main__":
	try:
		setup()
		while True:
			pass
	finally:
		destroy()

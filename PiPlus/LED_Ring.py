#!/usr/bin/env python
from PiPlus import *

dot		=	[100,   0,   0,   0,   0,   0,   0,   0]
tail	=	[100,  70,  40,  10,   0,   0,   0,   0]
bright	=	[100, 100, 100, 100, 100, 100, 100, 100]
dark	=	[ 60,  60,  60,  60,  60,  60,  60,  60]
off		=	[  0,   0,   0,   0,   0,   0,   0,   0]
four	=	[  0,  60,   0,  60,   0,  60,   0,  60]

def setup(port='A'):
	global led1, led2, led3, led4, led5, led6, led7, led8
	if port == 'A':
		LED = [DA1, DA2, DA3, DA4, DA5, DA6, DA7, DA8]
	elif port == 'B':
		LED = [DB1, DB2, DB3, DB4, DB5, DB6, DB7, DB8]
	else:
		return os.strerror(errno.EINVAL)
	for x in LED:
		GPIO.setup(x, GPIO.OUT, initial=1)
		
	led1 = GPIO.PWM(LED[0], 100)
	led2 = GPIO.PWM(LED[1], 100)
	led3 = GPIO.PWM(LED[2], 100)
	led4 = GPIO.PWM(LED[3], 100)
	led5 = GPIO.PWM(LED[4], 100)
	led6 = GPIO.PWM(LED[5], 100)
	led7 = GPIO.PWM(LED[6], 100)
	led8 = GPIO.PWM(LED[7], 100)
	led1.start(100)
	led2.start(100)
	led3.start(100)
	led4.start(100)
	led5.start(100)
	led6.start(100)
	led7.start(100)
	led8.start(100)

def LED_onoff(ring):
	global led1, led2, led3, led4, led5, led6, led7, led8
	for i in range(8):
		if ring[i] > 100:
			ring[i] = 100
		if ring[i] < 0:
			ring[i] = 0
	led1.ChangeDutyCycle(100 - ring[0])
	led2.ChangeDutyCycle(100 - ring[1])
	led3.ChangeDutyCycle(100 - ring[2])
	led4.ChangeDutyCycle(100 - ring[3])
	led5.ChangeDutyCycle(100 - ring[4])
	led6.ChangeDutyCycle(100 - ring[5])
	led7.ChangeDutyCycle(100 - ring[6])
	led8.ChangeDutyCycle(100 - ring[7])

def _spin(w, ring):
	if w == 0:
		a = ring[0]
		ring[0] = ring[1]
		ring[1] = ring[2]
		ring[2] = ring[3]
		ring[3] = ring[4]
		ring[4] = ring[5]
		ring[5] = ring[6]
		ring[6] = ring[7]
		ring[7] = a
	if w == 1:
		a = led[7]
		ring[7] = ring[6]
		ring[6] = ring[5]
		ring[5] = ring[4]
		ring[4] = ring[3]
		ring[3] = ring[2]
		ring[2] = ring[1]
		ring[1] = ring[0]
		ring[0] = a
	return ring

def LED_breath(t=0.03):
	breathLED = [0, 0, 0, 0, 0, 0, 0, 0]
	for b in range(200):
		value = math.cos(b*0.0314) * -70 + 70
		for i in range(8):
			if i == 4:
				breathLED[i] = value
			if i == 3 or i == 5:
				breathLED[i] = value - 20
			if i == 2 or i == 6:
				breathLED[i] = value - 40
			if i == 1 or i == 7:
				breathLED[i] = value - 60
			if i == 0:
				breathLED[i] = value - 80
		time.sleep(t)
#		print breathLED
		LED_onoff(breathLED)

def _ledmount(x, brightness):
	mount = [0, 0, 0, 0, 0, 0, 0, 0]
	for i in range(x):
		mount[7-i] = brightness
	return mount

def LED_spin(ring=dot, w=0, t=0.2):
	LED_onoff(LED)
	LED = _spin(w, LED)
	time.sleep(t)

def LED_meter(value, brightness=40):
	ring = [0, 0, 0, 0, 0, 0, 0, 0]
	if value < 0:
		print 'Value =', value, 'Value ERROR, Value should not be negative'
	for i in range(1, 9):
		if value < 32*i:
			ring = _ledmount(i,brightness=brightness)
			break
	for i in range(3):
		ring = _spin(0, ring)
	LED_onoff(ring)
	time.sleep(0.001)

def test():
	for i in range(255):
		LED_meter(i)
		time.sleep(0.1)
		print i

def destroy():
	led1.stop()
	led2.stop()
	led3.stop()
	led4.stop()
	led5.stop()
	led6.stop()
	led7.stop()
	led8.stop()
	GPIO.cleanup()

if __name__ == "__main__":
	try:
		setup(port=1)
		while True:
			test()
	except KeyboardInterrupt:
		destroy()

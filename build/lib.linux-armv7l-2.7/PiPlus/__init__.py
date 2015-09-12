#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import math
import smbus
import time

D0		=	7

D1		=	11
D2		=	12
D3		=	13
D4		=	15
D5		=	16
D6		=	18
D7		=	22
D8		=	29

D9		=	31
D10 	=	33
D11 	=	35
D12 	=	37
D13 	=	32
D14 	=	36
D15 	=	38
D16		=	40
	
CE0		=	24
CE1		=	26

SDA		=	3
SCL		=	5
TXD		=	8
RXD		=	10
MOSI	=	19
MISO	=	21
SCLK	=	23

AIN0	=	0
AIN1	=	1
AIN2	=	2
AIN3	=	3

GPIO.setmode(GPIO.BOARD)

def map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def NormalDistribution(x, u=0, d=1):
	PI = 3.1415926
	E = 2.718281828
	result = (E ** (- ((x-u)**2) / (2*d*d))) / (math.sqrt(2 * PI) * d)
	return result

bus = smbus.SMBus(1)

class PCF8591(object):
	"""PCF8597 on Plus Shield"""
	def __init__(self, Address=0x48, bus=bus):
		super(PCF8591, self).__init__()
		self._address = Address
		self._bus = bus

	def read(self, chn): #channel
		if chn == 0:
			self._bus.write_byte(self._address,0x40)
		if chn == 1:
			self._bus.write_byte(self._address,0x41)
		if chn == 2:
			self._bus.write_byte(self._address,0x42)
		if chn == 3:
			self._bus.write_byte(self._address,0x43)
		self._bus.read_byte(self._address) # dummy read to start conversion
		return self._bus.read_byte(self._address)

	def write(self, val):
		_temp = val # move string value to temp
		_temp = int(_temp) # change string to integer
		# print temp to see on terminal else comment out
		self._bus.write_byte_data(self._address, 0x40, _temp)

class RotaryEncoder(object):
	# Plus Rotary Encoder Module
	def __init__(self, call, port='A'):
		self._port = port
		self._callback = call
		if self._port == 'A':
			self._APin	 = D1    # A Pin
			self._BPin	 = D2    # B Pin
			self._BtnPin = D3    # Button Pin
		if self._port == 'B':
			self._APin	 = D9    # A Pin
			self._BPin	 = D10    # B Pin
			self._BtnPin = D11    # Button Pin

		self._flag = 0
		self._Last_RoB_Status = 0
		self._Current_RoB_Status = 0

		GPIO.setup(self._APin, GPIO.IN)    # input mode
		GPIO.setup(self._BPin, GPIO.IN)
		GPIO.setup(self._BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.add_event_detect(self._BtnPin, GPIO.FALLING, callback=self._callback)

	def rotaryDeal(self, _counter):
		self._Last_RoB_Status = GPIO.input(self._BPin)
		while(not GPIO.input(self._APin)):
			self._Current_RoB_Status = GPIO.input(self._BPin)
			self._flag = 1
		if self._flag == 1:
			self._flag = 0
			if (self._Last_RoB_Status == 0) and (self._Current_RoB_Status == 1):
				_counter = _counter + 1
			if (self._Last_RoB_Status == 1) and (self._Current_RoB_Status == 0):
				_counter = _counter - 1
		return _counter

class RGBLED(object):
	# Plus RGB LED Module
	def __init__(self, port='A'):
		#!/usr/bin/env python
		if port == 'A':
			self._pins = [D5, D6, D7]
		if port == 'B':
			self._pins = [D13, D14, D15]
		for i in self._pins:
			GPIO.setup(i, GPIO.OUT, initial=GPIO.HIGH)   # Set pins' mode is output
		
		self._R = GPIO.PWM(self._pins[0], 100)  # set Frequece to 100Hz
		self._G = GPIO.PWM(self._pins[1], 100)
		self._B = GPIO.PWM(self._pins[2], 100)
		
		self._R.start(100)      # Initial duty Cycle = 1000(leds off)
		self._G.start(100)
		self._B.start(100)

	def off(self):
		for i in self._pins:
			GPIO.output(self._pins[i], GPIO.HIGH)    # Turn off all leds

	def on(self, _R_val, _G_val, _B_val):
		_R_val = map(_R_val, 0, 255, 0, 100)
		_G_val = map(_G_val, 0, 255, 0, 100)
		_B_val = map(_B_val, 0, 255, 0, 100)
		
		self._R.ChangeDutyCycle(100-_R_val)     # Change duty cycle
		self._G.ChangeDutyCycle(100-_G_val)
		self._B.ChangeDutyCycle(100-_B_val)

	def destroy(self):
		self._R.stop()
		self._G.stop()
		self._B.stop()
		off()

class Buzzer(object):
	def __init__(self, port='A'):
		self._port = port
		if self._port == 'A':
			self._Buzzer = D4
		if self._port == 'B':
			self._Buzzer = D12
		GPIO.setup(self._Buzzer, GPIO.OUT, initial=0)

	def on(self):
		GPIO.output(self._Buzzer, 1)

	def off(self):
		GPIO.output(self._Buzzer, 0)

	def beep(self, dt, times=1):	# x for dalay time.
		for i in range(times):
			on()
			time.sleep(dt)
			off()
			time.sleep(dt)

	def destroy(self):
		GPIO.output(self._Buzzer, 0)		
		time.sleep(0.5)
		GPIO.cleanup()

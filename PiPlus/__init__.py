#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import math
import smbus
import time
import os
import logging

D0		=	7

DA1		=	11
DA2		=	12
DA3		=	13
DA4		=	15
DA5		=	16
DA6		=	18
DA7		=	22
DA8		=	29

DB1		=	31
DB2 	=	33
DB3 	=	35
DB4 	=	37
DB5 	=	32
DB6 	=	36
DB7 	=	38
DB8		=	40
	
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

class PCF8591(object):
	"""PCF8597 on Plus Shield"""
	_ADC_bus = smbus.SMBus(1)
	def __init__(self, Address=0x48, bus=_ADC_bus):
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

class LED_Ring(object):
	# Plus LED_Ring module from PiPlus@SunFounder
	def __init__(self, port='A'):
		if port not in ['A', 'a', 'B', 'b']:
			raise ValueError("Unexpected port value {0}, Set port to 'A' or 'B', like: '(port='A')'".format(port))

		if port in ['A', 'a']:
			LED = [DA1, DA2, DA3, DA4, DA5, DA6, DA7, DA8]
		elif port in ['B', 'b']:
			LED = [DB1, DB2, DB3, DB4, DB5, DB6, DB7, DB8]
			
		for x in LED:
			GPIO.setup(x, GPIO.OUT, initial=1)
	
		self.SINGLE		=	(100,   0,   0,   0,   0,   0,   0,   0)
		self.TAIL		=	(100,  70,  40,  10,   0,   0,   0,   0)
		self.STAR		=	(  0,  60,   0,  60,   0,  60,   0,  60)
		self.ALL_BRIGHT	=	(100, 100, 100, 100, 100, 100, 100, 100)
		self.ALL_DARK	=	( 60,  60,  60,  60,  60,  60,  60,  60)
		self.ALL_OFF	=	(  0,   0,   0,   0,   0,   0,   0,   0)

		self._led1 = GPIO.PWM(LED[0], 100)
		self._led2 = GPIO.PWM(LED[1], 100)
		self._led3 = GPIO.PWM(LED[2], 100)
		self._led4 = GPIO.PWM(LED[3], 100)
		self._led5 = GPIO.PWM(LED[4], 100)
		self._led6 = GPIO.PWM(LED[5], 100)
		self._led7 = GPIO.PWM(LED[6], 100)
		self._led8 = GPIO.PWM(LED[7], 100)
		self._led1.start(100)
		self._led2.start(100)
		self._led3.start(100)
		self._led4.start(100)
		self._led5.start(100)
		self._led6.start(100)
		self._led7.start(100)
		self._led8.start(100)

	def LED_onoff(self, _ring):
		for i in range(8):
			if _ring[i] > 100:
				_ring[i] = 100
			if _ring[i] < 0:
				_ring[i] = 0
		self._led1.ChangeDutyCycle(100 - _ring[0])
		self._led2.ChangeDutyCycle(100 - _ring[1])
		self._led3.ChangeDutyCycle(100 - _ring[2])
		self._led4.ChangeDutyCycle(100 - _ring[3])
		self._led5.ChangeDutyCycle(100 - _ring[4])
		self._led6.ChangeDutyCycle(100 - _ring[5])
		self._led7.ChangeDutyCycle(100 - _ring[6])
		self._led8.ChangeDutyCycle(100 - _ring[7])

	def _spin(self, _w, _ring):
		if _w == 0:
			_tmp = _ring[0]
			_ring[0] = _ring[1]
			_ring[1] = _ring[2]
			_ring[2] = _ring[3]
			_ring[3] = _ring[4]
			_ring[4] = _ring[5]
			_ring[5] = _ring[6]
			_ring[6] = _ring[7]
			_ring[7] = _tmp
		if _w == 1:
			_tmp = _ring[7]
			_ring[7] = _ring[6]
			_ring[6] = _ring[5]
			_ring[5] = _ring[4]
			_ring[4] = _ring[3]
			_ring[3] = _ring[2]
			_ring[2] = _ring[1]
			_ring[1] = _ring[0]
			_ring[0] = _tmp
		return _ring

	def LED_breath(self, dt=0.03):
		_breathLED = list(self.ALL_OFF)
		for b in range(200):
			_value = math.cos(b*0.0314) * -70 + 70
			for i in range(8):
				if i == 4:
					_breathLED[i] = _value
				if i == 3 or i == 5:
					_breathLED[i] = _value - 20
				if i == 2 or i == 6:
					_breathLED[i] = _value - 40
				if i == 1 or i == 7:
					_breathLED[i] = _value - 60
				if i == 0:
					_breathLED[i] = _value - 80
			time.sleep(dt)
			self.LED_onoff(_breathLED)

	def _ledmount(self, _x, _brightness):
		_mount = list(self.ALL_OFF)
		for i in range(_x):
			_mount[7-i] = _brightness
		return _mount

	def LED_spin(self, _ring, w=0, dt=0.2):
		_tmp = _ring
		self.LED_onoff(_tmp)
		_tmp = self._spin(w, _tmp)
		time.sleep(dt)
		time.sleep(dt)

	def LED_meter(self, _value, brightness=40):
		_ring = list(self.ALL_OFF)
		if _value < 0:
			raise ValueError("Unexpected '_value' value {0}, _value should not be negective)'".format(_value))
		for i in range(1, 9):
			if _value < 32*i:
				_ring = self._ledmount(i,brightness)
				break
		for i in range(3):
			_ring = self._spin(0, _ring)
		self.LED_onoff(_ring)
		time.sleep(0.001)

	def destroy(self):
		self._led1.stop()
		self._led2.stop()
		self._led3.stop()
		self._led4.stop()
		self._led5.stop()
		self._led6.stop()
		self._led7.stop()
		self._led8.stop()

class Buzzer(object):
	def __init__(self, port='A'):
		self._port = port
		if self._port == 'A' or self._port == 'a':
			self._Buzzer = DA4
		elif self._port == 'B' or self._port == 'b':
			self._Buzzer = DB4
		else:
			print "port should be 'A' or 'B' like: '(port='A')'"
			quit()
		GPIO.setup(self._Buzzer, GPIO.OUT, initial=0)

	def on(self):
		GPIO.output(self._Buzzer, 1)

	def off(self):
		GPIO.output(self._Buzzer, 0)

	def beep(self, dt=0.5, times=1):	# x for dalay time.
		for i in range(times):
			self.on()
			time.sleep(dt)
			self.off()
			time.sleep(dt)

	def destroy(self):
		self.off()

class LED_Bar_Graph(object):
	def __init__(self, port='A'):
			# Plus LED_Bar_Graph module from PiPlus@SunFounder
		if port not in ['A', 'a', 'B', 'b']:
			raise ValueError("Unexpected port value {0}, Set port to 'A' or 'B', like: '(port='A')'".format(port))

		if port in ['A', 'a']:
			self.LED = [CE0, DA1, DA2, DA3, DA4, DA5, DA6, DA7, DA8, CE1]
		elif port in ['B', 'b']:
			self.LED = [CE0, DB1, DB2, DB3, DB4, DB5, DB6, DB7, DB8, CE1]
			
		for x in self.LED:
			GPIO.setup(x, GPIO.OUT, initial=1)

	def off(self):
		for i in self.LED:
			GPIO.output(i, 1)

	def meter(self, value):
		self.off()
		for i in range(10):
			if value < 25.5*i:
				break
			GPIO.output(self.LED[i], 0)
	
	def pulse(self, value):
		self.off()
		for i in range(5):
			if value < 51*i:
				break
			GPIO.output(self.LED[i+5], 0)
			GPIO.output(self.LED[4-i], 0)

	def destroy(self):
		self.off()


class RotaryEncoder(object):
	# Plus Rotary Encoder Module
	def __init__(self, call, port='A'):
		self._port = port
		self._callback = call
		if self._port == 'A':
			self._APin	 = DA1    # A Pin
			self._BPin	 = DA2    # B Pin
			self._BtnPin = DA3    # Button Pin
		if self._port == 'B':
			self._APin	 = DB1    # A Pin
			self._BPin	 = DB2    # B Pin
			self._BtnPin = DB3    # Button Pin

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
			self._pins = [DA5, DA6, DA7]
		if port == 'B':
			self._pins = [DB5, DB6, DB7]
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
		self.off()

class LCD1602(object):
	_LCD_bus = smbus.SMBus(1)
	def __init__(self, BACKGROUND_LIGHT=1, ADDRESS=0x27, _bus=_LCD_bus):
		self._LCD_bus = _bus
		self._LCD_ADDR = ADDRESS
		self._background_light = BACKGROUND_LIGHT
		
		self._send_command(0x33) # Must initialize to 8-line mode at first
		time.sleep(0.005)
		self._send_command(0x32) # Then initialize to 4-line mode
		time.sleep(0.005)
		self._send_command(0x28) # 2 Lines & 5*7 dots
		time.sleep(0.005)
		self._send_command(0x0C) # Enable display without cursor
		time.sleep(0.005)
		self._send_command(0x01) # Clear Screen
		self._LCD_bus.write_byte(self._LCD_ADDR, 0x08)
					
	def _write_data(self, data):
		_tmp = data
		if self._background_light == 1:
			_tmp |= 0x08
		else:
			_tmp &= 0xF7
		self._LCD_bus.write_byte(self._LCD_ADDR, _tmp)

	def _send_data(self, data):
		# Send bit7-4 firstly
		_tmp = data & 0xF0
		_tmp |= 0x05               # RS = 1, RW = 0, EN = 1
		self._write_data(_tmp)
		time.sleep(0.002)
		_tmp &= 0xFB               # Make EN = 0
		self._write_data(_tmp)

		# Send bit3-0 secondly
		_tmp = (data & 0x0F) << 4
		_tmp |= 0x05               # RS = 1, RW = 0, EN = 1
		self._write_data(_tmp)
		time.sleep(0.002)
		_tmp &= 0xFB               # Make EN = 0
		self._write_data(_tmp)
	
	def _send_command(self, comm):
		# Send bit7-4 firstly
		_tmp = comm & 0xF0
		_tmp |= 0x04               # RS = 0, RW = 0, EN = 1
		self._write_data(_tmp)
		time.sleep(0.002)
		_tmp &= 0xFB               # EN = 0
		self._write_data(_tmp)

		# Send bit3-0 secondly
		_tmp = (comm & 0x0F) << 4
		_tmp |= 0x04               # RS = 0, RW = 0, EN = 1
		self._write_data(_tmp)
		time.sleep(0.002)
		_tmp &= 0xFB               # EN = 0
		self._write_data(_tmp)

	def clear(self):
		self._send_command(0x01) # Clear Screen

	def _openlight(self):  # Enable the backlight
		self._LCD_bus.write_byte(self._LCD_ADDR,0x08)
		self._LCD_bus.close()

	def write(self, x, y, str):
		if x < 0:
			x = 0
		if x > 15:
			x = 15
		if y <0:
			y = 0
		if y > 1:
			y = 1

		# Move cursor
		_addr = 0x80 + 0x40 * y + x
		self._send_command(_addr)

		for chr in str:
			self._send_data(ord(chr))

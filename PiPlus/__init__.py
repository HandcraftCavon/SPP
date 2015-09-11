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

# PCF8591:
class PCF8597(object):
	"""PCF8597 on Plus Shield"""
	def __init__(self, Address=0x48, bus=bus):
		super(PCF8597, self).__init__()
		self._address = Address
		#self._bus = smbus.SMBus(1)

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

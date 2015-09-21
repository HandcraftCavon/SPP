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
	# PCF8597 on Plus Shield
	_ADC_bus = smbus.SMBus(1) # or bus = smbus.SMBus(0) for Revision 1 boards
	def __init__(self, Address=0x48, _bus=_ADC_bus):
		super(PCF8591, self).__init__()
		self._address = Address
		self._bus = _bus

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
	# Plus LED Ring module of PiPlus from SunFounder
	def __init__(self, port='A'):
		if port not in ['A', 'a', 'B', 'b']:
			raise ValueError("Unexpected port value {0}, Set port to 'A' or 'B', like: '(port='A')'".format(port))

		if port in ['A', 'a']:
			LED = [DA1, DA2, DA3, DA4, DA5, DA6, DA7, DA8]
		elif port in ['B', 'b']:
			LED = [DB1, DB2, DB3, DB4, DB5, DB6, DB7, DB8]
			
		for x in LED:
			GPIO.setup(x, GPIO.OUT, initial=1)

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
		
		
	def SINGLE(self):
		return [100,   0,   0,   0,   0,   0,   0,   0]
		
	def ARC(self):
		return [100, 100, 100,   0,   0,   0,   0,   0]
		
	def STAR(self):
		return [  0,  60,   0,  60,   0,  60,   0,  60]
		
	def ALL_BRIGHT(self):
		return [100, 100, 100, 100, 100, 100, 100, 100]
		
	def ALL_DARK(self):
		return [ 60,  60,  60,  60,  60,  60,  60,  60]
		
	def ALL_OFF(self):
		return [  0,   0,   0,   0,   0,   0,   0,   0]


	def on(self, _ring):
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

	def _spin(self, _w, _ring): # w=0: clockwise, w=1: anticlockwise
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

	def breath(self, dt=0.03):
		_breathLED = self.ALL_OFF()
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
			self.on(_breathLED)

	def _ledmount(self, _x, _brightness):
		_mount = self.ALL_OFF()
		for i in range(_x):
			_mount[7-i] = _brightness
		return _mount

	def spin(self, _ring, w=0, dt=0.2):
		_tmp = _ring
		self.on(_tmp)
		_tmp = self._spin(w, _tmp)
		time.sleep(dt)

	def meter(self, _value, brightness=40):
		_ring = self.ALL_OFF()
		if _value < 0:
			raise ValueError("Unexpected '_value' value {0}, _value should not be negective)'".format(_value))
		for i in range(1, 9):
			if _value < 32*i:
				_ring = self._ledmount(i,brightness)
				break
		for i in range(3):
			_ring = self._spin(0, _ring)
		self.on(_ring)
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
	# Plus Buzzer module of PiPlus from SunFounder
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
	# Plus LED Bar Graph module of PiPlus from SunFounder
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

class RGB_LED(object):
	# Plus RGB LED module of PiPlus from SunFounder
	def __init__(self, port='A'):
		#!/usr/bin/env python
		if port not in ['A', 'a', 'B', 'b']:
			raise ValueError("Unexpected port value {0}, Set port to 'A' or 'B', like: '(port='A')'".format(port))

		if port in ['A', 'a']:
			self._pins = [DA5, DA6, DA7]
		elif port in ['B', 'b']:
			self._pins = [DB5, DB6, DB7]
		for i in self._pins:
			GPIO.setup(i, GPIO.OUT, initial=GPIO.HIGH)   # Set _pins mode to output
		
		self._R = GPIO.PWM(self._pins[0], 100)  # set Frequece to 100Hz
		self._G = GPIO.PWM(self._pins[1], 100)
		self._B = GPIO.PWM(self._pins[2], 100)
		
		self._R.start(100)      # Initial duty Cycle = 100(leds off)
		self._G.start(100)
		self._B.start(100)

	def off(self):
		for i in self._pins:
			GPIO.output(i, GPIO.HIGH)    # Turn off all LEDs

	def rgb(self, _R_val, _G_val, _B_val):
		_R_val = map(_R_val, 0, 255, 0, 100)
		_G_val = map(_G_val, 0, 255, 0, 100)
		_B_val = map(_B_val, 0, 255, 0, 100)
		
		self._R.ChangeDutyCycle(100-_R_val)
		self._G.ChangeDutyCycle(100-_G_val)
		self._B.ChangeDutyCycle(100-_B_val)
		
	def breath(self, _R_val, _G_val, _B_val, dt = 0.01):
		for x in range(628):
			y = -math.cos(x/100.0)*128+128
			_R = map(y, 0, 256, 0, _R_val)
			_G = map(y, 0, 256, 0, _G_val)
			_B = map(y, 0, 256, 0, _B_val)
			self.rgb(_R, _G, _B)
			time.sleep(dt)
			
	def hsb(self, _h, _s = 1, _b = 1):
		_hi = (_h/60)%6
		_f = _h / 60.0 - _hi
		_p = _b * (1 - _s)
		_q = _b * (1 - _f * _s)
		_t = _b * (1 - (1 - _f) * _s)
		
		if _hi == 0:
			_R_val = _b
			_G_val = _t
			_B_val = _p
		if _hi == 1:
			_R_val = _q
			_G_val = _b
			_B_val = _p
		if _hi == 2:
			_R_val = _p
			_G_val = _b
			_B_val = _t
		if _hi == 3:
			_R_val = _p
			_G_val = _q
			_B_val = _b
		if _hi == 4:
			_R_val = _t
			_G_val = _p
			_B_val = _b
		if _hi == 5:
			_R_val = _b
			_G_val = _p
			_B_val = _q
			
		try:
			self.rgb(_R_val*255.0, _G_val*255.0, _B_val*255.0)
		except:
			print _R_val, _G_val, _B_val
		'''
		R = abs(i-384)-128
		G = -abs(i-256)+256
		B = -abs(i-512)+256
		if R < 0:
			R = 0
		if G < 0:
			G = 0
		if B < 0:
			B = 0
		self.on(R, G, B)
		'''
	def destroy(self):
		self.off()
		self._R.stop()
		self._G.stop()
		self._B.stop()

class Buttons(object):
	# Plus Buttons module of PiPlus from SunFounder	
	def __init__(self, port='A'):
		#!/usr/bin/env python
		if port not in ['A', 'a', 'B', 'b']:
			raise ValueError("Unexpected port value {0}, Set port to 'A' or 'B', like: '(port='A')'".format(port))

		if port in ['A', 'a']:
			self.btn1 = DA1
			self.btn2 = DA2
			self.btn3 = DA3
			self.btn4 = DA4
		elif port in ['B', 'b']:
			self.btn1 = DB1
			self.btn2 = DB2
			self.btn3 = DB3
			self.btn4 = DB4
		
		GPIO.setup(self.btn1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.btn2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.btn3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.btn4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	def add_event_detect(self, btn1_falling=None, btn2_falling=None, btn3_falling=None, btn4_falling=None, btn1_rising=None, btn2_rising=None, btn3_rising=None, btn4_rising=None, btn1_both=None, btn2_both=None, btn3_both=None, btn4_both=None):
		_c_btn1 = [btn1_falling, btn1_rising, btn1_both]
		_c_btn2 = [btn2_falling, btn2_rising, btn2_both]
		_c_btn3 = [btn3_falling, btn3_rising, btn3_both]
		_c_btn4 = [btn4_falling, btn4_rising, btn4_both]
		
		if _c_btn1.count(None) < 2 or _c_btn2.count(None) < 2 or _c_btn3.count(None) < 2 or _c_btn4.count(None) < 2:
			raise RuntimeError('Conflicting edge detection events, The same button should not be defined as two different edge detection events')
		if btn1_falling != None:
			GPIO.add_event_detect(self.btn1, GPIO.FALLING, callback=btn1_falling)
		if btn2_falling != None:
			GPIO.add_event_detect(self.btn2, GPIO.FALLING, callback=btn2_falling)
		if btn3_falling != None:
			GPIO.add_event_detect(self.btn3, GPIO.FALLING, callback=btn3_falling)
		if btn4_falling != None:
			GPIO.add_event_detect(self.btn4, GPIO.FALLING, callback=btn4_falling)
			
		if btn1_rising != None:
			GPIO.add_event_detect(self.btn1, GPIO.RISING, callback=btn1_rising)
		if btn2_rising != None:
			GPIO.add_event_detect(self.btn2, GPIO.RISING, callback=btn2_rising)
		if btn3_rising != None:
			GPIO.add_event_detect(self.btn3, GPIO.RISING, callback=btn3_rising)
		if btn4_rising != None:
			GPIO.add_event_detect(self.btn4, GPIO.RISING, callback=btn4_rising)

		if btn1_both != None:
			GPIO.add_event_detect(self.btn1, GPIO.BOTH, callback=btn1_both)
		if btn2_both != None:
			GPIO.add_event_detect(self.btn2, GPIO.BOTH, callback=btn2_both)
		if btn3_both != None:
			GPIO.add_event_detect(self.btn3, GPIO.BOTH, callback=btn3_both)
		if btn4_both != None:
			GPIO.add_event_detect(self.btn4, GPIO.BOTH, callback=btn4_both)
		
	def destroy(self):
		pass

class Rotary_Encoder(object):
	# Plus Rotary Encoder module of PiPlus from SunFounder
	def __init__(self, port='A'):
		self._port = port
		if port not in ['A', 'a', 'B', 'b']:
			raise ValueError("Unexpected port value {0}, Set port to 'A' or 'B', like: '(port='A')'".format(port))

		if port in ['A', 'a']:
			self._APin	 = DA1    # A Pin
			self._BPin	 = DA2    # B Pin
			self.BTN = DA3    # Button Pin
		elif port in ['B', 'b']:
			self._APin	 = DB1    # A Pin
			self._BPin	 = DB2    # B Pin
			self.BTN = DB3    # Button Pin

		self._flag = 0
		self._Last_RoB_Status = 0
		self._Current_RoB_Status = 0

		GPIO.setup(self._APin, GPIO.IN)    # input mode
		GPIO.setup(self._BPin, GPIO.IN)
		GPIO.setup(self.BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	def rotarydeal(self, _counter):
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

class LCD1602(object):
	# Plus LCD1602 module of PiPlus from SunFounder
	_LCD_bus = smbus.SMBus(1) # or bus = smbus.SMBus(0) for Revision 1 boards
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

	def _openlight(self):  # Enable the backlight
		self._LCD_bus.write_byte(self._LCD_ADDR,0x08)
		self._LCD_bus.close()

	def clear(self):
		self._send_command(0x01) # Clear Screen

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

	def destroy(self):
		self.clear()

class Motion_Sensor(object):
	# Plus Motion Sensor of PiPlus from SunFounder
	_MS_bus = smbus.SMBus(1) # or bus = smbus.SMBus(0) for Revision 1 boards

	def __init__(self, _bus=_MS_bus):
		# Power management registers
		self._power_mgmt_1 = 0x6b
		self._power_mgmt_2 = 0x6c
		self._MS_bus = _bus
		self._address = 0x69
		# Now wake the 6050 up as it starts in sleep mode
		self._MS_bus.write_byte_data(self._address, self._power_mgmt_1, 0)
		
	def _read_byte(self, _adr):
		return self._MS_bus.read_byte_data(self._address, _adr)

	def _read_word(self, _adr):
		_high = self._MS_bus.read_byte_data(self._address, _adr)
		_low = self._MS_bus.read_byte_data(self._address, _adr+1)
		_val = (_high << 8) + _low
		return _val

	def _read_word_2c(self, _adr):
		_val = self._read_word(_adr)
		if (_val >= 0x8000):
			return -((65535 - _val) + 1)
		else:
			return _val

	def _dist(self, _a, _b):
		return math.sqrt((_a * _a) + (_b * _b))

	def _get_x_rotation(self, _x, _y, _z):
		_radians = math.atan2(_y, self._dist(_x, _z))
		return math.degrees(_radians)
		
	def _get_y_rotation(self, _x, _y, _z):
		_radians = math.atan2(_x, self._dist(_y, _z))
		return -math.degrees(_radians)

	def _get_z_rotation(self, _x, _y, _z):
		_radians = math.atan2(_z, self._dist(_x, _y))
		return math.degrees(_radians)
		
	def get_gyro(self):
		_gyro_xout = self._read_word_2c(0x43)
		_gyro_yout = self._read_word_2c(0x45)
		_gyro_zout = self._read_word_2c(0x47)

		return _gyro_xout, _gyro_yout, _gyro_zout
		
	def get_scaled_gyro(self):
		_gyro_xout, _gyro_yout, _gyro_zout = self.get_gyro()
		
		return (_gyro_xout / 131.0), (_gyro_yout / 131.0), (_gyro_zout / 131.0)

	def get_accel(self):
		_accel_xout = self._read_word_2c(0x3b)
		_accel_yout = self._read_word_2c(0x3d)
		_accel_zout = self._read_word_2c(0x3f)
		
		return _accel_xout, _accel_yout, _accel_zout
		
	def get_scaled_accel(self):
		_accel_xout, _accel_yout, _accel_zout = self.get_accel()
		
		_accel_xout_scaled = _accel_xout / 16384.0
		_accel_yout_scaled = _accel_yout / 16384.0
		_accel_zout_scaled = _accel_zout / 16384.0

		return _accel_xout_scaled, _accel_yout_scaled, _accel_zout_scaled
	
	def get_rotation(self):
		_x, _y, _z = self.get_scaled_accel()
		return self._get_x_rotation(_x, _y, _z), self._get_y_rotation(_x, _y, _z), self._get_z_rotation(_x, _y, _z)
	
	def destroy():
		pass


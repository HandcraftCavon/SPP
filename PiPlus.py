#!/usr/bin/env python
import RPi.GPIO as GPIO
import PCF8591 as ADC

D0 = 4
D1 = 17
D2 = 18
D3 = 27
D4 = 22
D5 = 23
D6 = 24
D7 = 25
D8 = 5

D9 = 6
D10 = 13
D11 = 19
D12 = 26
D13 = 12
D14 = 16
D15 = 20
D16 = 21

CE0 = 8
CE1 = 7
GPIO.setmode(GPIO.BCM)


#!/usr/bin/env python
import RPi.GPIO as GPIO
import PCF8591 as ADC
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

GPIO.setmode(GPIO.BOARD)


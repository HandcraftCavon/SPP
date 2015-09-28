#!/usr/bin/env python

from PiPlus import *

DT = DS1307()
while True:
	print DT.get_datetime()

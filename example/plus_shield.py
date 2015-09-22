#!/usr/bin/env python

from PiPlus import *

DT = DS1307()

print DT.get_datetime()

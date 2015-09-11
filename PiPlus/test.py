from plus_led_ring import *
import PCF8591 as ADC

ADC.setup()
setup()

while True:
	value = ADC.read(3)
	print value
	LED_meter(value)

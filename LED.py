import RPi.GPIO as GPIO
import time
import random

red = 29
green = 32
blue = 31


GPIO.setmode(GPIO.BOARD)
GPIO.setup([red, green, blue], GPIO.OUT)
GPIO.output([red, green, blue], GPIO.LOW)

if not random.randint(0, 1000):
	GPIO.output(blue, GPIO.HIGH)
else:
	GPIO.output(green, GPIO.HIGH)
time.sleep(2)
GPIO.output([red, green, blue], GPIO.LOW)
time.sleep(2)

GPIO.cleanup([red, green, blue])

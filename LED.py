import RPi.GPIO as GPIO
import time
import random

red = 23
green = 22
blue = 24
rgb = [red, green, blue]

GPIO.setmode(GPIO.BCM)
GPIO.setup(rgb, GPIO.OUT)
GPIO.output(rgb, GPIO.LOW)

#Red
GPIO.output(red, GPIO.HIGH)
time.sleep(2)
GPIO.output(rgb, GPIO.LOW)

#Green
GPIO.output(green, GPIO.HIGH)
time.sleep(2)
GPIO.output(rgb, GPIO.LOW)

#Blue
GPIO.output(blue, GPIO.HIGH)
time.sleep(2)
GPIO.output(rgb, GPIO.LOW)

#White
GPIO.output(rgb, GPIO.HIGH)
time.sleep(2)
GPIO.output(rgb, GPIO.LOW)

GPIO.cleanup()

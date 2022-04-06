import RPi.GPIO as GPIO
import time
#red at pin 5 (29)
#blue at pin 6 (31)
#green at pin 12 (32)


GPIO.SetupGPIO
GPIO.PinMode(5,GPIO.OUTPUT)
GPIO.PinMode(6,GPIO.OUTPUT)
GPIO.PinMode(12,GPIO.OUTPUT)
 
GPIO.DigitalWrite(5,GPIO.OFF)
GPIO.DigitalWrite(6,GPIO.OFF)
GPIO.DigitalWrite(12,GPIO.OFF)

GPIO.DigitalWrite(5,GPIO.ON)
GPIO.DigitalWrite(6,GPIO.ON)
GPIO.DigitalWrite(12,GPIO.ON)

time.sleep(10)

GPIO.DigitalWrite(5,GPIO.OFF)
GPIO.DigitalWrite(6,GPIO.OFF)
GPIO.DigitalWrite(12,GPIO.OFF)


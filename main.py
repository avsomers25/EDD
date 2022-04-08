import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time 
import sys
import datetime
reader = SimpleMFRC522()

try:
    while True:
        print("Hold a tag near the reader")
        id, text = reader.read()
        cur_time = datetime.datetime.now() 
        print("ID: {}\nText: {}\nTime:".format(id,text, cur_time))
        sleep(5)
except KeyboardInterrupt:
    GPIO.cleanup()
    raise
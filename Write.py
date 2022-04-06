import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:	
	text = input("new data:")
	print("NOW PLACE TAG TO WRTE")
	reader.write(text)
	print("written")
finally:
	GPIO.cleanup()

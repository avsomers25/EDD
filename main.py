#Import necessary libraries
import RPi.GPIO as GPIO #For the LED
from mfrc522 import SimpleMFRC522 #For the RFID communication
import asyncio #For managing the queue
import datetime #Current time
import pytz #Timezones
import time #Sleep

#Setup LED
LEDR = 23
LEDG = 22
LEDB = 24
LED = [LEDR, LEDG, LEDB]
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, GPIO.LOW)

#Setup RFID
reader = SimpleMFRC522()

async def reporter(queue):
	while True:
		text, tagTime = await queue.get()
		print(f"{text} signed out at {tagTime}")
		queue.task_done()

async def readLoop():
	#Setup queue
	queue = asyncio.Queue()
	asyncio.create_task(reporter(queue))
	try:
		while True:
			print("Awaiting tag")
			GPIO.output(LED, GPIO.LOW)
			id, text = reader.read()
			GPIO.output(LED, (GPIO.HIGH, GPIO.HIGH, GPIO.LOW))
			tagTime = datetime.datetime.now(pytz.timezone("America/New_York"))
			await queue.put((text, tagTime))
			GPIO.output(LEDR, GPIO.LOW)
			time.sleep(2)
	except KeyboardInterrupt:
		GPIO.output(LED, (GPIO.LOW, GPIO.LOW, GPIO.HIGH))
		await queue.join()
		GPIO.output(LED, (GPIO.LOW, GPIO.HIGH, GPIO.LOW))
		time.sleep(1)
		GPIO.cleanup()

asyncio.run(readLoop())

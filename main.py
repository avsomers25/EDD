#Import necessary libraries
 #For the LED
from mfrc522 import SimpleMFRC522 #For the RFID communication
import multiprocessing #For managing the queue
import datetime #Current time
import pytz #Timezones
import time #Sleep
import csv #CSV 

def IDtoNAME(idnum):
    with open('student_ids.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        idnum = str(idnum)
        for row in spamreader:
            if row[0] == idnum:
                name = row[1]
                break

    return name
	
def report(child):
	while True:
		try:
			text, tagTime = child.recv()
			if text == "STOP":
				break
			else:
				#Need to make the actual sheets functions here
				time.sleep(5)
				print(f"{text} signed out at {tagTime}")
		#Need to figure out a better stop function
		except KeyboardInterrupt:
			pass

if __name__ == "__main__":
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

	#Setup queue
	parent, child = multiprocessing.Pipe()
	reporterThread = multiprocessing.Process(target=report, args=(child,))
	reporterThread.start()
	try:
		while True:
			print("Awaiting tag")
			GPIO.output(LED, GPIO.LOW)
			id, text = reader.read()
			#Need to add error handling here
			GPIO.output(LED, (GPIO.HIGH, GPIO.HIGH, GPIO.LOW))
			tagTime = datetime.datetime.now(pytz.timezone("America/New_York"))
			parent.send((text, tagTime))
			GPIO.output(LEDR, GPIO.LOW)
			time.sleep(1)
	except KeyboardInterrupt:
		GPIO.output(LED, (GPIO.LOW, GPIO.LOW, GPIO.HIGH))
		parent.send(("STOP", ""))
		reporterThread.join()
		parent.close()
		GPIO.output(LED, (GPIO.LOW, GPIO.HIGH, GPIO.LOW))
		time.sleep(1)
		GPIO.cleanup()

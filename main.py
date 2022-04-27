#Import necessary libraries
import RPi.GPIO as GPIO #LED Interface
from mfrc522 import SimpleMFRC522 #RFID Communication
import multiprocessing #Queue
import datetime #Current Time
import pytz #Timezones
import time #Sleep
import csv #CSV Reader

#Google Sheets libraries
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def id2name(idnum):
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
				sid = text.rstrip()
				name = id2name(sid)
				#Need to make the actual sheets functions here
				time.sleep(5)
				print(f"{sid}:{name} signed out at {tagTime}")
		#Need to figure out a better stop function
		except KeyboardInterrupt:
			pass

if __name__ == "__main__":
	#Setup Google Sheets
	SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
	SPREADSHEET_ID = '1QbBu2w8edM74y4hWAWeEmzG8FQika9F9uLVoelOAIFY'
	creds = None
	if os.path.exists('token.json'):
		creds = Credentials.from_authorized_user_file('token.json', SCOPES)
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		with open('token.json', 'w') as token:
			token.write(creds.to_json())

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

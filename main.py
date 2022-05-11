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

#Convert student id from PICC to name in csv
def id2name(idnum):
    with open('student_ids.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        idnum = str(idnum)
        for row in spamreader:
            if row[0] == idnum:
                name = row[1]
                break
    return name

#Queue that handles sending scans to the spreadsheet
#Runs asynchronously from the reader so that both can operate at the same time
def report(child, creds):
	SPREADSHEET_ID = '1QbBu2w8edM74y4hWAWeEmzG8FQika9F9uLVoelOAIFY'
	while True:
		try:
			text, tagTime = child.recv()
			if text == "STOP":
				break
			else:
				sid = text.rstrip()
				name = id2name(sid)
				service = build('sheets', 'v4', credentials=creds)
				result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range="Sheet1", majorDimension="COLUMNS", valueRenderOption="UNFORMATTED_VALUE", dateTimeRenderOption="FORMATTED_STRING").execute()['values']
				direction = "Out"
				index = -1
				for i in range(len(result[0])):
					if str(result[4][i]) == sid and result[0][i][:11] == tagTime[:11]:
						index = i
				if index >= 0 and result[3][index] == "Out":
					direction = "In"

				values = [[tagTime, name.split(' ')[1], name.split(' ')[0], direction, sid]]
				body = {'values': values}
				service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID, range="A2", valueInputOption="RAW", body=body).execute()
		except KeyboardInterrupt:
			pass

if __name__ == "__main__":
	#Setup Google Sheets
	SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
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
	reporterThread = multiprocessing.Process(target=report, args=(child,creds))
	reporterThread.start()
	try:
		#Read loop
		while True:
			print("Awaiting tag")
			GPIO.output(LED, GPIO.LOW)
			id, text = reader.read()
			GPIO.output(LED, (GPIO.HIGH, GPIO.HIGH, GPIO.LOW))
			tagTime = datetime.datetime.now(pytz.timezone("America/New_York")).strftime("%b %d, %Y at %H:%M:%S %Z")
			parent.send((text, tagTime))
			GPIO.output(LEDR, GPIO.LOW)
			time.sleep(2.5)
	#Shutdown protocol
	except KeyboardInterrupt:
		GPIO.output(LED, (GPIO.LOW, GPIO.LOW, GPIO.HIGH))
		parent.send(("STOP", ""))
		reporterThread.join()
		parent.close()
		GPIO.output(LED, (GPIO.LOW, GPIO.HIGH, GPIO.LOW))
		time.sleep(1)
		GPIO.cleanup()

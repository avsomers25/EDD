import csv



#Import necessary libraries
 #For the LED
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
				print(f"\n {text} signed out at {tagTime}")
		#Need to figure out a better stop function
		except KeyboardInterrupt:
			print("KEYBOARD THING")
			#Need to make the actual sheets functions here
			time.sleep(5)
			print(f"\n {text} signed out at {tagTime}")
			pass

if __name__ == "__main__":
	#Setup LED
	LEDR = 23
	LEDG = 22
	LEDB = 24
	LED = [LEDR, LEDG, LEDB]


	#Setup queue
	parent, child = multiprocessing.Pipe()
	reporterThread = multiprocessing.Process(target=report, args=(child,))
	reporterThread.start()

	try:
		while True:
			text = input("INPUT THING")
			tagTime = "4"
			#tagTime = datetime.datetime.now(pytz.timezone("America/New_York"))
			parent.send((text, tagTime))
			time.sleep(1)
	except KeyboardInterrupt:
		print("KEYBOARD STOP")
		parent.send(("STOP", ""))
		reporterThread.join()
		parent.close()
		time.sleep(1)
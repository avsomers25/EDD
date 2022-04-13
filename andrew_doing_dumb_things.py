import csv



def IDtoNAME(idnum):
    with open('student_ids.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            if row[0] == str(idnum):
                name = row[1]
                print(name)

    return name


print(IDtoNAME(30042))
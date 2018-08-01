import csv

#column values from boris export
timeStamp = 0
eventName = 5
eventType = 8

#initializing rater 1
rater1 = {}
rater1["events"] = []
rater1["eventProfile"] = []

#initializing rater2
rater2 = {}
rater2["events"] = []
rater2["eventProfile"] = []

finalProfile = []

#collects all the event information from the file provided
def collectEvents(file, rater):
    #set the rater that we are collecting from
    r = rater2
    if rater == 1:
        r = rater1
    #opens the tsv and reads the lines
    with open(file) as tsv:
        for line in csv.reader(tsv, delimiter="\t"):
            event_data = {}
            #convert to float then floor
            event_data["eventName"] = line[eventName]
            event_data["timeStamp"] = int(float(line[timeStamp]))
            event_data["eventType"] = line[eventType]
            #add to events
            r["events"].append(event_data)

#find the events stop
def eventStop(r, e, pos):
    for x in range(pos, len(r["events"])):
        c = r["events"][x] #the event being checked
        if c["eventName"] == e["eventName"] and c["eventType"] == 'STOP':
            return c["timeStamp"]
    return -1

#creates a valid profile of the raters events that can be passed to SPSS
def createProfile(rater):
    #set the rater that we are collecting from
    r = rater2
    if rater == 1:
        r = rater1
    #loop through the raters logged events
    events = r["events"]
    for x in range(0,len(events)):
        e = events[x]
        #handle event start
        if e["eventType"] == 'START':
            startTime = e["timeStamp"]
            endTime = eventStop(r, e, x)
            assert (endTime != -1)
            for i in range(startTime, endTime):
                r["eventProfile"].append((i , e["eventName"]))

def alignProfiles():
    pos1 = 0
    pos2 = 0
    acc  = 0
    time = 0
    endTime1 = rater1["eventProfile"][len(rater1["eventProfile"]) - 1][0]
    endTime2 = rater2["eventProfile"][len(rater2["eventProfile"]) - 1][0]
    maxTime = max(endTime1, endTime2)
    done1 = False
    done2 = False
    while time < maxTime:
        #set rater data
        rater_data = {}
        rater_data['rater 1'] = "None"
        rater_data['rater 2'] = "None"
        #check for end
        if pos1 >= len(rater1["eventProfile"]):
            done1 = True
            event1 = (0, "None")
        else:
            event1 = rater1["eventProfile"][pos1]

        if pos2 >= len(rater2["eventProfile"]):
            done2 = True
            event2 = (0, "None")
        else:
            event2 = rater2["eventProfile"][pos2]

        if not done1 and not done2:
            time = min(event1[0],event2[0])
        elif done1:
            time = event2[0]
        elif done2:
            time = event1[0]

        if event1[0] == time:
            rater_data['rater 1'] = event1[1]
            pos1 += 1
        if event2[0] == time:
            rater_data['rater 2'] = event2[1]
            pos2 += 1
        finalProfile.append(rater_data)

def exportData():
    with open("raterTimelines.csv", "w+") as output:
        fieldnames = ['rater 1','rater 2']
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for e in finalProfile:
            writer.writerow(e)


file_name = raw_input("file name: ")
collectEvents("Rater1/" + file_name + ".tsv", 1)
collectEvents("Rater2/" + file_name + ".tsv", 2)
createProfile(1)
createProfile(2)
alignProfiles()
exportData()

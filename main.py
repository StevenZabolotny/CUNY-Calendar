import os.path
import calenderScrape
import CunyFirstScraper
import eventprep
import pickle
from apiclient import discovery
import httplib2

def updateCalendar(uname, credentials):
    if (not(os.path.isfile("calendar.txt"))):
        calenderScrape.scrapeCalender()

    http_auth = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http_auth)
        
    classes = CunyFirstScraper.scrapeCFirst(uname)
    calendar = open("calendar.txt", "r")
    line = calendar.readline()
    while(line != ""):
        for classinfo in classes:
            event = eventprep.eventPrep(classinfo, line)
            print(event)
            if (event != None):
                service.events().insert(calendarId="primary", body=event).execute()
        line = calendar.readline()
    return True

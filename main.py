import os.path
import calenderScrape
import CunyFirstScraper
import eventprep
import pickle
from apiclient import discovery
from apiclient.http import BatchHttpRequest
import httplib2


def callbackPlaceholder(request_id, response, exception):
    pass

def updateCalendar(uname, credentials):
    if (not(os.path.isfile("calendar.txt"))):
        calenderScrape.scrapeCalender()

    http_auth = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http_auth)
        
    classes = CunyFirstScraper.scrapeCFirst(uname)
    calendar = open("calendar.txt", "r")
    line = calendar.readline()
    requests = []
    while(line != ""):
        for classinfo in classes:
            event = eventprep.eventPrep(classinfo, line)
            print(event)
            if (event != None):
                requests.append(service.events().insert(calendarId="primary", body=event))
        if len(requests) > 45:
            batch = service.new_batch_http_request(callback=callbackPlaceholder)
            for i in requests:
                batch.add(i)
            batch.execute(http=http)
            requests = []
        line = calendar.readline()
    if len(requests) != 0:
        batch = service.new_batch_http_request(callback=callbackPlaceholder)
        for i in requests:
            batch.add(i)
        batch.execute(http=http)
    return True

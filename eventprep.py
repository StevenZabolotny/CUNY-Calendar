import datetime
import time
from CunyFirstScraper import *

def eventPrep(classInfo, dateline):
    spaceloc = classInfo[2].find(' ')
    weekday = dateline[-3:-1]
    if weekday in classInfo[2][:spaceloc]:
        summary = classInfo[0]
        location = classInfo[3][1:]
        slashloc = dateline.find('/')
        spaceloc2 = dateline.find(' ')
        month = int(dateline[:slashloc])
        date = int(dateline[slashloc+1:spaceloc2 - 1])
        year = datetime.date.today().year
        timeport = classInfo[2][spaceloc+1:]
        spaceloc = timeport.find(' ')
        starttime = timeport[:spaceloc]
        colonloc = starttime.find(':')
        hour = int(starttime[:colonloc])
        minute = int(starttime[colonloc+1:-2])
        if hour == 12:
            hour -= 12
        if starttime[-2:] == 'PM':
            hour += 12
        start = {'DateTime': datetime.datetime(year, month, date, hour, minute, 0), 'TimeZone': None}
        dashloc = timeport.find('-')
        endtime = timeport[dashloc+2:]
        colonloc = endtime.find(':')
        hour = int(endtime[:colonloc])
        minute = int(endtime[colonloc+1:-2])
        if hour == 12:
            hour -= 12
        if endtime[-2:] == 'PM':
            hour += 12
        end = {'DateTime': datetime.datetime(year, month, date, hour, minute, 0), 'TimeZone': None}
        event = {'Summary':summary, 'Location':location, 'Start':start, 'End':end}
        return event
    else:
        return None
    

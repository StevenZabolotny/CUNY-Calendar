import datetime
import time

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
        minute = starttime[colonloc+1:-2]
        zone = 'standard'
        if month < 11 or (month == 11 and date < 6):
            zone = 'day'
        if hour == 12:
            hour -= 12
        if starttime[-2:] == 'PM':
            hour += 12
        if hour < 10:
            hour = '0' + str(hour)
        else:
            hour = str(hour)
        if month < 10:
            month = '0' + str(month)
        else:
            month = str(month)
        if date < 10:
            date = '0' + str(date)
        else:
            date = str(date)
        if zone == 'day':
            start = {'dateTime': year+'-'+month+'-'+day+'T'+hour+':'+minute+':00-04:00', 'timeZone': 'Eastern Daylight Time'}
        else:
            start = {'dateTime': year+'-'+month+'-'+day+'T'+hour+':'+minute+':00-05:00', 'timeZone': 'Eastern Standard Time'}
        dashloc = timeport.find('-')
        endtime = timeport[dashloc+2:]
        colonloc = endtime.find(':')
        hour = int(endtime[:colonloc])
        minute = endtime[colonloc+1:-2]
        if hour == 12:
            hour -= 12
        if endtime[-2:] == 'PM':
            hour += 12
        if hour < 10:
            hour = '0' + str(hour)
        else:
            hour = str(hour)
        if zone == 'day':
            end = {'dateTime': year+'-'+month+'-'+day+'T'+hour+':'+minute+':00-04:00', 'timeZone': 'Eastern Daylight Time'}
        else:
            end = {'dateTime': year+'-'+month+'-'+day+'T'+hour+':'+minute+':00-05:00', 'timeZone': 'Eastern Standard Time'}
        event = {'summary':summary, 'location':location, 'start':start, 'end':end}
        return event
    else:
        return None
    

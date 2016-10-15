from lxml import html
import requests
import datetime

__weekdays = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']

def scrapeCalender():
    page = requests.get('http://www2.cuny.edu/academics/academic-calendars/')
    tree = html.fromstring(page.content)
    dates = tree.xpath('//td/text()')
    dates2 = []
    for i in dates:
        if len(i) > 8:
            pass
        elif len(i) < 3:
            pass
        elif (not(i[1] == '/' or i[2] == '/')):
            pass
        else:
            dates2.append(i)
    calenderf = open('calender.txt', 'w')
    finals = 0
    for i in dates2:
        if finals == 1:
            calenderf.write(i[:-1])
            calenderf.write(', ')
            calenderf.write('**')
        elif '**' in i:
            calenderf.write(i[:-3])
            calenderf.write(', ')
            calenderf.write(i[-1:])
            if i[-1] == 'M':
                calenderf.write('o')
            elif i[-1] == 'T':
                calenderf.write('u')
        elif i[-1] == 'R':
            finals = 1
            calenderf.write(i[:-2])
            calenderf.write(', ')
            calenderf.write('**')
        else:
            calenderf.write(i)
            calenderf.write(', ')
            ind = i.find('/')
            datep = datetime.date(datetime.date.today().year, int(i[:ind]), int(i[ind+1:]))
            calenderf.write(__weekdays[datep.weekday()])
        calenderf.write('\n')
    calenderf.close()

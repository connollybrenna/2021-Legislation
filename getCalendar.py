import requests
import json
from ics import Calendar, Event
from datetime import datetime
from dateutil import tz

date_input = '%Y-%m-%dT%H:%M:%S'
date_output = '%Y-%m-%d %H:%M:%S'

url = "http://www.gencourt.state.nh.us:80/house/schedule/CalendarWS.asmx/GetEvents"
headers = {"Content-Type": "application/json; charset=utf-8", "DNT": "1", "Connection": "close"}
r = requests.get(url, headers=headers)
j = json.loads(r.json()['d'])
c = Calendar()
for entry in j:
    try:
        begin = datetime.strptime(entry['start'],date_input).replace(tzinfo=tz.gettz('EST'))
        begin = begin.astimezone(tz.tzutc())
        end = datetime.strptime(entry['end'],date_input).replace(tzinfo=tz.gettz('EST'))
        end = end.astimezone(tz.tzutc())
        e = Event()
        e.name = entry['title']
        e.begin = begin.strftime(date_output)
        e.end = end.strftime(date_output)
        e.description = 'http://www.gencourt.state.nh.us/house/schedule/' + entry['url']
        c.events.add(e)
    except:
        print(entry)

path = r'C:\git\2021-Legislation\meetings.ics'
with open(path, "w") as f:
	f.writelines(c)
	f.close()
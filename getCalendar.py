import requests
import json
from ics import Calendar, Event
from datetime import datetime
from dateutil import tz
from bs4 import BeautifulSoup

date_input = '%Y-%m-%dT%H:%M:%S'
date_output = '%Y-%m-%d %H:%M:%S'

url_0 = "http://www.gencourt.state.nh.us:80/house/schedule/CalendarWS.asmx/GetEvents"
headers_0 = {"Content-Type": "application/json; charset=utf-8", "DNT": "1", "Connection": "close"}
r_0 = requests.get(url_0, headers=headers_0)
j = json.loads(r_0.json()['d'])
c_hearings = Calendar()
for entry in j:
    if entry['backgroundColor'] == '#2980B9':
        event_type = 'Hearing'
    if entry['backgroundColor'] == '#6CA464':
        event_type = 'Meeting'
    if entry['backgroundColor'] == '#9933ff':
        event_type = 'Session Day'
    begin = datetime.strptime(entry['start'],date_input).replace(tzinfo=tz.gettz('EST'))
    r_1 = requests.get('http://www.gencourt.state.nh.us/house/schedule/' + entry['url'])
    soup = BeautifulSoup(r_1.content,features="lxml")
    if(event_type == 'Hearing'):
        table = soup.table
        for row in table.find_all('tr'):
            cols =  row.find_all('td')
            time = cols[0].text.zfill(8)
            bill = cols[1].text
            link = cols[1].a.get('href')
            desc = cols[2].text
            ts = datetime.strptime(time,'%I:%M %p').time()
            ds = begin.date()
            dt = datetime.combine(ds,ts)
            
            e = Event()
            e.name = event_type + ": " + bill
            e.begin = dt.astimezone(tz.tzutc()).strftime(date_output)
            e.end = e.begin
            e.description = "\n".join([bill,desc,link])
            c_hearings.events.add(e)
path = r'C:\git\2021-Legislation\hearings.ics'
with open(path, "w") as f:
	f.writelines(c_hearings)
	f.close()
import requests
import json
from ics import Calendar, Event
from datetime import datetime
from dateutil import tz
from bs4 import BeautifulSoup
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

date_input = '%Y-%m-%dT%H:%M:%S'
date_output = '%Y-%m-%d %H:%M:%S'

url_0 = "http://www.gencourt.state.nh.us:80/house/schedule/CalendarWS.asmx/GetEvents"
headers_0 = {"Content-Type": "application/json; charset=utf-8", "DNT": "1", "Connection": "close"}
r_0 = requests.get(url_0, headers=headers_0)
j_0 = json.loads(r_0.json()['d'])
c_hearings = Calendar()
c_meetings = Calendar()
c_sessions = Calendar()
for entry in j_0:
    if entry['backgroundColor'] == '#2980B9':
        begin = datetime.strptime(entry['start'],date_input).replace(tzinfo=tz.gettz('EST'))
        r = requests.get('http://www.gencourt.state.nh.us/house/schedule/' + entry['url'])
        soup = BeautifulSoup(r.content,features="lxml")
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
            e.name = bill + " - " + desc
            e.begin = dt.astimezone(tz.tzutc()).strftime(date_output)
            e.end = e.begin
            e.description = "\n".join([bill,desc,link])
            c_hearings.events.add(e)
    if entry['backgroundColor'] == '#6CA464':
        e = Event()
        begin = datetime.strptime(entry['start'],date_input).replace(tzinfo=tz.gettz('EST'))
        end = datetime.strptime(entry['end'],date_input).replace(tzinfo=tz.gettz('EST'))
        e.description = 'http://www.gencourt.state.nh.us/house/schedule/' + entry['url']
        e.name = "Meeting: " + entry['title']
        c_meetings.events.add(e)
    if entry['backgroundColor'] == '#9933ff':
        e = Event()
        begin = datetime.strptime(entry['start'],date_input).replace(tzinfo=tz.gettz('EST'))
        end = datetime.strptime(entry['end'],date_input).replace(tzinfo=tz.gettz('EST'))
        e.description = 'http://www.gencourt.state.nh.us/house/schedule/' + entry['url']
        e.name = "Session Day: " + entry['title']
        c_sessions.events.add(e)
url_1 = "http://www.gencourt.state.nh.us:80/senate/schedule/CalendarWS.asmx/GetEvents"
headers_1 = {"Content-Type": "application/json; charset=utf-8", "DNT": "1", "Connection": "close"}
r_1 = requests.get(url_1, headers=headers_1)
j_1 = json.loads(r_1.json()['d'])
for entry in j_1:
    if entry['backgroundColor'] == '#B74545':
        begin = datetime.strptime(entry['start'],date_input).replace(tzinfo=tz.gettz('EST'))
        r = requests.get('http://www.gencourt.state.nh.us/senate/schedule/' + entry['url'])
        soup = BeautifulSoup(r.content,features="lxml")
        table = soup.table
        if table:
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
                e.name = bill + " - " + desc
                e.begin = dt.astimezone(tz.tzutc()).strftime(date_output)
                e.end = e.begin
                e.description = "\n".join([bill,desc,link])
                c_hearings.events.add(e)
    if entry['backgroundColor'] == '#6CA464':
        e = Event()
        begin = datetime.strptime(entry['start'],date_input).replace(tzinfo=tz.gettz('EST'))
        end = datetime.strptime(entry['end'],date_input).replace(tzinfo=tz.gettz('EST'))
        e.description = 'http://www.gencourt.state.nh.us/senate/schedule/' + entry['url']
        e.name = "Meeting: " + entry['title']
        c_meetings.events.add(e)
    if entry['backgroundColor'] == '#9933ff':
        e = Event()
        begin = datetime.strptime(entry['start'],date_input).replace(tzinfo=tz.gettz('EST'))
        end = datetime.strptime(entry['end'],date_input).replace(tzinfo=tz.gettz('EST'))
        e.description = 'http://www.gencourt.state.nh.us/senate/schedule/' + entry['url']
        e.name = "Session Day: " + entry['title']
        c_sessions.events.add(e)
path = r'meetings.ics'
with open(path, "w") as f:
    f.writelines(c_meetings)
    f.close()
path = r'sessions.ics'
with open(path, "w") as f:
    f.writelines(c_sessions)
    f.close()
path = r'hearings.ics'
with open(path, "w") as f:
    f.writelines(c_hearings)
    f.close()
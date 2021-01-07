import requests
import re
r = requests.get('http://www.gencourt.state.nh.us/lsr_search/rss.aspx?cmbbody=&txttitle=&txtlsr=&comblast=')
match = not bool(re.search('error',r.text[:5]))
if match:
    with open(r'C:\git\2021-Legislation\2021_LSR.xml', 'wb') as f:
        f.write(r.content)
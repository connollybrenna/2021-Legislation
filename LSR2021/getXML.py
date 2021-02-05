import requests
import re
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
r = requests.get('http://www.gencourt.state.nh.us/lsr_search/rss.aspx?cmbbody=&txttitle=&txtlsr=&comblast=')
match = not bool(re.search('error',r.text[:5]))
if match:
    with open(r'2021_LSR.xml', 'wb') as f:
        f.write(r.content)
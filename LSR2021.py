import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

df = pd.read_csv (r'C:\git\2021-Legislation\2021_LSR.csv')
for index, row in df.iterrows():
    num = int(row.LSRNumber.split('-')[1])
    payload = {'id': num, 'type': '4'}
    r = requests.get('http://www.gencourt.state.nh.us/lsr_search/billText.aspx', params=payload)
    if r.text != 'error: Index 0 is either negative or above rows count.':
        row.BillURL = r.url
        soup = BeautifulSoup(r.content, features="lxml")
        txt = soup.get_text()
        with open((r'C:\git\2021-Legislation\Bills-HTML' + '\\' + row.LSRNumber + ".html"), "w", encoding="utf-8") as f:
            if(txt != 'error: Index 0 is either negative or above rows count.\r\n\r\n'):
                f.write(str(soup))
                f.close()
            else:
                f.close()
                os.remove(r'C:\git\2021-Legislation\Bills-HTML' + '\\' + row.LSRNumber + ".html")
df.to_csv(r'C:\git\2021-Legislation\2021_LSR.csv', index = False)

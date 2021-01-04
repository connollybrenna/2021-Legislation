import pandas as pd
import requests
import os
from bs4 import BeautifulSoup
from markdownify import markdownify as md

df = pd.read_csv (r'C:\git\2021-Legislation\2021_LSR.csv')
for index, row in df.iterrows():
    num = int(row.LSRNumber.split('-')[1])
    payload = {'id': num, 'type': '4'}
    r = requests.get('http://www.gencourt.state.nh.us/lsr_search/billText.aspx', params=payload)
    if r.text != 'error: Index 0 is either negative or above rows count.':
        row.BillURL = r.url
        soup = BeautifulSoup(r.content, features="lxml")
        txt = soup.get_text()
        htmlPath = r'C:\git\2021-Legislation\Bills-HTML' + '\\' + row.LSRNumber + ".html"
        mdPath = r'C:\git\2021-Legislation\Bills-MD' + '\\' + row.LSRNumber + ".md"
        with open(htmlPath, "w", encoding="utf-8") as f, open(mdPath, "w", encoding="utf-8") as g:
            if(txt != 'error: Index 0 is either negative or above rows count.\r\n\r\n'):
                f.write(str(soup))
                f.close()
                g.write(md(str(soup.body)))
                g.close()
            else:
                f.close()
                g.close()
                os.remove(htmlPath)
                os.remove(mdPath)
df.to_csv(r'C:\git\2021-Legislation\2021_LSR.csv', index = False)

import pandas as pd
from bs4 import BeautifulSoup
import os
import requests
import re
from markdownify import markdownify as md

os.chdir(os.path.dirname(os.path.abspath(__file__)))

df = pd.read_csv (r'2021_LSR.csv')
for index, row in df.iterrows():
    if row.isna().BillURL:
        num = int(row.LSRNumber.split('-')[1])
        payload = {'sy': '2021', 'id': num, 'txtFormat': 'html'}
        try:
            r = requests.get('http://gencourt.state.nh.us/bill_Status/billText.aspx', params=payload)
            match = not bool(re.search('error',r.text[:5]))
            if match:
                df.loc[index,'BillURL'] = r.url
                soupBill = BeautifulSoup(r.content, features="lxml")
                
                billnum = soupBill.find(class_="cs2E86D3A6")
                billanalysis = soupBill.find(class_="cs9224F58F")
                if billnum:
                    try:
                        billnum = billnum.text.split(' ')
                        billnum = (billnum[0] + ' ' + billnum[1]).strip()
                        df.loc[index,'BillNumber'] = billnum
                    except: billnum = 'NA'
                else:
                    billnum = 'NA'
                if billanalysis:
                    billanalysis = billanalysis.text.strip()
                    df.loc[index,'BillAnalysis'] = billanalysis
                htmlRoot = r'.\Bills-HTML'
                mdRoot = r'.\Bills-MD'
                if not os.path.isdir(htmlRoot):
                    os.mkdir(htmlRoot)
                if not os.path.isdir(mdRoot):
                    os.mkdir(mdRoot)
                htmlPath = htmlRoot + '\\' + billnum.replace(' ', '_') + '__' + row.LSRNumber + ".html"
                mdPath = mdRoot + '\\' + billnum.replace(' ', '_') + '__' + row.LSRNumber + ".md"
                if not os.path.isfile(htmlPath):
                    with open(htmlPath, "w", encoding="utf-8") as f, open(mdPath, "w", encoding="utf-8") as g:
                        f.write(str(soupBill))
                        f.close()
                        g.write(md(str(soupBill.body)))
                        g.close()
            df.to_csv(r'2021_LSR.csv', index = False)
        except:
            print('unable to reach server')
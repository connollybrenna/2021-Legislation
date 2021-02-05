import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

url = 'http://gencourt.state.nh.us/bill_Status/results.aspx?txtsessionyear=2021&sortoption='
r = requests.get(url)
path = r'billStatusResults.html'
with open(path, "w", encoding="utf=8") as f:
	f.write(r.text)
	f.close()

soup = BeautifulSoup(open(path,encoding="utf-8"), features='lxml')
table = soup.find_all(class_='ptable')[1]
prettyTable = table.prettify()
splits = prettyTable.split('<big>')

df_cols = ('Bill Number', 'Bill Docket', 'Bill Status', 'HTML', 'PDF', 'BillTitle', 'BillAnalysis', 'G-Status:', 'House Status:', 'Senate Status:', 'Next/Last Comm:', 'Next/Last Hearing:')
df = pd.DataFrame(columns = df_cols, dtype='str')
index = 0
for s in splits:
    df = df.append(pd.Series(name=index))
    s = '<big>' + s
    splitsoup = BeautifulSoup(s,features='lxml')
    billnum = ''.join(splitsoup.body.big.text.strip().split())
    #print(billnum)
    df.loc[index,'Bill Number'] = billnum
    for link in splitsoup.find_all('a'):
        df.loc[index, ' '.join(link.text.split()).replace('[','').replace(']','')] = str('http://gencourt.state.nh.us/bill_Status/' + str(link.get('href')))
    try:
        billtitle = splitsoup.find('b').next_sibling.strip()
        df.loc[index,'BillTitle'] = billtitle
    except: pass
    for tr in splitsoup.find_all('tr'):
        td = tr.find_all('td',colspan=None)
        if td:
            for colname in df_cols[6:]:
                if td[0].text.strip() == colname:
                    df.loc[index,colname] = td[1].text.strip()
    try:
        Billurl = df.loc[index,'HTML']
    except: pass
    #print(Billurl)
    if str(df.loc[index,'HTML'])[:4] == 'http' :
        r = requests.get(Billurl)
        soupBill = BeautifulSoup(r.content, features="lxml")
        billanalysis = soupBill.find(class_="cs9224F58F")
        if billanalysis:
            billanalysis = billanalysis.text.strip()
            df.loc[index,'BillAnalysis'] = billanalysis
        htmlRoot = r'.\Bills-HTML_fromStatusPage'
        htmlPath = htmlRoot + '\\' + billnum + ".html"
        if not os.path.isdir(htmlRoot):
            os.mkdir(htmlRoot)
        if not os.path.isfile(htmlPath):
            with open(htmlPath, "w", encoding="utf-8") as f:
                f.write(str(soupBill))
                f.close()
    index += 1
df.to_csv(r'2021Bills.csv', index = False)
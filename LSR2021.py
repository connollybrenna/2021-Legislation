from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
from markdownify import markdownify as md


r = requests.get('http://www.gencourt.state.nh.us/lsr_search/rss.aspx?cmbbody=&txttitle=&txtlsr=&comblast=')
match = not bool(re.search('error',r.text[:5]))

if match:
    with open(r'C:\git\2021-Legislation\2021_LSR.xml', 'wb') as f:
        f.write(r.content)
soup = BeautifulSoup(open(r'C:\git\2021-Legislation\2021_LSR.xml',encoding="utf-8"), features='lxml')

df_cols = ["LSRNumber","LSRTitle","BillNumber","BillAnalysis","BillURL","PrimeSponsor","Sponsors","pubDate"]
rows = []

LSR = soup.findAll('item')
for a in LSR:
    s_LSRNumber = a.find('lsrnumber').text
    s_LSRTitle = a.find('lsrtitle').text
    s_BillNumber = a.find('billnumber').text
    s_BillAnalysis = ''
    s_BillURL = ''
    s_PrimeSponsor = a.find('primesponsor').text
    s_Sponsors = ', '.join([sponsor.text for sponsor in a.find_all('sponsor')])
    s_pubDate = a.find('pubdate').text
    
    num = int(s_LSRNumber.split('-')[1])
    payload = {'sy': '2021', 'id': num, 'txtFormat': 'html'}
    rBill = requests.get('http://gencourt.state.nh.us/bill_Status/billText.aspx', params=payload)
    match = not bool(re.search('error',rBill.text[:5]))
    if match:
        s_BillURL = rBill.url
        soupBill = BeautifulSoup(rBill.content, features="lxml")
        
        billnum = soupBill.find(class_="cs2E86D3A6")
        if billnum:
            try:
                billnum = billnum.text.split(' ')
                s_BillNumber =  (billnum[0] + ' ' + billnum[1]).strip()
            except:
                s_BillNumber = ''
        try:
            s_BillAnalysis = soupBill.find(class_="cs9224F58F").text.strip()
        except:
            s_BillAnalysis = ''
        htmlPath = r'C:\git\2021-Legislation\Bills-HTML' + '\\' + s_LSRNumber + ".html"
        mdPath = r'C:\git\2021-Legislation\Bills-MD' + '\\' + s_LSRNumber + ".md"
        with open(htmlPath, "w", encoding="utf-8") as f, open(mdPath, "w", encoding="utf-8") as g:
            f.write(str(soupBill))
            f.close()
            g.write(md(str(soupBill.body)))
            g.close()

    newrows = {"LSRNumber": s_LSRNumber,"LSRTitle": s_LSRTitle,"BillNumber": s_BillNumber,"BillAnalysis": s_BillAnalysis,"BillURL": s_BillURL,"PrimeSponsor": s_PrimeSponsor,"Sponsors": s_Sponsors,"pubDate": s_pubDate}
    print(s_LSRNumber + " : " + s_BillNumber + " : " + s_BillAnalysis)
    rows.append(newrows)
out_df = pd.DataFrame(rows, columns = df_cols)
out_df.to_csv(r'C:\git\2021-Legislation\2021_LSR.csv', index = False)
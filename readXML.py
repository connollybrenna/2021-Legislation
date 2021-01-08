from bs4 import BeautifulSoup
import pandas as pd

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

    newrows = {"LSRNumber": s_LSRNumber,"LSRTitle": s_LSRTitle,"BillNumber": s_BillNumber,"BillAnalysis": s_BillAnalysis,"BillURL": s_BillURL,"PrimeSponsor": s_PrimeSponsor,"Sponsors": s_Sponsors,"pubDate": s_pubDate}
    rows.append(newrows)
out_df = pd.DataFrame(rows, columns = df_cols)
out_df.to_csv(r'C:\git\2021-Legislation\2021_LSR.csv', index = False)
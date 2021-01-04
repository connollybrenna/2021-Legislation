import pandas as pd
import requests
df = pd.read_csv (r'C:\scripts\2021-Legislation\2021_LSR.csv')
for index, row in df.iterrows():
    num = int(row.LSRNumber.split('-')[1])
    payload = {'id': num, 'type': '4'}
    r = requests.get('http://www.gencourt.state.nh.us/lsr_search/billText.aspx', params=payload)
    if r.text != 'error: Index 0 is either negative or above rows count.':
        row.BillURL = r.url
df.to_csv(r'C:\scripts\2021-Legislation\2021_LSR.csv', index = False)
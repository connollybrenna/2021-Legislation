import os
import pandas as pd
from datetime import datetime
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

ts = datetime.now().strftime("%Y%m%d%H%M%S")
mdPath = r'C:\git\2021-Legislation\analysis.md'

if os.path.isfile(mdPath):
    os.rename(mdPath, (mdPath + ts))

df = pd.read_csv (r'2021_LSR.csv')
df = df.sort_values(by=['BillNumber'])
for index, row in df.iterrows():
    if row.notna().BillAnalysis: 
        analysis = str(row.BillAnalysis)
        bill = str(row.BillNumber)
        url = str(row.BillURL)
        output = "[" + bill + "](" + url + ") - " + analysis
        outfile = open(r'analysis.md',"a")
        outfile.write(output + "  \n")
        outfile.close()
from bs4 import BeautifulSoup
import os

directory = r'C:\git\2021-Legislation\Bills-HTML'
for filename in os.listdir(directory):
    soup = BeautifulSoup(open(os.path.join(directory, filename), encoding="utf8"), "lxml")
    try:
        analysis = soup.find(class_="cs9224F58F").text.strip()
        bill = soup.find(class_="cs2E86D3A6").text.split(' ')
        bill = (bill[0] + ' ' + bill[1]).strip()
        num = int(filename[:-5].split('-')[1])
        url = 'http://gencourt.state.nh.us/bill_Status/billText.aspx?sy=2021&id='+ str(num) +'&txtFormat=html'
        output = "[" + bill + "](" + url + ") - " + analysis
        outfile = open(r'C:\git\2021-Legislation\analysis.md',"a")
        outfile.write(output + "  \n")
        outfile.close()
    except: pass
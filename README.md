# 2021-Legislation
This is where I will be storing scripts and data related to the 2021 legislative year, primarily focused on my home state of New Hampshire.

## About the scripts
### LSR2021.py
This script scrapes the LSRs from the http://www.gencourt.state.nh.us/ RSS feed and stores them in an XML (2021_LSR.xml), then parses through that XML to extract useful data into a CSV (2021_LSR.csv). It also tries to find the HTML pages for the associated bills for each LSR, and stores the URLs and bill numbers in the CSV if it's able to. It grabs copies of the HTML pages, and also converts them to MarkDown so they're more human-readable here on GitHub.

### BillAnalyses.py
This script goes through the HTML pages backed up by LSR2021.py and tries to find the 'Analysis' tag in each page, and outputs it to a MarkDown file including the bill name (linked to the gencourt webpage for it) and the analysis.

# 2021-Legislation
This is where I will be storing scripts and data related to the 2021 legislative year, primarily focused on my home state of New Hampshire. I'll be breaking them out into subprojects for organization.

## About the projects
### LSR2021
There are four scripts in this project, which are meant to be run in this order:
#### 1. getXML.py
This script scrapes the LSRs from the http://www.gencourt.state.nh.us/ RSS feed and stores them in an XML (2021_LSR.xml)
#### 2. readXML.py
This script parses through the generated XML to extract useful data into a CSV (2021_LSR.csv)
#### 3. LSR2021.py
This script parses through the generated CSV and tries to find the HTML pages for the associated bills for each LSR, and stores the URLs and bill numbers in the CSV if it's able to. It grabs copies of the HTML pages, and also converts them to MarkDown so they're more human-readable here on GitHub.
#### 4. BillAnalyses.py
This script goes through the HTML pages backed up by LSR2021.py and tries to find the 'Analysis' tag in each page, and outputs it to a MarkDown file including the bill name (linked to the gencourt webpage for it) and the analysis.
### BillStatus
This project consists of one script, which parses through data on the Bill Status page to create a CSV of the data and backs up what it can to HTML files.
### CalendarGen
This project consists of one script, which uses the new House Calendar tool to generate .ICS files for upcoming Hearings, Meetings, and Sessions. I plan to update this project to also support the Senate digital calendar as well soon.
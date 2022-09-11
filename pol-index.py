import collections
import csv
import datetime
import os
import requests
import time
from bs4 import BeautifulSoup

file = open("pol-index.csv", "w")
writer = csv.writer(file)
url = "https://boards.4chan.org/pol/archive"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html5lib")
sources = soup.find_all('a', {'class':'quotelink'}, href=True)
for source in sources: 
    print("https://boards.4chan.org" + source['href'])
    writer.writerow(["https://boards.4chan.org" + source['href']])
file.close()

with open('pol-index.csv','r') as source:
    lines_src = source.readlines()
with open('pol-scraped.csv','r') as f:
    lines_f = f.readlines()
to_scrape = open("pol-queue.csv","w")
for data in lines_src:
    if data not in lines_f:
        print(data)
        to_scrape.write(data)
to_scrape.close()
exec(open("pol.py").read())
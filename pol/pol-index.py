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

exec(open("pol.py").read())

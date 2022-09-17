import collections
import csv
from collections import deque
import datetime
import os
import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError, ConnectTimeout, Timeout
from ssl import CertificateError, SSLError


my_file = open("qresearch-queue.csv", "r")
data = my_file.read()
data_into_list = data.split("\n")
urls = collections.deque(data_into_list)
my_file.close()


while True:
    dt = str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%f"))
    url = urls[0]
    try:
        page = requests.get(url)
    except OSError or ConnectionError or ConnectTimeout or Timeout or CertificateError or SSLError:
        try:
            page = requests.get(url)
        except OSError or ConnectionError or ConnectTimeout or Timeout or CertificateError or SSLError:
            urls.popleft()
            url = urls[0]
            page = requests.get(url)
    soup = BeautifulSoup(page.content, "html5lib")
    file = open("8kun-test.txt", "w")
    scraped = open("qresearch-scraped.csv", "a")
    subject = soup.find(class_="subject")
    texts = soup.find_all(class_="body")
    idnumbers = soup.find_all("span", class_="poster_id")
    users = soup.find_all("span", class_="name")
    meta = soup.find_all('time')
    sources = soup.find_all('a', {'class':'post_no'}, href=True)

    writer = csv.writer(file, delimiter="\t")
    while True:
        subject = soup.find(class_="subject")
        try:
            print(subject.text)
            writer.writerow(["</m " + subject.text + " >"])
        except AttributeError:
            writer.writerow(["</m NO SUBJECT >"])
        texts = soup.find_all(class_="body")
        idnumbers = soup.find_all("span", class_="poster_id")
        users = soup.find_all("span", class_="name")
        meta = soup.find_all('time')
        sources = soup.find_all('a', {'class':'post_no'}, href=True)
        for text, idnumber, user, meta, source in zip(texts, idnumbers, users, meta, sources):
            print(text.text + " \t " + idnumber.text + " \t " + user.text + " \t " + meta.text +  " \t " + source['href'])
            writer.writerow([text.text, "</m ID# " + idnumber.text + " >", "</m USERNAME " +  user.text + " >", "</m TIME " +  meta.text + " >", "</m SOURCE " +  source['href'] + " >"])
        newname2 = 'qresearch'+dt+'.txt'
        os.rename('8kun-test.txt', newname2)
        file.close()
        break
    swriter = csv.writer(scraped)
    swriter.writerow([str(urls[0])])
    scraped.close()
    urls.popleft()
my_file.close()

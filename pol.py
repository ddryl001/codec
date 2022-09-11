import collections
import csv
import datetime
import os
import requests
import time
from bs4 import BeautifulSoup
from requests.exceptions import MissingSchema

my_file = open("pol-queue.csv", "r")
data = my_file.read()
data_into_list = data.split("\n")
urls = collections.deque(data_into_list)
my_file.close()
start_time = str(datetime.datetime.now().strftime("%H:%M"))
while True:
    dt = str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%f"))
    url = urls[0]
    try:
        page = requests.get(url)
    except MissingSchema or TypeError:
        print(start_time)
        end_time = str(datetime.datetime.now().strftime("%H:%M"))
        print(end_time)
        break
    soup = BeautifulSoup(page.content, "html5lib")
    file = open("4chan-test.txt", "w")
    file2 = open("4chan-test.tsv", "w")
    scraped = open("pol-scraped.csv", "a")
    subject = soup.find(class_="subject")
    posts = soup.find_all(class_="postMessage")
    idnumbers = soup.find_all("span", class_="hand")
    users = soup.find_all("span", class_="name")
    times = soup.find_all("span", class_="dateTime")
    sources = soup.find_all('a', {'title':'Link to this post'}, href=True)
    while True:
        writer = csv.writer(file)
        subject = soup.find(class_="subject")
        try:
            print(subject.text)
            writer.writerow([subject.text])
        except AttributeError:
            print("")
            writer.writerow([""])
        posts = soup.find_all(class_="postMessage")
        for post in posts:
            posted = post.get_text(separator=" [BREAK] ").strip()
            print(posted)
            writer.writerow([posted])
        file.close()
        newname1 = 'pol'+dt+'.txt'
        os.rename('4chan-test.txt', newname1)
        break
    while True:
        writer = csv.writer(file2)
        subject = soup.find(class_="subject")
        try:
            print(subject.text)
            writer.writerow([subject.text, "ID", "USER", "META", str(urls[0])])
        except AttributeError:
            print("")
            writer.writerow(["", "ID", "USER", "META", str(urls[0])])
        posts = soup.find_all(class_="postMessage")
        for post in posts:
            posted = post.get_text(separator="py").strip()
        idnumbers = soup.find_all("span", class_="hand")
        users = soup.find_all("span", class_="name")
        times = soup.find_all("span", class_="dateTime")
        sources = soup.find_all('a', {'title':'Link to this post'}, href=True)
        for posted, idnumber, user, time, source in zip(posts, idnumbers, users, times, sources):
            print(posted.text + idnumber.text + " \t " + user.text + " \t " + time.text +  " \t " + str(urls[0]) + source['href'])
            writer.writerow([posted.text, idnumber.text, user.text, time.text, source['href']])
        file2.close()
        newname2 = 'pol'+dt+'.tsv'
        os.rename('4chan-test.tsv', newname2)
        break
    swriter = csv.writer(scraped)
    swriter.writerow([str(urls[0])])
    scraped.close()
    urls.popleft()

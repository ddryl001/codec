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
    scraped = open("pol-scraped.csv", "a")
    subject = soup.find(class_="subject")
    posts = soup.find_all(class_="postMessage")
    idnumbers = soup.find_all("span", class_="hand")
    users = soup.find_all("span", class_="name")
    times = soup.find_all("span", class_="dateTime")
    replied = soup.find_all("a", class_="quotelink")
    sources = soup.find_all('a', {'title':'Link to this post'}, href=True)
    while True:
        writer = csv.writer(file, delimiter="\t")
        posts = soup.find_all(class_="postMessage")
        subject = soup.find(class_="subject")
        idnumbers = soup.find_all("span", class_="hand")
        users = soup.find_all("span", class_="name")
        times = soup.find_all("span", class_="dateTime")
        replied = soup.find_all("a", class_="quotelink")
        sources = soup.find_all('a', {'title':'Link to this post'}, href=True)
        urlstr = str(urls[0])
        try:
            writer.writerow(["<m> " + subject.text + " </m>"])
        except AttributeError:
            writer.writerow(["<m> NO SUBJECT </m>"])
        for post, idnumber, user, time, replied, source in zip(posts, idnumbers, users, times, replied, sources):
            post = post.get_text(separator=" <break> ")
            print(post + "\t" + "</m " + idnumber.text + " >" + " \t " + "</m " + user.text + " >" + " \t " + "</m " + time.text + " >" +  " \t " + "</m " + source['href'] + " >" + "\t" + "</m " + str(urls[0]) + " >" + "\t" + "</m " + replied.text + " >")
            writer.writerow([post, "<m> ID# " + idnumber.text + " </m>", "<m> USERNAME " + user.text + " </m>", "<m> TIME " + time.text + " </m>", "<m> POST# " + source['href'] + " </m>", "<m> THREAD " + str(urls[0]) + " </m>", "<m> REPLYING TO " + replied.text + " </m>"])
        file.close()
        newname2 = 'pol'+dt+'.txt'
        os.rename('4chan-test.txt', newname2)
        break
    swriter = csv.writer(scraped)
    swriter.writerow([str(urls[0])])
    scraped.close()
    urls.popleft()

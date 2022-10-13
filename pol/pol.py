import collections
import csv
import datetime
import os
import requests
import time
from bs4 import BeautifulSoup
from requests.exceptions import MissingSchema

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

my_file = open("pol-queue.csv", "r")
data = my_file.read()
data_into_list = data.split("\n")
urls = collections.deque(data_into_list)
my_file.close()
start_time = str(datetime.datetime.now().strftime("%H:%M"))
loop = 0
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
    
    while True:
        writer = csv.writer(file, delimiter="\t")
        writer.writerow(["<h> TEXT </h>", "<h> ID </h>", "<h> USERNAME </h>", "<h> TIME </h>", "<h> POSTNUM </h>", "<h> THREAD </h>", "<h> REPLY </h>", "<h> FLAG </h>", "<h> SUBJECT </h>"])
        try:
            subjects = soup.find(class_="subject")
            subject = subjects.text
        except AttributeError:
            subject = " NO SUBJECT "
        for div in soup.find_all('div', {'class':'postContainer'}):
            posts = div.find(class_="postMessage")
            post = posts.get_text(separator=" <break> ")
            try:
                idnumber = div.find(class_='hand', text=True).text
            except AttributeError:
                idnumber = " NONE "
            try:
                user = div.find(class_='name', text=True).text
            except AttributeError:
                try:
                    user = div.find(class_='postertrip', text=True).text
                except AttributeError:
                    user = " NONE "
            try:
                time = div.find(class_='dateTime', text=True).text
            except AttributeError:
                time = " NONE "
            replied = div.find("a", {'class':'quotelink'}, href=True)
            source = div.find('a', {'title':'Link to this post'}, href=True)
            flags = div.find('span', {'class':'posteruid'})
            urlstr = str(urls[0])
            
            try:
                try:
                    flag = flags.find_next_sibling()
                except AttributeError:
                    break
                print(post + "\t" + idnumber + " \t " + user + " \t " + time +  " \t " + source['href'] + "\t" + str(urls[0]) + " \t " + replied['href'] + " \t " + flag['title'] + " \t " + subject)
                writer.writerow([post, "<m> ID# " + idnumber + " </m>", "<m> USERNAME " + user + " </m>", "<m> TIME " + time + " </m>", "<m> POST# " + source['href'] + " </m>", "<m> THREAD " + str(urls[0]) + " </m>", "<m> REPLYING TO " + replied['href'] + " </m>", "<m> FLAG " + flag['title'] + " </m>", "<m> " + subject + " </m>"])
            except TypeError or AttributeError:
                try:
                    try:
                        flag = flags.find_next_sibling()
                    except AttributeError:
                        break
                    print(post + "\t" + idnumber + " \t " + user + " \t " + time +  " \t " + source['href'] + "\t" + str(urls[0]) + "\t" + "</m NO REPLY >" + "\t" + flag['title'] + " \t " + subject)
                    writer.writerow([post, "<m> ID# " + idnumber + " </m>", "<m> USERNAME " + user + " </m>", "<m> TIME " + time + " </m>", "<m> POST# " + source['href'] + " </m>", "<m> THREAD " + str(urls[0]) + " </m>", "<m> NO REPLY </m>", "<m> FLAG " + flag['title'] + " </m>", "<m> " + subject + " </m>"])
                except AttributeError:
                    break                         
        file.close()
        newname2 = 'pol'+dt+'.txt'
        os.rename('4chan-test.txt', newname2)
        
        break
    swriter = csv.writer(scraped)
    swriter.writerow([str(urls[0])])
    scraped.close()
    urls.popleft()
    looped = int(loop) + 1
    print("NUMBER OF THREADS SCRAPED: " + str(looped))
    loop = int(looped)

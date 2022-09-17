import csv
import os
from collections import deque
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import getpass
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True
driver = Service('/usr/bin/chromedriver')
driver = webdriver.Chrome(service=driver, options=options)
url = "https://8kun.top/qresearch/2.html?"
driver.get(url)

sources = driver.find_elements(By.XPATH, "//a[@class='open_thread_index']")
file = open("qresearch-index.csv", "w")
writer = csv.writer(file)
while True:
    sources = driver.find_elements(By.XPATH, "//a[@class='open_thread_index']")
    for source in sources:
            print(source.get_attribute("href"))
            writer.writerow([source.get_attribute("href")])
    try:
         driver.find_element(By.XPATH, '//html/body/div[7]/form[2]/input').click()
    except NoSuchElementException:
        break
file.close()


with open('qresearch-index.csv','r') as source:
    lines_src = source.readlines()
with open('qresearch-scraped.csv','r') as f:
    lines_f = f.readlines()
to_scrape = open("qresearch-queue.csv","w")
for data in lines_src:
    if data not in lines_f:
        print(data)
        to_scrape.write(data)
to_scrape.close()

exec(open("qresearch.py").read())

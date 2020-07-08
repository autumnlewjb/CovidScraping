import re

from bs4 import BeautifulSoup as bs
import urllib.request
from time import sleep
from datetime import datetime

import requests
from selenium import webdriver

opt = webdriver.ChromeOptions()
opt.add_argument('--no-sandbox')
opt.add_argument('--headless')


def identify_iframe(tag):
    source = str(tag.get('src'))
    regex = re.compile(r"https://e.infogram.com/\S*")
    return tag.name == 'iframe' and regex.search(source) and tag.get('title') == 'Copy: S: Dashboard Ringkas'


file = "latest_covid_cases.csv"
f = open(file, 'a+')
browser = webdriver.Chrome(options=opt)
browser.get('http://covid-19.moh.gov.my/')
page_source = browser.page_source
soup = bs(page_source, 'lxml')

iframe = soup.find(identify_iframe)
print(iframe)

browser.get(str(iframe.get('src')))
info = browser.find_elements_by_xpath('//h2/div/span/span')

tmp_list = list()

for i in info:
    tmp = i.text
    if re.match(r"[0-9]+", tmp):
        tmp_list.append(tmp)

current = datetime.now()
day = current.day
month = current.month
year = current.year

date = "{}/{}/{}".format(day, month, year)

f.write("\n{}, {}, {}, ".format(date, tmp_list[-1], tmp_list[0]))

if not f.closed:
    print("Web Scrapping done...")
    print("Data saved to %s" % file)
    f.close()
sleep(3)

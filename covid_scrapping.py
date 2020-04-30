from bs4 import BeautifulSoup
import urllib.request
from time import sleep

file = "latest_covid_cases.csv"
f = open(file,'a+')
f.write("\n")
source = urllib.request.urlopen("http://www.moh.gov.my/index.php/pages/view/2019-ncov-wuhan").read()
soup = BeautifulSoup(source,'lxml')

section1 = soup.body
titles = []
title = ""

for elements in section1.find_all("h3"):
    titles.append(elements.text)


if len(titles) == 1:
    title = titles[0].replace(",","->")

f.write(str(title) + "\n")
section2 = soup.center
# print(section2)
table = section2.find('table')
row = table.find_all('tr')

for tr in row:
    td = tr.find_all('td')
    row = [i.text for i in td]
    if len(row) == 2:
        data_input = str(row[0]) + "," + str(row[1])
        f.write(data_input + "\n")

if not(f.closed):
    print("Web Scrapping done...")
    print("Data saved to %s" % (file))
    f.close()
sleep(3)

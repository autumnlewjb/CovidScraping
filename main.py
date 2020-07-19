import re
import time
from datetime import datetime

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def identify_iframe(tag):
    source = str(tag.get('src'))
    regex = re.compile(r"https://e.infogram.com/\S*")
    return tag.name == 'iframe' and regex.search(source) and tag.get('title') == 'Copy: S: Dashboard Ringkas'


class ScrapeCovid:
    def __init__(self):
        self.driver = None
        self._driver_wait = WebDriverWait(self.driver, 30)
        self.url = 'http://covid-19.moh.gov.my/'
        self.soup = None
        self.date = None
        self.output_file = "output.csv"

    @property
    def driver(self):
        return self._driver

    @driver.setter
    def driver(self, value):
        opt = webdriver.ChromeOptions()
        opt.add_argument('--no-sandbox')
        opt.add_argument('--headless')
        opt.add_argument('--disable-gpu')
        self._driver = webdriver.Chrome(options=opt)

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        current = datetime.now()
        day = current.day
        month = current.month
        year = current.year

        self._date = "{}/{}/{}".format(day, month, year)

    def get_numbers(self):
        self.driver.get(self.url)
        page_source = self.driver.page_source
        self.soup = bs(page_source, 'lxml')

        iframe = self.soup.find(identify_iframe)

        self.driver.get(str(iframe.get('src')))
        self._driver_wait.until(EC.presence_of_element_located((By.XPATH, "//h2/div/span/span")))
        info = self.driver.find_elements_by_xpath('//h2/div/span/span')

        result = list()

        for i in info:
            tmp = i.text
            if re.match(r"[0-9]+", tmp):
                result.append(tmp)

        return result

    def main(self):
        tmp_list = self.get_numbers()
        with open(self.output_file, 'a+') as f:
            if tmp_list:
                f.write("\n{}, {}, {}, ".format(self.date, tmp_list[-1], tmp_list[0]))

        print("Web Scrapping done...")
        print("Data saved to %s" % self.output_file)


if __name__ == '__main__':
    start_time = time.time()
    obj = ScrapeCovid()
    obj.main()
    print(time.time() - start_time, 's')
    # TODO: script running slow 19s

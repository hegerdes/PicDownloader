##############################################################################
# Testing File with just one chanel to download

import requests
import re
import os
import errno
import shutil
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from operator import is_not
from functools import partial
import datetime
from selenium.webdriver.common.action_chains import ActionChains

now = datetime.datetime.now()
url = 'https://www.jodel.city/1213'

browser = webdriver.Firefox()
browser.get(url)
browser.get(url)
ActionChains(browser).move_to_element(browser.find_element_by_id('notif-connected')).perform()

elem = browser.find_element_by_id('contentArea')
contentList = elem.find_elements_by_tag_name("li")

dropdown = browser.find_elements_by_class_name('padded-list')
#dropdowntList = dropdown.find_elements_by_tag_name("li")

chanels = []
for t in dropdown:
    if(t.get_attribute("data-value") != None):
        chanels.append(t.get_attribute("data-value"))

for i in chanels:
    print(i)

photostr = []
chanalTitel = browser.title
print(browser.title)

for row in contentList:
    photoRow = row.find_elements_by_xpath(".//*[@class='ic']")
    for ph in photoRow:
        tmp = ph.get_attribute("data-navigation")
        photostr.append(tmp[6:])
browser.quit()

#Get the pics
for x in photostr:
    picure = x + 't.jpg'
    tmp = "https://g.jodel.me/" + picure
    path = str(datetime.datetime.today()).split()[0] + "/" + chanalTitel + "/" + picure
    print(path)
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    response = requests.get(tmp, stream=True)
    with open( path, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    print(x)

#str(datetime.datetime.today()).split()[0] +

#ua = UserAgent()
#headers = {'User-Agent': ua.Firefox}
#pic = browser.find_element_by_css_selector('body.web:nth-child(2) #home.app-page.app-active:nth-child(8) div.content div.tab-content:nth-child(1) ul.list #li.img:nth-child(21) div.ic div:nth-child(1) > div.entry')
#print(pic.get_property("style")['background-image'])
#res = requests.get(url, headers=headers ,allow_redirects=False)
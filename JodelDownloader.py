##########################################################################
# IMPORTANT
# ONLY Testet on LINUX with Python 3.7
# This provides a script to download all pictues on jodelCity
# Supportet are jpg pictures and mp4 video
# To work all below packages must be installed and the chrome or firefoc webdriver.
# The driver must be in your PATH. (Chrome is much faster)
#
# KNOWN BUGS:   This Script does not get all the pics. JodelCity only loads the first 80
#               or so comments. So only the pics within thes loaded comments will be found.
#               TODO: Scroll the page and wit to load all comments and pic IDs
#               Somtimes the dirver chraches without a abvious reason. Just restart the Script
#               TODO Invesigate chrach
import requests
import re
import os
import errno
import shutil
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from operator import is_not
from functools import partial


#Start URL
url = 'https://www.jodel.city/3300'

#Get the driver
driver = webdriver.Chrome()
#or
#driver = webdriver.Firefox()

#Need to call the URL twice
driver.get(url)
driver.get(url)

dropdown = driver.find_elements_by_class_name('padded-list')

#Save all chanel IDs
chanels = []
for t in dropdown:
    if(t.get_attribute('data-value') != None):
        chanels.append(t.get_attribute('data-value'))

#Go through all chanels
for ch in chanels:
    ch_url = 'https://www.jodel.city/' + ch
    driver.get(ch_url)

    buttons = driver.find_element_by_id('flacbtn')
    elem = driver.find_element_by_id('contentArea')
    contentList = elem.find_elements_by_tag_name('li')

    #Save all picture IDs
    photostr = []
    chTitel = driver.title
    print('Getting Pictures form ' + driver.title)
    #get pic ids
    for row in contentList:
        photoRow = row.find_elements_by_xpath(".//*[@class='ic']")
        for ph in photoRow:
            tmp = ph.get_attribute('data-navigation')
            if(tmp.__contains__('vid')):
                #Videos
                tmp = 'https://i.jodel.me/' + tmp[4:] + '.mp4'
            else:
                #Pictures
                tmp = 'https://g.jodel.me/' + tmp[6:] + 't.jpg'
            photostr.append(tmp)

    #Download the pics
    for x in photostr:
        path = 'pics/' + str(datetime.datetime.today()).split()[0] + '/' + ch + '/' + x
        if not os.path.exists(os.path.dirname(path)):
            try:
                os.makedirs(os.path.dirname(path))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
        response = requests.get(x, stream=True)
        with open( path, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
            print('Downloading:' + x)
        del response
#Close browser
driver.quit()
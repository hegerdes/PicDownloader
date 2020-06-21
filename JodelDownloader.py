# ##########################################################################
# IMPORTANT
# ONLY Testet on LINUX with Python 3.7
# This provides a script to download all pictues on jodelCity
# Supportet are jpg pictures and mp4 video
# To work all below packages must be installed and the chrome or firefoc webdriver.
# The driver must be in your PATH. (Chrome is much faster)
#
# KNOWN BUGS:   Now all Pictures in the entire channel gets Downloaded but not all videos
#               TODO Make sure the video ID is loaded
#
#               This Script does not get all the pics. JodelCity only loads the first 80
#               or so comments. So only the pics within thes loaded comments will be found.
#               SOLVED
#
#               Somtimes the dirver chraches without a abvious reason. Just restart the Script
#               SOLVED
# Future imprufments:
#               Use base_url + '6789?ajax=1&no=200&to=300' to load post 200 to 300 or base_url + '?gal=1' for picture gallery
##############################################################################
import requests
import re
import os
import traceback
import logging
import time
import emoji
import errno
import shutil
import datetime
import unicodedata
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from operator import is_not
from functools import partial

#Changeable Data
#pause time to scroll
SCROLL_PAUSE_TIME = 0.5
#Number of stars a picture must have to download
MIN_OF_STARS = 5


#URLs
counter = 0
base_url = 'https://www.jodel.city/'
start_chanel_url = base_url + '3300'
dir_path = os.path.dirname(os.path.realpath(__file__))
todaydate = str(datetime.datetime.today()).split()[0]

try:
    #Get the driver
    # On Windows you might have to put the filepath to the driver in like driver = webdrver.Chrome('Path_to_driver')
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)
    #or
    #driver = webdriver.Firefox()

    #Need to call the URL twice
    driver.get(start_chanel_url)
    driver.get(start_chanel_url)

    dropdown = driver.find_elements_by_class_name('padded-list')

    #Save all chanel IDs
    chanels = []
    for t in dropdown:
        if(t.get_attribute('data-value') != None):
            chanels.append(t.get_attribute('data-value'))


    if(len(chanels) < 1):
        print('No Chanels. System exit')
        exit(0)

    #Remove dick chanel
    if('3300' in chanels):
        chanels.remove('3300')

     #Go through all chanels
    for ch in chanels:
        ch_url = base_url + ch
        driver.get(ch_url)

        #Save all picture IDs
        photostr = []
        chTitel = driver.title
        print('Getting Pictures form ' + driver.title)

        #get number of comments that are loaded
        elem = driver.find_element_by_id('contentArea')
        contentList = elem.find_elements_by_tag_name('li')

        #scroll page till no more comments get loaded
        while(len(contentList) > 65):
            elem = driver.find_element_by_id('contentArea')
            contentList = elem.find_elements_by_tag_name('li')
            if(len(contentList) > 30):
                info = driver.find_element_by_xpath('//*[@id="contentArea"]/li[20]')
                driver.execute_script("arguments[0].scrollIntoView();", info)
                time.sleep(SCROLL_PAUSE_TIME)
            if(len(contentList) > 45):
                info = driver.find_element_by_xpath('//*[@id="contentArea"]/li[40]')
                driver.execute_script("arguments[0].scrollIntoView();", info)
                time.sleep(SCROLL_PAUSE_TIME)
            if(len(contentList) > 60):
                info = driver.find_element_by_xpath('//*[@id="contentArea"]/li[60]')
                driver.execute_script("arguments[0].scrollIntoView();", info)
                time.sleep(SCROLL_PAUSE_TIME)

            #get the currend loaded pic-id
            photoRow = driver.find_elements_by_xpath(".//*[@class='ic']")
            for ph in photoRow:
                #get the number of stars
                parent = ph.find_element_by_xpath('./..')
                fav = parent.find_element_by_class_name('fav')
                #get tagname
                tag = parent.find_element_by_class_name('tag')
                try:
                    tag_name = tag.find_element_by_class_name('name')
                    value = tag_name.text
                except NoSuchElementException:
                    value = 'NoTag'
                    continue
                #serialize to filesave name
                value = emoji.demojize(value)
                value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode("utf-8")
                value = value.replace('::','-')
                value = value.replace(':','-')
                value = value.replace(' ','_')
                value = value.replace('#','')
                value = re.sub(r'[-\s]+', '-', value)
                #perfome filename beauty
                if(value[-1:] == '-'):
                    value = value[:-1]
                if(value[:1] == '-'):
                   value = value[1:]
                if(fav.text.strip()):
                    #only downlad if pic has more than MIN_OF_STARS
                    if(int(fav.text) > MIN_OF_STARS):
                        try:
                            tmp = ph.get_attribute('data-navigation')
                        except StaleElementReferenceException:
                            #print('FEHLER1: Element not loaded')
                            continue
                        if(tmp.__contains__('vid')):
                            #Videos
                            ph = ph.find_element_by_class_name('entry')
                            helper = ph.get_attribute('style')
                            #help.split('/')
                            vid = helper.split('/')[-1][:-8]
                            tmp = 'https://jodel.city/v/' + vid + '.mp4'
                        else:
                            #Pictures
                            tmp = 'https://jodel.city/p/' + tmp[6:] + 't.jpg'
                        #Add to list
                        tmp = value + ';' + tmp
                        photostr.append(tmp)

            print("Scrolling...")
            #trigger reload of new posts
            if(len(contentList) > 65):
                #TODO finde a better way
                try:
                    info = driver.find_element_by_xpath('//*[@id="contentArea"]/li[65]')
                    driver.execute_script("arguments[0].scrollIntoView();", info)
                except NoSuchElementException:
                    #print('FEHLER2: No more elements')
                    continue

        #Remove dublicates
        photostr = list(dict.fromkeys(photostr))
        #Download the pics
        for x in photostr:
            if(len(x) > 30):
                username, picurl = x.split(';')
                tmp1, tmp2 = picurl.split('city/')

                path = str(dir_path) + '/Pics/' + todaydate + '/' + username + '-' + todaydate + '-'+ tmp2
                #Create Path
                if not os.path.exists(os.path.dirname(path)):
                    try:
                        os.makedirs(os.path.dirname(path))
                    except OSError as exc:
                        if exc.errno != errno.EEXIST:
                            raise
                #Download files
                response = requests.get(picurl, stream=True)
                with open( path, 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                    print('Downloading: ' + picurl)
                    counter +=1
                del response

#error handling
except Exception as e:
    logging.error(traceback.format_exc())
    print('Error while grabing JC Media. Please tyr again or send the Log to Henne')

print('Downloaded: ' + counter.__str__() + ' Files')
#Close driver
driver.quit()

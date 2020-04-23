
# PicDownloader for Jodel.City

Python Script to Download Pictures and Videos

**UPDATE:** Jode.city doesn't work anymore. You have to find other pages but this still provides a good example for webscraping

**NOTE: NO RESPONSIBILITY FOR THE SITE CONTENT**

**IMPORTANT**

Only Testet on LINUX with Python 3.7

This provides a script to download all pictues on Minus. The website heavy uses JavaScript to prevent downloading. So this scripts automatically visits all the channels and downloads the Pics.

Supported are jpg pictures and mp4 video.

To work all below packages must be installed and the Chrome or Firefox webdriver.
The driver must be in your PATH. *(Chrome is much faster)*

# How to use

* download and install the Webdriver for Chrome (http://chromedriver.chromium.org/downloads) or Firefox (https://github.com/mozilla/geckodriver/releases).
* Put the location of the driver in your PATH.
* Download and install Python3 and pip
* Put both Python and pip in your PATH
* Use `pip install [Name]` to install 
* 1. requests
* 2. selenium
* 3. urllib3
* 4. emoji
* Or use `pip install -r requirments.txt` to install all at one
*
* If you want you can change the MIN_OF_STARS Value the the the minimum of stars a picture must have to be downloaded. Default is 5
* run `python JodelDownloader.py`


# KNOWN BUGS:

               Now all Pictures in the entire channel gets Downloaded but not all videos
               TODO Make sure the video ID is loaded

               This Script does not get all the pics. JodelCity only loads the first 80
               or so comments. So only the pics within thes loaded comments will be found.
               SOLVED

               Somtimes the dirver chraches without a abvious reason. Just restart the Script
               SOLVED

# Future imprufments:

               Use base_url + '6789?ajax=1&no=200&to=300' to load post 200 to 300 or base_url + '?gal=1' for picture gallery

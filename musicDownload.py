# This is the where we download the music request by the user
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time
'''
Path Section:
    geckodriver_path: Path to an executable geckodriver to launch up firefox
    yt_converter_url: Url used to paste youtube links that will convert to mp3 format
    -- testing_youtube_url: Url that will be used to test (Remove later) --
'''
geckodriver_path = os.environ.get('GECKODRIVER')
yt_converter_url = 'https://ytmp3.cc/en13/'
testing_youtube_url = 'https://www.youtube.com/watch?v=gD7lUu-SRwY&list=RDgD7lUu-SRwY&index=1&ab_channel=MixHound'

# We are going to request a url from users and use that url to download using a youtube to mp3 converter
# yt_url = input("Please enter a youtube url of your music: ")
yt_url = testing_youtube_url
web = webdriver.Firefox(executable_path=geckodriver_path)
web.get(yt_converter_url)

# Start putting the url and downloading the mp3 version of the yt link
web.find_element_by_id('input').send_keys(yt_url)
web.find_element_by_id('submit').click()

# Gives 10 seconds to convert and download
try:
    web.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/a[1]').click()
except Exception:
    time.sleep(10)
    web.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/a[1]').click()

web.quit()
# This is the where we download the music request by the user
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from time import sleep

'''
Path Section:
    geckodriver_path: Path to an executable geckodriver to launch up firefox
    yt_converter_url: Url used to paste youtube links that will convert to mp3 format
    -- testing_youtube_url: Url that will be used to test (Remove later) --
'''
default_download_path = f'{os.getcwd()}\\music_downloaded\\'
geckodriver_path = os.environ.get('GECKODRIVER')
yt_converter_url = 'https://ytmp3.cc/en13/'
yt_converter_download_button = '/html/body/div[2]/div[1]/div[1]/div[3]/a[1]'
testing_youtube_url = 'https://www.youtube.com/watch?v=BL1aQsEobOs&ab_channel=Shepuz'

# Creating the default download root
if not os.path.exists(default_download_path):
    os.mkdir(default_download_path)

# FireFox Preferences for Selenium
fp = webdriver.FirefoxProfile()
fp.set_preference('browser.download.dir', default_download_path)
fp.set_preference('browser.download.manager.showWhenStarting', False)
fp.set_preference('browser.download.folderList', 2)
# This preference ignores the download tab that asks what to do with mp3 files
fp.set_preference('browser.helperApps.neverAsk.saveToDisk', '.mp3 audio/mpeg')

# We are going to request a url from users and use that url to download using a youtube to mp3 converter
# yt_url = input("Please enter a youtube url of your music: ")
yt_url = testing_youtube_url
web = webdriver.Firefox(executable_path=geckodriver_path, firefox_profile=fp)
web.get(yt_converter_url)

# Start putting the url and downloading the mp3 version of the yt link
try:
    web.find_element_by_id('input').send_keys(yt_url)
    web.find_element_by_id('submit').click()
except Exception:
    print("Sorry there was an error with your download. Please send a new link of the same song.")

# This is where we want to wait for the download button
try:
    WebDriverWait(web, 60).until(EC.visibility_of_all_elements_located(('tag name', 'a')))
    web.find_element_by_xpath(yt_converter_download_button).click()
except Exception:
    print('We apologize but your download exceeded 1 minute... We will wait for another 40 seconds')
    WebDriverWait(web, 40).until(EC.visibility_of_all_elements_located(('tag name', 'a')))
    web.find_element_by_xpath(yt_converter_download_button).click()


# We wait to wait for the download
def download_not_finished(download_folder):
    part_file = [file for file in os.listdir(download_folder) if file.endswith('.part')]
    if part_file:
        print(part_file)
        return True
    else:
        print('We good')
        return False


while True:
    download_status = download_not_finished(default_download_path)
    if not download_status:
        print('Download Finished')
        web.quit()
        break
    else:
        print('Tick')
        sleep(10)
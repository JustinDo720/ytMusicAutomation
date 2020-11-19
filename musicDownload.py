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
yt_convert_next_button = '/html/body/div[2]/div[1]/div[1]/div[3]/a[3]'
testing_youtube_url1 = 'https://www.youtube.com/watch?v=gD7lUu-SRwY&ab_channel=MixHound'
testing_youtube_url2 = 'https://www.youtube.com/watch?v=YXQUFcsSI7Y'
testing_youtube_url3 = 'https://www.youtube.com/watch?v=32faUlvDxCw&list=PLna2m8Qg4Uj54H6-vz6Vbwv2FgRwio71p&index=1'

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
multi_yt_url = [testing_youtube_url1, testing_youtube_url2]
# CURRENT_LINK_NUMBER = 1
#
# print('''
# Please enter a youtube link below to convert that youtube video to an mp3 form.
# Note: Press "q" to stop adding links.
# ''')
#
# while True:
#     yt_url = input(f'Link {CURRENT_LINK_NUMBER}: ')
#     if yt_url[0].lower() == 'q':
#         break
#     multi_yt_url.append(yt_url)
#     CURRENT_LINK_NUMBER += 1

initial_url = multi_yt_url[0]
last_url = multi_yt_url[-1]
web = webdriver.Firefox(executable_path=geckodriver_path, firefox_profile=fp)
web.get(yt_converter_url)


# We want to have a function that could wait for the download.

def check_existence_of_xpath(xpath):
    try:
        web.find_element_by_xpath(xpath).click()
    except Exception:
        return False
    return True


def download_not_finished(download_folder):
    part_file = [file for file in os.listdir(download_folder) if file.endswith('.part')]
    if part_file:
        print(part_file)
        return True
    else:
        print('We good')
        return False


def wait_for_download(download_directory):
    while True:
        download_in_progress = download_not_finished(download_directory)
        if not download_in_progress:
            print('Download Finished')
            sleep(5)
            web.quit()
            break
        else:
            print('Tick')
            sleep(10)


def convert_and_download(url_to_download, mode):
    try:
        web.find_element_by_id('input').send_keys(url_to_download)
        web.find_element_by_id('submit').click()
    except Exception:
        print("Sorry there was an error with your download. Please send a new link of the same song.")

    # This is where we want to wait for the download button
    try:
        WebDriverWait(web, 60).until(EC.visibility_of_all_elements_located(('tag name', 'a')))
        web.find_element_by_xpath(yt_converter_download_button).click()
    except Exception:
        print('We apologize but your conversion exceeded 1 minute... We will wait for another 40 seconds')
        WebDriverWait(web, 40).until(EC.visibility_of_all_elements_located(('tag name', 'a')))
        web.find_element_by_xpath(yt_converter_download_button).click()


# Start putting the url and downloading the mp3 version of the yt link
for url in multi_yt_url:
    if url == initial_url and url != last_url:
        # Url is the initial but not final
        print('Initial but not final')
    elif url != initial_url and url != last_url:
        # This is part of the middle url
        print('Middle')
    elif url 






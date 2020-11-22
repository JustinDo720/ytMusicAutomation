# This is the where we download the music request by the user
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from time import sleep

"""
Path Section:
    geckodriver_path: Path to an executable geckodriver to launch up firefox
    yt_converter_url: Url used to paste youtube links that will convert to mp3 format
    default_download_path: A directory where users will see their downloaded mp3 files. Auto created if not present.

X Path buttons:
    yt_converter_download_button: download button on the website
    yt_convert_next_button: The convert another button that allows us to enter another url 
"""
default_download_path = f'{os.getcwd()}\\music_downloaded\\'
geckodriver_path = os.environ.get('GECKODRIVER')
yt_converter_url = 'https://ytmp3.cc/en13/'
yt_converter_download_button = '/html/body/div[2]/div[1]/div[1]/div[3]/a[1]'
yt_convert_next_button = '/html/body/div[2]/div[1]/div[1]/div[3]/a[3]'

# Creating the default download root
if not os.path.exists(default_download_path):
    os.mkdir(default_download_path)

# FireFox Preferences for Selenium
fp = webdriver.FirefoxProfile()
fp.set_preference('browser.download.dir', default_download_path)
fp.set_preference('browser.download.folderList', 2)
# This preference ignores the download tab that asks what to do with mp3 files
fp.set_preference('browser.helperApps.neverAsk.saveToDisk', '.mp3 audio/mpeg')
#fp.set_preference('browser.download.manager.showWhenStarting', False)
# We are going to request a url from users and use that url to download using a youtube to mp3 converter

multi_yt_url = []
CURRENT_LINK_NUMBER = 1

print('''
Please enter a youtube link below to convert that youtube video to an mp3 form.
Note: Press "q" to stop adding links.''')


while True:
    yt_url = input(f'Link {CURRENT_LINK_NUMBER}: ').strip()
    if yt_url[0].lower() == 'q':
        break
    multi_yt_url.append(yt_url)
    CURRENT_LINK_NUMBER += 1

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
        # We want these things to be normal regardless of mode.
        web.find_element_by_id('input').send_keys(url_to_download)
        web.find_element_by_id('submit').click()
    except Exception:
        print("Sorry there was an error with your download. Please send a new link of the same song.")

    # This is where we want to wait for the download button
    try:
        WebDriverWait(web, 60).until(EC.visibility_of_all_elements_located(('tag name', 'a')))
        web.find_element_by_xpath(yt_converter_download_button).click()
        # But if theres an initial and that initial != the final then theres a next button that we need to click
        if mode == 'initial' or mode == 'middle':
            web.find_element_by_xpath(yt_convert_next_button).click()
    except Exception:
        print('We apologize but your conversion exceeded 1 minute... We will wait for another 1 minute and 30 seconds')
        WebDriverWait(web, 90).until(EC.visibility_of_all_elements_located(('tag name', 'a')))
        web.find_element_by_xpath(yt_converter_download_button).click()


# Start putting the url and downloading the mp3 version of the yt link
for url in multi_yt_url:
    if url == initial_url and url != last_url:
        # Url is the initial but not final which means there are some middle urls
        # We don't want to end off here because there are some middle urls
        print(url, 'Init')
        convert_and_download(url, mode='initial')
    elif url != initial_url and url != last_url:
        # This is part of the middle url
        print(url,'middle')
        convert_and_download(url, mode='middle')
    else:
        # Url is the last one but could also be the first if the list only contains one url
        print(url, 'first or last')
        convert_and_download(url, mode='first_and_last')
        wait_for_download(default_download_path)






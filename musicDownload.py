# This is the where we download the music request by the user
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from time import sleep
import shutil
from musicDownloadPlaylist import all_links_from_playlist

"""
Path Section:
    geckodriver_path: Path to an executable geckodriver to launch up firefox
    yt_converter_url: Url used to paste youtube links that will convert to mp3 format
    default_download_path: A directory where users will see their downloaded mp3 files. Auto created if not present.

X Path buttons:
    yt_converter_download_button: download button on the website
    yt_convert_next_button: The convert another button that allows us to enter another url 
    yt_error_here_button: When downloading there could have an issue with the download so this button appears for a
    restart
"""
default_download_path = f'{os.getcwd()}\\music_downloaded\\'
geckodriver_path = os.environ.get('GECKODRIVER')
yt_converter_url = 'https://ytmp3.cc/en13/'
yt_converter_download_button = '/html/body/div[2]/div[1]/div[1]/div[3]/a[1]'
yt_convert_next_button = '/html/body/div[2]/div[1]/div[1]/div[3]/a[3]'
yt_error_here_button = '/html/body/div[2]/div[1]/p[2]/a[1]'


def set_up():
    # Creating the default download root
    if not os.path.exists(default_download_path):
        os.mkdir(default_download_path)
    # FireFox Preferences for Selenium
    fp = webdriver.FirefoxProfile()
    fp.set_preference('browser.download.folderList', 2)
    fp.set_preference('browser.download.manager.showWhenStarting', False)
    # This preference ignores the download tab that asks what to do with mp3 files
    fp.set_preference('browser.helperApps.neverAsk.saveToDisk', '.mp3 audio/mpeg')
    # We are going to send the download to our default download folder which is at music_downloaded directory
    fp.set_preference('browser.download.dir', default_download_path)
    web = webdriver.Firefox(executable_path=geckodriver_path, firefox_profile=fp)
    web.get(yt_converter_url)
    return web


# We want to have a function that could wait for the download.
def check_existence_of_xpath(xpath, web):
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


def wait_for_download(download_directory, web):
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


def swap_window_close(yt_download_window, web):
    # Search for pop ups
    try:
        window_after = web.window_handles[1]
        web.switch_to.window(window_after)
        try:
            web.switch_to.alert.accept()
        except Exception:
            print('There is no accept button')
        # If this works then we have pop up window
        web.close()
        web.switch_to.window(yt_download_window)
    except Exception:
        print('No pop ups')


def convert_and_download(url_to_download, mode, web):
    # For our recursion. We want to make this as dynamic as possible.
    current_web = web
    current_download_url = url_to_download
    current_mode = mode
    current_window = web.current_window_handle  # This is the same as web.window_handles[0] which is the initial web

    try:
        # We want these things to be normal regardless of mode.
        web.find_element_by_id('input').send_keys(url_to_download)
        web.find_element_by_id('submit').click()
    except Exception:
        print("Sorry there was an error with your download. Please send a new link of the same song.")

    # This is where we want to wait for the download button
    try:
        WebDriverWait(web, 30).until(EC.element_to_be_clickable(('xpath', yt_converter_download_button)))
        web.find_element_by_xpath(yt_converter_download_button).click()
        swap_window_close(current_window, current_web)
        # But if theres an initial and that initial != the final then theres a next button that we need to click
        if mode == 'initial' or mode == 'middle':
            web.find_element_by_xpath(yt_convert_next_button).click()
    except Exception:
        """
            If we reach here we have one of two problems:
                a) There is an error with the link so we have to retry by clicking an xpath with a label 'here'
                b) The download is actually just too long
            Note: The issue isn't anything with the program but rather the website itself so we need to find a way to 
            identify which of the two are causing the problem
        """
        if check_existence_of_xpath(yt_error_here_button, current_web):
            print('Sorry we got a browser error. Retrying with the same link')
            # We need to wait for that download button to appear before running the process again
            WebDriverWait(web, 10).until(EC.element_to_be_clickable(('xpath', '//*[@id="input"]')))
            # We are back at the home page so we need to run this function again with the same mode
            print(f'Past the driver wait, url:{current_download_url=}, mode:{mode=}')
            convert_and_download(current_download_url, current_mode, current_web)
        else:
            print('We apologize but your conversion exceeded 30 sec. We will wait for another 1 minute and 30 seconds')
            WebDriverWait(web, 90).until(EC.element_to_be_clickable(('xpath', yt_converter_download_button)))
            web.find_element_by_xpath(yt_converter_download_button).click()
            swap_window_close(current_window, current_web)


def download_music(multi_yt_url, changed_dir=None):
    print(multi_yt_url)
    print(changed_dir)
    web = set_up()
    initial_url = multi_yt_url[0]['url']
    last_url = multi_yt_url[-1]['url']
    # Start putting the url and downloading the mp3 version of the yt link
    for url_dict in multi_yt_url:
        # We are targeting the url. Since we passed in dictionaries, we want the url key's value.
        url = url_dict['url']
        print(f'{url=}')
        if url == initial_url and url != last_url:
            # Url is the initial but not final which means there are some middle urls
            # We don't want to end off here because there are some middle urls
            convert_and_download(url, mode='initial', web=web)
        elif url != initial_url and url != last_url:
            # This is part of the middle url
            convert_and_download(url, mode='middle', web=web)
        else:
            # Url is the last one but could also be the first if the list only contains one url
            convert_and_download(url, mode='first_and_last', web=web)
            wait_for_download(default_download_path, web=web)
            # Once all the downloads are in we are going to check if any changes were made to the default dir
            # If the user changes the download path we will send this music_downloaded directory to that path
            if changed_dir:
                shutil.move(default_download_path, changed_dir)


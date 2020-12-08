from selenium import webdriver
import os

default_download_path = f'{os.getcwd()}\\music_downloaded\\'
geckodriver_path = os.environ.get('GECKODRIVER')
total_video_xpath = '/html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-playlist-sidebar-renderer/div/ytd-playlist-sidebar-primary-info-renderer/div[1]/yt-formatted-string[1]/span[1]'


# We are just going to gather info from the playlists
def all_links_from_playlist(url_of_playlist):
    web = webdriver.Firefox(executable_path=geckodriver_path)
    web.get(url_of_playlist)
    total_videos = web.find_elements_by_xpath(total_video_xpath)
    print(type(total_videos[0].text))
    # Initial index is going to be 1 for every playlists but we need to find the total amount of videos
    INITIAL_VALUE = 1
    TOTAL_VALUE = int(total_videos[0].text) + 1 # We add an extra 1 because we want to include the max as our index
    all_links = []
    # Example url: https://www.youtube.com/watch?v=32faUlvDxCw&list=PLna2m8Qg4Uj54H6-vz6Vbwv2FgRwio71p&index=1
    base_url = 'https://www.youtube.com/playlist?list=PLna2m8Qg4Uj54H6-vz6Vbwv2FgRwio71p&index='
    while INITIAL_VALUE != TOTAL_VALUE:
        actual_link_to_download = base_url + str(INITIAL_VALUE)
        all_links.append(actual_link_to_download)
        INITIAL_VALUE += 1

    # At this point all the urls should be in our all_links list so
    web.close()
    return all_links

links = all_links_from_playlist('https://www.youtube.com/playlist?list=PLna2m8Qg4Uj54H6-vz6Vbwv2FgRwio71p')
print(links)
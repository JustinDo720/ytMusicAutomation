from selenium import webdriver
import os

geckodriver_path = os.environ.get('GECKODRIVER')
links_css_path = 'html body ytd-app div#content.style-scope.ytd-app ytd-page-manager#page-manager.style-scope.ytd-app ytd-browse.style-scope.ytd-page-manager ytd-two-column-browse-results-renderer.style-scope.ytd-browse.grid div#primary.style-scope.ytd-two-column-browse-results-renderer ytd-section-list-renderer.style-scope.ytd-two-column-browse-results-renderer div#contents.style-scope.ytd-section-list-renderer ytd-item-section-renderer.style-scope.ytd-section-list-renderer div#contents.style-scope.ytd-item-section-renderer ytd-playlist-video-list-renderer.style-scope.ytd-item-section-renderer div#contents.style-scope.ytd-playlist-video-list-renderer ytd-playlist-video-renderer.style-scope.ytd-playlist-video-list-renderer div#content.style-scope.ytd-playlist-video-renderer a.yt-simple-endpoint.style-scope.ytd-playlist-video-renderer'


# We are just going to gather info from the playlists
def all_links_from_playlist(url_of_playlist):
    web = webdriver.Firefox(executable_path=geckodriver_path)
    try:
        web.get(url_of_playlist)
        all_links = web.find_elements_by_css_selector(links_css_path)
        links = [{'url': url.get_attribute('href'), 'url_name': url.text} for url in all_links]
        web.close()
        return links

    except Exception:
        print("This playlist does not exist or is currently private")



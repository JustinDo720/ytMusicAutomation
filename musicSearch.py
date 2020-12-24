import os
from googleapiclient.discovery import build
from musicImage import save_thumbnail

'''
We are going to need the google python api lib 
    pip install google-api-python-client
    google-api-link: https://github.com/googleapis/google-api-python-client
'''

api_key = os.environ.get('GOOGLE_YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


def search_for_music(music):
    request = youtube.search().list(
        part='snippet',
        maxResults=5,
        q=music

    )

    response = request.execute()

    all_thumbnails = [videos['snippet']['thumbnails']['medium']['url'] for videos in response['items']]

    # Our save_thumbnail function from musicImage returns a list of the file name such as image_1.jpg and image_2.jpg
    new_images = save_thumbnail(all_thumbnails)

    # Note that this will go in order meaning index 0 will have image_1.jpg along with our title and id
    all_videos = [{'video_title': videos['snippet']['title'],
                   'video_id': videos['id']['videoId'],
                   'video_photo': photo}
                  for videos in response['items']
                  for photo in new_images]

    return all_videos
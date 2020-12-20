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
    all_videos = [{'video_title': videos['snippet']['title'], 'video_id': videos['id']['videoId']}
                  for videos in response['items']]

    save_thumbnail(all_thumbnails)
    return all_videos
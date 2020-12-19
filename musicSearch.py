import os
from googleapiclient.discovery import build

'''
We are going to need the google python api lib 
    pip install google-api-python-client
    google-api-link: https://github.com/googleapis/google-api-python-client
'''

api_key = os.environ.get('GOOGLE_YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)

request = youtube.search().list(
    part='snippet',
    maxResults=5,
    q='BEAUZ - Outerspace (feat. Dallas) [Monstercat Release]'

)

response = request.execute()

for videos in response['items']:
    video_id = videos['id']['videoId']
    video_title = videos['snippet']['title']
    video_thumbnail_medium = videos['snippet']['thumbnails']['medium']['url']
    print(video_title)
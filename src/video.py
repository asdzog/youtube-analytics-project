import os
from googleapiclient.discovery import build
api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    """
    Класс для видео
    """
    def __init__(self, video_id):
        self.video_id = video_id
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self.video_id
                                               ).execute()
        self.video_url = f'https://www.youtube.com/watch?v={self.video_id}'
        self.video_title = video_response['items'][0]['snippet']['title']
        self.view_count = int(video_response['items'][0]['statistics']['viewCount'])
        self.like_count = int(video_response['items'][0]['statistics']['likeCount'])
        self.comment_count = int(video_response['items'][0]['statistics']['commentCount'])

    def __str__(self):
        return f'{self.video_title}'


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.pl_id = playlist_id

    def __str__(self):
        return super().__str__()


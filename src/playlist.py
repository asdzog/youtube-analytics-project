import isodate
import os
from googleapiclient.discovery import build
api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:
    """
    Класс для плейлиста на YouTube
    """
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'
        playlist_response = youtube.playlists(
            ).list(part='snippet',
            id=self.playlist_id).execute()
        self.title = playlist_response['items'][0]['snippet']['title']
        self.playlist_videos = youtube.playlistItems(
                    ).list(playlistId=playlist_id,
                           part='contentDetails',
                           maxResults=50,).execute()

    @property
    def total_duration(self):
        """
        Возвращает суммарную длительность всех роликов из плейлиста
        """
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        video_response = youtube.videos().list(
            part='contentDetails,statistics',
            id=','.join(video_ids)).execute()
        total_duration = isodate.parse_duration('PT0S')
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        """
        Возвращает ссылку на видео с наибольшим количеством лайков
        """
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        video_response = youtube.videos().list(
            part='contentDetails,statistics',
            id=','.join(video_ids)).execute()
        max_like_count = int(video_response['items'][0]['statistics']['likeCount'])
        best_video_id = video_response['items'][0]['id']
        for video in video_response['items']:
            like_count = int(video['statistics']['likeCount'])
            if like_count > max_like_count:
                max_like_count = like_count
                best_video_id = video['id']
        return f'https://youtu.be/{best_video_id}'

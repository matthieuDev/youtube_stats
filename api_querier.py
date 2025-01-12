import googleapiclient.discovery

from secret_keys import API_KEY

class youtube_querier_class:
    def __init__(self, apikey=API_KEY):
        self.request_builder = googleapiclient.discovery.build(
            serviceName="youtube", version="v3", developerKey=apikey
        )

    def get_id_channel(self, channel_name):
        request = self.request_builder.channels().list(
            part="id",
            forHandle=channel_name,
        )
        return request.execute()
    
    def get_video_list_from_channel_id(self, channel_id, page_token=None):
        request = self.request_builder.search().list(
            part="snippet",
            channelId=channel_id,
            maxResults=50,
            order="date",
            pageToken=page_token,
        )
        return request.execute()
    
    def get_video_statistic(self, video_id_list):
        request = self.request_builder.videos().list(
            part="snippet,contentDetails,statistics",
            id=','.join(video_id_list)
        )
        return request.execute()

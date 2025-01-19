import googleapiclient.discovery
import os, json

from secret_keys import API_KEY
from path_folder import dump_folder

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

    def get_info_all_videos_of_channel(self, channel_name, dump_folder=dump_folder) :
        save_path = f'{dump_folder}{channel_name}.json'
        if os.path.exists(save_path):
            with open(save_path, encoding='utf8') as f :
                return json.load(f)
            
        channel_info_res = self.get_id_channel(channel_name).get('items', [])
        assert(len(channel_info_res)) == 1
        id_channel = channel_info_res[0].get('id')
        assert id_channel

        nextPageToken = None
        video_list = []
        for i in range(100) :
            video_list_it = self.get_video_list_from_channel_id(id_channel, nextPageToken)
            video_list.extend(video_list_it.get('items', []))
            nextPageToken = video_list_it.get('nextPageToken')
            if not nextPageToken :
                break
                
        info_video = []
        list_video_id = [info['id']['videoId'] for info in video_list if info['id'].get('kind') == 'youtube#video']
        for i in range(0, len(list_video_id), 50):
            info_video.extend(self.get_video_statistic(list_video_id[i:i+50])['items'])

        with open(save_path, 'w', encoding='utf8') as f :
            json.dump(info_video, f)

        return info_video
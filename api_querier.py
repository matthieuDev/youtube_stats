'''
This script interacts with the YouTube Data API to retrieve information 
about channels and their videos. It includes methods to fetch channel IDs, 
video lists, video statistics, and to save all video information of a channel 
to a JSON file for local use.
'''

import googleapiclient.discovery
import os, json

from secret_keys import API_KEY
from path_folder import dump_folder

class youtube_querier_class:
    '''
    A class to query YouTube Data API and retrieve channel and video information.
    '''
    
    def __init__(self, apikey=API_KEY):
        '''
        Initializes the YouTube querier class with an API key.
        Sets up the request builder for YouTube Data API interactions.
        
        :param apikey: API key for authenticating with the YouTube Data API.
        '''
        self.request_builder = googleapiclient.discovery.build(
            serviceName="youtube", version="v3", developerKey=apikey
        )

    def get_id_channel(self, channel_name):
        '''
        Retrieves the channel ID for a given channel name.
        
        :param channel_name: The YouTube channel handle.
        :return: A dictionary containing the channel ID.
        '''
        request = self.request_builder.channels().list(
            part="id",
            forHandle=channel_name,
        )
        return request.execute()
    
    def get_video_list_from_channel_id(self, channel_id, page_token=None):
        '''
        Retrieves a list of videos from a given channel ID.
        
        :param channel_id: The ID of the YouTube channel.
        :param page_token: Token for fetching the next page of results (optional).
        :return: A dictionary containing a list of videos.
        '''
        request = self.request_builder.search().list(
            part="snippet",
            channelId=channel_id,
            maxResults=50,
            order="date",
            pageToken=page_token,
        )
        return request.execute()
    
    def get_video_statistic(self, video_id_list):
        '''
        Retrieves statistics for a list of video IDs.
        
        :param video_id_list: List of video IDs for which statistics are requested.
        :return: A dictionary containing video statistics.
        '''
        request = self.request_builder.videos().list(
            part="snippet,contentDetails,statistics",
            id=','.join(video_id_list)
        )
        return request.execute()

    def get_info_all_videos_of_channel(self, channel_name, dump_folder=dump_folder):
        '''
        Retrieves and saves information for all videos of a specific channel.
        
        :param channel_name: The YouTube channel handle.
        :param dump_folder: Path to the folder where data should be saved.
        :return: A list of dictionaries containing information for all videos.
        '''
        # Determine the file path for saving the data
        save_path = f'{dump_folder}{channel_name}.json'
        
        # Check if the data is already saved locally
        if os.path.exists(save_path):
            with open(save_path, encoding='utf8') as f:
                return json.load(f)
        
        # Fetch the channel ID
        channel_info_res = self.get_id_channel(channel_name).get('items', [])
        assert(len(channel_info_res)) == 1
        id_channel = channel_info_res[0].get('id')
        assert id_channel
        
        # Fetch video list in pages (up to 100 pages or as long as there are results)
        nextPageToken = None
        video_list = []
        for i in range(100):
            video_list_it = self.get_video_list_from_channel_id(id_channel, nextPageToken)
            video_list.extend(video_list_it.get('items', []))
            nextPageToken = video_list_it.get('nextPageToken')
            # Stop if no more pages are available
            if not nextPageToken:
                break
        
        # Retrieve detailed information about videos
        info_video = []
        list_video_id = [
            info['id']['videoId'] 
            for info in video_list 
            if info['id'].get('kind') == 'youtube#video'
        ]
        # Batch requests for up to 50 video IDs
        for i in range(0, len(list_video_id), 50):
            info_video.extend(self.get_video_statistic(list_video_id[i:i+50])['items'])
        
        # Save the collected data to a JSON file
        with open(save_path, 'w', encoding='utf8') as f:
            json.dump(info_video, f)
        
        return info_video

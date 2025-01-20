'''
This script retrieves video data for a specified YouTube channel and generates a 
scatter plot showing the evolution of video views over time. The graph is saved 
to the appropriate folder.
'''

from api_querier import youtube_querier_class
from create_graph import create_view_graph

from path_folder import graph_folder

import sys

if __name__ == '__main__':
    channel_name = sys.argv[1]
    youtube_querier = youtube_querier_class()
    info_videos = youtube_querier.get_info_all_videos_of_channel(channel_name)
    create_view_graph(info_videos, f'{graph_folder}{channel_name}', channel_name)

'''
This script generates a scatter plot showing the evolution of video views for a YouTube channel 
over time.
'''

from datetime import datetime
import matplotlib.pyplot as plt

def create_view_graph(info_videos, save_path, channel_name):
    '''
    Creates and saves a scatter plot of video views over time for a specific channel.

    :param info_videos: List of dictionaries containing video information, including publication 
                        date and view count. Result of youtube_querier_class.get_info_all_videos_of_channel
    :param save_path: Path where the graph image will be saved.
    :param channel_name: The name of the YouTube channel being analyzed.
    '''
    x, y = [], []

    # Process each video to extract publication date and view count
    for info in info_videos:
        dt_created = datetime.strptime(info['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
        second_from_start_year = (dt_created - datetime.fromisoformat(f'{dt_created.year}-01-01')).total_seconds()
        second_in_year = (datetime.fromisoformat(f'{dt_created.year + 1}-01-01') - datetime.fromisoformat(f'{dt_created.year}-01-01')).total_seconds()
        x.append(dt_created.year + second_from_start_year / second_in_year)
        
        y.append(int(info['statistics']['viewCount']))

    # Create the scatter plot
    plt.scatter(x, y, s=5)
    plt.yscale('log')

    # Add titles and labels
    plt.title(f'Evolution des vues de {channel_name} en fonction de leurs dates de sorties')
    plt.xlabel('Année')
    plt.ylabel('Vues')
    plt.grid(True)

    # Save the generated plot to the specified file path
    plt.savefig(save_path)

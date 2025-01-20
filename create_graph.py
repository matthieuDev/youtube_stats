from datetime import datetime
import matplotlib.pyplot as plt

def create_view_graph(info_videos, save_path, channel_name):
    x, y = [] , []

    for info in info_videos :
        dt_created = datetime.strptime(info['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
        second_from_start_year = (dt_created - datetime.fromisoformat(f'{dt_created.year}-01-01')).total_seconds()
        second_in_year = (datetime.fromisoformat(f'{dt_created.year + 1}-01-01') - datetime.fromisoformat(f'{dt_created.year}-01-01')).total_seconds()
        x.append(dt_created.year + second_from_start_year / second_in_year)
        
        y.append(int(info['statistics']['viewCount']))

    plt.scatter(x,y, s=5)
    plt.yscale('log')

    plt.title(f'Evolution des vues de {channel_name} en fonction de leurs dates de sorties')
    plt.xlabel('Année')
    plt.ylabel('Vues')
    plt.grid(True)

    plt.savefig(save_path)
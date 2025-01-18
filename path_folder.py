import os

data_folder = 'data/'

dump_folder = f'{data_folder}/dumps/'
graph_folder = f'{data_folder}/graphs/'

for path in [data_folder, dump_folder, graph_folder] :
    if not os.path.exists(path) :
        os.mkdir(path)
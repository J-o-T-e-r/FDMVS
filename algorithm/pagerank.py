import numpy as np
import pandas as pd
import networkx as nx

data = pd.read_csv('train.csv', names=['v_1', 'v_2'])
v_1s = data['v_1'].values.tolist()
v_2s = data['v_2'].values.tolist()

edges = []
for i in range(len(data)):
    link = (str(v_1s[i]), str(v_2s[i]))
    print(link)
    edges.append(link)

#制作无向图
G = nx.Graph()
for edge in edges:
    G.add_edge(edge[0], edge[1])
G.to_undirected()
#直接调库算pagerank
pagerank_list = nx.pagerank(G, alpha=1)
#排了序列表里面是元组，元组格式是（id, pagerank的值）
pagerank = sorted(pagerank_list.items(), key=lambda x: x[1], reverse=True)
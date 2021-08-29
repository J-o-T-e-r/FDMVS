import networkx as nx

#计算每一条边的边介数
def edge_to_remove(graph):
  G_dict = nx.edge_betweenness_centrality(graph)
  edge = ()
  for key, value in sorted(G_dict.items(), key=lambda item: item[1], reverse = True):
      edge = key
      break
  return edge

def girvan_newman(graph):
    #计算联通分支
    sg = nx.connected_components(graph)
    sg_count = nx.number_connected_components(graph)
    #当联通分支数为1的是谷歌i有进行社区预测
    while (sg_count == 1):
        graph.remove_edge(edge_to_remove(graph)[0])
        sg = nx.connected_components(graph)
        sg_count = nx.number_connected_components(graph)
    return sg

def find_c(G):
    #在图中找到社区
    c = girvan_newman(G.copy())
    #从社区重找到节点
    node_groups = []
    for i in c:
        node_groups.append(list(i))


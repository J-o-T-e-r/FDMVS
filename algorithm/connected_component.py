import pandas as pd

#使用并查集寻找图联通分支

#读取文件信息
data = pd.read_csv('train.csv', names = ['v_1', 'v_2'])
#结点、与其相连的结点
v_1s = data['v_1'].values.tolist()
v_2s = data['v_2'].values.tolist()

#定义图类
class Graph():
    def __init__(self):
        #结点名
        self.nodes = set([])
        #边
        self.edges = []
        #结点数
        self.nodeNumber = 0
        #边数
        self.edgeNumber = 0
        #联通分支
        self.connectedComponents = 0
    #添加结点
    def addNode(self, node):
        self.nodes.add(node)
        self.nodeNumber += 1
    #添加边
    def addEdge(self, node_1, node_2):
        self.edges.append((node_1, node_2))
        self.edgeNumber += 1
    #获取graph当前的结点
    def getNode(self):
        print(self.nodes)
        return list(self.nodes)
    #获取graph当前的边
    def getEdge(self):
        return self.edges

#找到结点的根
def find_root(node):
    son = node
    while father[node] != node:
        node = father[node]

    #路径压缩
    while son != node:
        tmp = father[son]
        father[son] = node
        son = tmp
    return node

def unite(x, y):
    fx, fy = find_root(x), find_root(y)
    if fx != fy:
        father[fx] = fy

def cal_connected_compnt(graph):
    edges, edgesNumber = graph.getEdge(), graph.edgeNumber
    for u, v in edges:
        unite(u, v)
    for key, value in father.items():
        if key == value:
            graph.connectedComponents += 1
    return graph.connectedComponents


if __name__ == '__main__':
    graph = Graph()
    u, v = v_1s, v_2s
    for i in range(len(data)):
        graph.addNode(u[i])
        graph.addNode(v[i])
        graph.addEdge(u[i], v[i])

    father = {}
    #father = {number: number for number in graph.getNode()}
    for node in graph.getNode():
        father[node] = node
    print(cal_connected_compnt(graph))
import pandas as pd
import json


class ClusteringCoefficient:
    def __init__(self):
        pass

    def clustering_coefficient(self, data_file, total_num):
        _data = pd.read_csv('./data/%s.csv' % data_file, header=None)

        df_data = pd.DataFrame(_data)

        _data = list(df_data.values)

        # 计算邻接矩阵（data）

        data = [[0] * total_num for _ in range(total_num)]

        for i, j in _data:
            data[i - 1][j - 1] = 1
            data[j - 1][i - 1] = 1

        # 定义一total_num x total_num的矩阵，用于存储最短路径

        sp_length = [[0] * total_num for _ in range(total_num)]
        node_sp_num = {}

        for i in range(total_num):
            i -= 1
            past_node = []  # 用于存储节点i已经走过的节点
            _past_node = []  # 用于存储节点i上次走过的节点

            for j in range(total_num):  # 遍历total_num个节点，判断是否可达
                if data[i][j] != 0 and sp_length[i][j] == 0:
                    sp_length[i][j] = 1
                    _past_node.append(j)

            n = 2
            while _past_node:  # 判断是否已经走到末节点
                past_node_ = []
                for a in _past_node:
                    if a not in past_node:  # 判断节点a是否已经走过
                        for b in range(total_num):
                            if data[a][b] != 0 and sp_length[i][b] == 0:
                                sp_length[i][b] = n
                                past_node_.append(b)
                past_node.extend(_past_node)  # 将上次走过的节点添加到已经走过的节点集合里
                _past_node = past_node_
                n += 1

            for x in past_node:  # 记录通过每一节点的最短路径数
                node_sp_num.setdefault(x - 1, 0)
                node_sp_num[x - 1] += 1

        # 导出最短路径数

        with open('./data/sp_length.json', 'w', encoding='utf-8') as f1:
            json.dump(sp_length, f1, ensure_ascii=False)

        f1.close()

        # 计算并导出节点中心数

        node_centrality = {}
        for i in range(total_num):
            node_centrality.setdefault(i+1, (total_num - 1)/sum(sp_length[i]))

        with open('./data/node_centrality.json', 'a', encoding='utf-8') as f2:
            json.dump(node_centrality, f2, ensure_ascii=False)

        f2.close()

        all_sp_length = 0  # 计算最短路径总数
        for i in range(total_num):
            all_sp_length += sum(sp_length[i])

        node_intermediate = {}  # 计算节点点介数
        for i in range(total_num):
            node_intermediate.setdefault(i+1, node_sp_num[i]/all_sp_length)

        # 导出节点点介数
        with open('./data/node_intermediate.json', 'a', encoding='utf-8') as f3:
            json.dump(node_intermediate, f3, ensure_ascii=False)

        f3.close()


if __name__ == '__main__':
    cluster = ClusteringCoefficient()
    cluster.clustering_coefficient('train', 10755)

import pandas as pd
import json
import math


class ClusteringCoefficient:
    def __init__(self):
        pass

    def clustering_coefficient(self, data_file, total_num):
        _data = pd.read_csv('./data/%s.csv' % data_file, header=None)

        df_data = pd.DataFrame(_data)

        _data = list(df_data.values)

        # 计算可达性矩阵（data）

        data = [[0] * total_num for _ in range(total_num)]

        for i, j in _data:
            data[i - 1][j - 1] = 1
            data[j - 1][i - 1] = 1

        for x in range(total_num):
            data[x] = [math.inf if i == 0 else i for i in data[x]]

        for i in range(total_num):  # 十字交叉法的位置位置，先列后行
            for j in range(total_num):  # 列 表示dis[j][i]的值，即j->i
                for k in range(total_num):  # 行 表示dis[i][k]的值，即i->k
                    # 先列后行，形成一个传递关系，若比原来距离小，则更新
                    if data[j][k] > data[j][i] + data[i][k]:
                        data[j][k] = data[j][i] + data[i][k]

        # 导出最短路径数
        with open('./data/sp_length.json', 'w', encoding='utf-8') as f1:
            json.dump(data, f1, ensure_ascii=False)

        f1.close()

        # 计算并导出节点中心度
        node_centrality = {}
        for i in range(total_num):
            node_centrality.setdefault(i + 1, (total_num - 1) / sum(data[i]))

        with open('./data/node_centrality.json', 'a', encoding='utf-8') as f2:
            json.dump(node_centrality, f2, ensure_ascii=False)

        f2.close()


if __name__ == '__main__':
    cluster = ClusteringCoefficient()
    cluster.clustering_coefficient('train', 10755)

import pandas as pd
import json


class PredictedDataProcessing:
    def __init__(self):
        df_data = pd.read_csv('./data/train.csv', header=None)

        data = list(df_data.values)

        # 计算邻接矩阵（data）

        self.raw_data = [[0] * 10755 for _ in range(10755)]

        for i, j in data:
            self.raw_data[i - 1][j - 1] = 1
            self.raw_data[j - 1][i - 1] = 1

    def data_processing(self, file_name, total_num):
        processing_data = {}
        with open('./data/%s.json' % file_name, 'r+', encoding='utf-8') as f:
            _processing_data = f.readline()
            _processing_data = dir(_processing_data)
            processing_data.update(_processing_data)
        f.close()

        for i in range(1, total_num):
            i_items = processing_data[str(i)]
            for j in i_items:
                if self.raw_data[i - 1][j[0] - 1] == 1:
                    i_items.remove(j)
            processing_data[str(i)] = i_items

        with open('./data/%s.json' % file_name, 'w', encoding='utf-8') as f:
            json.dump(processing_data, f, ensure_ascii=False)

        f.close()


if __name__ == '__main__':
    processing_data = PredictedDataProcessing()
    processing_data.data_processing('', 10755)

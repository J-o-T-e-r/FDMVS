import pandas as pd


class NetworkDensity:
    def __init__(self):
        pass

    def network_density(self, data_file, total_num):
        df_data = pd.read_csv('./data/%s.csv' % data_file, header=None)

        _data = pd.DataFrame(df_data)

        data = _data.values

        accommodated_num = (total_num * (total_num - 1)) / 2
        actual_num = len(data)

        network_density = actual_num / accommodated_num

        return network_density


if __name__ == '__main__':
    culter = NetworkDensity()
    network_density = culter.network_density('train', 10755)
    print(network_density)

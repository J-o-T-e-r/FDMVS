import json
import pandas as pd
import pymysql

conn = pymysql.connect(  # 连接本地数据库
            host="localhost",
            user="root",  # 要填root
            password="htht0928",  # 填上自己的密码
            database="background",
            charset="utf8"
        )
cur = conn.cursor()


def neighbor_num(id: int, df):
    """计算节点邻居数（边数）"""
    return (df['node1'] == id).sum() + (df['node2'] == id).sum()


def get_connection(id: int, df):
    """计算"""
    con_1 = set(df[df['node1'] == id]['node2'])
    con_2 = set(df[df['node2'] == id]['node1'])
    total_con = list(con_1 | con_2)
    data = {id: total_con}
    return data

df = pd.read_csv('../data/train.csv', header=None)
df.columns = ['node1', 'node2']
content = json.load(open('../data/interests.json'))


sql_i = """
    INSERT INTO NodeInfo(id, neighbour_num, interest, connection)
    VALUES(%s, %s, %s, %s)
"""

a = dict()
for i in range(1, 10756):
    data = (i, neighbor_num(i, df), str(content[str(i)]), str(get_connection(i, df)))
    try:
        cur.execute(sql_i, data)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()

conn.close()
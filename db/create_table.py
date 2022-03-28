import pymysql


conn = pymysql.connect(  # 连接本地数据库
            host="localhost",
            user="root",  # 要填root
            password="htht0928",  # 填上自己的密码
            charset="utf8"
        )
cur = conn.cursor()
cur.execute("create database background character set utf8;")  # 创建一个名为background的数据库
cur.execute("use background;")  # 使用表


# 创建PersonalInfo表
sql_c1 = """
    CREATE TABLE NodeInfo(
    id INT PRIMARY KEY,
    neighbour_num INT,
    interest text,
    connection text
    )
"""
try:
    cur.execute(sql_c1)
except Exception as e:
    print(e)
    # 发生错误则回滚
    conn.rollback()

# 创建一个user表
sql_c2 = """
    CREATE TABLE user(
    username VARCHAR(100),
    pwd VARCHAR(100),
    interest text,
    age INT,
    workplace VARCHAR(50)
    )
"""
try:
    cur.execute(sql_c2)
except Exception as e:
    print(e)
    # 发生错误则回滚
    conn.rollback()

conn.close()
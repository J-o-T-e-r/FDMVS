import pymysql

conn = pymysql.connect(  # 连接本地数据库
            host="localhost",
            user="root",  # 要填root
            password="htht0928",  # 填上自己的密码
            database="background",
            charset="utf8"
        )
cur = conn.cursor()

sql = 'show tables from background'
rows = cur.execute(sql)  # 返回执行成功的结果条数
print(f'一共有 {rows} 张表')


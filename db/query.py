import pymysql
import traceback
from App.log_config import *


def show_table_num():
    """
    展示mysql当前 background数据库表的数量
    主要是用来检查建表是否成功
    """
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


def sql_find(conn, cur, sql, data):
    """
    封装sql的select操作，返回查找结果
    :param conn: 与数据库连接联系的连接对象
    :param cur: 光标对象
    :param sql: sql语句
    :param data: 要查询的数据
    :return: 查找结果results，没有查找到就返回None
    """
    results = None
    try:
        conn.ping(reconnect=True)  # 时间长了可能会断开数据库的连接，需要重连
        cur.execute(sql, data)
        results = cur.fetchone()  # 找到的元组
    except Exception as e:
        msg = traceback.format_exc()
        sql_log.debug(msg)
    return results


def sql_modify(conn, cur, sql, data):
    """
    封装sql的insert和update操作，提交结果
    :param conn: 与数据库连接联系的连接对象
    :param cur: 光标对象
    :param sql: sql语句
    :param data: 需要操作的数据
    :return: 操作是否成功,'success'或'fault'
    """
    res = 'fault'
    try:
        conn.ping(reconnect=True)
        cur.execute(sql, data)
        conn.commit()
        res = 'success'
    except Exception as e:
        msg = traceback.format_exc()
        sql_log.debug(msg)
        conn.rollback()
    return res
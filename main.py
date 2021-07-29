import pandas as pd
import os
from flask import Flask, redirect, url_for, request, render_template
import pymysql
import json
import random
from App.token_fun import *


conn = pymysql.connect(  # 连接本地数据库
            host="localhost",
            user="root",  # 要填root
            password="htht0928",  # 填上自己的密码
            database="background",
            charset="utf8"
        )
cur = conn.cursor()

app = Flask(__name__)


@app.route("/test")
def helloWorld():
    data = {'status': 200, 'mid': '', 'tip': '系统中无此用户'}
    res_json = json.dumps(data, ensure_ascii=False)
    return res_json


@app.route("/")
def index():
    return "index"
    # return render_template('index.html')


@app.route("/api-register-verify", methods=['POST'])
def register_verify():
    username = request.form.get('username') #接受get参数
    sql_f1 = "SELECT * FROM user WHERE name = %s"
    try:
        cur.execute(sql_f1, username)
        results = cur.fetchone()
    except Exception as e:
        print(e)
    if results:
        return 0
    else:
        return 1


@app.route("/api-interest-given", methods=['GET'])
def interest_given():
    print(os.path.abspath('data/AA_similar_.json'))
    interests_rank = json.load(open('data/interests_rank.json'))
    return str(random.sample(list(interests_rank.keys()), 10))


@app.route("/api-register-data", methods=['POST'])
def register_commit():
    username = request.form.get('username')
    pwd = request.form.get('pwd')
    interest = request.form.get('interest')
    age = request.form.get('age')
    workplace = request.form.get('workplace')
    sql_i = """
        INSERT INTO user(username, pwd, interest, age, workplace)
        VALUES(%s, %s, %s, %s, %s)
    """
    data = (username, pwd, interest, age, workplace)
    try:
        cur.execute(sql_i, data)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()


@app.route("/api-login", methods=['POST'])
def login():
    username = request.form.get('username')
    pwd = request.form.get('pwd')
    # 查询是否有此用户
    sql_f1 = "SELECT * FROM user WHERE username = %s"
    try:
        cur.execute(sql_f1, username)
        results = cur.fetchone()
    except Exception as e:
        print(e)
    if not results:
        # 无此账号
        return ''
    elif results[1] != pwd:
        # 密码对不上
        return ''
    else:
        return generate_token(username)


@app.route("/api-login-verify", methods=['POST'])
def login_verify():
    web_token = request.form.get('token')  # 请求发过来的token
    username = request.form.get('username')
    # 查询是否有此用户
    sql_f = "SELECT * FROM user WHERE username = %s"
    try:
        cur.execute(sql_f, username)
        result = cur.fetchone()
    except Exception as e:
        print(e)
    if not result:
        # 无此账号
        return dict()
    else:
        # 有此账号，开始验证
        if certify_token(username, web_token):
            interest = result[2]
            age = result[3]
            workplace = result[4]
            data = {'username': username, 'interest': interest, 'age': age, 'workplace': workplace}
            return json.dumps(data, ensure_ascii=False)
        else:
            return dict()


@app.route("/api-ChangeInfo", methods=['POST'])
def ChangeInfo():
    username = request.form.get('username')
    pwd = request.form.get('pwd')
    interest = request.form.get('interest')
    age = request.form.get('age')
    workplace = request.form.get('workplace')
    sql_update = """
        UPDATE user SET pwd=%s , interest=%s, age=%s, workplace=%s WHERE username=%s
    """
    data = (pwd, interest, age, workplace, username)
    try:
        cur.execute(sql_update, data)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()


@app.route("/api-shown_nodes-data", methods=['GET'])
def shown_nodes():
    # 这里选取的点集是连通分支，也就是说不会有连点集外的边
    connected_nodes = json.load(open('data/connected_component.json', encoding='gbk'))
    sql_f = "SELECT * FROM NodeInfo WHERE id = %s"
    data = []
    for connected_node in connected_nodes:
        try:
            cur.execute(sql_f, connected_node)
            result = cur.fetchone()
        except Exception as e:
            print(e)
        connection = result[-1]
        data.append({"id": connected_node, "connection": connection, "class": "class1"})
    return data


@app.route("/api-id-data", methods=['POST'])
def id_data():
    _id = request.form.get('id')
    sql_f = "SELECT * FROM NodeInfo WHERE id = %s"
    try:
        cur.execute(sql_f, _id)
        results = cur.fetchone()
    except Exception as e:
        print(e)
    interest = results[2]
    neighbour = results[1]
    data = {"interest": interest, "neighbour": 50}
    return json.dumps(data, ensure_ascii=False)


@app.route("/overview-data", methods=['GET'])
def overview_data():
    node_num = 10755
    edge_num = 168540
    net_density = round(0.0029144226831104847, 5)
    connected_component = 164
    data = {"node_num": node_num, "edge_num": edge_num, "net_density": net_density,
            "connected_component": connected_component}
    return json.dumps(data, ensure_ascii=False)


@app.route("/hot_domain", methods=['GET'])
def hot_domain():
    interests_rank = json.load(open('data/interests_rank.json', encoding='gbk'))
    top_num = 10
    top_rank = {list(interests_rank.keys())[i]: list(interests_rank.values())[i] for i in range(top_num)}
    return json.dumps(top_rank, ensure_ascii=False)


@app.route("/excellent_school", methods=['GET'])
def excellent_school():
    university_rank = json.load(open('data/university.json'))
    top_num = 10
    top_rank = {list(university_rank.keys())[i]: list(university_rank.values())[i] for i in range(10)}
    return json.dumps(top_rank, ensure_ascii=False)


@app.route("/excellent_scholar", methods=['GET'])
def excellent_scholar():
    pass
    return "这些是很nb的学者： 鹏总，春妹，芳琪，嘉涛，雍圆"


@app.route("/<_id>", methods=['POST'])
def personal_page():
    pass
    return "这是某个个人页"
    # return render_template("scholar.html", id=_id)


@app.route("/root-data", methods=['POST'])
def root_data():
    _id = request.form.get('id')
    sql_f = "SELECT * FROM NodeInfo WHERE id = %s"
    try:
        cur.execute(sql_f, _id)
        results = cur.fetchone()
    except Exception as e:
        print(e)
    interest = results[2]
    connection = json.dumps(eval(results[-1])[_id], ensure_ascii=False)
    data = {"id": _id, "interest": interest, "connection": connection}
    return json.dumps(data, ensure_ascii=False)


@app.route("/ori-connections", methods=['POST'])
def ori_connections():
    _id = request.form.get('id')
    sql_f = "SELECT * FROM NodeInfo WHERE id = %s"
    try:
        cur.execute(sql_f, _id)
        results = cur.fetchone()
    except Exception as e:
        print(e)
    connection_node = eval(results[-1])[_id]  # 有关系的节点列表
    data = dict()  # 建立一个空字典存放数据
    for node_id in connection_node:
        try:
            cur.execute(sql_f, node_id)
            result = cur.fetchone()
        except Exception as e:
            print(e)
        node_connection = list(eval(result[-1]).values())[0]
        data.setdefault(_id, node_connection)

    return json.dumps(data, ensure_ascii=False)


@app.route("/predict-connections", methods=['POST'])
def predict_connections():
    _id = request.form.get('id')
    pre_nodes = list(json.load(open('data/AA_similar_.json'))[str(_id)])
    data = dict()
    for pre_node in pre_nodes:
        sql_f = "SELECT * FROM NodeInfo WHERE id = %s"
        try:
            cur.execute(sql_f, pre_node)
            results = cur.fetchone()
            interest = results[2]
            data.setdefault(_id, interest)
        except Exception as e:
            print(e)
    return json.dumps(data, ensure_ascii=False)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8787, debug=True)
    app.run(debug=True)
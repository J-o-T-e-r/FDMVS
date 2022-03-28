from flask import Flask, request, render_template
import json
import random
from db.query import *
from flask_cors import *
from App.token_fun import *
from App.log_config import *


conn = pymysql.connect(  # 连接本地数据库
            host="localhost",
            user="root",  # 要填root
            password="htht0928",  # 填上自己的密码
            database="background",
            charset="utf8"
        )
cur = conn.cursor()

app = Flask(__name__)
# limiter = Limiter(
#     app,
#     key_func=get_remote_address,
#     default_limits=["1000 per day", "100 per hour"]
# )
# app.config.from_object(config)
# mail = Mail(app)
CORS(app, supports_credentials=True)


@app.route("/test")
@cross_origin()
def helloWorld():
    data = {'status': 200, 'mid': '', 'tip': '系统中无此用户'}
    res_json = json.dumps(data, ensure_ascii=False)
    return res_json


@app.route("/")
@cross_origin()
def index():
    user_log.info("view index.html")
    return "index.html"


@app.route("/login_register")
@cross_origin()
def login_register_page():
    user_log.info("view login and register page html")
    return "login.html"


@app.route("/api-register-verify", methods=['POST'])
@cross_origin()
def register_verify():
    username = request.form.get('username')  # 接受get参数
    sql_f1 = "SELECT * FROM user WHERE username = %s"
    results = sql_find(conn, cur, sql_f1, username)
    if results is not None:
        # 代表用户重复，不能进行注册
        return 'fault'
    else:
        return 'success'


@app.route("/api-interest-given", methods=['GET'])
@cross_origin()
def interest_given():
    # 用户可选择的研究兴趣
    interests_rank = json.load(open('data/interests_rank.json', encoding="gbk"))
    return str(random.sample(list(interests_rank.keys()), 10))


@app.route("/api-register-data", methods=['POST'])
@cross_origin()
def register_commit():
    username = request.form.get('username')
    pwd = request.form.get('pwd')
    interest = ''
    age = 0
    workplace = ''
    sql_i = """
        INSERT INTO user(username, pwd, interest, age, workplace)
        VALUES(%s, %s, %s, %s, %s)
    """
    data = (username, pwd, interest, age, workplace)
    res = sql_modify(conn, cur, sql_i, data)
    return res


@app.route("/api-login", methods=['POST'])
@cross_origin()
def login():
    # username = request.form.get('username')
    # pwd = request.form.get('pwd')
    # # 查询是否有此用户
    # sql_f1 = "SELECT * FROM user WHERE username = %s"
    # try:
    #     cur.execute(sql_f1, username)
    #     results = cur.fetchone()
    # except Exception as e:
    #     msg = traceback.format_exc()
    #     sql_log.error(msg)
    # if not results:
    #     # 无此账号
    #     return ''
    # elif results[1] != pwd:
    #     # 密码对不上
    #     return ''
    # else:
    #     return generate_token(username)
    username = request.form.get('username')
    pwd = request.form.get('pwd')
    # 查询是否有此用户
    sql_f1 = "SELECT * FROM user WHERE username = %s"
    res = sql_find(conn, cur, sql_f1, username)
    if res is None:
        # 无此账号
        return ''
    elif res[1] != pwd:
        # 密码对不上
        return ''
    else:
        # 匹配则返回token
        return generate_token(username)


@app.route("/api-login-verify", methods=['POST'])
@cross_origin()
def login_verify():
    web_token = request.form.get('token')  # 请求发过来的token
    username = request.form.get('username')
    # 查询是否有此用户
    sql_f = "SELECT * FROM user WHERE username = %s"
    res = sql_find(conn, cur, sql_f, username)
    if res is None:
        # 无此账号
        return dict()
    else:
        # 有此账号，开始验证token（是否为此用户，登录时限是否到了）
        if certify_token(username, web_token):
            interest = res[2]
            age = res[3]
            workplace = res[4]
            data = {'username': username, 'interest': interest, 'age': age, 'workplace': workplace}
            return json.dumps(data, ensure_ascii=False)
        else:
            return dict()


@app.route("/api-ChangeInfo", methods=['POST'])
@cross_origin()
def ChangeInfo():
    username = request.form.get('username')
    interest = request.form.get('interest')
    age = request.form.get('age')
    workplace = request.form.get('workplace')
    sql_update = """
        UPDATE user SET interest=%s, age=%s, workplace=%s WHERE username=%s
    """
    data = (interest, age, workplace, username)
    res = sql_modify(conn,cur, sql_update, data)
    return res


@app.route("/api-shown_nodes-data", methods=['GET'])
@cross_origin()
def shown_nodes():
    # 这里选取的点集是连通分支，也就是说不会有连点集外的边
    connected_nodes = json.load(open('data/connected_component.json', encoding='gbk'))
    sql_f = "SELECT * FROM NodeInfo WHERE id = %s"
    data = []
    for connected_node in connected_nodes:
        result = sql_f(conn, cur, sql_f, connected_node)
        connection = result[-1]
        neighbour = result[1]
        if neighbour > 70:
            _class = "class1"
        elif neighbour > 50:
            _class = "class2"
        else:
            _class = "class3"
        data.append({"id": connected_node, "connection": connection, "class": _class})
    return str(data)


@app.route("/api-id-data", methods=['POST'])
@cross_origin()
def id_data():
    _id = request.form.get('id')
    sql_f = "SELECT * FROM NodeInfo WHERE id = %s"
    results = sql_find(conn, cur, sql_f, _id)
    data = dict()
    if results is not None:
        interest = results[2]
        neighbour = results[1]
        data = {"interest": interest, "neighbour": neighbour}
    return data


def overview_data():
    node_num = 10755
    edge_num = 168540
    net_density = round(0.0029144226831104847, 5)
    connected_component = 164
    data = {"node_num": node_num, "edge_num": edge_num, "net_density": net_density,
            "connected_component": connected_component}
    return data


def hot_domain():
    interests_rank = json.load(open('data/interests_rank.json', encoding='gbk'))
    top_num = 10
    top_rank = {list(interests_rank.keys())[i]: list(interests_rank.values())[i] for i in range(top_num)}
    return top_rank


def excellent_school():
    university_rank = json.load(open('data/university.json', encoding='gbk'))
    top_num = 10
    total_num = sum(list(university_rank.values())[:top_num])
    schools = list(university_rank.keys())[:top_num]
    nums = list(university_rank.values())[:top_num]
    percentages = [round(i / total_num, 2) for i in list(university_rank.values())[:top_num]]
    top_rank = {schools[i]: [nums[i], percentages[i]] for i in range(top_num)}
    return top_rank


def excellent_scholar():
    # 利用了pagerank的数据来绘制气泡图
    bubble_data = json.load(open('data/bubble_diagram.json', encoding="gbk"))
    return bubble_data


@app.route("/api-index_graph_data", methods=['GET'])
def index_graph_data():
    all_data = dict()
    all_data.update(overview_data())
    all_data.update(hot_domain())
    all_data.update(excellent_school())
    all_data.update(excellent_scholar())
    return json.dumps(all_data, ensure_ascii=False)

# @app.route("/<postID>/page", methods=['GET'])
# @cross_origin()
# def personal_page(postID):
#     if not isinstance(postID, str):
#         return "请传输正确的节点值"
#     if int(postID) < 1 or int(postID) > 10755:
#         return "请输入1到10755的节点"
#     user_log.info('view ' + str(postID) + ' personal page')
#     # return '这是节点' + str(postID) + '的个人节点'
#     return render_template("scholar.html", id=postID)


@app.route("/<postID>/root-data", methods=['GET'])
@cross_origin()
def root_data(postID):
    sql_f = "SELECT * FROM NodeInfo WHERE id = %s"
    results = sql_find(conn, cur, sql_f, postID)
    data = dict()
    if results is not None:
        interest = results[2]
        ori_num = results[1]
        predict_connection = list(json.load(open('data/AA_similar_.json', encoding='gbk'))[str(postID)])
        predict_num = len(predict_connection)
        ori_connection = eval(results[-1])[int(postID)]
        data = {"id": postID, "interest": interest, "ori-connection": ori_connection,
                "predict-connection": predict_connection,
                "ori-num": ori_num, "predict-num": predict_num}
        data = json.dumps(data, ensure_ascii=False)
    return data


@app.route("/<postID>/ori-connections", methods=['GET'])
@cross_origin()
def ori_connections(postID):
    if not isinstance(postID, str):
        return "请传输正确的节点值"
    if int(postID) < 1 or int(postID) > 10755:
        return "请输入1到10755的节点"
    sql_f = "SELECT * FROM NodeInfo WHERE id = %s"
    results = sql_find(conn, cur, sql_f, postID)
    data = dict()  # 建立一个空字典存放数据
    if results is not None:
        connection_node = eval(results[-1])[int(postID)]  # 有关系的节点列表
        for node_id in connection_node:
            mid = sql_find(conn, cur, sql_f, node_id)
            node_interest = mid[2]
            data.setdefault(node_id, node_interest)
    return json.dumps(data, ensure_ascii=False)


@app.route("/<postID>/predict-connections", methods=['GET'])
@cross_origin()
def predict_connections(postID):
    if not isinstance(postID, str):
        return "请传输正确的节点值"
    if int(postID) < 1 or int(postID) > 10755:
        return "请输入1到10755的节点"
    pre_nodes = list(json.load(open('data/AA_similar_.json', encoding='gbk'))[str(postID)])
    data = dict()
    for pre_node in pre_nodes:
        sql_f = "SELECT * FROM NodeInfo WHERE id = %s"
        res = sql_find(conn, cur, sql_f, pre_node)
        if res is not None:
            interest = res[2]
            data.setdefault(pre_node, interest)
    return json.dumps(data, ensure_ascii=False)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8787, debug=True)
    app.run(debug=True)

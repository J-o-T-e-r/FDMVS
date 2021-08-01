from flask import Flask, redirect, url_for, request, render_template, make_response
import pymysql
import json
import random
import traceback
from flask_cors import *
from flask_mail import Mail, Message
# from App.mail import *
from App.token_fun import *
from App.log_config import *
import config


conn = pymysql.connect(  # 连接本地数据库
            host="localhost",
            user="root",  # 要填root
            password="htht0928",  # 填上自己的密码
            database="background",
            charset="utf8"
        )
cur = conn.cursor()

app = Flask(__name__)
app.config.from_object(config)
mail = Mail(app)
CORS(app, supports_credentials=True)


@app.route('/mail')
def sendEmail():
    msg = Message('QG中期考核云端服务器事务处理', sender='1219730837@qq.com', recipients=['Horace_01@126.com'])
    msg.body = "服务器出现了bug！"
    mail.send(msg)
    return '已发送'


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
    return render_template('index.html')


@app.route("/login_register")
@cross_origin()
def login_register_page():
    user_log.info("view login and register page html")
    return render_template('log-reg.html')


@app.route("/api-register-verify", methods=['POST'])
@cross_origin()
def register_verify():
    username = request.form.get('username')  # 接受get参数
    sql_f1 = "SELECT * FROM user WHERE username = %s"
    try:
        cur.execute(sql_f1, username)
        results = cur.fetchone()
    except Exception as e:
        msg = traceback.format_exc()
        sql_log.error(msg)
    if results:
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
    try:
        cur.execute(sql_i, data)
        conn.commit()
    except Exception as e:
        msg = traceback.format_exc()
        sql_log.error(msg)
        conn.rollback()
        return 'fault'
    return 'success'


@app.route("/api-login", methods=['POST'])
@cross_origin()
def login():
    username = request.form.get('username')
    pwd = request.form.get('pwd')
    # 查询是否有此用户
    sql_f1 = "SELECT * FROM user WHERE username = %s"
    try:
        cur.execute(sql_f1, username)
        results = cur.fetchone()
    except Exception as e:
        msg = traceback.format_exc()
        sql_log.error(msg)
    if not results:
        # 无此账号
        return ''
    elif results[1] != pwd:
        # 密码对不上
        return ''
    else:
        return generate_token(username)


@app.route("/api-login-verify", methods=['POST'])
@cross_origin()
def login_verify():
    web_token = request.form.get('token')  # 请求发过来的token
    username = request.form.get('username')
    # 查询是否有此用户
    sql_f = "SELECT * FROM user WHERE username = %s"
    try:
        cur.execute(sql_f, username)
        result = cur.fetchone()
    except Exception as e:
        msg = traceback.format_exc()
        sql_log.error(msg)
        return dict()
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
@cross_origin()
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
        msg = traceback.format_exc()
        sql_log.error(msg)
        conn.rollback()
        return 'fault'
    return 'success'


@app.route("/api-shown_nodes-data", methods=['GET'])
@cross_origin()
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
            msg = traceback.format_exc()
            sql_log.error(msg)
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
    try:
        cur.execute(sql_f, _id)
        results = cur.fetchone()
        interest = results[2]
        neighbour = results[1]
        data = {"interest": interest, "neighbour": neighbour}
        return json.dumps(data, ensure_ascii=False)
    except Exception as e:
        msg = traceback.format_exc()
        sql_log.error(msg)
        return redirect(url_for('sendEmail'))



@app.route("/overview-data", methods=['GET'])
@cross_origin()
def overview_data():
    node_num = 10755
    edge_num = 168540
    net_density = round(0.0029144226831104847, 5)
    connected_component = 164
    data = {"node_num": node_num, "edge_num": edge_num, "net_density": net_density,
            "connected_component": connected_component}
    return json.dumps(data, ensure_ascii=False)


@app.route("/hot_domain", methods=['GET'])
@cross_origin()
def hot_domain():
    interests_rank = json.load(open('data/interests_rank.json', encoding='gbk'))
    top_num = 10
    top_rank = {list(interests_rank.keys())[i]: list(interests_rank.values())[i] for i in range(top_num)}
    return json.dumps(top_rank, ensure_ascii=False)


@app.route("/excellent_school", methods=['GET'])
@cross_origin()
def excellent_school():
    university_rank = json.load(open('data/university.json', encoding="gbk"))
    top_num = 10
    total_num = sum(list(university_rank.values())[:top_num])
    schools = list(university_rank.keys())[:top_num]
    nums = list(university_rank.values())[:top_num]
    percentages = [round(i / total_num, 2) for i in list(university_rank.values())[:top_num]]
    top_rank = {schools[i]: [nums[i], percentages[i]] for i in range(top_num)}
    return json.dumps(top_rank, ensure_ascii=False)


@app.route("/excellent_scholar", methods=['GET'])
@cross_origin()
def excellent_scholar():
    # 利用了pagerank的数据来绘制气泡图
    bubble_data = json.load(open('data/bubble_diagram.json', encoding="gbk"))
    return str(bubble_data)


@app.route("/<postID>/page", methods=['GET'])
@cross_origin()
def personal_page(postID):
    if not isinstance(postID, str):
        return "请传输正确的节点值"
    if int(postID) < 1 or int(postID) > 10755:
        return "请输入1到10755的节点"
    user_log.info('view ' + str(postID) + ' personal page')
    return '这是节点' + str(postID) + '的个人节点'
    return render_template("scholar.html", id=postID)


@app.route("/<postID>/root-data", methods=['GET'])
@cross_origin()
def root_data(postID):
    if not isinstance(postID, str):
        return "请传输正确的节点值"
    if int(postID) < 1 or int(postID) > 10755:
        return "请输入1到10755的节点"
    sql_f = "SELECT * FROM NodeInfo WHERE id = %s"
    try:
        cur.execute(sql_f, postID)
        results = cur.fetchone()
        interest = results[2]
        ori_num = results[1]
        predict_connection = list(json.load(open('data/AA_similar_.json', encoding='gbk'))[str(postID)])
        predict_num = len(predict_connection)
        ori_connection = eval(results[-1])[int(postID)]
        data = {"id": postID, "interest": interest, "ori-connection": ori_connection,
                "predict-connection": predict_connection,
                "ori-num": ori_num, "predict-num": predict_num}
        return json.dumps(data, ensure_ascii=False)
    except Exception as e:
        msg = traceback.format_exc()
        sql_log.error(msg)
        return dict()



@app.route("/<postID>/ori-connections", methods=['GET'])
@cross_origin()
def ori_connections(postID):
    if not isinstance(postID, str):
        return "请传输正确的节点值"
    if int(postID) < 1 or int(postID) > 10755:
        return "请输入1到10755的节点"
    sql_f = "SELECT * FROM NodeInfo WHERE id = %s"
    try:
        cur.execute(sql_f, postID)
        results = cur.fetchone()
    except Exception as e:
        msg = traceback.format_exc()
        sql_log.error(msg)
        return dict()
    connection_node = eval(results[-1])[int(postID)]  # 有关系的节点列表
    data = dict()  # 建立一个空字典存放数据
    for node_id in connection_node:
        try:
            cur.execute(sql_f, node_id)
            result = cur.fetchone()
        except Exception as e:
            msg = traceback.format_exc()
            sql_log.error(msg)
        node_interest = result[2]
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
        try:
            cur.execute(sql_f, pre_node)
            results = cur.fetchone()
            interest = results[2]
            data.setdefault(pre_node, interest)
            return json.dumps(data, ensure_ascii=False)
        except Exception as e:
            msg = traceback.format_exc()
            sql_log.error(msg)
            return dict()



if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8787, debug=True)
    app.run(debug=True)

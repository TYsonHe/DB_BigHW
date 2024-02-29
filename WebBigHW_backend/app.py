import pymysql
import os
import io
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, decode_token
from werkzeug.security import generate_password_hash, check_password_hash


# 引入自己编写的模块
from CrawlManager import CrawlManager

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'Tyson'  # 使用一个安全的密钥
jwt = JWTManager(app)


# 解决跨域问题
CORS(app, resources={r'/*': {'origins': '*'}})


# 测试
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

# 登录区域


@app.route('/user/login', methods=['POST'])
def login():
    # 获取前端传过来的数据
    username = request.get_json()['username']
    password = request.get_json()['password']
    print(f'username: {username}, password: {password}')
    # 连接数据库
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='',
        db='ocean_data',
        charset='utf8'
    )
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select * from user_info where user_name = '%s' and password = '%s'" % (
        username, password)
    data = cur.execute(sql)
    result = cur.fetchall()
    print(result)
    if len(result) == 0:
        return jsonify(
            {
                'code': 400,
                'message': '用户名或密码错误'
            }
        )
    else:
        token = create_access_token(identity=username)
        roles = result[0]['roles']
        return jsonify(
            {
                'code': 200,
                'token': token,
                'message': '登录成功',
                'roles': roles
            }
        )


@app.route('/user/info', methods=['GET'])
def user_info():
    # 获取token
    token = request.headers.get('X-Token')
    # 根据token获取用户名
    decoded_token = decode_token(token)
    print(decoded_token)
    username = decoded_token['sub']
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='',
        db='ocean_data',
        charset='utf8'
    )
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select * from user_info where user_name = '%s'" % username
    data = cur.execute(sql)
    result = cur.fetchall()
    print(result)
    temp = result[0]['roles']
    result[0]['roles'] = [temp]
    return jsonify(
        {
            'code': 200,
            'data': result
        }
    )


if __name__ == '__main__':
    app.run(debug=True)

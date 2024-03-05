import pymysql
import os
import io
from CrudDb import CrudDb
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, decode_token
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'Tyson'  # 使用一个安全的密钥
jwt = JWTManager(app)

db = CrudDb('configs\db.yml')

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
    sql = "select * from user_info where user_name = '%s' and password = '%s'" % (
        username, password)
    result = db.RetrieveData(sql)
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
    sql = "select * from user_info where user_name = '%s'" % username
    result = db.RetrieveData(sql)
    print(result)
    temp = result[0]['roles']
    result[0]['roles'] = [temp]
    return jsonify(
        {
            'code': 200,
            'data': result
        }
    )


@app.route('/user/all', methods=['GET'])
def user_all():
    sql = "select * from user_info"
    result = db.RetrieveData(sql)
    print(result)
    return jsonify(
        {
            'code': 200,
            'data': result
        }
    )


@app.route('/user/add', methods=['POST'])
def user_add():
    username = request.get_json()['user_name']
    password = request.get_json()['password']
    roles = request.get_json()['roles']
    station_id = request.get_json()['station_id']
    sql = "insert into user_info(user_name, password, roles, station_id) values('%s', '%s', '%s', '%s')" % (
        username, password, roles, station_id)
    result = db.CreateData(sql)
    if result == 'CreateSuccess':
        return jsonify(
            {
                'code': 200,
                'message': '添加成功'
            }
        )
    else:
        return jsonify(
            {
                'code': 400,
                'message': '添加失败'
            }
        )


@app.route('/user/update', methods=['POST'])
def user_update():
    user_id = request.get_json()['user_id']
    username = request.get_json()['user_name']
    password = request.get_json()['password']
    roles = request.get_json()['roles']
    station_id = request.get_json()['station_id']
    sql = "update user_info set user_name = '%s', password = '%s', roles = '%s', station_id = '%s' where user_id = '%s'" % (
        username, password, roles, station_id, user_id)
    result = db.UpdateData(sql)
    if result == 'UpdateSuccess':
        return jsonify(
            {
                'code': 200,
                'message': '更新成功'
            }
        )
    else:
        return jsonify(
            {
                'code': 400,
                'message': '更新失败'
            }
        )


@app.route('/user/delete', methods=['POST'])
def user_delete():
    user_ids = request.get_json()['user_ids']
    # 支持批量删除,这里的user_ids是一个列表,需要转换成字符串,里面是int类型
    user_ids = ','.join([str(i) for i in user_ids])
    sql = "delete from user_info where user_id in (%s)" % user_ids
    result = db.DeleteData(sql)
    if result == 'DeleteSuccess':
        return jsonify(
            {
                'code': 200,
                'message': '删除成功'
            }
        )
    else:
        return jsonify(
            {
                'code': 400,
                'message': '删除失败'
            }
        )


if __name__ == '__main__':
    app.run(debug=True)

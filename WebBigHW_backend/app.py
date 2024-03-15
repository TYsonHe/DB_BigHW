import pymysql
import os
import io
import pendulum
from CrudDb import CrudDb
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, decode_token
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'Tyson'  # 使用一个安全的密钥
jwt = JWTManager(app)

db = CrudDb('configs\db.yml')

# 时区设置
pendulum.set_locale('zh')

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


# user_management区域
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
        now_time = pendulum.now().format('YYYY-MM-DD HH:mm:ss')
        # 这里只能admin添加用户,所以user_id写死为1
        sql = "insert into logs(user_id, action, time) values('%s', '添加用户', '%s')" % (
            1, now_time)
        db.CreateData(sql)
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
        now_time = pendulum.now().format('YYYY-MM-DD HH:mm:ss')
        # 这里只能admin更改用户,所以user_id写死为1
        sql = "insert into logs(user_id, action, time) values('%s', '更改用户', '%s')" % (
            1, now_time)
        db.CreateData(sql)
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
        now_time = pendulum.now().format('YYYY-MM-DD HH:mm:ss')
        # 这里只能admin删除用户,所以user_id写死为1
        sql = "insert into logs(user_id, action, time) values('%s', '删除用户', '%s')" % (
            1, now_time)
        db.CreateData(sql)
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


# species_management区域
@app.route('/species/all', methods=['GET'])
def species_all():
    sql = "select * from species"
    result = db.RetrieveData(sql)
    print(result)
    return jsonify(
        {
            'code': 200,
            'data': result
        }
    )


@app.route('/species/add', methods=['POST'])
def species_add():
    all_data = request.get_json()
    species_name = all_data['species_name']
    # 是否重复名字
    sql = "select * from species where species_name = '%s'" % species_name
    result = db.RetrieveData(sql)
    if len(result) != 0:
        return jsonify(
            {
                'code': 400,
                'message': '物种名字重复'
            }
        )
    # 查看是否有description
    if 'description' in all_data:
        description = all_data['description']
        sql = "insert into species(species_name, description) values('%s', '%s')" % (
            species_name, description)
    else:
        sql = "insert into species(species_name) values('%s')" % species_name
    result = db.CreateData(sql)
    if result == 'CreateSuccess':
        now_time = pendulum.now().format('YYYY-MM-DD HH:mm:ss')
        # 这里需要获取当前用户的user_id
        token = request.headers.get('X-Token')
        decoded_token = decode_token(token)
        username = decoded_token['sub']
        sql = "select * from user_info where user_name = '%s'" % username
        result = db.RetrieveData(sql)
        user_id = result[0]['user_id']
        sql = "insert into logs(user_id, action, time) values('%s', '添加物种', '%s')" % (
            user_id, now_time)
        db.CreateData(sql)
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


@app.route('/species/update', methods=['POST'])
def species_update():
    all_data = request.get_json()
    species_id = all_data['species_id']
    species_name = all_data['species_name']
    # 是否重复名字
    sql = "select * from species where species_name = '%s' and species_id != '%s'" % (
        species_name, species_id)
    result = db.RetrieveData(sql)
    if len(result) != 0:
        return jsonify(
            {
                'code': 400,
                'message': '物种名字重复'
            }
        )
    # 查看是否有description
    if 'description' in all_data:
        description = all_data['description']
        sql = "update species set species_name = '%s', description = '%s' where species_id = '%s'" % (
            species_name, description, species_id)
    else:
        sql = "update species set species_name = '%s' where species_id = '%s'" % (
            species_name, species_id)
    result = db.UpdateData(sql)
    if result == 'UpdateSuccess':
        now_time = pendulum.now().format('YYYY-MM-DD HH:mm:ss')
        # 这里需要获取当前用户的user_id
        token = request.headers.get('X-Token')
        decoded_token = decode_token(token)
        username = decoded_token['sub']
        sql = "select * from user_info where user_name = '%s'" % username
        result = db.RetrieveData(sql)
        user_id = result[0]['user_id']
        sql = "insert into logs(user_id, action, time) values('%s', '更改物种', '%s')" % (
            user_id, now_time)
        db.CreateData(sql)
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


@app.route('/species/delete', methods=['POST'])
def species_delete():
    species_ids = request.get_json()['species_ids']
    # 支持批量删除,这里的species_ids是一个列表,需要转换成字符串,里面是int类型
    species_ids = ','.join([str(i) for i in species_ids])
    sql = "delete from species where species_id in (%s)" % species_ids
    result = db.DeleteData(sql)
    if result == 'DeleteSuccess':
        now_time = pendulum.now().format('YYYY-MM-DD HH:mm:ss')
        # 这里需要获取当前用户的user_id
        token = request.headers.get('X-Token')
        decoded_token = decode_token(token)
        username = decoded_token['sub']
        sql = "select * from user_info where user_name = '%s'" % username
        result = db.RetrieveData(sql)
        user_id = result[0]['user_id']
        sql = "insert into logs(user_id, action, time) values('%s', '删除物种', '%s')" % (
            user_id, now_time)
        db.CreateData(sql)
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

# station_management区域


@app.route('/station/all', methods=['GET'])
def station_all():
    sql = "select * from stations"
    result = db.RetrieveData(sql)
    print(result)
    return jsonify(
        {
            'code': 200,
            'data': result
        }
    )


@app.route('/station/add', methods=['POST'])
def station_add():
    all_data = request.get_json()
    station_name = all_data['station_name']
    location_name = all_data['location_name']
    # 是否重复名字
    sql = "select * from stations where station_name = '%s'" % station_name
    result = db.RetrieveData(sql)
    if len(result) != 0:
        return jsonify(
            {
                'code': 400,
                'message': '站点名字重复'
            }
        )
    # 查看是否有equipment
    if 'equipment' in all_data:
        equipment = all_data['equipment']
        sql = "insert into stations(station_name, location_name, equipment) values('%s', '%s', '%s')" % (
            station_name, location_name, equipment)
    else:
        sql = "insert into stations(station_name, location_name) values('%s', '%s')" % (
            station_name, location_name)
    result = db.CreateData(sql)
    if result == 'CreateSuccess':
        now_time = pendulum.now().format('YYYY-MM-DD HH:mm:ss')
        # 因为只有admin可以添加站点,所以user_id写死为1
        sql = "insert into logs(user_id, action, time) values('%s', '添加站点', '%s')" % (
            1, now_time)
        db.CreateData(sql)
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


@app.route('/station/update', methods=['POST'])
def station_update():
    all_data = request.get_json()
    station_id = all_data['station_id']
    station_name = all_data['station_name']
    location_name = all_data['location_name']
    # 是否重复名字
    sql = "select * from stations where station_name = '%s' and station_id != '%s'" % (
        station_name, station_id)
    result = db.RetrieveData(sql)
    if len(result) != 0:
        return jsonify(
            {
                'code': 400,
                'message': '站点名字重复'
            }
        )
    # 查看是否有equipment
    if 'equipment' in all_data:
        equipment = all_data['equipment']
        sql = "update stations set station_name = '%s', location_name = '%s', equipment = '%s' where station_id = '%s'" % (
            station_name, location_name, equipment, station_id)
    else:
        sql = "update stations set station_name = '%s', location_name = '%s' where station_id = '%s'" % (
            station_name, location_name, station_id)
    result = db.UpdateData(sql)
    if result == 'UpdateSuccess':
        now_time = pendulum.now().format('YYYY-MM-DD HH:mm:ss')
        # 因为只有admin可以更改站点,所以user_id写死为1
        sql = "insert into logs(user_id, action, time) values('%s', '更改站点', '%s')" % (
            1, now_time)
        db.CreateData(sql)
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


@app.route('/station/delete', methods=['POST'])
def station_delete():
    station_ids = request.get_json()['station_ids']
    # 支持批量删除,这里的station_ids是一个列表,需要转换成字符串,里面是int类型
    station_ids = ','.join([str(i) for i in station_ids])
    sql = "delete from stations where station_id in (%s)" % station_ids
    result = db.DeleteData(sql)
    if result == 'DeleteSuccess':
        now_time = pendulum.now().format('YYYY-MM-DD HH:mm:ss')
        # 因为只有admin可以删除站点,所以user_id写死为1
        sql = "insert into logs(user_id, action, time) values('%s', '删除站点', '%s')" % (
            1, now_time)
        db.CreateData(sql)
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

# logs_management区域


@app.route('/logs/all', methods=['GET'])
def logs_all():
    sql = "select * from logs"
    result = db.RetrieveData(sql)
    print(result)
    return jsonify(
        {
            'code': 200,
            'data': result
        }
    )


if __name__ == '__main__':
    app.run(debug=True)

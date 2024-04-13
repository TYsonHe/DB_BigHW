import pymysql
import os
import io
import pendulum
from CrudDb import CrudDb
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, decode_token
from werkzeug.security import generate_password_hash, check_password_hash

from monitoring_mission import MonitoringMission
from alert_task import Alert_task
from station import Station
from species import Species
from user import User
from station_species import Station_species

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
    return User().get_all_users(db)


@app.route('/user/add', methods=['POST'])
def user_add():
    all_data = request.get_json()
    return User().add_user(db, all_data)


@app.route('/user/update', methods=['POST'])
def user_update():
    all_data = request.get_json()
    return User().update_user(db, all_data)


@app.route('/user/delete', methods=['POST'])
def user_delete():
    all_data = request.get_json()
    return User().delete_user(db, all_data)


# species_management区域
@app.route('/species/all', methods=['GET'])
def species_all():
    return Species().get_all_species(db)


@app.route('/species/add', methods=['POST'])
def species_add():
    all_data = request.get_json()
    return Species().add_species(db, all_data, request)


@app.route('/species/update', methods=['POST'])
def species_update():
    all_data = request.get_json()
    return Species().update_species(db, all_data, request)


@app.route('/species/delete', methods=['POST'])
def species_delete():
    all_data = request.get_json()
    return Species().delete_species(db, all_data, request)

# station_management区域


@app.route('/station/all', methods=['GET'])
def station_all():
    return Station().get_all_stations(db)


@app.route('/station/add', methods=['POST'])
def station_add():
    all_data = request.get_json()
    return Station().add_station(db, all_data)


@app.route('/station/update', methods=['POST'])
def station_update():
    all_data = request.get_json()
    return Station().update_station(db, all_data)


@app.route('/station/delete', methods=['POST'])
def station_delete():
    all_data = request.get_json()
    return Station().delete_station(db, all_data)

# logs_management区域


@app.route('/logs/all', methods=['GET'])
def logs_all():
    sql = "select * from logs ORDER BY `timestamp` DESC"
    result = db.RetrieveData(sql)
    print(result)
    return jsonify(
        {
            'code': 200,
            'data': result
        }
    )

# monitoring_management区域
# 共2个页面，一个是监控任务管理，一个是接受任务
# 监控任务管理界面


@app.route('/monitor_mission_management/getAllMonitoringTasks', methods=['GET'])
def getAllMonitoringTasks():
    return MonitoringMission().get_all_missions(db)


@app.route('/monitor_mission_management/addMonitoringTask', methods=['POST'])
def addMonitoringTask():
    all_data = request.get_json()
    return MonitoringMission().add_mission(db, all_data)


@app.route('/monitor_mission_management/updateMonitoringTask', methods=['POST'])
def updateMonitoringTask():
    all_data = request.get_json()
    return MonitoringMission().update_mission(db, all_data)


@app.route('/monitor_mission_management/deleteMonitoringTask', methods=['POST'])
def deleteMonitoringTask():
    all_data = request.get_json()
    return MonitoringMission().delete_mission(db, all_data)

# 接受监控任务界面


@app.route('/monitor_task/getMonitorTaskListByRole', methods=['GET'])
def getMonitorTaskListByRole():
    return MonitoringMission().get_task_list_by_role(db, request)


@app.route('/monitor_task/acceptMonitorTask', methods=['POST'])
def acceptMonitorTask():
    return MonitoringMission().accept_monitor_task(db, request)


@app.route('/monitor_task/getAllMonitorTaskCount', methods=['GET'])
def getAllMonitorTaskCount():
    return MonitoringMission().get_all_task_count(db)


@app.route('/monitor_task/getMiddleChartData', methods=['POST'])
def getMiddleChartData():
    return MonitoringMission().get_middle_chart_data(db, request)


@app.route('/monitor_task/getRightChartData', methods=['POST'])
def getRightChartData():
    return MonitoringMission().get_right_chart_data(db, request)

# alert_task_management区域
# 报警任务界面，只有一个界面


@app.route('/alert_task/getAlertTaskListByRole', methods=['GET'])
def getAlertTaskListByRole():
    return Alert_task().get_alert_task_by_role(db, request)


@app.route('/alert_task/acceptAlertTask', methods=['POST'])
def acceptAlertTask():
    return Alert_task().accept_alert_task(db, request)


@app.route('/alert_task/getAllAlertTaskCount', methods=['GET'])
def getAllTaskCount():
    return Alert_task().get_all_task_count(db)


@app.route('/alert_task/getMiddleChartData', methods=['POST'])
def getAlertMiddleChartData():
    return Alert_task().get_middle_chart_data(db, request)


@app.route('/alert_task/getRightChartData', methods=['POST'])
def getAlertRightChartData():
    return Alert_task().get_right_chart_data(db, request)


@app.route('/alert_task/generateAlertTask', methods=['GET'])
def generateAlertTask():
    return Alert_task().generate_alert_task(db,request)

# 站点物种数量观察页面


@app.route('/station_species_management/get_station_species_list', methods=['GET'])
def get_station_species_list():
    return Station_species().get_station_species_list(db, request)


@app.route('/station_species_management/get_station_species_quantity_series', methods=['POST'])
def get_station_species_quantity_series():
    return Station_species().get_station_species_quantity_series(db, request)


@app.route('/station_species_management/get_station_species_quantity_total', methods=['POST'])
def get_station_species_quantity_total():
    return Station_species().get_station_species_quantity_total(db, request)


@app.route('/station_species_management/get_station_species_quantity_rank', methods=['POST'])
def get_station_species_quantity_rank():
    return Station_species().get_station_species_quantity_rank(db, request)


if __name__ == '__main__':
    app.run(debug=True)

from flask import jsonify
import pendulum
from CrudDb import CrudDb
import random
from flask_jwt_extended import decode_token


class Alert_task:

    def __init__(self) -> None:
        # 时区设置
        pendulum.set_locale('zh')

    def get_all_alert_task(self, db: CrudDb):
        sql = "select * from alert_task ORDER BY CASE status WHEN 'Undone' THEN 1 WHEN 'Done' THEN 2 END"
        result = db.RetrieveData(sql)
        return jsonify(
            {
                'code': 200,
                'data': result
            }
        )

    def generate_alert_task(self, db: CrudDb):
        generate_cnt = 0
        return jsonify(
            {
                'code': 200,
                'message': f'生成{generate_cnt}个报警任务,生成成功'
            }
        )

    def get_alert_task_by_role(self, db: CrudDb, request):
        # 获取token
        token = request.headers.get('X-Token')
        # 解析token
        user_info = decode_token(token)
        # 获取用户名
        user_name = user_info['sub']
        # 获取用户信息
        sql = "select * from user_info where user_name = '%s'" % user_name
        result = db.RetrieveData(sql)
        user_role = result[0]['roles']
        # 获取用户所在的观测站id
        station_id = result[0]['station_id']
        if user_role == 'admin':
            sql = "select * from alert_task ORDER BY CASE status WHEN 'Undone' THEN 1 WHEN 'Done' THEN 2 END"
            task_list = db.RetrieveData(sql)
            return jsonify(
                {
                    'code': 200,
                    'data': {
                        'task_list': task_list,
                        'user_role': 'admin',
                        'station_id': station_id
                    }
                }
            )

        # 获取用户所在的观测站对应的报警任务
        sql = "select * from alert_task where station_id = %d ORDER BY CASE status WHEN 'Undone' THEN 1 WHEN 'Done' THEN 2 END" % station_id
        task_list = db.RetrieveData(sql)
        return jsonify(
            {
                'code': 200,
                'data': {
                    'task_list': task_list,
                    'user_role': 'user',
                    'station_id': station_id
                }
            }
        )

    def accept_alert_task(self, db: CrudDb, request):

        return jsonify(
            {
                'code': 200,
                'message': '接受任务成功'
            }
        )

    def get_all_task_count(self, db: CrudDb):
        sql = "select count(*) from alert_task"
        task_count = db.RetrieveData(sql)[0]['count(*)']
        return jsonify(
            {
                'code': 200,
                'data': {
                    'task_count': task_count
                }
            }
        )

    def get_middle_chart_data(self, db: CrudDb, request):

        curstation_id = request.get_json()['station_id']
        if curstation_id == 0:
            # 代表是admin,获取所有站点的数据
            sql = "select count(*) from user_info"
            user_count = db.RetrieveData(sql)[0]['count(*)']
            # 获取今日已完成的任务数
            today = pendulum.now().format('YYYY-MM-DD')
            sql = "select count(*) from alert_task where status = 'Done' and end_time like '%s%%'" % today
            done_count = db.RetrieveData(sql)[0]['count(*)']
            # 获取未完成的任务数
            sql = "select count(*) from alert_task where status = 'Undone'"
            undone_count = db.RetrieveData(sql)[0]['count(*)']
            data_list = []
            data_list.append(user_count)
            data_list.append(done_count)
            data_list.append(undone_count)
            return jsonify(
                {
                    'code': 200,
                    'data': {
                        'dataList': data_list
                    }
                }
            )
        # 获取该站点的人员总数
        sql = "select count(*) from user_info where station_id = %d" % curstation_id
        user_count = db.RetrieveData(sql)[0]['count(*)']
        # 获取今日已完成的任务数
        today = pendulum.now().format('YYYY-MM-DD')
        sql = "select count(*) from alert_task where station_id = %d and status = 'Done' and end_time like '%s%%'" % (
            curstation_id, today)
        done_count = db.RetrieveData(sql)[0]['count(*)']
        # 获取未完成的任务数
        sql = "select count(*) from alert_task where station_id = %d and status = 'Undone'" % curstation_id
        undone_count = db.RetrieveData(sql)[0]['count(*)']

        data_list = []
        data_list.append(user_count)
        data_list.append(done_count)
        data_list.append(undone_count)
        return jsonify(
            {
                'code': 200,
                'data': {
                    'dataList': data_list
                }
            }
        )

    def get_right_chart_data(self, db: CrudDb, request):
        all_data = request.get_json()
        station_id = all_data['station_id']
        quantity_series = []
        # 随机生成10个数据
        for i in range(10):
            quantity_series.append(
                random.randint(2, 4)
            )
        return jsonify(
            {
                'code': 200,
                'data': {
                    'dataQuantityList': quantity_series
                }
            }
        )

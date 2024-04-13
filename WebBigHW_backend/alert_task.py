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

    def generate_alert_task(self, db: CrudDb, request):
        generate_cnt = 0
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
        now_time = pendulum.now().format('YYYY-MM-DD HH:mm:ss')
        if user_role == 'admin':
            # 查找所有的观测站记录
            # alert_type 有3类，分别是：
            # 1、 物种数量锐减 < 100
            # 2、 物种数量激增 > 10000
            # 3、 物种即将消失 < 10
            sql = "select * from species_records where quantity < 500 or quantity > 10000 or quantity < 10"
            species_records = db.RetrieveData(sql)
            for species_record in species_records:
                alert_type = ''
                if species_record['quantity'] < 100:
                    alert_type = '物种数量锐减'
                elif species_record['quantity'] > 10000:
                    alert_type = '物种数量激增'
                else:
                    alert_type = '物种即将消失'
                sql = "insert into alert_task (station_id, alert_type, start_time, species_id) values (%d, '%s', '%s', %d)" % (
                    station_id, alert_type, now_time, species_record['species_id'])
                db.CreateData(sql)
                generate_cnt += 1

        # 生成用户所在的观测站对应的报警任务
        sql = "select * from species_records where station_id = %d and (quantity < 500 or quantity > 10000 or quantity < 10)" % station_id
        species_records = db.RetrieveData(sql)
        for species_record in species_records:
            alert_type = ''
            if species_record['quantity'] < 100:
                alert_type = '物种数量锐减'
            elif species_record['quantity'] > 10000:
                alert_type = '物种数量激增'
            else:
                alert_type = '物种即将消失'
            sql = "insert into alert_task (station_id, alert_type, start_time, species_id) values (%d, '%s', '%s', %d)" % (
                station_id, alert_type, now_time, species_record['species_id'])
            db.CreateData(sql)
            generate_cnt += 1

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
        # 获取token
        token = request.headers.get('X-Token')
        # 解析token
        user_info = decode_token(token)
        # 获取用户名
        user_name = user_info['sub']
        # 获取用户信息
        sql = "select * from user_info where user_name = '%s'" % user_name
        result = db.RetrieveData(sql)
        # 获取用户角色,用户id
        user_role = result[0]['roles']
        user_id = result[0]['user_id']

        all_data = request.get_json()
        species_id = all_data['species_id']
        quantity = int(all_data['quantity'])
        station_id = all_data['station_id']
        alert_task_id = all_data['alert_task_id']
        now_time = pendulum.now().format('YYYY-MM-DD HH:mm:ss')
        # 更新预警记录表
        sql = "insert into alert_records (alert_task_id, species_id, quantity, station_id, create_time) values (%d, %d, %d, %d, '%s')" % (
            alert_task_id, species_id, quantity, station_id, now_time)
        print(db.CreateData(sql))

        # 更新物种数量表
        # 插入数据,判断是否曾经有过相同的species_id,station_id,如果有,则更新quantity,否则插入新数据
        sql = "select * from species_records where species_id = %d and station_id = %d" % (
            species_id, station_id)
        result = db.RetrieveData(sql)
        if len(result) > 0:
            sql = "update species_records set quantity = %d and timestamp = '%s' where species_id = %d and station_id = %d" % (
                quantity, now_time, species_id, station_id)
            print(db.UpdateData(sql))
        else:
            sql = "insert into species_records (species_id, quantity, station_id, timestamp) values (%d, %d, %d,'%s')" % (
                species_id, quantity, station_id, now_time)
            print(db.CreateData(sql))

        # 插入日志
        sql = "insert into logs (user_id, action, timestamp) values (%d, '接受了预警任务,物种id:%d,数量:%d', '%s')" % (
            user_id, species_id, quantity, now_time)
        print(db.CreateData(sql))

        # 更新预警任务状态为已完成
        sql = "update alert_task set status = 'Done', end_time = '%s' where alert_task_id = %d" % (
            now_time, alert_task_id)
        print(db.UpdateData(sql))

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
                random.randint(1, 3)
            )
        return jsonify(
            {
                'code': 200,
                'data': {
                    'dataQuantityList': quantity_series
                }
            }
        )

from flask import jsonify
import pendulum
from CrudDb import CrudDb
from flask_jwt_extended import decode_token


class MonitoringMission:

    def __init__(self) -> None:
        # 时区设置
        pendulum.set_locale('zh')

    def get_all_missions(self, db: CrudDb):
        sql = "select * from monitoring_task"
        result = db.RetrieveData(sql)
        return jsonify(
            {
                'code': 200,
                'data': result
            }
        )

    def add_mission(self, db: CrudDb, all_data):
        monitoring_task_name = all_data['monitoring_task_name']
        station_id = all_data['station_id']
        # 检查任务名字是否重复
        sql = "select * from monitoring_task where monitoring_task_name = '%s'" % monitoring_task_name
        result = db.RetrieveData(sql)
        if len(result) > 0:
            return jsonify(
                {
                    'code': 400,
                    'message': '任务名字重复'
                }
            )
        start_time = pendulum.now().format('YYYY-MM-DD HH:mm:ss')
        sql = "insert into monitoring_task (monitoring_task_name, station_id, start_time) values ('%s', '%s', '%s')" % (
            monitoring_task_name, station_id, start_time)
        result = db.CreateData(sql)
        if result == 'CreateSuccess':
            now_time = pendulum.now().format('YYYY-MM-DD HH:mm:ss')
            # 因为只有admin可以添加监控任务,所以user_id写死为1
            sql = "insert into logs (user_id, action, timestamp) values ('1', '添加了监控任务:%s', '%s')" % (
                monitoring_task_name, now_time)
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

    def update_mission(self, db: CrudDb, all_data):
        monitoring_task_id = all_data['monitoring_task_id']
        monitoring_task_name = all_data['monitoring_task_name']
        station_id = all_data['station_id']
        # 检查任务名字是否重复
        sql = "select * from monitoring_task where monitoring_task_name = '%s'" % monitoring_task_name
        result = db.RetrieveData(sql)
        if len(result) > 0:
            return jsonify(
                {
                    'code': 400,
                    'message': '任务名字重复'
                }
            )
        sql = "update monitoring_task set monitoring_task_name = '%s', station_id = '%s' where monitoring_task_id = '%s'" % (
            monitoring_task_name, station_id, monitoring_task_id)
        result = db.UpdateData(sql)
        if result == 'UpdateSuccess':
            now_time = pendulum.now().format('YYYY-MM-DD HH:mm:ss')
            # 因为只有admin可以更改监控任务,所以user_id写死为1,赋上修改的任务id
            sql = "insert into logs (user_id,action,timestamp) values ('1','修改了监控任务id为%s的任务','%s')" % (
                monitoring_task_id, now_time)
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

    def delete_mission(self, db: CrudDb, all_data):
        monitoring_task_ids = all_data['monitoring_task_ids']
        # 支持批量删除,这里的monitoring_task_ids是一个列表,需要转换成字符串,里面是int类型
        monitoring_task_ids = ','.join([str(i) for i in monitoring_task_ids])
        sql = "delete from monitoring_task where monitoring_task_id in (%s)" % monitoring_task_ids
        result = db.DeleteData(sql)
        if result == 'DeleteSuccess':
            now_time = pendulum.now().format('YYYY-MM-DD HH:mm:ss')
            # 因为只有admin可以删除站点,所以user_id写死为1
            sql = "insert into logs(user_id, action, timestamp) values('%s', '删除监控任务id:%s', '%s')" % (
                1, monitoring_task_ids, now_time)
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

    # 下面是接受监控任务的接口
    def get_task_list_by_role(self, db: CrudDb, request):
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
            # 获取所有的监控任务
            sql = "select * from monitoring_task"
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
        # 获取用户角色所在的观测站对应的监控任务
        sql = "select * from monitoring_task where station_id = %d" % station_id
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

    def accept_monitor_task(self, db: CrudDb, request):
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
        monitoring_task_id = all_data['monitoring_task_id']
        now_time = pendulum.now().format('YYYY-MM-DD HH:mm:ss')
        # 更新监测记录表
        sql = "insert into monitoring_records (species_id, quantity, station_id, monitoring_task_id, timestamp) values (%d, %d, %d, %d, '%s')" % (
            species_id, quantity, station_id, monitoring_task_id, now_time)
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
        sql = "insert into logs (user_id, action, timestamp) values (%d, '接受了监控任务,物种id:%d,数量:%d', '%s')" % (
            user_id, species_id, quantity, now_time)
        print(db.CreateData(sql))

        # 判断任务是否完成
        # 获取任务id
        is_done = all_data['is_done']
        if is_done == 'Done':
            monitoring_task_id = all_data['monitoring_task_id']
            sql = "update monitoring_task set status='Done' where monitoring_task_id=%d" % monitoring_task_id
            db.UpdateData(sql)

        return jsonify(
            {
                'code': 200,
                'message': '接受成功'
            })

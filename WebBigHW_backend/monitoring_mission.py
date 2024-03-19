from flask import jsonify
import pendulum
from CrudDb import CrudDb


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

    def add_mission(self, db, all_data):
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

    def update_mission(self, db, all_data):
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

    def delete_mission(self, db, all_data):
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

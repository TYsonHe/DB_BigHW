from flask import request, jsonify
import pendulum
from CrudDb import CrudDb
from flask_jwt_extended import decode_token


class User:

    def __init__(self) -> None:
        # 时区设置
        pendulum.set_locale('zh')

    def get_all_users(self, db: CrudDb):
        sql = "select * from user_info"
        result = db.RetrieveData(sql)
        return jsonify(
            {
                'code': 200,
                'data': result
            }
        )

    def add_user(self, db: CrudDb, all_data):
        username = all_data['user_name']
        password = all_data['password']
        roles = all_data['roles']
        station_id = all_data['station_id']
        sql = "insert into user_info(user_name, password, roles, station_id) values('%s', '%s', '%s', '%s')" % (
            username, password, roles, station_id)
        result = db.CreateData(sql)
        if result == 'CreateSuccess':
            now_time = pendulum.now().format('YYYY-MM-DD HH:mm:ss')
            # 这里只能admin添加用户,所以user_id写死为1
            sql = "insert into logs(user_id, action, timestamp) values('%s', '添加用户:%s', '%s')" % (
                1, username, now_time)
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

    def update_user(self, db: CrudDb, all_data):
        user_id = all_data['user_id']
        username = all_data['user_name']
        password = all_data['password']
        roles = all_data['roles']
        station_id = all_data['station_id']
        sql = "update user_info set user_name = '%s', password = '%s', roles = '%s', station_id = '%s' where user_id = '%s'" % (
            username, password, roles, station_id, user_id)
        result = db.UpdateData(sql)
        if result == 'UpdateSuccess':
            now_time = pendulum.now().format('YYYY-MM-DD HH:mm:ss')
            # 这里只能admin更改用户,所以user_id写死为1
            sql = "insert into logs(user_id, action, timestamp) values('%s', '更改用户id:%s', '%s')" % (
                1, user_id, now_time)
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

    def delete_user(self, db: CrudDb, all_data):
        user_ids = all_data['user_ids']
        # 支持批量删除,这里的user_ids是一个列表,需要转换成字符串,里面是int类型
        user_ids = ','.join([str(i) for i in user_ids])
        sql = "delete from user_info where user_id in (%s)" % user_ids
        result = db.DeleteData(sql)
        if result == 'DeleteSuccess':
            now_time = pendulum.now().format('YYYY-MM-DD HH:mm:ss')
            # 这里只能admin删除用户,所以user_id写死为1
            sql = "insert into logs(user_id, action, timestamp) values('%s', '删除用户id:%s', '%s')" % (
                1, user_ids, now_time)
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

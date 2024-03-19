from flask import request, jsonify
import pendulum
from CrudDb import CrudDb
from flask_jwt_extended import decode_token


class Species:

    def __init__(self) -> None:
        # 时区设置
        pendulum.set_locale('zh')

    def get_all_species(self, db: CrudDb):
        sql = "select * from species"
        result = db.RetrieveData(sql)
        return jsonify(
            {
                'code': 200,
                'data': result
            }
        )

    def add_species(self, db: CrudDb, all_data, request):
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
            sql = "insert into logs(user_id, action, timestamp) values('%s', '添加物种:%s', '%s')" % (
                user_id, species_name, now_time)
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

    def update_species(self, db: CrudDb, all_data, request):
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
            sql = "insert into logs(user_id, action, timestamp) values('%s', '更改物种id:%s', '%s')" % (
                user_id, species_id, now_time)
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

    def delete_species(self, db: CrudDb, all_data, request):
        species_ids = all_data['species_ids']
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
            sql = "insert into logs(user_id, action, timestamp) values('%s', '删除物种id:%s', '%s')" % (
                user_id, species_ids, now_time)
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

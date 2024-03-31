from flask import jsonify
import pendulum
from CrudDb import CrudDb
from flask_jwt_extended import decode_token
import random


class Station_species:

    def __init__(self) -> None:
        # 时区设置
        pendulum.set_locale('zh')

    def get_station_species_list(self, db: CrudDb, request):
        # 获取token
        token = request.headers['X-Token']
        # 解析token
        user_info = decode_token(token)
        # 获取用户名
        user_name = user_info['sub']
        # 获取用户信息
        sql = "select * from user_info where user_name = '%s'" % user_name
        result = db.RetrieveData(sql)
        # 获取用户角色,观测站id
        user_role = result[0]['roles']
        station_id = result[0]['station_id']
        # 如果是管理员
        if user_role == 'admin':
            # 获取所有的观测站物种
            sql = "select * from species_records join species on species_records.species_id = species.species_id"
            species_list = db.RetrieveData(sql)
            return jsonify(
                {
                    'code': 200,
                    'data': {
                        'species_list': species_list,
                        'user_role': 'admin',
                        'station_id': station_id
                    }
                }
            )
        else:
            # 获取用户所在观测站的物种
            sql = "select * from species_records join species on species_records.species_id = species.species_id where station_id = %d" % station_id
            species_list = db.RetrieveData(sql)
            return jsonify(
                {
                    'code': 200,
                    'data': {
                        'species_list': species_list,
                        'user_role': 'user',
                        'station_id': station_id
                    }
                }
            )

    def get_station_species_quantity_series(self, db: CrudDb, request):
        all_data = request.get_json()
        station_id = all_data['station_id']
        quantity_series = []
        # 随机生成10个数据
        for i in range(10):
            quantity_series.append(
                random.randint(700, 1000)
            )

        return jsonify(
            {
                'code': 200,
                'data': {
                    'dataQuantityList': quantity_series,
                }
            }
        )

    def get_station_species_quantity_total(self, db: CrudDb, request):
        all_data = request.get_json()
        station_id = all_data['station_id']
        # 获取物种总数
        sql = "select count(*) from species_records where station_id = %d" % station_id
        result = db.RetrieveData(sql)
        num = random.randint(700, 1000)
        return jsonify(
            {
                'code': 200,
                'data': {
                    'total': num
                }
            })

    def get_station_species_quantity_rank(self, db: CrudDb, request):
        all_data = request.get_json()
        station_id = all_data['station_id']
        # 获取物种数量排名
        # 随机制作10个物种，降序排列，格式为[id,value]
        species_list = []
        for i in range(10):
            species_list.append(
                [random.randint(1, 100), random.randint(700, 1000)]
            )
        return jsonify(
            {
                'code': 200,
                'data': {
                    'species_list': species_list
                }
            })

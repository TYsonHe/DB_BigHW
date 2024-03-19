from flask import jsonify
import pendulum
from CrudDb import CrudDb


class Station:

    def __init__(self) -> None:
        # 时区设置
        pendulum.set_locale('zh')

    def get_all_stations(self, db: CrudDb):
        sql = "select * from stations"
        result = db.RetrieveData(sql)
        return jsonify(
            {
                'code': 200,
                'data': result
            }
        )

    def add_station(self, db: CrudDb, all_data):
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
            sql = "insert into logs(user_id, action, timestamp) values('%s', '添加站点:%s', '%s')" % (
                1, station_name, now_time)
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

    def update_station(self, db: CrudDb, all_data):
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
            sql = "insert into logs(user_id, action, timestamp) values('%s', '更改站点id:%s', '%s')" % (
                1, station_id, now_time)
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

    def delete_station(self, db: CrudDb, all_data):
        station_ids = all_data['station_ids']
        # 支持批量删除,这里的station_ids是一个列表,需要转换成字符串,里面是int类型
        station_ids = ','.join([str(i) for i in station_ids])
        sql = "delete from stations where station_id in (%s)" % station_ids
        result = db.DeleteData(sql)
        if result == 'DeleteSuccess':
            now_time = pendulum.now().format('YYYY-MM-DD HH:mm:ss')
            # 因为只有admin可以删除站点,所以user_id写死为1
            sql = "insert into logs(user_id, action, timestamp) values('%s', '删除站点id:%s', '%s')" % (
                1, station_ids, now_time)
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

from flask import jsonify
import pendulum
from CrudDb import CrudDb
from flask_jwt_extended import decode_token
import random


class Bigscreen:

    def __init__(self) -> None:
        # 时区设置
        pendulum.set_locale('zh')

    def get_scoll_down_data(self, db: CrudDb):
        '''
        获取滚动数据
        包含monitoring task和alert task
        '''
        # 获取monitoring task
        sql = "select * from monitoring_task"
        monitoring_task = db.RetrieveData(sql)
        # 获取alert task
        sql = "select * from alert_task"
        alert_task = db.RetrieveData(sql)

        # 拼成一个列表
        # ['task_id', 'task_type','station_id','status']
        # 其中task_id就用各自的
        # task_type就用monitoring和alert
        # station_id就用各自的
        # status就用各自的

        # 生成monitoring task的数据
        monitoring_task_data = []
        for data in monitoring_task:
            monitoring_task_data.append(
                [data['monitoring_task_id'], 'monitoring',
                    data['station_id'], data['status']]
            )
        # 生成alert task的数据
        alert_task_data = []
        for data in alert_task:
            alert_task_data.append(
                [data['alert_task_id'], 'alert', data['station_id'], data['status']]
            )

        # 合并两个列表
        all_data = monitoring_task_data + alert_task_data

        return jsonify(
            {
                'code': 200,
                'data': all_data
            }
        )

    def get_species_number(self, db: CrudDb):
        '''
        获取物种数量
        '''
        # 获取species表中的物种数量
        sql = "select count(*) from species"
        species_number = db.RetrieveData(sql)
        return jsonify(
            {
                'code': 200,
                'data': species_number[0]['count(*)']
            }
        )

    def get_species_count(self, db: CrudDb):
        '''
        获取物种数量总数
        '''
        # 获取species表中的物种数量
        sql = "select sum(quantity) as total_quantity from species_records"
        species_count = db.RetrieveData(sql)
        return jsonify(
            {
                'code': 200,
                'data': species_count[0]['total_quantity']
            }
        )

    def get_monitoring_task_cnt(self, db: CrudDb):
        '''
        获取monitoring task的数量
        '''
        sql = "select count(*) from monitoring_task"
        monitoring_task_cnt = db.RetrieveData(sql)
        return jsonify(
            {
                'code': 200,
                'data': monitoring_task_cnt[0]['count(*)']
            }
        )

    def get_alert_task_cnt(self, db: CrudDb):
        '''
        获取alert task的数量
        '''
        sql = "select count(*) from alert_task"
        alert_task_cnt = db.RetrieveData(sql)
        return jsonify(
            {
                'code': 200,
                'data': alert_task_cnt[0]['count(*)']
            }
        )

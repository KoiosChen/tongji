from .. import db, logger, socketio, redis_db
from flask_socketio import send, emit
import json

import re
from datetime import timedelta


@socketio.on('connect', namespace='/test')
def test_connect():
    print('connect')


@socketio.on('cashier check', namespace='/test')
def cashier_check():
    # 获取出口闸机对应的摄像头信息
    print('cashier check')
    # exit_camera = Camera.query.filter_by(gate_id=EXIT_GATE).first()
    #
    # # 获取出口记录
    # if redis_db.get(exit_camera.device_number):
    #     exit_record = json.loads(redis_db.get(exit_camera.device_number).decode())
    #     print(exit_record.get('number_plate'))
    #
    #     exit_check.exit_check(exit_record, operate_source=10)
    # else:
    #     socketio.emit('ws_test', {'status': 'true',
    #                               'content': {
    #                                   'number_plate': '',
    #                                   'entry_time': '',
    #                                   'exit_time': '',
    #                                   'entry_unit_price': '',
    #                                   'entry_pic': '',
    #                                   'entry_plate_number_pic': '',
    #                                   'exit_pic': '',
    #                                   'exit_plate_number_pic': '',
    #                                   'fee': '',
    #                                   'totally_time': '',
    #                                   'parking_record_id': ''}
    #                               }, namespace='/test')


@socketio.on('paid opening', namespace='/test')
def paid_opening(data):
    logger.debug(data)
    # try:
    #     parking_record_id = data.get('parking_record_id')
    #     fee = eval(re.findall('(\d+\.?\d+)', data.get('fee'))[0])
    #     parking_record = ParkingRecords.query.filter_by(uuid=parking_record_id).first()
    #     if parking_record.exit_time:
    #         parking_record.exit_validate_before = parking_record.exit_time + timedelta(minutes=20)
    #     pay_result = do_pay(parking_record_id, fee, operate_source=10)
    #     if pay_result:
    #         assert open_gate(parking_record_id, direction=1, operate_source=12), "开闸失败"
    #         emit('paid result', {'status': 'true', 'content': '已付费可离场'}, namespace='/test')
    #     else:
    #         emit('paid result', {'status': 'false', 'content': '付费失败'}, namespace='/test')
    # except Exception as e:
    #     logger.error(e)

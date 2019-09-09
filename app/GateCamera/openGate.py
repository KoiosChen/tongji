from .. import redis_db, logger, hSDK_handle
from flask import request, jsonify

def open(camera_ip):
    try:
        #assert True if redis_db.get('open_gate_func').decode() == '1' else False, 'open gate service stopped'

        if camera_ip in hSDK_handle.keys():
            hSDK_handle[camera_ip].open_gate()
            redis_db.delete(camera_ip)
            return {'code': 'success', 'message': '已发送开门指令', 'data': ''}
        else:
            return {'code': 'fail', 'message': '开门失败，无法连接摄像头', 'data': ''}

    except Exception as e:
        logger.error(e)
        return {'code': 'fail', 'message': '开门失败 ' + str(e), 'data': ''}

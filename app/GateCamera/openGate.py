from .. import redis_db, logger, hSDK_handle
from flask import request, jsonify




def open(camera_ip):
    try:
        assert True if redis_db.get('open_gate_func').decode() == '1' else False, 'open gate service stopped'

        if camera_ip in hSDK_handle.keys():
            hSDK_handle[camera_ip].open_gate()
            return {'code': 'success', 'message': 'open gate command has been sent', 'data': ''}
        else:
            return {'code': 'fail', 'message': 'hSDK does not exist', 'data': ''}

    except Exception as e:
        logger.error(e)
        return {'code': 'fail', 'message': 'job put into queue fail for ' + str(e), 'data': ''}
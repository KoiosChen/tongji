from .. import redis_db, logger, hSDK_handle


def open(camera_ip):
    try:
        # assert True if redis_db.get('open_gate_func').decode() == '1' else False, 'open gate service stopped'

        if camera_ip in hSDK_handle.keys():
            hSDK_handle[camera_ip].open_gate()
            redis_db.delete(camera_ip + '_camera')
            return {'code': 'success', 'message': '已发送开门指令', 'data': ''}
        else:
            return {'code': 'fail', 'message': '开门失败，无法连接摄像头', 'data': ''}

    except Exception as e:
        logger.error(e)
        return {'code': 'fail', 'message': '开门失败 ' + str(e), 'data': ''}


def close(camera_ip):
    try:
        if camera_ip in hSDK_handle.keys():
            close_result = hSDK_handle[camera_ip].close_gate()
            return {'code': 'success', 'message': '已关闸' if close_result else '关闸失败', 'data': ''}
        else:
            return {'code': 'fail', 'message': '关门失败，无法连接摄像头', 'data': ''}
    except Exception as e:
        logger.error(e)
        return {'code': 'fail', 'message': '关门失败 ' + str(e), 'data': ''}

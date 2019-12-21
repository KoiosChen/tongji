from .. import redis_db, logger, hSDK_handle
from .camera_status import status


def open_it(camera_ip):
    try:
        if camera_ip in hSDK_handle.keys():
            assert status(camera_ip), "道闸无法连接"
            hSDK_handle[camera_ip].open_gate()
            redis_db.delete(camera_ip + '_camera')
            return {'code': 'success', 'message': '已发送开门指令', 'data': ''}
        else:
            return {'code': 'fail', 'message': '开门失败，无法连接摄像头', 'data': ''}

    except Exception as e:
        logger.error(e)
        return {'code': 'fail', 'message': f'open_gate gate {camera_ip} fail for ' + str(e), 'data': ''}


def close_it(camera_ip):
    try:
        if camera_ip in hSDK_handle.keys():
            close_result = hSDK_handle[camera_ip].close_gate()
            return {'code': 'success', 'message': '已关闸' if close_result else '关闸失败', 'data': ''}
        else:
            return {'code': 'fail', 'message': '关门失败，无法连接摄像头', 'data': ''}
    except Exception as e:
        logger.error(e)
        return {'code': 'fail', 'message': '关门失败 ' + str(e), 'data': ''}

from flask import request, jsonify
from ..models import *
from .. import logger, work_q, redis_db, hSDK_handle
from . import main
from ..decorators import permission_ip


@main.route('/openGate', methods=['POST'])
@permission_ip(PermissionIP)
def openGate():
    """
    只允许PermissionIP中涉及的服务器访问
    :return:
    """

    try:
        assert True if redis_db.get('open_gate_func').decode() == '1' else False, 'open gate service stopped'
        print(request.json)
        request_data = request.json['data']
        if request_data['ip'] in hSDK_handle.keys():
            hSDK_handle[request_data['ip']].open_gate()
            return jsonify({'code': 'success', 'message': 'open gate command has been sent', 'data': ''})
        else:
            return jsonify({'code': 'fail', 'message': 'hSDK does not exist', 'data': ''})

    except Exception as e:
        logger.error(e)
        return jsonify({'code': 'fail', 'message': 'job put into queue fail for ' + str(e), 'data': ''})

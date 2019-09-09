from flask import request, jsonify
from ..models import *
from .. import logger, work_q, redis_db, hSDK_handle, socketio
from . import main
from ..decorators import permission_ip
from ..GateCamera import openGate


@main.route('/open_gate', methods=['POST'])
@permission_ip(PermissionIP)
def open_gate():
    """
    只允许PermissionIP中涉及的服务器访问
    :return:
    """
    print(request.json)
    request_data = request.json['data']

    return jsonify(openGate.open(request_data['ip']))



@main.route('/socket_test', methods=['POST'])
def socket_test():
    """
    只允许PermissionIP中涉及的服务器访问
    :return:
    """
    socketio.emit('test', 'socket test', namespace='/test')
    work_q.put('10.170.0.230')
    return jsonify({'status': 'ok'})

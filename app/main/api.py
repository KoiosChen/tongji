from flask import request, jsonify
from ..models import *
from .. import logger, work_q, redis_db, hSDK_handle
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

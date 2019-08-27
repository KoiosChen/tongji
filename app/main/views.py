from flask import request, jsonify, render_template
from ..models import *
from .. import logger, work_q, redis_db, hSDK_handle
from . import main
from ..decorators import permission_ip


@main.route('/', methods=['GET'])
# @permission_ip(PermissionIP)
def index():
    """
    只允许PermissionIP中涉及的服务器访问
    :return:
    """

    return render_template("/parking_gate_switch.html")
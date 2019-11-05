from flask import request, jsonify
from ..models import *
from .. import socketio
from . import main
from ..decorators import permission_ip
from ..GateCamera import Gate
from ..MyModule import send_socketio


@main.route('/open_gate', methods=['POST'])
@permission_ip(PermissionIP)
def open_gate():
    """
    只允许PermissionIP中涉及的服务器访问
    :return:
    """
    print(request.json)
    request_data = request.json['data']
    return jsonify(Gate.open_gate(request_data['ip']))


@main.route('/close_gate', methods=['POST'])
@permission_ip(PermissionIP)
def close_gate():
    """
    只允许PermissionIP中涉及的服务器访问
    :return:
    """
    print(request.json)
    request_data = request.json['data']
    return jsonify(Gate.close_gate(request_data['ip']))


@main.route('/socket_test', methods=['POST'])
@permission_ip(PermissionIP)
def socket_test():
    """
    只允许PermissionIP中涉及的服务器访问
    :return:
    """
    ip = request.form.get('ip')
    print(ip)
    socketio.emit('test', 'socket test', namespace='/test')
    send_socketio.run(ip)
    return jsonify({'status': 'ok'})


@main.route('/close_gate_api', methods=['POST'])
@permission_ip(PermissionIP)
def close_gate_api():
    """
    只允许PermissionIP中涉及的服务器访问
    :return:
    """
    camera_ip = request.json['camera_ip']
    print("closing gate test ", camera_ip)
    socketio.emit('test', 'close_gate gate test', namespace='/test')
    return jsonify({'status': Gate.close_gate(camera_ip)})

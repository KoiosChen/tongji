from .. import logger, socketio, redis_db
from ..GateCamera import Gate
from ..models import gate_dict
import re
import json


@socketio.on('connect', namespace='/test')
def test_connect():
    logger.debug('>>> web socket connected')
    all_keys = redis_db.keys()
    if all_keys:
        for key in all_keys:
            if re.search(r'camera', key.decode()):
                value = json.loads(redis_db.get(key))
                socketio.emit('ws_test', {'content': value}, namespace='/test')


@socketio.on('open gate', namespace='/test')
def open_gate(data):
    camera_ip = data.get('camera_ip') if 'camera_ip' in data.keys() else gate_dict[data.get('gate')]['camera_in']

    logger.info('open_gate gate {}'.format(camera_ip))

    socketio.emit('ws_test',
                  {'content': {'gate': [k for k, v in gate_dict.items() for kk, vv in v.items() if vv == camera_ip][0],
                               'camera_type': '',
                               'camera_ip': '',
                               'pic_path': '',
                               'gate_name': ''}},
                  namespace='/test') \
        if Gate.open_it(camera_ip).get('code') == 'success' \
        else socketio.emit('test', 'open_gate gate fail', namespace='/test')


@socketio.on('close gate', namespace='/test')
def close_gate(data):
    camera_ip = data.get('camera_ip') if 'camera_ip' in data.keys() else gate_dict[data.get('gate')]['camera_in']

    logger.info('closing gate {}'.format(camera_ip))
    socketio.emit('close_result', {'content': Gate.close_it(camera_ip)}, namespace='/test')

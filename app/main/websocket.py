from .. import logger, socketio, redis_db
from ..GateCamera import Gate
from ..models import gate_dict
import re
import json


@socketio.on('connect', namespace='/test')
def test_connect():
    print('connect')
    all_keys = redis_db.keys()
    if all_keys:
        for key in all_keys:
            if re.search(r'camera', key.decode()):
                value = json.loads(redis_db.get(key).decode())
                socketio.emit('ws_test',  {'content': value}, namespace='/test')

@socketio.on('open gate', namespace='/test')
def open_gate(data):
    camera_ip = data.get('camera_ip') if 'camera_ip' in data.keys() else gate_dict[data.get('gate')]['camera_in']

    logger.info('open gate {}'.format(camera_ip))

    gate_name = [k for k, v in gate_dict.items() for kk, vv in v.items() if vv == camera_ip][0]

    socketio.emit('ws_test',
                  {'content':
                       {'gate': gate_name,
                        'camera_type': '',
                        'camera_ip': '',
                        'pic_path': '',
                        'gate_name': ''}},
                  namespace='/test')

    redis_db.delete(camera_ip)


@socketio.on('close gate', namespace='/test')
def close_gate(data):
    camera_ip = data.get('camera_ip') if 'camera_ip' in data.keys() else gate_dict[data.get('gate')]['camera_in']

    logger.info('close gate {}'.format(camera_ip))
    socketio.emit('close_result', {'content': Gate.close(camera_ip)}, namespace='/test')

    gate_name = [k for k, v in gate_dict.items() for kk, vv in v.items() if vv == camera_ip][0]

    socketio.emit('ws_test',
                  {'content':
                       {'gate': gate_name,
                        'camera_type': '',
                        'camera_ip': '',
                        'pic_path': '',
                        'gate_name': ''}},
                  namespace='/test')
